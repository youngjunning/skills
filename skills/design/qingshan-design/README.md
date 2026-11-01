# Qingshan Design

[English](#english) · [简体中文](#简体中文)

A cross-platform Codex Skill for turning the atmosphere of mist, lake water, cypress forests, and distant hills into a quiet, accessible product design system.

This repository supports macOS, iPhone and iPad, Android, React Native, web dashboards, and landing pages. It provides one semantic design language while preserving each platform's native interaction model.

---

## English

### Why this Skill exists

AI can generate interfaces quickly, but it does not automatically know what deserves emphasis, what should remain quiet, or when a visual effect has become noise. Qingshan Design turns those judgments into reusable constraints: semantic colors, information hierarchy, material strategy, motion boundaries, accessibility checks, and explicit anti-patterns.

It is designed for implementation and review, not just visual inspiration.

### Design principles

- Start with product hierarchy before changing colors.
- Use mist white, deep lake blue, lake teal, cypress green, and distant-hill gray as semantic roles rather than decorative swatches.
- Prefer spacing, typography, native controls, and one clear action over nested glass cards.
- Add blur, particles, landscape imagery, and narrative motion only after the interface works without them.
- Preserve keyboard, touch, focus, screen-reader, reduced-motion, and reduced-transparency behavior.
- Reject generic blue-purple AI gradients, tourism-poster backgrounds, full neon, glass-on-glass, and state communicated by color alone.

### Platform coverage

| Target | Guidance and assets |
| --- | --- |
| macOS | SwiftUI/AppKit, menu bar, settings, floating panels, window resizing, keyboard and pointer input |
| iPhone and iPad | Safe areas, Dynamic Type, compact/regular layouts, touch and accessibility behavior |
| Android | Jetpack Compose, Material 3, edge-to-edge, adaptive layouts, tablets and foldables |
| React Native / Expo | Shared typed theme, iOS/Android behavior boundaries, responsive windows, VoiceOver/TalkBack |
| Web dashboard | Dense data UI, focus, keyboard navigation, responsive structure, reduced effects |
| Landing page | Narrative hierarchy, responsive media, LCP, progressive atmosphere and motion |

### Install

Ask Codex to install the Skill:

```text
Install qingshan-design from https://github.com/youngjunning/skills/tree/main/skills/design/qingshan-design
```

Or clone it manually:

```bash
npx skills add youngjunning/skills --skill qingshan-design -g
  "${CODEX_HOME:-$HOME/.codex}/skills/qingshan-design"
```

Start a new Codex conversation after installation so the Skill can be discovered.

### Use

Invoke it explicitly:

```text
Use $qingshan-design to redesign this React Native habit tracker for iOS,
Android, tablets, and foldables. Preserve accessibility and Reduced Motion.
```

```text
Audit this dashboard with $qingshan-design. Report hierarchy, contrast,
material, state, keyboard, and responsive-layout issues before changing code.
```

Codex can also trigger it automatically when a request mentions 青山湖风格, Qingshan Lake, Jiangnan landscape glass UI, mist-and-lake visual systems, or a restrained natural glass redesign.

### Repository contents

```text
qingshan-design/
├── SKILL.md                       # Core workflow and routing
├── agents/openai.yaml             # Codex UI metadata
├── assets/
│   ├── qingshan.tokens.json  # Canonical semantic tokens
│   ├── qingshan.css          # Web variables and reduced-effect fallbacks
│   ├── QingshanPalette.swift  # Apple platform palette
│   ├── QingshanTheme.kt       # Jetpack Compose theme
│   └── QingshanTheme.ts       # React Native typed theme
├── references/                    # Platform-specific implementation guidance
└── scripts/validate_tokens.py     # Token and contrast validation
```

Validate the bundled token system with:

```bash
python3 scripts/validate_tokens.py
```

### Origin

Qingshan Design is independently authored and inspired by the mist, water, cypress forests, hills, and boardwalk atmosphere of Qingshan Lake in Lin'an, Hangzhou. It is not an official design system of the scenic area or its operators.

Released under the [MIT License](LICENSE).

---

## 简体中文

### 为什么需要这个 Skill

AI 可以快速生成界面，但它不会天然知道什么应该被强调、什么应该保持安静，也不会自动判断一个视觉效果何时已经变成噪声。Qingshan Design 把这些判断沉淀为可复用的约束：语义色、信息层级、材质策略、动效边界、无障碍检查，以及明确的反模式。

它不是一份只供欣赏的视觉灵感，而是一套可以直接用于实现和审查的 Codex Skill。

### 设计原则

- 先恢复产品层级，再修改颜色。
- 把雾白、深湖蓝、湖青、杉绿和远山灰作为 semantic roles，而不是装饰性色板。
- 优先使用留白、字体、原生控件和一个清晰主操作，避免层层嵌套的玻璃卡片。
- 只有在界面脱离 blur、粒子、风景图和叙事动效后仍然成立，才加入氛围效果。
- 保留键盘、触控、focus、读屏、Reduced Motion 和 Reduced Transparency 行为。
- 拒绝通用蓝紫 AI 渐变、景区宣传画背景、全霓虹、glass-on-glass，以及只靠颜色表达状态。

### 平台覆盖

| 平台 | 规范与资产 |
| --- | --- |
| macOS | SwiftUI/AppKit、menu bar、设置页、悬浮面板、窗口缩放、键盘与鼠标输入 |
| iPhone 与 iPad | Safe Area、Dynamic Type、compact/regular 布局、触控与无障碍行为 |
| Android | Jetpack Compose、Material 3、edge-to-edge、自适应布局、tablet 与 foldable |
| React Native / Expo | 共享 typed theme、iOS/Android 行为边界、响应式窗口、VoiceOver/TalkBack |
| Web Dashboard | 高密度数据界面、focus、键盘导航、响应式结构与 reduced effects |
| Landing Page | 叙事层级、响应式媒体、LCP、渐进式氛围与动效 |

### 安装

直接让 Codex 安装：

```text
从 https://github.com/youngjunning/skills/tree/main/skills/design/qingshan-design 安装 qingshan-design Skill
```

也可以手动 clone：

```bash
npx skills add youngjunning/skills --skill qingshan-design -g
  "${CODEX_HOME:-$HOME/.codex}/skills/qingshan-design"
```

安装后新建一个 Codex 会话，让 Skill 被重新发现。

### 使用

可以显式调用：

```text
使用 $qingshan-design，把这个 React Native 习惯追踪 App 改成青山湖风格，
覆盖 iOS、Android、tablet 和 foldable，并保留无障碍与 Reduced Motion。
```

```text
使用 $qingshan-design 审查这个 Dashboard。先报告信息层级、对比度、
材质、状态、键盘和响应式布局问题，再修改代码。
```

当请求中出现“青山湖风格”、Qingshan Lake、江南山水玻璃、雾与湖泊视觉系统，或克制自然的 glass redesign 时，Codex 也可以自动触发这个 Skill。

### 仓库内容

```text
qingshan-design/
├── SKILL.md                       # 核心工作流与平台路由
├── agents/openai.yaml             # Codex UI metadata
├── assets/
│   ├── qingshan.tokens.json  # 规范化 semantic tokens
│   ├── qingshan.css          # Web 变量与 reduced-effect fallback
│   ├── QingshanPalette.swift  # Apple 平台色板
│   ├── QingshanTheme.kt       # Jetpack Compose theme
│   └── QingshanTheme.ts       # React Native typed theme
├── references/                    # 各平台实现规范
└── scripts/validate_tokens.py     # Token 与对比度验证
```

验证内置 token system：

```bash
python3 scripts/validate_tokens.py
```

### 来源说明

Qingshan Design 是一套独立创作的设计语言，灵感来自杭州临安青山湖的雾、水面、水杉、远山和栈道氛围。它不是青山湖景区或其运营方的官方设计系统。

项目采用 [MIT License](LICENSE)。
