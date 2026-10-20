# Map and figure compliance · 地图与图件合规

What the figure card's checklist refers to. Every rule below either has a
source or is marked **以期刊 / 官方要求为准 (follow the journal's or the
authority's current requirement)**. Requirements change, so before submission
open the target journal's current figure guide and, for maps of China, the
current documents from the Ministry of Natural Resources (自然资源部). This file
is a reminder list, not legal advice. When in doubt, the agent reports a risk
and the authors decide.

---

## 1. Maps of China · 中国地图合规

### 1.1 Use an official base map and show the review number

- Under the 《地图管理条例》 (State Council Order No. 664, 2015), maps made
  public in China must pass map review (地图审核), and an approved map must
  carry its **审图号 (map review number)**. Exemptions and the scope of these
  rules (which maps, which uses, which publications): **以官方要求为准**.
- The simplest compliant route is a base map from the **国家标准地图服务
  (Standard Map Service of the Ministry of Natural Resources)**, which
  publishes standard maps with their own 审图号. Follow that service's
  instructions on how to show the number and on what changes are allowed.
  Whether a modified or overlaid map needs its own review: **以官方要求为准**.
- Third-party global boundary datasets (global administrative-boundary
  libraries, generic world maps) may draw China's borders differently from the
  official map. Do not use them as the national boundary of China. Whether
  they may be used for internal or sub-national units: **以官方要求为准**.
- Record the base-map source in `basemap` and the review number in
  `review_number` on the figure card. If either is missing, the checklist item
  is **at risk** and the agent says so. The agent does not decide that it is
  fine to omit.

### 1.2 South China Sea islands and the dashed line · 南海诸岛与断续线

- A map of the whole country shows the **South China Sea islands (南海诸岛)**,
  either in the main map or as an inset, with the dashed boundary line
  complete.
- **Terminology varies.** Chinese and English texts call the line
  “断续线”, “九段线 (nine-dash line)” or “十段线 (ten-dash line)”. Do not
  settle the count or the geometry yourself. **Copy the line from the
  official standard map and do not edit it.** In text, use the term the
  authors and the journal accept (以期刊 / 官方要求为准).
- Do not redraw or simplify the line when reprojecting or generalising
  geometry. Check the inset after every export.

### 1.3 Taiwan, Hong Kong and Macao · 港澳台的表达

- Show Taiwan as part of China, consistent with the official standard map.
  Hong Kong and Macao are shown with special-administrative-region
  boundaries as on the standard map.
- In thematic maps, a region without data must not get a colour that reads as
  a different political status. Use the map's "no data / 资料暂缺" class and
  say so in the legend. Exact display rules: **以官方要求为准**.

### 1.4 Journals outside China

- Springer Nature journals state that the publisher remains neutral on
  jurisdictional claims in published maps. Other publishers have their own
  policies, and some ask authors to change map content. **以期刊要求为准.**
- If a journal's request conflicts with Chinese map rules (e.g. if the paper
  will also be used in China), flag it to the authors. Do not resolve it
  silently in either direction.

---

## 2. Size, fonts and export (Nature Portfolio)

- **Width:** single column **89 mm**, double column **183 mm** (Nature
  formatting guide). Draw panels at final print size so that font sizes are
  real.
- **Fonts:** Nature's figure guide asks for a sans-serif font (e.g. Arial /
  Helvetica) at small sizes, commonly cited as 5–7 pt. Exact sizes, maximum
  height and panel-label style: **以期刊要求为准**.
- **Export:** vector (PDF / EPS / SVG) with embedded fonts and editable text;
  bitmap resolution per the journal's guide (以期刊要求为准). Keep the
  script that produces each panel. A hand-assembled composite is for preview
  only.
- Other journals: use their own column widths. Record the target in `size`.

---

## 3. Colour · 色彩

- **Colour-blind friendly.** Avoid red–green contrasts and rainbow (jet)
  colour maps. Use perceptually uniform maps (e.g. viridis / cividis family)
  or a colour-blind-safe qualitative set (e.g. the Okabe–Ito set). Run a
  colour-vision-deficiency simulation before finalising.
- **One colour, one meaning.** A colour stands for the same thing in every
  figure of the paper. Keep a project palette table and write the hex codes
  and meanings in `palette`.
- Use sequential maps for ordered values. For signed values, use diverging maps
  centred on 0 or a meaningful reference. Do not encode the direction of
  significance by colour alone.
- Generate colour descriptions in captions from the plotting script, or check
  them against the figure, so caption and image cannot disagree.

References (checked against Crossref):
- Crameri, F., Shephard, G. E. & Heron, P. J. (2020). The misuse of colour in science communication. *Nature Communications* 11:5444. doi:10.1038/s41467-020-19160-7
- Wong, B. (2011). Points of view: Color blindness. *Nature Methods* 8(6):441. doi:10.1038/nmeth.1618

---

## 4. Source data and captions · 源数据与图注

- **Source data.** For every panel, export the numbers behind it (CSV / XLSX)
  and record the path in `data_path`. Many Nature Portfolio journals ask for
  Source Data files for main-text figures. Whether it is required:
  **以期刊要求为准**.
- **Traceability.** Every number printed in a figure traces to a result table
  or a claim card. No hand-typed numbers.
- **Captions state:**
  - the sample size (people, units, days, cells…);
  - the kind of interval (e.g. 95% CI, which clustering or bootstrap);
  - the reference group and time window;
  - what was excluded.
- **Maps also state:** projection, boundary source and, for maps of China,
  the 审图号 (or where it appears).
