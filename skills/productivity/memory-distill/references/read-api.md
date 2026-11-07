# 兼容读取接口

所有路径相对于显式配置的 HTTP(S) 根地址，不接受凭证、子路径、查询参数或片段。只读取已授权的共享快照；客户端过滤不能替代服务端访问控制。

| 路径 | 响应与用途 |
| --- | --- |
| `/api/persona` | 含 recordsUrl、evidence 的介绍 |
| `/api/records`、`/api/records/:id` | `{ records }`、`{ record }`，仅 visibility: shared |
| `/api/catalog` | `{ documents, generatedAt, source }`，含稳定 ID、真实日期、原文 SHA-256、可选同源 url |
| `/api/search` | `[{ id, text }]` 文章全文索引 |
| `/raw/:id` | text/plain 或 text/markdown 原文字节，先校验再分页 |
| `/api/graph` | `{ nodes, edges }`，references、belongs_to 与其他关系分开 |
| `/api/favorites`、`/api/favorites/:id` | `{ version, favorites }`、`{ favorite }` |
| `/api/research`、`/api/excerpts` | `{ version, items }` |
| `/api/okr` | period、objectives、materials 及实际目标元数据 |
| `/api/skills` | `{ version: 1, updatedAt, skills }` |
| `/api/subjects` | `{ version: 1, subjects }` |
| `/api/activity` | version、start、end、entries、counts、weekly；时间与整周计数照原响应保留 |

## 命令和筛选

`persona`、`search QUERY`、`record ID`、`article ID`、`graph ID|favorite:ID`、`favorites [QUERY]`、`favorite ID`、`research [QUERY]`、`excerpts [QUERY]`、`okr [QUERY]`、`skills [QUERY]`、`subjects [QUERY]`、`activity [QUERY]`。

ID 是 16 位小写十六进制值。记录链接为 `/records/:id`，百宝箱为 `/favorites#ID`，其他集合沿各自页面真实入口。文章优先使用目录的同源 url，缺省 `/blog/:id`，站点 wrapper 可配置 `/docs/:id`；不接受跨站文章阅读地址。

`--limit` 默认 6，范围 1–20，各类别独立限制。`--chars` 默认 12000，范围 1–40000；`--offset` 默认 0，按 JavaScript 字符串索引计算，继续读取用返回的 nextOffset。`activity` 保留原始 counts 与 totalEntries，entries 是本次筛选后的有界清单，不把录入时间当事件发生时间。

`--type tool|reference|concept|method`、`--subject ID`、`--used` 只筛选百宝箱，在 search 中不影响其他类别。主题 ID 为 grounding、browser、memory、engineering、business、design、infra、agents。`--used` 包括 trial、adopted、retired 的有证据项目历史；回答时保留实际阶段。

## 百宝箱和归属

v2 的 kind 为 resource/note，type 为 tool/reference/concept/method。笔记正文在 note.body，date 与 recordedAt 是原始和录入时间，context/example/boundary 可省略；attribution 为 user/source/ai/mixed，与 explicit/discovered 的保存方式独立。混合内容结合正文区分本人表达与补充。主题相同不证明因果、引用或采用。

资源 usages 逐项目保存 project、stage、purpose、evidence；收藏或某项目采用不证明本人掌握全部原理。来源与 relatedIds 保留真实关联，脚本不继续抓外链。v1 部署过渡仍可读，但不推断缺失的主题或归属；favorite 单条接口仅在 404 且集合明确为 v1 时回退，其他错误照实报告。

## 失败与边界

search 并行读取七类来源；snapshot 只描述文章目录，不能宣称所有接口为同一个原子版本。任一必要接口不存在或结构不匹配时失败，不静默丢类别。

每次响应最多 8 MiB，超时 15 秒。跨站重定向、错误内容类型、非共享条目或原文 SHA-256 不匹配时失败；stdout 输出 JSON，stderr 输出 `{ error }` 并返回非零状态。所有操作为 GET，不需要模型 key，不调用站点问答。
