# Joyally Design 能力路由

Joyally Design 的领域方法、专项参考、工具、素材与测试都在本目录。按需读取本次任务涉及的文件；来源包更新时用 `scripts/sync-upstream.py` 检查变更和冲突，先维护 Joyally 视觉契约再导入。

先读[完整设计流程](../DESIGN_PROCESS.md)和[融合方法](fused-method.md)。它规定领域方法如何落到 Joyally 的视觉语义、组件和跨平台验收；本文件给出每一类参考与工具的路径。两份文件合用，形成单一的 Joyally Design 输出。

## 运行顺序与边界

改法已完全明确且没有新的设计判断时，直接按项目规则实施和验收；以下路径用于需要设计判断的任务。

1. 读取项目指令、当前页面与用户目标，选择本次交付物和改动范围。读取 `../DESIGN_PROCESS.md` 的任务路由，再按下表读取本次领域与专项文件；不把整个 `references/` 目录一次性装入上下文。
2. Joyally 品牌界面先按任务和品牌环境从六套并列主题中选择，再按[token 契约](token-contract.md)与目标平台参考固定语义、状态和可读性。选用景观主题时读[景观视觉规则](visual-language.md)，选用雪山时再读[雪山主题细则](alpine-snow-mountains.md)；选用小香风时读[小香风主题](fashion-xiaoxiang.md)及[20 张参考图](../assets/references/xiaoxiang/README.md)。随包平台 token 完整实现青山湖预设，小香风另有浅色与深色语义样本；进入具体产品仍须映射组件并检查对比度。每轮留下结构、tokens、组件状态和验收证据。其他品牌沿用其现有设计系统。
3. 用户本轮要求、项目现有约束和平台行为决定可改范围、确认点、构建与发布。阶段确认点只在确有必要时使用；用户已授权的工作继续完成。用户已授权直接实施时完成到验收；需要独立评审且当前环境允许时可按对应评审材料与派发方法执行。
4. Web/HTML 的对比页、截图、素材与规范校验可使用本目录工具；macOS、iOS、Android、React Native 的画面与交互验收仍用对应平台工具。报告与图表继续用 Joyally Design 的 `report`、`deck` 和 `diagram` 命令。工具输出是证据，需亲自看画面并核对真实操作。



## 任务路由

以下文件均相对于 本目录。先读一行任务入口；仅在问题出现时继续读专项。领域文件中若提示跳过通用方向步骤，按领域文件处理。

| 任务 | 领域入口 | Joyally 接法 |
| --- | --- | --- |
| 新建品牌、发布或说服型页面 | `direction-persuasion.md`；需要概念时 `direction-concept.md`，整页延续看 `direction-whole-page.md` | 保留已定品牌与主张；以页面内容决定首屏骨架和叙事 |
| SaaS、后台、控制台、编辑器 | `direction-workspace.md` | 以对象、判断字段、动作与反馈组织工作区；复杂报表读 `workspace-data.md`，复杂高频操作读 `workspace-interaction.md` |
| 画廊、商店、信息流、文档站 | `direction-content.md` | 先让可浏览对象成为主角；需要策展容器或卡片时读 `staging-containers.md`、`cards.md` |
| 游戏、抽奖、计时养成或强手感操控 | `play.md`、`play-craft.md` | 以规则、反馈和手感验收；视觉身份仍由产品决定 |
| 单个组件深度打磨 | `component.md` | 在真实尺寸与状态中打磨；工作区组件同时服从 `direction-workspace.md` 的组件规则 |
| Chrome 扩展图标制作或精修 | `chrome-extension-icon.md` | 以工具栏实际显示尺寸判断识别度；生成源图时调用 `joyally-imagegen` |
| React Web 页面或工作台 | `react-design-system.md`；工作台再读 `direction-workspace.md` | 新建界面默认从 Magic UI registry 选组件；H5、Chrome 扩展和 React Native 按各自场景路径 |
| H5 页面 | `h5-ui.md`；按内容领域读取对应参考 | 以 daisyUI 作为默认组件基础，保留项目框架和交互合同 |
| Chrome 扩展页面或独立窗口 | `chrome-extension-ui.md`；工作区界面再读 `direction-workspace.md` | 以 daisyUI 作为默认组件基础，按扩展打包与实际入口验收 |
| 新界面方向未定 | 适用领域入口；领域未覆盖时 `design-direction.md` | 用真实产品事实与参考形成可落地方向；默认深化一个 |
| 用户要求多方向或版式比较 | `task-explore.md`、`style-explorer.md` | 固定内容、主任务与 Joyally 品牌语义，比较结构、图像、密度或获准的变量 |
| 已有页面局部精修、回改 | `existing-polish.md`、`iterate.md` | 看现状与前后画面，保留已确认的身份和行为；明确改法的小改动直接完成 |
| 存量产品升级、改流程或加功能 | `existing-project.md`；流程变更读 `existing-project-workflow.md` | 先走实际任务，定位共享变量、组件或流程根因，再改源头 |
| 重设计或按图还原 | `task-redesign.md` 或 `layout-and-viewport.md` | 先锁定保留项；按图还原时参考图决定可见版式，原生平台仍服从系统交互 |
| 把已认可原型转成项目代码 | `implementation.md` | 用项目现有组件和 tokens 实现，对照原型画面与状态 |
| 只读 UI/UX 评审 | `task-review.md`；复杂工作区加 `workspace-review.md` | 交可复现位置、证据、影响与建议，不把评审变成改版 |
| 多页铺开或规范治理 | `rollout.md`、`design-spec.md` | 用代表性页面定共享规则；规范写入项目既有位置，并核对变量、组件和样板页 |

## 专项能力

| 出现的问题 | 按需读取的专项参考 |
| --- | --- |
| 视觉层级、字体、色彩、表面或细节粗糙 | [通用视觉规则](visual-craft.md)、`visual-polish.md`；选用景观主题时再读[景观视觉规则](visual-language.md) |
| 状态、表单、列表、错误恢复或操作层级 | `interaction-and-state.md` |
| 多栏、浮层、独立滚动、窄屏或截图比例 | `layout-surfaces.md`、`layout-and-viewport.md` |
| 主视觉、真实素材、配图许可、成套图或 UI 生图 | `media.md`、`image-ideation.md` |
| 交互反馈、空间连续性、滚动叙事或少量特效 | `motion.md`、`scroll-narrative.md`、`ornament.md`；按产品任务决定是否需要，不把特效变成默认要求 |
| 视觉或 UX 独立走查、修正轮次 | 主执行者读 `visual-review.md`、`ux-review.md`、`review-loop.md`；独立评审者按评审协议读 `reviewer-manual.md`、`review-modes.md`、`ux-reviewer.md`；评审结论仍需主执行者核对实际画面与功能 |
| 候选、截图、过程素材放置 | `workdir.md`；项目已有目录约定优先 |

## 直接使用设计工具

使用前读 `tools.md` 和相应脚本的 `--help`。调用 `node <joyally-dir>/scripts/design-engine.mjs <命令> [工具参数]`；它直接运行本目录脚本，保留工具的输出和退出码。常用命令如下；`path <相对文件>` 可定位本目录的任一参考、素材或脚本，`run <脚本名> [参数]` 可运行 本目录脚本，保持完整能力可达。输出放在项目约定或临时任务目录，不写入技能安装目录。

| 目的 | Joyally 命令 | 验收 |
| --- | --- | --- |
| 生成 HTML 报告或演示 | `report`、`deck` → [HTML 报告与演示](html-reports.md) | 核对离线打开、阅读或播放、打印 |
| 生成自包含交互图表 | `diagram` → [交互图表](interactive-diagrams.md) | 校验输入、图表内容和关键交互 |
| 把 HTML、图片或本机页面组装成同屏对比页 | `explore` → `scripts/build_explorer.py` | 看每个候选实际画面；选定方向后继续完整页面 |
| 截图、交互状态、前后拼图、动效帧与可读性提示 | `shoot` → `scripts/shoot.mjs` | 桌面与窄屏、关键状态、真实点击路径；截图成功仍要亲自看 |
| 查找并下载有来源说明的图片、纹理或参考 | `media` → `scripts/curate-media.mjs` | 核对原始来源、用途、许可、尺寸与实际画面 |
| 处理图片比例、尺寸与格式 | `prep-image` → `scripts/prep-image.mjs` | 核对页面中最终显示尺寸与清晰度 |
| 测量参考图或固定画布 | `measure` → `scripts/measure_reference.py` | 用测量辅助布局，不把差异分数当设计质量 |
| 检查项目设计规范的路径与变量 | `design-check` → `scripts/check_design_md.py` | 回读规范和代表性页面，确认与代码一致 |
| 查阅卡片构型 | `../assets/cards/gallery.html` 与 `cards.md` | 打开现成画廊，按当前对象选择构型；常规设计不运行维护用的 `build_cards.py` |
| 探索图像方向 | `image` → `scripts/joyally-image.mjs` | 仅在任务需要且有使用权限时调用；生成图需进入实际页面验证 |

例如 `node <joyally-dir>/scripts/design-engine.mjs explore <候选目录>` 生成对比页，`node <joyally-dir>/scripts/design-engine.mjs shoot <页面> --size desktop,mobile --out <截图目录>` 取得双端画面。`node <joyally-dir>/scripts/design-engine.mjs design-check <项目规范>` 检查项目设计规则。需要完整参数时在命令末尾加 `--help`。

更新源包时使用 `scripts/sync-upstream.py`，检查冲突后再导入，并重新核对路由与脚本参数。
