# React 组件工作流

用于编码 Agent 在 React Web 的中后台与展示页选择、安装和组合组件。Joyally Design 负责设计语义、状态和页面组合；基础组件从目标项目或 shadcn/ui CLI 取得，Magic UI、React Bits 与 ReactDrops 在需要时按组件接入。H5、Chrome 扩展和 React Native 沿各自平台参考，不套用本路径。

1. **检查项目。** 先读项目指令、`components.json`、现有 `components/ui`、主题变量和包管理器。列出本次界面需要的操作、输入、数据、导航与反馈部件，以及项目已有实现。完成条件：每个部件有现成组件、待安装组件或明确的组合方案。
2. **选组件。** 在 [shadcn/ui 组件目录](https://ui.shadcn.com/docs/components)按基础部件检索；工作台中的指标、动态列表、文件或代码视图及重点操作也可查 [Magic UI 组件目录](https://magicui.design/docs/components)，文字、背景与微交互可查 [React Bits 组件目录](https://www.reactbits.dev/)。需要玻璃、折射、物理或空间动效时，查 [ReactDrops 全量目录与来源](reactdrops-components.md)。这些展示组件按任务选用，不代替操作控件的语义与状态。已安装组件直接读目标项目的源码与用例。Joyally 自有新建中后台用官方 CLI 的 `add --all` 建立完整基础；其他项目沿用现有组件，局部功能只安装选中的组件。先运行当前 CLI 的 `--help` 核对命令和包管理器，再执行安装。对 Data Table、Date Picker 等组合控件，分别确定底层 Table、Calendar、Popover 等依赖及目标项目的数据和日期契约。完成条件：来源、文件路径和组合依赖可回查。
3. **落地 Joyally。** 读 [React 设计系统](react-design-system.md)与 [token 契约](token-contract.md)，将目标主题的 seed、map、alias、component 角色接入项目。基础控件保留官方键盘和可访问性行为；业务术语、路由、校验和数据源沿用目标项目。已有品牌使用项目品牌派生 tokens，不照搬 Joyally 展示站的色值。完成条件：代表性页面上的基础控件与组合控件共用语义角色。
4. **验收。** 在真实页面检查默认、hover、focus、disabled、loading、empty、error 和 success，以及桌面、窄屏、键盘和 reduced motion。逐个核对本次新增或修改的按钮、输入框、选择器等控件是否真正加载所选组件样式与语义 tokens；若仍呈现浏览器默认外观，修复样式接入或改用对应组件后再交付。浮层需实际打开，表单需触发校验和恢复，表格需操作搜索、排序或分页。源码存在、构建通过和页面可用分别记录证据；目录链接也要点击确认目标可读。完成条件：本次涉及的每个组件都有可见预览或实际页面状态，且关键操作有结果。

给编码 Agent 的任务可以这样写：

> `$joyally-design 在这个 React 中后台实现任务列表。先检查现有组件与主题；选用 Button、Input、Select、Table 和反馈组件，在现有数据层上组合搜索、筛选、分页与空状态。保留项目业务逻辑，验证窄屏、键盘和错误恢复，并列出实际使用的组件源码路径。`

展示站点用于选型参考。编码 Agent 从目标项目中已安装组件、shadcn/ui 官方 CLI、[Magic UI 安装入口](https://magicui.design/docs/installation)、[React Bits 安装入口](https://www.reactbits.dev/get-started/installation)或 [ReactDrops 官方组件页](https://reactdrops.dev/components)获取所选组件源码，并在目标项目的真实页面中验收。记录组件名称、上游链接、变体、引入的依赖和许可声明；[React Bits 许可](https://github.com/DavidHDev/react-bits/blob/main/LICENSE.md)使用 MIT + Commons Clause；[ReactDrops Component License 1.0](https://github.com/crisjavr/reactdrops/blob/main/LICENSE)允许成品项目使用，但独立组件库、UI kit、registry 和模板再分发需另获书面许可。组件源码留在使用它的应用内，不随 Joyally Design 技能或独立组件包再分发。
