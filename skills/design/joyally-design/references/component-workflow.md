# React 组件工作流

用于编码 Agent 在 React Web 中后台选择、安装和组合组件。Joyally Design 负责设计语义、状态和页面组合；可执行的基础组件源码由目标项目中的 shadcn/ui CLI 管理。H5、Chrome 扩展和 React Native 沿各自平台参考，不套用本路径。

1. **检查项目。** 先读项目指令、`components.json`、现有 `components/ui`、主题变量和包管理器。列出本次界面需要的操作、输入、数据、导航与反馈部件，以及项目已有实现。完成条件：每个部件有现成组件、待安装组件或明确的组合方案。
2. **选组件。** 在 [shadcn/ui 组件目录](https://ui.shadcn.com/docs/components)按部件检索；已安装组件直接读目标项目的源码与用例。Joyally 自有新建中后台用官方 CLI 的 `add --all` 建立完整基础；其他项目沿用现有组件，局部功能只安装选中的组件。先运行当前 CLI 的 `--help` 核对命令和包管理器，再执行安装。对 Data Table、Date Picker 等组合控件，分别确定底层 Table、Calendar、Popover 等依赖及目标项目的数据和日期契约。完成条件：来源、文件路径和组合依赖可回查。
3. **落地 Joyally。** 读 [React 设计系统](react-design-system.md)与 [token 契约](token-contract.md)，将目标主题的 seed、map、alias、component 角色接入项目。基础控件保留官方键盘和可访问性行为；业务术语、路由、校验和数据源沿用目标项目。已有品牌使用项目品牌派生 tokens，不照搬 Joyally 展示站的色值。完成条件：代表性页面上的基础控件与组合控件共用语义角色。
4. **验收。** 在真实页面检查默认、hover、focus、disabled、loading、empty、error 和 success，以及桌面、窄屏、键盘和 reduced motion。逐个核对本次新增或修改的按钮、输入框、选择器等控件是否真正加载所选组件样式与语义 tokens；若仍呈现浏览器默认外观，修复样式接入或改用对应组件后再交付。浮层需实际打开，表单需触发校验和恢复，表格需操作搜索、排序或分页。源码存在、构建通过和页面可用分别记录证据；目录链接也要点击确认目标可读。完成条件：本次涉及的每个组件都有可见预览或实际页面状态，且关键操作有结果。

给编码 Agent 的任务可以这样写：

> `$joyally-design 在这个 React 中后台实现任务列表。先检查现有组件与主题；选用 Button、Input、Select、Table 和反馈组件，在现有数据层上组合搜索、筛选、分页与空状态。保留项目业务逻辑，验证窄屏、键盘和错误恢复，并列出实际使用的组件源码路径。`

展示站点只能作为视觉参考。编码 Agent 以目标项目中的已安装组件和 shadcn/ui 官方 CLI 为源码来源，并在目标项目的真实页面中验收。
