---
name: geo-dataset-cards
description: Build and audit dataset cards and study-area cards for geospatial research in a PaperBell (CIMPO) vault. Use when the user adds or reviews a dataset or study area, wants its CRS, resolution, coverage, license, version and known pitfalls recorded, or needs a downloaded dataset verified before use.
---

# Geo dataset cards

A dataset is an **entity card** in the CIMPO "C" layer: `10 - Cards/Datasets/<name>.md`,
with `category: dataset` and the tag `dataset`. It lives outside
`10 - Cards/Concepts/` so that dataset cards do not crowd the bounded concept
vocabulary (about 50 `featured` cards) or the concept wall. The
back-reference to papers still works, because it only needs `name` /
`aliases`.
A study area is **metadata** ("M" layer): `30 - Metadata/StudyAreas/<name>.md`, not a card.
Read `paperbell-note-conventions` first; this skill follows it.

## Files this skill ships

| File | Use |
|---|---|
| `assets/dataset-card-template.md` | Templater template for a dataset card |
| `assets/study-area-card-template.md` | Templater template for a study-area card |
| `assets/dataset-catalog.base` | Base: all datasets, unverified or with issues, sensitive, missing CRS or license. Save as `10 - Cards/Datasets/00. Datasets.base` (or any name in that folder) |
| `assets/study-area-catalog.base` | Base: all study areas, missing boundary source or code. Save in `30 - Metadata/StudyAreas/` |
| `references/common-pitfalls.md` | Generic geospatial traps to look for |

Copy templates and Bases into the vault only if absent. Never overwrite a file the user has changed.

The templates are for the user's Templater. When the agent creates a card
itself, it fills in literal values: every `<% … %>` / `<%* … %>` block is
replaced by its result (the file title, today's date, the answer from the
source, or an empty value). No Templater code is written into the vault.

## Card format

Dataset card frontmatter (the CIMPO entity fields first):

```yaml
tags: [dataset]          # entity card, never `concept`
name: <dataset name>     # the name papers use; this is what the back-reference matches
aliases: []              # variant names and abbreviations
ch: <Chinese name>       # may be empty
category: dataset
featured: false
related: []
keywords: []
provider: <organisation, author or platform>
source_url: <landing page>
doi: <dataset DOI, only if stated>
license: <e.g. CC BY 4.0>
version: <version or snapshot date>
data_type: raster        # vector | raster | points | table | trajectory | text
crs: <e.g. EPSG:4326, or none for non-spatial data>
spatial_resolution: <e.g. 1 km>
spatial_extent: <e.g. global>
temporal_coverage: <start to end, with time zone / day boundary>
temporal_resolution: <e.g. daily>
size: <size or row count>
local_path: <path relative to the project's data folder>
verified: unverified     # unverified | verified | issues
verified_date:           # YYYY-MM-DD, empty until verified
used_by: ["[[<project home note>]]"]   # link project home notes, not paper names
sensitive: false         # boolean
```

**`local_path` and privacy.** Write a path relative to the project's data
folder or repository (e.g. `data/raw/era5/`), or a repository URL plus a
path. An absolute path such as `/home/<name>/…` contains the user name, and
the vault carries it into every sync, backup or shared copy. Write an
absolute path only when the user explicitly asks for one, and never on a
`sensitive: true` card. The same rule applies in `geo-research-dashboard`
and `claim-figure-ledger`.

The card body ends with `![[概念反查.base#相关论文]]`. Literature notes
are linked automatically when their `keywords` contain the card's `name`,
`aliases` or `ch`. **Tell the user:** to link a paper to a dataset, put the
dataset's name (or an alias) into the paper's `keywords`. The association
exists only through that.

Study-area card: `tags: [study-area]`, with these fields:

```yaml
tags: [study-area]
name: <study area>
aliases: []
level: city              # country | province | city | district | neighbourhood
admin_code: ""           # a string, so leading zeros survive
boundary_source: <e.g. GADM 4.1>
crs: <CRS of the boundary file>
climate_zone: <with the scheme, e.g. Köppen Cfa>
population: <with source and year>
used_by: ["[[<project home note>]]"]
```

## Procedure: create a card

1. Collect the user's material: `DATA_README`, a data catalogue document, a
   download page's text, a paper's data section. Only these are sources.
2. Fill **only fields that a source states.** Leave the rest empty and write
   "not found" in the card's "字段出处" table. Do not infer a CRS from the
   country, a license from the provider's other products, or a version from
   the file date.
3. For every non-empty field in the required set, record the source (file and
   section or line, or DOI) in "字段出处". Required set: **crs, spatial
   resolution, temporal coverage (with time zone / day boundary), license,
   version, verification status, known pitfalls.**
4. Known pitfalls: copy only what the dataset's documentation, a paper or a
   recorded check says, each with its source. Use
   `references/common-pitfalls.md` to know what to look for, not as content to
   paste.
5. Name collisions: search `10 - Cards/Datasets/` and the aliases of existing
   cards first; update an existing card rather than create a second one.
6. Set `verified: unverified` unless the checks below have actually been run.
7. Report to the user: cards created, fields left empty, and any conflict
   between sources.

**Metadata only.** Do not open or load the big data files. Use documentation,
file listings, headers or a few rows' schema at most. Record size from the
file system listing, not by reading the file.

## Procedure: verify before use

Run when a dataset is newly downloaded or before its first use in an analysis.
Prefer cheap, metadata-level or small-sample checks; ask before any heavy
computation.

1. **Range and extremes.** Value ranges against the documented units and
   plausible physical limits; the documented fill or missing value is not
   counted as data. Spatial extent against the study area.
2. **Calendar completeness.** Every expected date or hour is present; list gaps
   and duplicates; check the time zone and day boundary.
3. **Mirror or version consistency.** If more than one copy, mirror or
   version exists, compare sizes, checksums or a small statistical fingerprint,
   and compare the version string with the card.
4. **CRS spot check.** Take a few known landmarks or admin-unit centroids and
   confirm the coordinates fall where expected in the declared CRS (see the
   GCJ-02 / BD-09 section of `references/common-pitfalls.md` for China).
   For data without coordinates (a table keyed by names or codes, text,
   survey answers), record this check as "不适用 / N/A" with the reason, e.g.
   "no coordinates; joined to units by admin code". Then check the join key
   instead: codes match the boundary vintage, no unmatched units.

**If anything looks wrong, report it first, then use the data.** Write the
finding in the card's "核验记录" table, set `verified: issues`, and tell the user
before any analysis continues. Set `verified: verified` and `verified_date`
only when all four checks passed (or were recorded as N/A with a reason),
listing what was checked.

## Procedure: audit existing cards

Open the Bases (missing CRS or license, unverified or issues, sensitive). For
each card: check the required set is present, "字段出处" is filled, pitfalls
have sources, `verified_date` matches a record in the log. Output a list of
gaps; fix only what the user's sources support.

## Sensitive data

Set `sensitive: true` for anything with personal information, restricted
license or "do not share" terms (for example personal social-media data,
mobile-phone traces, survey microdata). On such cards:

- Record schema, coverage, license and how to request access only.
- Do not write anything that identifies a person: no user IDs, names, home
  or workplace locations, sample rows or small-count cells.
- `local_path` gives the location only, as a relative path (see above); never
  paste content.
- Mention the data-sharing restriction in "引用格式".

## Do not

- Do not invent values, DOIs, licenses or versions.
- Do not turn dataset cards into concept cards (no `concept` tag).
- Do not store credentials, access tokens or download links with embedded keys.
- Do not edit data files.
