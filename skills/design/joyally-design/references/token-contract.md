# Joyally Design 统一 token 契约

采用 `Seed → Map → Alias → Component`。文件中的 `semantic` 就是 Alias；平台示例可以省略没有派生值的 Map 层，但不得另立语义体系。

| 角色 | 语义 token | 使用约定 |
| --- | --- | --- |
| 画布与阅读表面 | background / surface / surfaceMuted | 长文、表格、代码和证据用不透明表面 |
| 正文 | text / textSecondary | 在实际背景上验证对比度 |
| 操作 | primaryAction / onPrimaryAction | primary 是视觉强调，不能默认用于小号白字按钮 |
| 选中 | primaryContainer / onPrimaryContainer | 不改变控件几何；配合文字或图标 |
| 焦点 | focus | 保留键盘可见焦点 |
| 状态 | success / warning / error | 不仅靠颜色表达 |
| 深色 | darkBackground / darkSurface / onDark | 平台深色实现映射到同一角色 |

## 预设与平台适配

- `assets/joyally-design.tokens.json` 与 `joyally-html-theme.css`：报告和 React 的完整分层、四季/材质契约，保留现有青瓷釉与季节预设。
- `assets/joyally-native.tokens.json`：现有湖色预设的语义值与对比度声明；`JoyallyPalette.swift`、`JoyallyTheme.kt`、`JoyallyTheme.ts`、`joyally-native.css` 是对应平台的起点。
- 两份 JSON 是同一语义契约的不同预设，不要求色值相同。一次实现先选项目已有预设或明确一种预设，再映射全部相关角色；不要混用两份预设的前景/背景。
- 主题以景点或景观区域命名，并从同一区域的一组画面提炼成套视觉表达；主题内部保留三个独立外观维度：`season`（季节）、`material`（材质）、`mode`（明暗模式，`light`/`dark`，界面称浅色/深色）。`style` 和 `mood` 描述视觉语言与意境，不改变交互状态和语义角色。切换某一维度不应重置另外两维，也不单独改变主题身份。当前分发的 token 值仅完整实现青山湖水上森林主题；西湖、拙政园、阿尔卑斯雪山的主题规则见[视觉体系](visual-language.md)，进入具体产品时需映射同一批语义角色并逐项校验。
- 平台尺寸与交互由平台参考决定：桌面紧凑控件与移动端触控热区共存，不把 Web 布局和 32px 控件直接搬到手机。

变更预设时运行对应 token 校验器。交付产品还需核对运行时配色、字体缩放、键盘/触控、辅助技术与降低动态效果；静态 token 通过不代表设备验收。

## 图表配色

`joyally-design.tokens.json` 的 `diagram.light` / `diagram.dark` 是交互图表的配色源。通用画布与文字引用已有 seed，七种图表类别保留可区分的独立色相。四种 preset 使用同一映射，打印以浅色类别配色加白色背景输出。运行 `validate-diagram-theme.py` 检查模板映射及正文、节点和连线对比度。湖色种子保留原有命名，原生 CSS 使用 `joyally-` 前缀。
