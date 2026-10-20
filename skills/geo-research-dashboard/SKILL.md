---
name: geo-research-dashboard
description: Sync per-project STATUS.md files that live outside the vault (data and code folders, usually maintained by an AI coding session) into project cards, a dashboard Base and a "needs my decision" inbox inside the vault. Use when the user wants one overview of several research projects or papers, or asks what is waiting for their decision.
---

# Geo research dashboard

Geospatial researchers keep heavy data and code in project folders outside the
vault. Each project or paper has a `STATUS.md` (stage, what is being done, next
steps, questions for the researcher), often written by an AI coding session.
This skill turns those files into a read-only mirror inside the vault:

- one **project card** per project (`<card>.md`),
- one **dashboard** page plus a **Base** (`status-board.base`) with one row per project,
- one **decisions inbox** that lists every open "needs my decision" item with its source line.

Everything lives in an **existing CIMPO project folder**, `40 - Projects/<name>/`
(home note `<name>/<name>.md` with an `acronym`); the skill never creates a
free-floating folder. The script refuses to run unless the vault root has a
`.obsidian/` folder, the project folder exists, and its home note's `acronym`
equals the config's `acronym`. Follow `paperbell-note-conventions` for the project
itself. Cards are tagged `project/<acronym>` and `status-card`. They are
never tagged `paper` (that is the literature tag the concept cards'
"related papers" view filters on). The card's stage field is `status_stage`,
never `stage`: `stage` is the CIMPO project lifecycle field
(探索/进行/结题/归档/维护) and belongs to the project home note only.

The sync is **one-way**. The script only reads the external folders and only
writes inside `project_folder` in the vault. Nothing outside the
vault is created, changed or deleted.

## When to use

- The user runs several projects or papers and wants a single view of progress.
- The user asks "what is waiting for my decision?" or "which project is stale?".
- Not for projects without a `STATUS.md`-style file. Ask the user to start one first (see "STATUS.md tips").

## First-time setup

1. Find the CIMPO project the dashboard belongs to (`40 - Projects/<name>/`) and read its `acronym` from the home note. If the user has no such project, create it first following `paperbell-note-conventions` (preferably with PaperBell's project command); do not invent a folder.
2. Copy `assets/dashboard.config.example.json` to `<project folder>/dashboard.config.json` and edit it:
   - `project_folder`: vault-relative path of that project folder. It must stay inside the vault.
   - `acronym`: the project's acronym; it becomes the `project/<acronym>` tag.
   - `status_root`: absolute path of the folder that contains the project folders (or a path relative to the vault).
   - `projects`: one entry per project: `folder` (directory name under `status_root`), `card` (card title, used as file name and wiki-link), optional `code` (short id; defaults to the first word of `card`).
   - Optional: `lang` (`zh` or `en`, language of generated headings, default `zh`), `stale_days` (default 3), `board_name`, `inbox_name`, `base_name`, `link_targets` (files or folders listed on each card), `link_files` (default `false`, see "Paths and privacy"), `overview_file` (an overall progress file under `status_root` to check for staleness), `extra_decide_labels` (extra exact labels that mean "decision needed").
   - `card`, `inbox_name`, `board_name` and `base_name` are plain file names: no `/ \ : * ? " < > |`, no `..`, no absolute path. A card must not be named like the project folder (that is the home note), `inbox_name` or `board_name`. `base_name` ends in `.base`.
3. Dry run first and show the user the summary:
   `python3 <skill dir>/scripts/sync_status.py --vault <vault root> --config "40 - Projects/<name>/dashboard.config.json" --dry-run`
4. Run for real (drop `--dry-run`).
5. Tell the user to open the dashboard page. `assets/status-board.base` is a reference copy of the Base the script writes (filters `status-card` plus `project/<acronym>`; replace the placeholder if you copy it by hand). Re-running the script restores the Base file, so customise it by copying it under another name.

## Running

```
python3 <skill dir>/scripts/sync_status.py --vault <vault root> --config <config.json> [--status-root <folder>] [--dry-run]
```

`<skill dir>` is the folder this `SKILL.md` is in.

- `--vault` (required): the vault root, i.e. the folder that contains `.obsidian/`.
- `--config`: absolute, relative to the current directory, or relative to `--vault`.
- `--status-root`: overrides `status_root` from the config (handy when the data lives on a different path on a second machine).
- Output lists each file as `created`, `updated` or `unchanged`, then an extraction summary per project with warnings.

Run it again whenever STATUS files change, e.g. at the start of a work session. Nothing else is needed.

## What the script guarantees

- **Writes only inside the project folder.** Every target must resolve inside `project_folder`; symbolic links are refused. All targets are checked before the first write, so a refusal leaves the vault unchanged.
- **Never overwrites someone else's note.** An existing file is rewritten only if it carries the script's marks: the `status-card` or `status-dashboard` tag, an `<!-- AUTO:… -->` marker, or (for the `.base`) the generator comment on its first line. The files the script writes carry these marks. Otherwise it stops with an error; rename the card, `inbox_name`, `board_name` or `base_name` in the config, or move the existing note.
- **Hand-written area is never overwritten.** A card's body is replaced only between `<!-- AUTO:BEGIN -->` and `<!-- AUTO:END -->`. Write your own notes under "My notes". If the markers are deleted, the block is re-inserted after the title and all other text stays.
- **Frontmatter**: only the managed keys (`status_code`, `title`, `status_stage`, `status_updated`, `status_mtime`, `status_path`, `decisions_open`, `synced`) are updated. Other keys and tags you add are kept.
- **Idempotent**: unchanged inputs produce no file change, not even the `synced` stamp.
- **Inbox and dashboard pages are rewritten every run.** Do not hand-edit them. A ticked checkbox in the inbox is kept as long as the same item text is still present, but it is only a temporary mark; the real decision belongs in the project's STATUS.md.
- **Read-only on the external folders.**

## Paths and privacy

An absolute path such as `/home/<name>/…` contains the user name. Written
into a vault, it travels with every sync, backup or shared copy of that
vault. So nothing absolute goes into the vault unless the user explicitly
asks for it:

- `status_path` in the card frontmatter is relative to `status_root` (e.g. `p1`).
- Cards, inbox and dashboard show linked files as paths relative to `status_root`.
- `link_files: true` turns those into clickable `file://` links. These contain
  the absolute path; enable it only for a vault that is never synced or shared,
  and tell the user so.
- `status_root` itself stays in the config file; keep that file out of shared
  copies, or use a vault-relative `status_root`, or pass `--status-root` on the
  command line instead.

The other geo skills follow the same rule (see `geo-dataset-cards` for
`local_path`, `claim-figure-ledger` for evidence and script paths).

## What it extracts

From each STATUS.md it looks for (Chinese or English; matched by label, heading or table column):

| Field | Examples recognised |
|---|---|
| Update time | `更新时间：`, `Updated:`, `Last updated:`, or the first dated heading |
| Stage | `阶段：`, `Stage:`, `Phase:` |
| Current work | `当前在做`, `Current work`, `In progress`, `Doing` |
| Next steps | `下一步`, `Next steps` |
| Decisions needed | `需要用户决定`, `待用户决定`, `待我决定`, `Needs decision`, `Decisions needed`, `Awaiting user ...`, `Pending decisions`, as a `Label:` line, a heading with a list under it, or a table column |

Decision handling: items can be bullets, numbered (`1) ... 2) ...`) or `;`-separated. "None", "无" and similar mean no open decision. Items starting with "done", "resolved", "已完成", "已定", etc. are skipped. When a STATUS has several decision notes, the newest one counts; older unresolved items are folded under a "history" callout and are not counted.

## Limits (tell the user)

- STATUS.md is free text, so extraction is best effort. When a field cannot be found the card says "Not recognised - see the original" (the `unrecognized` state) and the extraction summary prints a hint. Do not guess the content; open the original file.
- Only the first standard header block is trusted for stage, current work and next steps. Older sections further down are ignored for those fields.
- Dates without a year (`10-20`, `Oct 20`) take the year of the file's modification time.
- If the user's STATUS files use a different decision label, add it to `extra_decide_labels` (exact label text) or suggest they adopt one of the recognised labels.

## STATUS.md tips (for projects that have none)

A header of this shape extracts cleanly:

```
# <Project name>

Updated: 2026-10-20
Stage: <one line>
Current work: <one line or a list>
Needs decision:
- <question for the researcher>
Next steps:
- <step>
```

Write `Needs decision: none` when nothing is waiting, so the dashboard can distinguish "no decisions" from "not recognised".

## Do not

- Do not edit STATUS.md files or anything outside the vault from this skill.
- Do not tag cards `paper` or add a `stage` key to them.
- Do not put credentials or personal data into the config or cards.
- Do not run the sync on a schedule the user did not ask for.
