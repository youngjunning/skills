# Joyally Design 完整设计方法

Joyally Design 使用可并列选择的审美方向、语义 tokens、跨平台状态契约和交付标准。中国风、景观与时尚潮流可以按产品任务并列或结合；[景观方向](visual-language.md)与时尚方向的[小香风](fashion-xiaoxiang.md)分别提供主题规则和视觉样本。完整设计引擎提供领域方法、专项判断与工具；每个阶段产生同一份可继续使用的结果。

本文件写 Joyally 的统一规则。具体做法按 [能力路由](capability-routing.md)读取本机安装目录中的完整参考；43 份参考和 11 个脚本均保留原路径与原参数。用户当前任务与项目规则决定范围、许可和发布。

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

## 按页面领域融合

| 领域 | 读取参考 | Joyally 的落地要求 |
| --- | --- | --- |
| 品牌页、官网、发布页 | `direction-persuasion.md`、按需 `direction-concept.md`、`direction-whole-page.md` | 按选定审美方向组织构图与材质；首屏的主要动作与内容关系延续到后续区块。图像只在承担叙事时使用。 |
| 画廊、文档与内容站 | `direction-content.md`、按需 `staging-containers.md`、`cards.md` | 内容对象先出现；标题与导航占用的首屏面积服从浏览任务。卡片区分对象属性，触屏也能打开。 |
| 工作台与后台 | `direction-workspace.md`、按需 `workspace-data.md`、`workspace-interaction.md` | 判断字段和主要动作靠近对象；密度服从任务频率。表格、日志和表单用清晰表面，当前操作与焦点使用对应语义色。 |
| 游戏与强反馈操作 | `play.md`、`play-craft.md` | 规则和反馈可被感知；视觉仍守住文字、操作和状态对比度。 |
| 单个组件 | `component.md`、`interaction-and-state.md` | 从语义 alias 消费颜色与尺度；在真实尺寸展示 default、hover、pressed、selected、focus、disabled、loading、empty、error、success 中适用的状态。 |
| 存量改造与重设计 | `existing-project.md`、`existing-project-workflow.md`、`existing-polish.md`、`task-redesign.md`、`iterate.md` | 先留住已确认的身份、内容和操作，再找共享 token、组件与流程根因；修正后对照前后画面与原任务路径。 |

## 从方向到实现

1. **方向**：使用 `design-direction.md`；需要明确比较时再读 `task-explore.md`、`style-explorer.md`。固定事实、主任务和操作语义，比较审美方向、内容顺序、骨架、密度、图像职责与交互方式；并列或组合的候选须在当前品牌内成立。
2. **代表页**：按 `implementation.md` 做一页或一条关键流程。先定 Seed → Map → Alias → Component 的取值路径，再让页面组件消费语义 token；映射主题、明暗和适用的季节或材质时，状态含义保持不变。
3. **专项**：按选定方向读景观的 `visual-language.md` 或时尚的 `fashion-xiaoxiang.md`，再根据实际问题读 `visual-polish.md`、`layout-surfaces.md`、`layout-and-viewport.md`、`media.md`、`image-ideation.md`、`motion.md`、`scroll-narrative.md`、`ornament.md`。视觉判断以 Joyally 品牌不变量为准；需要素材时记录来源与许可；动效在减少动态效果下保持完整信息。
4. **铺开**：多页使用 `rollout.md`，项目规范使用 `design-spec.md`。把确认过的色彩职责、组件状态、页面密度和样板页写进项目既有设计规范；不把单页临时尺寸变成全局规则。

## 双重验收

`shoot`、`explore`、`measure`、`design-check` 等工具产生画面与结构证据；Joyally 的 [验收契约](validation.md)检查任务和语义。至少回答两组问题：

- **画面**：首屏有无清楚的主要对象与下一步；所选方向的层级是否帮助扫读；中文、长文和窄屏是否可读；材质与动效是否干扰任务。
- **操作**：键盘与触控是否可用；选中、焦点、加载、空态、错误和成功是否准确；失败后能否继续；减少动态效果时是否完整。

只读评审读 `task-review.md`、按领域读 `workspace-review.md`；独立视觉与 UX 评审依 `visual-review.md`、`ux-review.md`、`review-loop.md` 执行，评审者按 `reviewer-manual.md`、`review-modes.md`、`ux-reviewer.md` 走查。主执行者依据实际画面和操作修正，并核对 Joyally 不变量。截图、构建、静态检查和人工操作各证明自己的范围。

## 专项质量补位

方向、视觉精修、操作状态和评审循环已经属于主流程。出现真实中文排版、本地化、字体缩放、权限受限、慢请求，或用户要求性能／无障碍技术审计时，再读取 [专项质量检查](design-quality.md) 的相应条目。它提供修复排序与可复现证据要求，不重新开一套方向或重复视觉评审。
