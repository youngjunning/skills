# 兼容读取接口

所有路径相对于用户显式配置的 HTTP(S) 站点根地址。地址不得包含凭证、子路径、查询参数或片段。

| 路径 | 响应 |
| --- | --- |
| `/api/persona` | 包含 `recordsUrl` 与 `evidence` 的介绍 |
| `/api/records`、`/api/records/:id` | `{records}`、`{record}`，只使用 `visibility: shared` |
| `/api/catalog` | `{documents, generatedAt, source}`，文档包含稳定 ID、标题与原文 SHA-256 |
| `/api/search` | `[{id,text}]` 文章检索索引 |
| `/raw/:id` | `text/plain` 或 `text/markdown` 原文 |
| `/api/graph` | `{nodes,edges}`，关系区分 `references` 与 `belongs_to` |
| `/api/favorites` | `{favorites}`，只使用共享收藏 |

阅读页使用 `/records/:id`、`/blog/:id` 与 `/favorites`。ID 为 16 位小写十六进制值。站点应在服务端排除私有与未公开内容；客户端过滤不能代替访问控制。

命令包括 `persona`、`search QUERY`、`record ID`、`article ID`、`graph ID`、`favorites [QUERY]`。`--limit` 默认 6，范围 1–20；文章 `--chars` 默认 12000，范围 1–40000；`--offset` 默认 0，按 JavaScript 字符串索引计算，继续读取时使用返回的 `nextOffset`。

每次响应最多读取 8 MiB，超时 15 秒。跨站重定向、错误内容类型、错误 ID、非共享记录或原文哈希不匹配时失败。stdout 输出 JSON，错误写 stderr 并返回非零状态。
