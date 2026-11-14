# 系统架构关系图

当读者需要回答“谁调用谁、谁提供资源、哪一段已接通”时，使用系统架构关系图。它以节点和有向连线表达运行关系；分类脑图只表达归属，不能替代调用和依赖关系。沿用 `diagram_type: "architecture"` 的 typed JSON IR、Joyally 主题与 `diagram validate/deliver` 链路。

## 先整理事实

1. 列产品入口、运行服务、数据与配置资源、身份权限、交付与可观测平台。产品名与仓库名分开：一个产品对应多个仓库时只画一个产品节点，仓库名放副标题。
2. 为每条线记录方向和动作：`请求`、`读取配置`、`读写数据`、`投递任务`、`采集日志`、`追踪请求`、`部署`、`授权`。若只是“平台已登记”或“预留能力”，不画成运行时调用。
3. 分开标注证据状态：资源已开通、代码已接入、环境已部署、真实请求已验证、待验收。不能只用线型或颜色表达状态；在线标签、节点 `tag` 或正文说明中写明。
4. 项目事实来自源码、配置、运行记录或用户确认。推测关系不要画实线。没有来源的运行路径放入待核对清单。

## 图面组织

- 主路径只保留读者完成一次任务必经的入口与服务；配置、存储、身份和观测按侧翼分组。大图按“入口 → 服务 → 资源 / 观测”阅读，避免把所有平台排成一条执行流程。
- 每条连接必须在 JSON IR 的 `connections` 中有独立端点和可辨方向。表示动作的边写简短 `label`；`dashed` 只用于明确的规划或待核对关系，并同时写文字状态。
- 同一资源的控制面与数据面分开：例如 CC 的“授权资源”与服务的“读写 OSS”、Aone 的“部署服务”与前台的“调用服务”。不能用一个箭头代替两种动作。
- 同一请求的日志和追踪是并行观测关系：应用日志进入 SLS，TraceId / Span 进入链路系统；不能把 SLS 画成 EagleEye 的前置步骤。
- 首屏主路径及文字应在实际阅读尺寸可辨。若边大量交叉，先减少非关键节点或拆成“业务请求 / 资源交付 / 观测排障”三个视图，不靠整体缩小解决。

## Joyally 实现

参考 [交互图表](interactive-diagrams.md) 和 `runtime/diagram/schemas/architecture.schema.json`。编写 `components`、`connections`，必要时才添加有事实依据的 `boundaries`；设置 `meta.locale: "zh-CN"` 与可移植的 `meta.output`。节点类别使用已有 `frontend`、`backend`、`database`、`cloud`、`security`、`messagebus`、`external`；类别色不代表验收状态。

先运行 `node scripts/design-engine.mjs diagram validate architecture input.json --quality showcase --json`，通过后运行 `diagram deliver architecture input.json output.html --quality showcase --json`。需要视觉证据时再运行 `visual-check`，核对桌面和窄屏、缩放、聚焦、边标签、打印及文字 fallback。交付时分别报告 IR 校验、HTML 生成和实际画面检查。
