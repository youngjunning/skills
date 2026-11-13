# Joyally Design 完整设计方法

Joyally Design 按任务明确范围与页面领域，再完成方向、实现、截图和走查。语义 tokens、跨平台状态、主题资产、报告与交互图表能力按实际需要使用；七套主题只在适合当前品牌与任务时使用。景观主题按[景观视觉规则](visual-language.md)取材，香奈儿风按[包袋、巴黎夜景与编辑呈现参考](fashion-xiaoxiang.md)取材，太空主题按[轨道与地平线规则](space.md)取材。

本文件写设计方法的选择规则。具体做法按 [能力路由](capability-routing.md)读取本机安装目录中的参考与工具。用户当前任务与项目规则决定范围、许可和发布。

## 选择依据

| 判断 | 采用方法 | 保留边界 |
| --- | --- | --- |
| 页面该怎样组织 | 按任务选说服、工作区、内容浏览或游玩领域；存量项目先走真实操作并核对现有规范 | 不让湖色、景观或组件库预设先决定骨架 |
| 视觉从哪里来 | 从当前产品的品牌、内容、素材与受众推导；Joyally 七套主题可作为有依据的候选 | 不因某主题已实现就优先套用；已确认的品牌资产优先 |
| 组件怎样落地 | Joyally 自有中后台使用完整 shadcn/ui 基础，H5 与扩展使用 daisyUI；服务其他项目时沿用其组件与平台习惯 | 语义状态与可读性跨主题保持；自有组件选择不强制其他项目迁移 |
| 结果怎样验收 | 用真实视口截图、存量前后对照与任务走查，结合跨平台 token、状态和可访问性检查 | 美观与操作分别验收，截图、源码和构建各证明其对应范围 |

方向确定时写明上述四项的依据。构图、精修减法、存量流程、主题和材质都服务于当前任务；遇到取舍时，以用户要求、产品事实、已确认品牌和实际验证结果作判断。

## 开始：锁定品牌与任务

记录实际用户、主要对象、目标动作、阅读频率、设备、已有页面和可改范围。对于 Joyally 自身的页面，还要固定下列共同契约；视觉取值从选定方向与主题映射：

| 不变量 | 可检查的结果 |
| --- | --- |
| 对象与操作清楚 | 首屏可见主要对象和下一步；文字、数据、输入放在清晰表面 |
| 导航有序 | 导航和局部工具各有位置，当前项与焦点可辨 |
| 氛围服从内容 | 氛围不遮挡内容，不承担状态或操作的唯一提示 |
| 色彩有职责 | 主操作、成功、警告和错误各使用独立语义角色；具体色值由方向和主题映射 |
| 材质守住阅读 | 材质按方向选择；代码、表单和长文保留清晰表面 |
| 状态可恢复 | loading、empty、error、disabled、focus 与成功反馈均能辨别下一步 |

其他品牌使用该品牌自己的视觉不变量，同时沿用以下方法和状态契约。

## 按页面领域选择

| 领域 | 读取参考 | Joyally 的落地要求 |
| --- | --- | --- |
| 品牌页、官网、发布页 | `direction-persuasion.md`、按需 `direction-concept.md`、`direction-whole-page.md` | 按选定审美方向组织构图与材质；首屏的主要动作与内容关系延续到后续区块。图像只在承担叙事时使用。 |
| 画廊、文档与内容站 | `direction-content.md`、按需 `staging-containers.md`、`cards.md` | 内容对象先出现；标题与导航占用的首屏面积服从浏览任务。卡片区分对象属性，触屏也能打开。 |
| 工作台与后台 | `direction-workspace.md`、按需 `workspace-data.md`、`workspace-interaction.md` | 判断字段和主要动作靠近对象；密度服从任务频率。表格、日志和表单用清晰表面，当前操作与焦点使用对应语义色。 |
| 游戏与强反馈操作 | `play.md`、`play-craft.md` | 规则和反馈可被感知；视觉仍守住文字、操作和状态对比度。 |
| 单个组件 | `component.md`、`interaction-and-state.md` | 从语义 alias 消费颜色与尺度；在真实尺寸展示 default、hover、pressed、selected、focus、disabled、loading、empty、error、success 中适用的状态。 |
| 存量改造与重设计 | `existing-project.md`、`existing-project-workflow.md`、`existing-polish.md`、`task-redesign.md`、`iterate.md` | 先留住已确认的身份、内容和操作，再找共享 token、组件与流程根因；修正后对照前后画面与原任务路径。 |

## 从方向到实现

1. **方向**：使用 `design-direction.md`；需要明确比较时再读 `task-explore.md`、`style-explorer.md`。固定事实、主任务和操作语义，比较审美方向、内容顺序、骨架、密度、图像职责与交互方式；候选由产品事实支持，Joyally 主题与其他方向按相同标准判断。
2. **代表页**：按 `implementation.md` 做一页或一条关键流程。先定 Seed → Map → Alias → Component 的取值路径，再让页面组件消费语义 token；映射主题、明暗和适用的季节或材质时，状态含义保持不变。
3. **专项**：按选定主题读景观的 `visual-language.md` 或香奈儿风的 `fashion-xiaoxiang.md` 与对应参考画面；遇到通用视觉问题读 `visual-craft.md`，再根据实际问题读 `visual-polish.md`、`layout-surfaces.md`、`layout-and-viewport.md`、`media.md`、`image-ideation.md`、`motion.md`、`scroll-narrative.md`、`ornament.md`。视觉判断以 Joyally 品牌不变量为准；需要素材时记录来源与许可；动效在减少动态效果下保持完整信息。
4. **铺开**：多页使用 `rollout.md`，项目规范使用 `design-spec.md`。把确认过的色彩职责、组件状态、页面密度和样板页写进项目既有设计规范；不把单页临时尺寸变成全局规则。

## 双重验收

`shoot`、`explore`、`measure`、`design-check` 等工具产生画面与结构证据；Joyally 的 [验收契约](validation.md)检查任务和语义。至少回答两组问题：

- **画面**：首屏有无清楚的主要对象与下一步；所选方向的层级是否帮助扫读；中文、长文和窄屏是否可读；材质与动效是否干扰任务。
- **操作**：键盘与触控是否可用；选中、焦点、加载、空态、错误和成功是否准确；失败后能否继续；减少动态效果时是否完整。

只读评审读 `task-review.md`、按领域读 `workspace-review.md`；独立视觉与 UX 评审依 `visual-review.md`、`ux-review.md`、`review-loop.md` 执行，评审者按 `reviewer-manual.md`、`review-modes.md`、`ux-reviewer.md` 走查。主执行者依据实际画面和操作修正，并核对 Joyally 不变量。截图、构建、静态检查和人工操作各证明自己的范围。

## 专项质量补位

方向、视觉精修、操作状态和评审循环已经属于主流程。出现真实中文排版、本地化、字体缩放、权限受限、慢请求，或用户要求性能／无障碍技术审计时，再读取 [专项质量检查](design-quality.md) 的相应条目。它提供修复排序与可复现证据要求，不重新开一套方向或重复视觉评审。
