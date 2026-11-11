# Chrome 扩展界面

从 [主入口](../SKILL.md) 进入 Chrome 扩展的 popup、options、side panel 或独立窗口设计时读取。扩展图标另读 [扩展图标](chrome-extension-icon.md)。

## 组件基础

Chrome 扩展界面默认使用 [daisyUI](https://daisyui.com/docs/install/) 作为组件样式基础。沿用项目现有 React、Vue 或原生 HTML/JavaScript 结构，以项目语义 tokens 定义主题；daisyUI 5 按官方要求经 Tailwind CSS 4 构建。已有项目先核对现用组件和交互合同，再按本次获准范围逐步接入；用户明确指定其他组件体系或项目约束不允许接入时，记录原因与本次替代方案。

扩展页面中的生成 CSS、脚本、字体和图标随 Manifest V3 安装包本地提供，不在运行时从 CDN 加载代码。构建产物只包含本扩展实际使用的样式与资源；核对打包清单、CSP 和相对路径。

daisyUI 的 `select` 仍使用原生 `<select>`，下拉选项菜单会呈现操作系统样式。保留项目已有的值、事件、表单提交和状态恢复语义，在实际扩展窗口检查控件外观、键盘操作、焦点、读屏名称和弹层裁切；若本次目标要求自绘选项菜单，另选与现有技术栈相容的可访问行为组件。普通文本与只读数据仍可使用语义 HTML。
