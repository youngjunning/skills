# Chrome 扩展界面

从 [主入口](../SKILL.md) 进入 Chrome 扩展的 popup、options、side panel 或独立窗口设计时读取。扩展图标另读 [扩展图标](chrome-extension-icon.md)。

## 组件基础

Chrome 扩展界面默认使用 [Web Awesome Core](https://webawesome.com/docs/) 的 Web Components。它可在原生 HTML/JavaScript 中使用，不要求迁入 React、Vue 或 Tailwind；按实际控件引入组件，使用项目语义 tokens 调整颜色、字号、尺寸与焦点状态。已有项目先核对现用组件和交互合同，再按本次获准范围逐步接入；用户明确指定其他组件基础或现有约束使 Web Awesome 不可用时，记录具体原因和替代方案。

扩展页面中的库脚本、样式、字体和图标必须随 Manifest V3 安装包本地提供，不在运行时从 CDN 加载代码。打包时只带用到的 Core 资源及许可声明，核对所有动态导入与资源路径。Web Awesome 的 [安装说明](https://webawesome.com/docs/) 区分无需构建工具的 `dist-cdn` 和适合 bundler 的 `dist`；选择与项目当前构建流程相符的一种。

优先把复杂选择、菜单、弹层、对话框等交互交给组件，保留项目已有的值、事件、表单提交和状态恢复语义。`wa-select` 等自绘列表要在实际扩展窗口中检查键盘操作、焦点、读屏名称、菜单定位、边界裁切和关闭恢复；不能以默认皮肤替代设计完成。普通文本与只读数据仍可使用语义 HTML。
