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

- `assets/joyally-design.tokens.json` 与 `assets/joyally-report-theme.css`：报告和 React 的完整分层、青山湖主题与材质契约；四季画面共同提供取色与构图依据。
- `assets/joyally-native.tokens.json`：现有湖色预设的语义值与对比度声明；`JoyallyPalette.swift`、`JoyallyTheme.kt`、`JoyallyTheme.ts`、`joyally-native.css` 是对应平台的起点。
- `assets/xiaoxiang-theme.tokens.json`：香奈儿风主题的浅色与深色语义色及几何样本；按[主题规则](fashion-xiaoxiang.md)与[20 张参考图](../assets/references/xiaoxiang/README.md)映射到目标产品组件，不自动替换现有平台预设。
- `assets/space-theme.tokens.json`：太空主题的浅色与深色语义色及几何样本；按[主题规则](space.md)映射到目标产品组件，不自动替换现有平台预设。
- 三份 JSON 是同一语义契约的不同预设，不要求色值相同。一次实现先选项目已有预设或明确一种预设，再映射全部相关角色；不要混用不同预设的前景/背景。
- 七套视觉主题各有取材边界；青山湖以春夏秋冬各 5 张授权实拍为收集目标，目前画册保留未完成位置。前五套以景点或景观区域为取景范围，香奈儿风以包袋、山茶花、巴黎夜景、服装细节和编辑呈现为取材范围；太空主题使用原创概念画面表达轨道与行星地平线，不声称这些画面是天文观测照片。青山湖主题包含四季，不把季节作为运行时外观维度；`material`（材质）与 `mode`（明暗模式）独立。香奈儿风与太空分别提供独立的 `light` / `dark` 映射。`style` 和 `mood` 描述视觉语言与意境，不改变交互状态和语义角色。当前平台 token 完整实现青山湖预设；其他主题进入具体产品时仍需映射相关组件并逐项校验。
- 平台尺寸与交互由平台参考决定：桌面紧凑控件与移动端触控热区共存，不把 Web 布局和 32px 控件直接搬到手机。

变更预设时运行对应 token 校验器。交付产品还需核对运行时配色、字体缩放、键盘/触控、辅助技术与降低动态效果；静态 token 通过不代表设备验收。

## 图表配色

`joyally-design.tokens.json` 的 `diagram.light` / `diagram.dark` 是交互图表的配色源。通用画布与文字引用已有 seed，七种图表类别保留可区分的独立色相。四种 preset 使用同一映射，打印以浅色类别配色加白色背景输出。运行 `validate-diagram-theme.py` 检查模板映射及正文、节点和连线对比度。湖色种子保留原有命名，原生 CSS 使用 `joyally-` 前缀。
