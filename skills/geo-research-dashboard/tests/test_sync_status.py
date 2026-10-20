#!/usr/bin/env python3
"""Tests for scripts/sync_status.py (stdlib only; run directly or via unittest)."""
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sync_status", HERE.parent / "scripts" / "sync_status.py")
ss = importlib.util.module_from_spec(spec)
sys.modules["sync_status"] = ss
spec.loader.exec_module(ss)

STATUS_EN = """# P1 Urban green-space access

Updated: 2026-10-18
Stage: **Robustness checks** on the main regression
Current work:
- Re-running the model with 500 m and 1 km buffers
- Waiting for the NDVI composite

Needs decision:
1) Use the 2020 or the 2023 census boundaries
2) Drop the three outlier districts (see notes)

Next steps:
- Draft the results section
"""

STATUS_ZH = """# P2 夜间灯光与经济

更新时间：2026-10-19
阶段：初步结果
当前在做：对比两套灯光产品的年际一致性
下一步：补充省级固定效应

## 需要用户决定

- 是否改用月度合成产品
- 已完成：城市名单已按建议执行

## 历史

### 10-01 记录
需要用户决定：无
"""

STATUS_FREE = """# P3 Street-view shade

Oct 12: sampled 2000 points, nothing blocked.
Decisions needed:
- Approve the extra Mapillary download?
"""


HOME_NOTE = """---
tags: [project/SER]
acronym: SER
stage: 进行
---

# Series
"""


def make_fixture(tmp: Path):
    root = tmp / "projects"
    for folder, text in (("p1", STATUS_EN), ("p2", STATUS_ZH), ("p3", STATUS_FREE)):
        (root / folder).mkdir(parents=True)
        (root / folder / "STATUS.md").write_text(text, encoding="utf-8")
    (root / "p4_missing").mkdir()
    vault = tmp / "vault"
    (vault / ".obsidian").mkdir(parents=True)
    home = vault / "40 - Projects" / "Series"
    home.mkdir(parents=True)
    (home / "Series.md").write_text(HOME_NOTE, encoding="utf-8")
    cfg = {
        "lang": "en", "status_root": str(root), "project_folder": "40 - Projects/Series", "acronym": "SER",
        "projects": [
            {"folder": "p1", "card": "P1 Green access", "code": "P1"},
            {"folder": "p2", "card": "P2 Night lights"},
            {"folder": "p3", "card": "P3 Shade", "code": "P3"},
            {"folder": "p4_missing", "card": "P4 Missing", "code": "P4"},
        ],
    }
    cfg_path = vault / "dashboard.config.json"
    cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
    return vault, root, cfg_path


def snapshot(d: Path):
    return {str(p.relative_to(d)): p.read_bytes() for p in sorted(d.rglob("*")) if p.is_file()}


def cli(*args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        code = ss.main(list(args))
    return code, buf.getvalue()


class SyncStatusTests(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.tmp = Path(self._td.name)
        self.vault, self.root, self.cfg_path = make_fixture(self.tmp)
        self.out = self.vault / "40 - Projects" / "Series"

    def tearDown(self):
        self._td.cleanup()

    def sync(self, *extra):
        return cli("--config", str(self.cfg_path), "--vault", str(self.vault), *extra)

    def test_extraction(self):
        code, _ = self.sync()
        self.assertEqual(code, 0)
        p1 = (self.out / "P1 Green access.md").read_text(encoding="utf-8")
        self.assertIn("decisions_open: 2", p1)
        self.assertIn("Use the 2020 or the 2023 census boundaries", p1)
        self.assertIn("Drop the three outlier districts", p1)
        self.assertIn("Robustness checks", p1)
        self.assertIn("Re-running the model", p1)
        self.assertIn("Draft the results section", p1)
        p2 = (self.out / "P2 Night lights.md").read_text(encoding="utf-8")
        self.assertIn("decisions_open: 1", p2)  # resolved item skipped, history "none" ignored
        self.assertIn("是否改用月度合成产品", p2)
        self.assertNotIn("城市名单已按建议执行", p2.split("## My notes")[0].split("历史")[0])
        self.assertIn('status_code: "P2"', p2)  # default code from card name
        p3 = (self.out / "P3 Shade.md").read_text(encoding="utf-8")
        self.assertIn("decisions_open: 1", p3)
        self.assertIn("Approve the extra Mapillary download?", p3)
        self.assertIn("Not recognised - see the original.", p3)  # no stage/next in free text
        p4 = (self.out / "P4 Missing.md").read_text(encoding="utf-8")
        self.assertIn("**STATUS.md not found**", p4)
        inbox = (self.out / "Decisions.md").read_text(encoding="utf-8")
        self.assertIn("**4** open decision(s)", inbox)
        self.assertTrue((self.out / "00 Dashboard.md").is_file())
        base = (self.out / "status-board.base").read_text()
        self.assertIn('file.hasTag("status-card")', base)
        self.assertIn('file.hasTag("project/SER")', base)
        self.assertNotIn("paper", p1.split("---")[1])
        self.assertNotRegex(p1.split("---")[1], r"(?m)^stage:")
        self.assertIn("status_stage:", p1)

    def test_idempotent_and_status_untouched(self):
        before_status = snapshot(self.root)
        self.sync()
        first = snapshot(self.out)
        _, text = self.sync()
        self.assertEqual(first, snapshot(self.out))
        self.assertNotIn("created", text)
        self.assertNotIn("updated", text)
        self.assertEqual(before_status, snapshot(self.root))

    def test_handwritten_area_and_frontmatter_preserved(self):
        self.sync()
        card = self.out / "P1 Green access.md"
        txt = card.read_text(encoding="utf-8")
        txt = txt.replace("tags: [project/SER, status-card]", "tags: [project/SER, status-card, mine]\nrating: 5")
        txt = txt.replace("## My notes\n", "## My notes\n\nHand-written thought about buffers.\n")
        card.write_text(txt, encoding="utf-8")
        # STATUS changes -> managed content changes, hand-written content must stay
        status = self.root / "p1" / "STATUS.md"
        status.write_text(STATUS_EN.replace("Robustness checks", "Writing"), encoding="utf-8")
        self.sync()
        new = card.read_text(encoding="utf-8")
        self.assertIn("Hand-written thought about buffers.", new)
        self.assertIn("rating: 5", new)
        self.assertIn("tags: [project/SER, status-card, mine]", new)
        self.assertIn("Writing", new)
        self.assertNotIn("Robustness checks", new)
        self.assertEqual(new.count("synced:"), 1)

    def test_deleted_markers_keep_text(self):
        self.sync()
        card = self.out / "P2 Night lights.md"
        txt = card.read_text(encoding="utf-8")
        b, e = txt.find(ss.AUTO_BEGIN), txt.find(ss.AUTO_END) + len(ss.AUTO_END)
        card.write_text(txt[:b] + "MY ONLY NOTE" + txt[e:], encoding="utf-8")
        self.sync()
        new = card.read_text(encoding="utf-8")
        self.assertIn("MY ONLY NOTE", new)
        self.assertEqual(new.count(ss.AUTO_BEGIN), 1)

    def test_checkbox_state_kept(self):
        self.sync()
        inbox = self.out / "Decisions.md"
        txt = inbox.read_text(encoding="utf-8")
        target = "- [ ] Approve the extra Mapillary download?"
        self.assertIn(target, txt)
        inbox.write_text(txt.replace(target, target.replace("[ ]", "[x]")), encoding="utf-8")
        self.sync()
        self.assertIn("- [x] Approve the extra Mapillary download?", inbox.read_text(encoding="utf-8"))

    def test_dry_run_writes_nothing(self):
        before = snapshot(self.out)
        code, text = self.sync("--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("[dry-run]", text)
        self.assertEqual(before, snapshot(self.out))

    def test_none_and_unrecognised(self):
        (self.root / "p3" / "STATUS.md").write_text("# P3\n\nNeeds decision: None\n\nJust prose.\n", encoding="utf-8")
        self.sync()
        p3 = (self.out / "P3 Shade.md").read_text(encoding="utf-8")
        self.assertIn("decisions_open: 0", p3)
        self.assertIn("says none", p3)
        (self.root / "p3" / "STATUS.md").write_text("# P3\n\nJust prose, no fields.\n", encoding="utf-8")
        self.sync()
        p3 = (self.out / "P3 Shade.md").read_text(encoding="utf-8")
        self.assertIn("Not recognised", p3)

    def test_config_errors(self):
        code, text = cli("--config", str(self.vault / "nope.json"), "--vault", str(self.vault))
        self.assertEqual(code, 2)
        bad = json.loads(self.cfg_path.read_text())
        bad["project_folder"] = "../outside"
        self.cfg_path.write_text(json.dumps(bad), encoding="utf-8")
        code, text = self.sync()
        self.assertEqual(code, 2)
        self.assertFalse((self.tmp / "outside").exists())


    # ---- writing stays inside the project folder ----

    def set_cfg(self, **kw):
        cfg = json.loads(self.cfg_path.read_text())
        cfg.update(kw)
        self.cfg_path.write_text(json.dumps(cfg), encoding="utf-8")

    def assert_refused(self, *extra):
        before_tmp = sorted(str(p) for p in self.tmp.rglob("*"))
        before_out = snapshot(self.out) if self.out.is_dir() else None
        code, text = self.sync(*extra)
        self.assertEqual(code, 2, text)
        self.assertEqual(before_tmp, sorted(str(p) for p in self.tmp.rglob("*")))
        if before_out is not None:
            self.assertEqual(before_out, snapshot(self.out))
        return text

    def test_unsafe_output_names_rejected(self):
        bad = {
            "base_name": ["../escape.base", "/abs/escape.base", "sub/x.base", "a\\b.base", "..base", "x.md"],
            "inbox_name": ["../Inbox", "/tmp/Inbox", "a/b", "x:y", "..", "Inbox..old"],
            "board_name": ["../../Board", "/Board", "a\\b", 'q"uote', "..hidden"],
        }
        for key, values in bad.items():
            for v in values:
                with self.subTest(key=key, value=v):
                    self.set_cfg(**{key: v})
                    self.assertIn("config error", self.assert_refused())
                    self.set_cfg(**{key: ss.DEFAULTS.get(key, "")})
        for card in ("../P9", "/P9", "..", "a/b"):
            with self.subTest(card=card):
                cfg = json.loads(self.cfg_path.read_text())
                cfg["projects"][0]["card"] = card
                self.cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
                self.assert_refused()
        self.assertFalse((self.tmp / "escape.base").exists())

    def test_symlink_target_refused(self):
        outside = self.tmp / "outside.md"
        outside.write_text("---\ntags: [status-card]\n---\nkeep me\n", encoding="utf-8")
        (self.out / "P1 Green access.md").symlink_to(outside)
        text = self.assert_refused()
        self.assertIn("symbolic link", text)
        self.assertEqual(outside.read_text(encoding="utf-8"), "---\ntags: [status-card]\n---\nkeep me\n")
        self.assertFalse((self.out / "Decisions.md").exists())  # nothing written before the refusal

    def test_symlinked_project_folder_refused(self):
        outside = self.tmp / "outside_dir"
        outside.mkdir()
        (outside / "outside_dir.md").write_text(HOME_NOTE, encoding="utf-8")
        (self.vault / "40 - Projects" / "Link").symlink_to(outside, target_is_directory=True)
        self.set_cfg(project_folder="40 - Projects/Link")
        self.assertIn("inside the vault", self.assert_refused())
        self.assertEqual(sorted(p.name for p in outside.iterdir()), ["outside_dir.md"])

    def test_check_target_containment(self):
        out = self.out.resolve()
        with self.assertRaises(ss.SyncError):
            ss.check_target(out, "../escape.md")
        with self.assertRaises(ss.SyncError):
            ss.check_target(out, str(self.tmp / "abs.md"))

    # ---- never overwrite notes the script did not write ----

    def test_foreign_notes_not_overwritten(self):
        cases = {
            "Decisions.md": "# My own decisions page\n",
            "00 Dashboard.md": "---\ntags: [mine]\n---\nhand-made board\n",
            "P3 Shade.md": "---\ntags: [project/SER]\n---\nan unrelated note with this name\n",
            "status-board.base": "filters:\n  and:\n    - file.hasTag(\"x\")\n",
        }
        for name, content in cases.items():
            with self.subTest(name=name):
                f = self.out / name
                f.write_text(content, encoding="utf-8")
                text = self.assert_refused()
                self.assertIn("not written by this script", text)
                self.assertIn("Rename", text)
                self.assertEqual(f.read_text(encoding="utf-8"), content)
                f.unlink()

    def test_own_marks_allow_rewrite(self):
        self.sync()
        inbox = (self.out / "Decisions.md").read_text(encoding="utf-8")
        board = (self.out / "00 Dashboard.md").read_text(encoding="utf-8")
        base = (self.out / "status-board.base").read_text(encoding="utf-8")
        self.assertIn("status-dashboard", inbox)
        self.assertIn(ss.GEN_MARK, inbox)
        self.assertIn(ss.GEN_MARK, board)
        self.assertEqual(base.splitlines()[0], ss.BASE_MARK)
        # a card with only the AUTO markers (tag removed by hand) is still recognised
        card = self.out / "P1 Green access.md"
        card.write_text(card.read_text(encoding="utf-8").replace(", status-card]", "]"), encoding="utf-8")
        self.assertTrue(ss.owned_by_script("P1 Green access.md", card.read_text(encoding="utf-8")))
        # block-list tags are recognised too
        self.assertTrue(ss.owned_by_script("x.md", "---\ntags:\n  - status-dashboard\n---\n"))
        code, _ = self.sync()
        self.assertEqual(code, 0)

    def test_card_name_collisions(self):
        for clash in ("Series", "Decisions", "00 Dashboard", "series"):
            with self.subTest(clash=clash):
                cfg = json.loads(self.cfg_path.read_text())
                cfg["projects"][0]["card"] = clash
                self.cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
                self.assertIn("collides", self.assert_refused())
        cfg = json.loads(self.cfg_path.read_text())
        cfg["projects"][0]["card"] = cfg["projects"][1]["card"]
        self.cfg_path.write_text(json.dumps(cfg), encoding="utf-8")
        self.assertIn("duplicate", self.assert_refused())
        self.assertEqual((self.out / "Series.md").read_text(encoding="utf-8"), HOME_NOTE)

    def test_project_folder_must_exist_with_home_note(self):
        self.set_cfg(project_folder="40 - Projects/Nope")
        self.assertIn("does not exist", self.assert_refused())
        self.assertFalse((self.vault / "40 - Projects" / "Nope").exists())
        (self.vault / "40 - Projects" / "Empty").mkdir()
        self.set_cfg(project_folder="40 - Projects/Empty")
        self.assertIn("home note not found", self.assert_refused())
        self.set_cfg(project_folder="40 - Projects/Series", acronym="OTHER")
        self.assertIn("acronym mismatch", self.assert_refused())

    def test_vault_needs_obsidian_folder(self):
        (self.vault / ".obsidian").rmdir()
        self.assertIn(".obsidian", self.assert_refused())

    def test_vault_argument_required(self):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf), self.assertRaises(SystemExit) as cm:
            ss.main(["--config", str(self.cfg_path)])
        self.assertEqual(cm.exception.code, 2)
        self.assertIn("--vault", buf.getvalue())

    # ---- no absolute paths in the vault by default ----

    def test_no_absolute_paths_by_default(self):
        self.set_cfg(overview_file="p1/STATUS.md")
        self.sync()
        for p in self.out.iterdir():
            text = p.read_text(encoding="utf-8")
            with self.subTest(file=p.name):
                self.assertNotIn("file://", text)
                self.assertNotIn(str(self.tmp), text)
                self.assertNotIn(str(self.tmp.resolve()), text)
        p1 = (self.out / "P1 Green access.md").read_text(encoding="utf-8")
        self.assertIn('status_path: "p1"', p1)
        self.assertIn("`p1/STATUS.md`", p1)

    def test_link_files_opt_in(self):
        self.set_cfg(link_files=True)
        self.sync()
        p1 = (self.out / "P1 Green access.md").read_text(encoding="utf-8")
        self.assertIn("file://", p1)
        self.assertIn('status_path: "p1"', p1)  # frontmatter stays relative either way
        self.set_cfg(link_files="yes")
        self.assertIn("link_files", self.assert_refused())


if __name__ == "__main__":
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    unittest.main()
