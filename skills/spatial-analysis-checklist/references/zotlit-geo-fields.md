# ZotLit geo-field patch · ZotLit 地理字段补丁

PaperBell imports Zotero items through ZotLit, using the templates
`00 - Obsidian/模板/zt-field.eta.md` (frontmatter) and
`00 - Obsidian/模板/zt-note.eta.md` (note body). This patch **appends** geo
fields to both, so Zotero notes and the non-Zotero reading template
(`assets/地理文献精读模板.md`) share one schema and both appear in
`文献方法矩阵.base`.

Never overwrite the user's templates. Their versions often carry custom tag
filters. Apply the patch by appending, and only after these steps:

1. Read both files. If a key below already exists, skip it. Never add a
   second copy.
2. Back up each file next to itself first (`zt-field.eta.md.bak-YYYYMMDD`),
   and tell the user the backup names.
3. Show the user the exact lines to be appended and wait for a yes.
4. Append. Then ask the user to import (or re-render) one Zotero item to
   confirm the note still renders. If it fails, restore from the backup.

## CIMPO rules this patch follows

- A literature note is an **input**. It carries `keywords` and never
  `concepts`.
- **Datasets and methods go into `keywords`**, for example `"MGWR"`,
  `"two-step floating catchment area"`, `"VIIRS"`, `"WorldPop"`. Method cards
  (`10 - Cards/Methods/`) and dataset cards find their papers through
  `keywords` via the `概念反查.base#相关论文` embed, so there are no separate
  `methods`, `data_sources` or `relevance` fields.
- A paper's link to a project is the tag `project/<acronym>`. It is not a
  frontmatter field.
- Only structural facts that `keywords` cannot express get their own keys.
  These are the eight below.

## 1. Append to `zt-field.eta.md`

Add these lines at the very end of the frontmatter template. ZotLit wraps the
file's output in `---` itself, so do not add delimiters. Keep the blank-line
spacing the file already uses between keys.

```yaml

study_area:

spatial_unit:

spatial_scale:

temporal_scale:

crs:

exposure_metric:

outcome:

replicable_recipe:
```

All values start empty and are filled while reading. `replicable_recipe` takes
only `是` or `否`.

## 2. Insert into `zt-note.eta.md`

Insert this block after the header (the Zotero / file / journal link table)
and before the annotations section, which is usually `## Annotations` with an
`include("annots", …)` call. Do not touch the include lines.

```markdown
## 地理空间速读

> [!abstract]- 填写说明
> 导入时留空，读的时候填。正文写依据（标页码或节号），对应的 frontmatter 键填简短值，供“文献方法矩阵”汇总。原文没写的项填“未述”，不要猜。数据集名和方法名写进 `keywords`，不另设字段；和某个项目有关就加标签 `project/<acronym>`。

- **研究区** `study_area`：国家 / 城市数 / 具体城市；时段内边界是否变化
- **数据**（写进 `keywords`）：每个数据源的名称、版本、规模
- **空间单元** `spatial_unit`：分析单元是什么（个体 / 格网 / 街区 / 行政区 / 城市）；暴露与结局是否在同一单元
- **空间尺度** `spatial_scale`：分辨率或单元大小（如 0.1°、1 km、城市级）；是否做过换尺度或换分区的敏感性
- **时间尺度** `temporal_scale`：时间分辨率与跨度；不同数据怎样对齐（时区、日界、滞后）
- **坐标系** `crs`：原文写的坐标系与投影；距离和面积在什么坐标系下算（未述就写“未述”）
- **方法**（写进 `keywords`）：主模型、识别策略、标准误怎么算（聚类层级 / 空间 SE）；有对应的方法卡片就链接过去
- **暴露指标** `exposure_metric`：用什么变量、怎么聚合
- **结局** `outcome`：结局变量与构念边界（原文怎样说明“测的是什么、不是什么”）
- **可照搬** `replicable_recipe`：是 / 否。只有当步骤和参数写全、能逐条复现时才填“是”，同时建一张方法卡片
- **空间陷阱**：对照空间分析审稿前检查清单，记下原文没有处理的问题，以及我们能补上的地方

```

## Notes

- Existing Zotero notes are not re-rendered automatically. Old notes simply
  lack the keys and drop out of the geo views until someone adds them. Do not
  bulk-edit old notes unless the user asks.
- If the user's ZotLit setup uses differently named templates, ask which file
  holds the frontmatter and which holds the body. Do not guess.
