<%* 
// Templater template: dataset card. Create it in `10 - Cards/Datasets/`.
// Leave a prompt empty when the source does not say; never guess a value.
var ask = async (q) => { const v = await tp.system.prompt(q, ""); return v ? '"' + v.replace(/"/g, "'") + '"' : ""; };
-%>
---
tags: [dataset]
name: <% tp.file.title %>
aliases: []
ch: 
category: dataset
featured: false
related: []
keywords: []
provider: <%* tR += await ask("数据提供方（机构 / 作者 / 平台）"); %>
source_url: <%* tR += (await tp.system.prompt("来源链接（可留空）", "")) || ""; %>
doi: <%* tR += (await tp.system.prompt("数据 DOI（可留空，不要猜）", "")) || ""; %>
license: <%* tR += await ask("许可（如 CC BY 4.0 / ODbL 1.0 / 私有；不清楚就留空）"); %>
version: <%* tR += await ask("版本 / 快照日期"); %>
data_type: <%* const _t = ["vector", "raster", "points", "table", "trajectory", "text"]; tR += (await tp.system.suggester(_t, _t, false, "数据类型")) || ""; %>
crs: <%* tR += await ask("坐标系（如 EPSG:4326 / GCJ-02 / BD-09；没有空间坐标写 none；不清楚留空）"); %>
spatial_resolution: <%* tR += await ask("空间分辨率 / 空间单元（如 0.25° / 1 km / 地级市）"); %>
spatial_extent: <%* tR += await ask("空间范围"); %>
temporal_coverage: <%* tR += await ask("时间覆盖（起止，注明时区 / 日界）"); %>
temporal_resolution: <%* tR += await ask("时间分辨率（hourly / daily / monthly / yearly / event）"); %>
size: <%* tR += await ask("体量（大小 / 行数）"); %>
local_path: <%* tR += await ask("数据所在路径：写相对项目数据文件夹或仓库的路径，不写含用户名的绝对路径（库同步或分享时会带出去）；敏感数据也只写位置，不贴内容"); %>
verified: <%* const _v = ["unverified", "verified", "issues"]; tR += (await tp.system.suggester(["未核验", "已核验", "有问题"], _v, false, "核验状态")) || "unverified"; %>
verified_date: <%* tR += (await tp.system.prompt("核验日期 YYYY-MM-DD（未核验就留空）", "")) || ""; %>
used_by: <%*
  const _ub = await tp.system.prompt("被哪些项目使用？写项目主页的名字（40 - Projects/<名>/<名>.md），逗号分隔", "");
  if (_ub && _ub.trim()) {
    tR += "\n" + _ub.split(/[,，]/).map(x => x.trim()).filter(Boolean).map(x => `  - "[[${x.replace(/["'\[\]]/g, "")}]]"`).join("\n");
  }
%>
sensitive: <%* tR += ((await tp.system.suggester(["否（公开数据）", "是（含个人信息 / 受限 / 不可外发）"], ["false", "true"], false, "是否敏感")) || "false"); %>
---

## 概况

一两句话：这是什么、怎么采集或生产的、在研究里扮演什么角色。

- 关键字段：
- 主要规模：
- 相关文档（DATA_README / 数据目录 / 论文）：

## 字段出处

> 每个非空字段写出处（文件名 + 章节或行号，或论文 DOI）。读不到出处的字段在 frontmatter 里留空，并在这里写“未找到”。

| 字段 | 出处 |
|---|---|
| crs | |
| spatial_resolution | |
| temporal_coverage | |
| license | |
| version | |

## 已知陷阱

> 每条后面写出处；查不到出处的不写。通用陷阱见技能的 `references/common-pitfalls.md`。

- 

## 核验记录

> 范围 / 极值、日历完整性、镜像或版本一致性、坐标系抽查。异常先写在这里并报告，再决定能否使用。
> 没有空间坐标的数据，坐标系一项写“不适用”加理由（如“无坐标，按行政区划代码连接”），改查连接键与区划年份是否对得上。

| 日期 | 核验内容 | 结论 | 证据 |
|---|---|---|---|
| <% tp.date.now('YYYY-MM-DD') %> | | | |

## 处理与派生产品

- 上游输入：
- 清洗规则 / 处理脚本：
- 派生产品（位置、行数、用途）：

## 引用格式

- 数据引用：
- 方法文献：
- 致谢 / 许可要求：
- Data Availability 范例句：

## 相关论文（按 keywords 自动反查）

> 文献的 `keywords` 里写上本卡的 `name` 或 `aliases`，下面的视图就会自动列出它。

![[概念反查.base#相关论文]]
