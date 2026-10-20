---
name: claim-figure-ledger
description: Claim ledger (each finding → evidence file → robustness → review verdict) and figure ledger (script, data, projection, map and journal compliance checks) for research projects in a PaperBell vault. Use when recording a result as a claim, preparing to report findings, registering or checking a figure or map, or reviewing which claims are still unreviewed.
---

# Claim and figure ledger

Two kinds of project cards, each with a Base table:

- **Claim cards (结论卡).** One finding per card. Each card records the claim,
  its effect copied from an evidence file, the robustness checks, and an
  independent review verdict.
- **Figure cards (图件卡).** One figure or panel per card. Each card records
  the script, data, output, projection, palette and size, plus a compliance
  checklist (`references/map-figure-compliance.md`).

Read `paperbell-note-conventions` first. Both card types are P-layer notes,
so they live inside an existing project folder.

## Where cards live

| Card | Folder | Template | Ledger |
|---|---|---|---|
| Claim | `40 - Projects/<project>/结论/` | `assets/结论卡模板.md` | `assets/结论台账.base` |
| Figure | `40 - Projects/<project>/图件/` | `assets/图件卡模板.md` | `assets/图件台账.base` |

Frontmatter rules:

- `tags` holds `claim` or `figure`, plus `project/<acronym>`, using the
  project's `acronym` from its home note. The project home note's "all related
  notes" view then picks the cards up automatically.
- `project` links the project home note (`"[[<project>]]"`). Use the optional
  `workstream` text field for sub-studies within a project.
- **Never use `stage` or `status`.** Those are CIMPO project fields. Claims use
  `claim_status` (候选 / 写进正文 / 已删) and figures use `fig_status`
  (草图 / 定稿 / 投稿).
- When the agent creates a card from a template, replace the Templater tags
  (`<% … %>`) and the `<acronym>` / `<项目主页>` placeholders with literal
  values.
- Paths (`evidence_path`, `script_path`, `data_path`, `output_path`) are
  relative to the project's code/data repository, or a repository URL plus a
  path. An absolute path such as `/home/<name>/…` contains the user name and
  leaks with every sync, backup or shared copy of the vault, so write one
  only when the user explicitly asks for it. The same rule applies in
  `geo-research-dashboard` and `geo-dataset-cards`.

Installing a ledger: copy the `.base` file into the project folder (e.g.
`40 - Projects/<project>/结论台账.base`) and replace `project/<acronym>` in
its filter with the real tag. Ask before copying. Never overwrite an
existing file.

## Claim rules (hard)

1. **The review verdict defaults to 未审 (unreviewed).** The agent never sets
   `review_verdict` to 通过 (pass), 有条件 (conditional) or 删除 (delete) on
   its own judgement. The field changes only in two cases:
   - copying the verdict from an independent review, with `review_file`
     pointing to it and `reviewed_on` filled;
   - the user tells the agent to change it.

   Analysing, re-running or "double-checking" a result yourself is not a
   review.
2. **Numbers are copied, never computed or rounded.** `effect` and every number
   in the card body are copied verbatim from the file at `evidence_path`, with
   section, table or line references under 证据摘录. If the evidence file has
   no such number, leave the field empty and say so. Do not derive one.
3. **Deleted claims keep their record.** A claim that fails review or is
   withdrawn gets `claim_status: 已删` (and `review_verdict: 删除` if that was
   the review's verdict), plus a row in its 变更记录 table explaining why.
   **Never delete the card file.** The ledger's 已删 view is the record of what
   was dropped.
4. **Offer a review before reporting outward.** This applies only when the
   user asks for conclusions to be reported to other people (a talk, a slide
   for a meeting, a progress report to a supervisor or co-authors, a
   manuscript paragraph). It does not apply to the user's own questions about
   their results. In that case, first ask the user whether to send the claims
   to an independent reviewer: a separate agent or session that did not take
   part in the analysis, briefed to be strict and to look for alternative
   explanations. If the user agrees, report what survived and say which
   claims are still 未审. If the user declines, or no independent reviewer can
   be started, mark every reported claim as unreviewed. Do not present a
   self-review as a review.
5. **Counterintuitive claims** (`claim_type: 反直觉`): flag them, and note
   whether each is on the paper's main line and directly measurable. Whether
   it goes into the main text is the authors' decision; the agent does not
   promote or demote it.
6. Every claim card links its evidence. Every figure card lists the claim
   cards it supports in `claims`.

## Figure checks

To check a figure, go through the card's 合规检查清单 using
`references/map-figure-compliance.md`.

- Tick an item only with evidence. Examples: the output file shows the inset;
  the caption states n; the script sets the font. Otherwise leave it unticked
  and write what is missing under 未解决的问题. Mark items that do not apply as
  `- [-]`. Do not delete them.
- For maps involving China, the agent **reports** a missing base-map source,
  review number (审图号), South China Sea inset or non-standard boundary as a
  risk. The agent does not judge it acceptable, and it does not edit boundary
  geometry. Terminology and journal-policy questions go to the authors, as
  marked "以期刊 / 官方要求为准" in the reference.
- Sizes follow the target journal (Nature: single column 89 mm, double
  column 183 mm). Anything else is to be confirmed against the journal's
  current guide.
- Every number drawn in a figure must trace to `data_path` or a claim card.
