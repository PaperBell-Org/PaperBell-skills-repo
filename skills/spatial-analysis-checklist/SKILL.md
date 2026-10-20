---
name: spatial-analysis-checklist
description: Pre-review self-check for geospatial research (MAUP, UGCoP/NEAP, spatial autocorrelation, ecological fallacy, CRS, positional error, spatial-CV leakage, temporal alignment, edge effects, representativeness, multiple testing, spatial heterogeneity), plus method cards that copy a published method step by step and geo fields for literature notes. Use when checking a manuscript or analysis before submission or reporting, when recording a published method to replicate, or when reading geospatial papers into a PaperBell vault.
---

# Spatial analysis checklist

Three jobs, one evidence rule:

1. **Pre-review check.** Go through a manuscript or analysis against the
   12-topic checklist in `references/checklist.md`.
2. **Method cards.** Record a published method so that it can be copied
   exactly, with every step traceable to the source paper.
3. **Geo fields on literature notes.** Record study area, spatial unit,
   scale, CRS and so on for each paper read, so papers can be compared in a
   matrix.

The evidence rule: **the agent lists risks; it does not decide whether a
method is acceptable.** Whether a risk is tolerable, and how to answer a
reviewer, is the user's call.

Read `paperbell-note-conventions` first. This skill adds note types on top of
those conventions and does not change them.

## 1. Pre-review check

Input: a manuscript (draft notes, a Longform folder, a PDF) or an analysis
(scripts, result files, a methods description). Read
`references/checklist.md` in full before starting.

For each of the 12 topics (13 rows, because MAUP has 1a scale and 1b zoning),
give one verdict.

| Verdict | Meaning |
|---|---|
| **通过 / Pass** | The material shows the check was done. Cite where it was done. |
| **有风险 / At risk** | The topic applies and the material shows no check, a partial check, or a check that contradicts the claim. Name what is missing. |
| **不适用 / N/A** | The topic does not arise for this design, with a one-line reason (e.g. "no spatial prediction, so no CV"). |

Rules:

- **Evidence or nothing.** "Pass" needs a pointer: file + section/line, table
  or figure number, or a quoted sentence. If you cannot point to it, the
  verdict is "At risk", not "Pass". Never infer that a check "was probably
  done".
- **Don't skip items.** Every row gets a verdict. N/A needs a reason.
- **Risks, not rulings.** Write what a reviewer would ask and which check from
  the checklist would answer it. Do not write "acceptable", "fine" or "not a
  problem". Do not rewrite the analysis unless asked.
- **Cite only from the checklist.** When suggesting literature, use the
  references in `references/checklist.md`. They were checked against Crossref.
  Do not add references from memory. If a topic needs a reference the list
  lacks, say so and leave it for the user to find and verify.
- Numbers you quote come from the material, copied exactly.

Output (in the user's language), as a note or in chat as the user prefers:

```markdown
## 空间分析审稿前自查 — <稿件或分析名> — <YYYY-MM-DD>

| # | 主题 | 判定 | 证据 / 理由 | 审稿人可能会问 | 建议的检查 |
|---|---|---|---|---|---|
| 1a | MAUP 尺度 | 有风险 | 只在 10 km 格网上估计（Methods §2.3） | 换尺度还成立吗？ | 1 / 2 / 4 km 并排报告 |
| … |

**汇总**：通过 n · 有风险 n · 不适用 n。有风险的条目按审稿人最可能先问的顺序列出。
```

If the user keeps a vault copy of the checklist, the method-card and reading
templates point to it by name (`空间分析审稿前检查清单`). Offer to copy
`references/checklist.md` to `00 - Obsidian/空间分析审稿前检查清单.md` (or into
the project folder, `40 - Projects/<project>/`) with frontmatter
`tags: [checklist]`. It is a reference document, not a method card: do not
put it in `10 - Cards/Methods/` and do not tag it `method`. Do not create it
unasked.

## 2. Method cards

A method card is a C-layer entity card: one card per replicable published
method.

- Location: `10 - Cards/Methods/Method - <Author> <Year> <short method name>.md`
  (e.g. `Method - Fotheringham 2017 MGWR.md`).
- Template: `assets/方法卡片模板.md`. When the agent creates a card, replace
  the Templater tags (`<% … %>`) with literal values (today's date, the file
  title).
- Frontmatter:
  - `name` is the method's own name as papers write it (e.g. `MGWR`), **not
    the file name**. The back-reference matches `keywords.contains(this.name)`,
    and papers put the method name in `keywords`, never the card's file name.
    `ch` is the Chinese name; `aliases` holds the full name, abbreviations and
    variant spellings.
  - `category: method`, `featured: false`, `related: []`, `keywords: []`.
  - `tags: [method]` only, never `concept`. A method card is an entity card
    (`category: method`) kept in `10 - Cards/Methods/`, outside
    `10 - Cards/Concepts/`, so that it does not crowd the bounded concept
    vocabulary (about 50 `featured` cards) or the concept wall. The
    back-reference still works, because it only needs `name` / `aliases`.
  - `source_paper` is one full citation ending in a DOI.
  - `used_by` links project home notes (`"[[<project>]]"`).
  - `recipe_status` is 候选 / 照搬中 / 已用. The field is not called
    `status`, so it cannot collide with project fields.
- The card body embeds `![[概念反查.base#相关论文]]`. Any literature note whose
  `keywords` contain the card's `name`, `ch` or an alias shows up there
  automatically, so there is no "used in papers" list to maintain.

Writing the card:

- **Steps are copied from the source, not paraphrased into something new.**
  Each step carries its page or section number (`p.4, §2.3`). Where the paper
  is silent, write "未述 / not stated". Do not fill gaps with what the method
  "usually" does.
- **Parameters** go in the parameter table with their source location. Leave
  "我们的取值" empty until the user's analysis actually sets it.
- **Deviations are listed separately**, each with what changed, why, and
  whether a source-specification version was run for comparison. A deviation
  without a reason is flagged to the user, not invented.
- **DOI**: verify before writing (Crossref,
  `https://api.crossref.org/works/<DOI>`, or the publisher page). If it cannot
  be verified, write "待核实" and tell the user. Never construct a DOI.
- Tick the relevant items under 空间陷阱自查 only when the card's text shows how
  the item is handled. Mark irrelevant items `- [-]`.

## 3. Geo fields on literature notes

Literature notes are inputs. Under CIMPO they carry `keywords` and **never
`concepts`**. A paper belongs to a project through the tag
`project/<acronym>`.

- **Datasets and methods go into `keywords`** (e.g. `"MGWR"`, `"VIIRS"`).
  Method cards and dataset cards find papers through them. There are no
  `methods`, `data_sources` or `relevance` fields.
- Eight structural fields that keywords cannot express: `study_area`,
  `spatial_unit`, `spatial_scale`, `temporal_scale`, `crs`, `exposure_metric`,
  `outcome`, `replicable_recipe` (`是` / `否` only).
- Fill them from the paper with page or section references in the body. Where
  the paper is silent, write `未述`. `replicable_recipe: 是` only when steps
  and parameters are complete enough to reproduce. In that case, also create
  a method card.
- Zotero items: the fields come from a ZotLit template patch. Follow
  `references/zotlit-geo-fields.md`, which requires back-up, approval and
  append-only edits. **Never overwrite the user's `zt-*.eta.md`.**
- Non-Zotero items (preprints, reports, web pages): use
  `assets/地理文献精读模板.md` (`tags: [paper]`, `cate: 论文`), saved under
  `20 - Inputs/`.

## Installing the assets into a vault

Copy only with the user's go-ahead, and never overwrite an existing file of
the same name. If a file already exists, show a diff and ask.

| Asset | Destination |
|---|---|
| `assets/方法卡片模板.md` | `00 - Obsidian/模板/方法卡片模板.md` |
| `assets/地理文献精读模板.md` | `00 - Obsidian/模板/地理文献精读模板.md` |
| `assets/文献方法矩阵.base` | `10 - Cards/Methods/文献方法矩阵.base` |

`文献方法矩阵.base` has four views: by study area, by spatial unit, replicable
recipes, and method cards. The first three list only papers whose
`study_area`, `spatial_unit` or `replicable_recipe` is filled in; the method
card view excludes notes tagged `checklist`. To see papers by method, open the method card,
which has the back-reference embed. The embed relies on the vault's
`10 - Cards/概念反查.base` (view `相关论文`). If that file is missing, tell the
user the embed will be empty.
