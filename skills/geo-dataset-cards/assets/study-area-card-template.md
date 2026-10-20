<%*
// Templater template: study-area card. Create it in `30 - Metadata/StudyAreas/`.
// Study areas are "地" (Metadata), not concept cards: no `category`, no `featured`.
var ask = async (q) => { const v = await tp.system.prompt(q, ""); return v ? '"' + v.replace(/"/g, "'") + '"' : ""; };
-%>
---
tags: [study-area]
name: <% tp.file.title %>
aliases: []
level: <%* const _l = ["country", "province", "city", "district", "neighbourhood"]; tR += (await tp.system.suggester(["国家", "省", "城市", "区县", "片区"], _l, false, "研究区层级")) || ""; %>
admin_code: <%* tR += await ask("行政区划代码（字符串；查不到留空）"); %>
boundary_source: <%* tR += await ask("边界来源与版本（如 GADM 4.1；某年区划）"); %>
crs: <%* tR += await ask("边界文件坐标系（不清楚留空）"); %>
climate_zone: <%* tR += await ask("气候分区（注明体系，如 Köppen Cfa）"); %>
population: <%* tR += await ask("人口（注明来源与年份）"); %>
used_by: <%*
  const _ub = await tp.system.prompt("被哪些项目使用？写项目主页的名字，逗号分隔", "");
  if (_ub && _ub.trim()) {
    tR += "\n" + _ub.split(/[,，]/).map(x => x.trim()).filter(Boolean).map(x => `  - "[[${x.replace(/["'\[\]]/g, "")}]]"`).join("\n");
  }
%>
---

## 边界来源与版本

- 边界文件、版本、年份（行政区划按哪一年的区划）：
- 与哪些数据集的空间单元对得上（链到数据集卡片）：
- 单元编码方式：
- 出处文件：

## 注意事项

> 每条写出处。常见：行政区划调整、海陆掩膜、驻地点与人口重心不一致、数据覆盖缺口。

- 
