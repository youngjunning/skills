# Joyally Design React design system reference

Joyally Design 在 React Web 项目中首先是一套可复用的设计系统约束，然后才是页面样式。新建中后台以 [shadcn/ui 官方组件集](https://ui.shadcn.com/docs/components)为完整基础：使用 CLI 的 add --all 获取本地源码，统一接入 Joyally 语义 tokens、状态与页面组合。Data Table、Date Picker 等复合控件在基础组件上组合，不从零重写输入、弹窗和导航。Magic UI 用于适合的展示动效。目标是让 tokens、组件状态、布局节奏和页面组合拥有同一套语义，同时保留项目原有的业务术语、路由和交互合同。H5、Chrome 扩展和 React Native 按各自平台路径选择组件。

Ant Design informs token derivation, component states, hierarchy, and density. Material 3 informs semantic roles; Radix Primitives and shadcn/ui supply accessible base controls and open composition; Tailwind CSS implements theme utilities; Magic UI supplies optional display motion. Lake-landscape and contemporary Chinese visual cues are the brand layer; the Chinese cultural layer is not tied to one dynasty and excludes Qing-dynasty aesthetics and characteristic symbols. The rules below translate that matrix into Alias tokens, layout rhythm, and responsive behavior for internal web products.

## Reference architecture for the current stack

| Layer | Joyally Design decision | Implementation boundary |
| --- | --- | --- |
| Seed | lake-landscape palette, contemporary Chinese color cues, type scale, 8px rhythm, radius and motion base values | `joyally-design.tokens.json` primitive values |
| Map | Derived hover, active, disabled, elevated, muted and status values | token derivation; never hand-tuned in page JSX |
| Alias | `background`, `surface`, `text`, `primary`, `focus`, `success`, `warning`, `error` | CSS variables consumed by Tailwind `@theme`; stored as `semantic` for compatibility |
| Component | Button, Input, Card, Table, Dialog, Sidebar, Empty, Toast and state variants | `components/ui`, `cva` variants and composable slots |

The project composes a reference-system matrix: Ant Design informs token derivation and enterprise density, Material 3 informs semantic roles and state layers, Radix Primitives informs accessible behavior, shadcn/ui and Tailwind CSS 4 own open implementation, and Magic UI supplies optional motion for suitable display surfaces. These roles must stay visible in source so an AI or engineer can change one layer without hunting through generated CSS.

## Design language and appearance axes

Keep design language and runtime appearance independent:

| Layer | Axis | Contract |
| --- | --- | --- |
| Design language | `style` | Visual grammar and cultural references; baseline `contemporary-chinese-cues` |
| Design language | `mood` | 意境：emotional atmosphere, spatial distance, temporal feeling, and pacing; baseline `quiet-youthful-distance` |
| Appearance | `mode`（明暗模式） | `light` / `dark`，界面称“浅色 / 深色”；控制亮度、对比度与表面配对，不是另一个主题 |
| Appearance | `season` | `spring` / `summer` / `autumn` / `winter`; controls seasonal palette and atmosphere while preserving aliases and component states |
| Implementation preset | `material` | `celadon-glaze` / `glass`; controls surface treatment such as translucency, border, highlight, and shadow |

Seasons share one component API and one accessibility contract. Do not duplicate dimensions, typography, density, or state tokens per season. The default appearance is `light + autumn + celadon-glaze`; previously saved choices take precedence. New seasonal values require palette evidence and contrast validation before entering the bundle.

The JSON `appearanceContract` is the implementation source for these axes. A season adapter must resolve every slot in `seasonTokens` into the existing semantic aliases before rendering. A material adapter may change only surface alpha, border/highlight, blur, and shadow; it must not rewrite `primary`, `success`, `warning`, `error`, or focus semantics. `materialRules.transparentForbidden` is an explicit deny-list for readable content surfaces, and `materialRules.reducedTransparencyFallback` is required whenever `prefers-reduced-transparency`, forced colors, or unsupported backdrop filters apply. Validate the contract with `python3 .codex/skills/joyally-design/scripts/validate-joyally-tokens.py` before changing shared CSS.

For application coverage, classify each rendered region using `materialRules.surfaceRoles` and the [element coverage matrix](design-system.md#element-coverage-and-material-boundaries). The shared material adapter must reach sidebar navigation tiles, page frames, card and dialog chrome, and Chat document headers/footers; keep tables, form inputs, editors, and document bodies opaque. Check page-specific CSS and inline styles for overrides before judging a material complete. Preview both materials under the same season and mode so the comparison isolates surface treatment.

Selected conversation rows, secondary navigation items, tabs, segmented controls, menu options, pagination pages, and primary/outline actions are material-bearing state surfaces. Their fill, edge, shadow, and blur must resolve from the material adapter. Primary action hue and label contrast remain seasonal; the glaze adds an opaque highlight and inset edge, while glass uses a quieter specular edge. Outline actions are opaque under glaze and may be translucent under glass, with an opaque reduced-transparency fallback. Keep selected-state meaning and text color in season tokens. Use warm mist-white paper for large canvases; summer green and autumn red/yellow cypress foliage provide the seasonal imagery. Lake color, water sparkle, duckweed, mist, morning light, and sunset light remain small accents outside reading areas.

Use user-provided images, when available, as references for summer cypress green, autumn foliage, lake water, and sunset light; private reference images are not bundled. Summer `primary` and interactive states use the saturated green of the summer cypress canopy rather than lake teal or olive matcha; the large canvas remains warm neutral. In autumn, matcha green carries primary actions, selected surfaces, and Chat interaction. Cypress red and yellow map to `error` and `warning` feedback across seasons: readable foregrounds `#A7472D` and `#96620F` sit on pale `#FBEAE2` and `#FFF2D9` fills, with visible `#D9A28E` and `#E5B663` borders. Each status needs an icon or label and stays off large interactive surfaces. Compact page headers use a face-readable portrait; full-body artwork belongs in a larger scene such as the loading view.

Keep seasonal CSS in `client/src/styles/seasons/`: `summer.css` owns summer seed values and `autumn.css` owns autumn palette and atmosphere overrides. `client/src/global.css` owns shared structure, component states, and layout contracts; it must not scatter season-specific overrides.

Style and mood are separate peer-level creative descriptors layered above these runtime axes. `style` describes visual form and behavior; `mood` is the implementation key for 意境: emotional atmosphere, spatial distance, temporal feeling, and narrative restraint. The current mood is quiet, youthful distance with restrained time-and-object cues. It may inform imagery and rhythm, but never changes semantic states or reduces content clarity.

## Reference responsibilities

| Concern | Primary reference | React implementation rule |
| --- | --- | --- |
| Token derivation and component tokens | Ant Design + Material 3 | Keep `Seed → Map → Alias → Component` with semantic roles; do not style directly from scenic names |
| Semantic roles, state layers, and tonal surfaces | Material 3 | Make selected, hover, pressed, disabled, and focus states explicit and composable |
| Keyboard, focus, overlay, and WAI-ARIA behavior | Radix Primitives | Preserve primitive behavior and accessible names before adding brand styling |
| Source ownership and composition | shadcn/ui | Keep primitives open in `components/ui`; use `cn` and `cva` for variants |
| Token-to-utility implementation | Tailwind CSS 4 | Use `@theme` namespaces and semantic utilities; document measured exceptions |
| Middle/back office component baseline | shadcn/ui CLI | Install the full available component set, then validate inventory, token mapping and interaction states |
| Display components and emphasis motion | Magic UI | Install only suitable registry components; map tokens and provide reduced-motion fallback |
| Brand and cultural expression | Joyally Design | Apply lake-landscape and contemporary Chinese cues through Alias tokens and bounded artwork |

These references are complementary. Do not merge their APIs into a new abstraction layer or install a library only to imitate its look.

## Complete middle/back office component baseline

For a new React admin system, initialize shadcn/ui for the project's existing React and Tailwind setup, then run its official CLI with add --all. Check the generated source inventory against the CLI result; do not describe a handful of styled examples as a complete library. Keep the installed components locally owned and updateable through the shadcn/ui registry.

Map the whole baseline to Joyally semantic roles: background and surfaces, foreground and muted text, primary and secondary actions, destructive and status colors, input and border, ring, radius, chart series, and sidebar. Scope theme variables to the intended app root and include overlays portaled to the document body. A theme switch must reach Button, Input, Select, Dialog, Table, Sidebar, Toast and their focus, disabled and error states together.

Build admin compositions from those components. Data Table adds search, filtering, sorting, selection, pagination and empty state to Table; Date Picker composes Calendar and Popover. A representative workbench combines Sidebar, context navigation, toolbar, metrics, data surface, form, confirmation, feedback and recovery. The component catalog should link each installed source file and make implemented compositions distinguishable from basic shadcn/ui files. Validate catalog coverage against the actual files, then verify a desktop width, narrow width, keyboard path and major interactive states.

## Language-neutral typography and layout

Do not split the system into Chinese and English variants. Use the same semantic type roles, spacing rhythm, component states, and responsive rules for all copy. The font stack may include platform fallbacks for rendering reliability, but components must not gain language-specific variants or padding hacks.

## Page anatomy and layout contracts

| Zone | Owns | Default contract |
| --- | --- | --- |
| App Shell | Global navigation, identity, persistent utilities | Expanded sidebar `248px`; compact rail `64px`; selection never changes item geometry |
| Context Bar | Route title, current object, contextual actions | One visible title for the current route; no duplicate global and local titles |
| Local Toolbar | Search, filters, view switch, refresh and creation actions | `32–36px` controls; actions remain grouped by intent |
| Primary Work Surface | The task's main content | Opaque readable surface; height follows content; wide tables scroll locally |
| Supporting Panel | Detail, history, evidence, or secondary navigation | Optional at wide width; collapses to drawer or below-content at medium/narrow widths |
| Continuation Action | Send, save, run, confirm, or retry | Sticky only for an active workflow; never reserve a large empty footer |

The shell, context bar, and work surface form one hierarchy. If a page has a conversation header, its avatar and title align on one baseline; if the page is empty, suppress secondary header chrome rather than showing a decorative placeholder.

On detail pages, the breadcrumb identifies the parent list and page type, while the summary card names the specific record and presents its metadata. Keep the record name in the summary so the two levels do not repeat the same title. When several related skills can be bound to one task, use a labeled skill filter alongside the other query controls; the default view shows all skills and the chosen filter applies when the user searches.

同类详情摘要卡的底色从 `card` 轻微过渡到 `primary-bg`，局部光晕从 `primary` 派生；不要在组件内固定某个季节的色相。

When a detail page has two local views such as details and logs, place the view switch at the right of the record summary header. Keep the breadcrumb for parent navigation; on narrow screens the switch wraps below the record name within the same card.

## State and geometry contract

| State | Visual treatment | Geometry rule | Feedback rule |
| --- | --- | --- | --- |
| Default | Opaque or quiet surface, standard border | Stable size | No extra ornament |
| Hover | Subtle surface or border lift | No reflow | Pointer affordance remains visible |
| Pressed | Darker semantic surface or inset | No reflow | Preserve label and icon |
| Selected | Primary container plus inset indicator or stronger text | No border-added width change | Must be distinguishable without color alone |
| Focus-visible | `2px` focus ring with offset | No layout shift | Keyboard focus remains obvious |
| Disabled | Reduced contrast and interaction | Same footprint | Explain unavailable state when useful |
| Loading | Skeleton/spinner in the final geometry | Reserve final footprint | Avoid replacing the whole page with a spinner |
| Empty | Short explanation and one next action | No giant illustration | Remove irrelevant controls and chrome |
| Error | Error semantic color plus text/icon | Preserve surrounding layout | Offer retry, correction, or escalation |
| Success | Success semantic color plus explicit result | Preserve surrounding layout | Explain what completed and what follows |

List surfaces share one compact status composition for loading, empty, and error: a 64px character portrait, one direct state sentence, and an optional action. A short next-step sentence appears only when it adds information beyond the action label. Loading may use a quiet portrait motion and a status spinner; error uses the semantic error badge and a retry action. Technical error detail stays collapsed by default and appears as a small speech bubble on badge hover or keyboard focus, with its arrow centered on the badge. Keep the table header and list frame stable, use the same composition for card grids, and stop all status motion under `prefers-reduced-motion`.

Compact labeled switches in a toolbar use a quiet neutral container when off. When on, the switch, label, pale primary fill, and primary border all communicate the selected state without increasing the toolbar height.

When an auxiliary model assesses a run, identify its output beside the execution log with a source label and the exact stage at which it participates. Keep the Agent's action log separate from a post-run judgment; do not imply that the auxiliary model made each browser action.

## Density modes

Joyally Design has one default density and two bounded adaptations, not page-specific spacing systems:

| Mode | Use | Control height | Content rhythm |
| --- | --- | --- | --- |
| Default | Most internal product pages and reports | `36px` | `8/12/16px` component rhythm |
| Compact | Tables, logs, dense sidebars, multi-row workbenches | `32px` | `4/8/12px` rhythm; preserve readable line height |
| Presentation | Empty states, summaries, or stakeholder readouts | Up to `40px` primary action | More section separation, never oversized controls everywhere |

Choose the mode at the surface or component boundary. Do not mix compact and presentation spacing inside one control group.

## Responsive contract

1. **Wide (`≥1024px`)**: show the stable shell, context bar, work surface, and optional supporting panel.
2. **Medium (`768–1023px`)**: keep the shell and context bar, collapse supporting content into a drawer or local disclosure, and preserve the primary work surface.
3. **Narrow (`<768px`)**: move secondary navigation into normal flow, keep one title and one primary action visible, and give wide evidence its own horizontal scroll container.
4. Never solve overflow by shrinking body text below the readable role or by making every card full-height.

## Motion and material budget

1. Interaction transitions use the normal token (`~200ms`); state continuity may use the fast token (`~140ms`).
2. Narrative reveal is one-time and local (`≤600ms`); no ambient loop is required for comprehension.
3. Shine, shimmer, beam, and wash effects stay outside opaque content and are removed under Reduced Motion, Reduced Transparency, or low-power fallback.
4. A component must still communicate selected, loading, error, and success states when all motion and translucency are disabled.
5. Verify the built CSS in a browser: opaque reading and evidence surfaces need an opaque computed background with zero effective backdrop blur, and reduced transparency must do the same for perimeter surfaces. Wait for state transitions to settle before reading computed styles; this build chain can drop the standard `backdrop-filter` declaration when the same rule also declares `-webkit-backdrop-filter`.
6. For a walking sprite that also travels across a surface, verify four distinct legs, plausible joint bends, a stable hoof baseline, and a smooth first-to-last-frame loop at the actual display size. Advance the image frame and its position on the same beat. Set the beat short enough for fluid motion and keep the distance per frame below one CSS pixel; do not let the body translate continuously while the feet are planted.

## Iconography and imagery contract

1. Functional icons prioritize accessible names, stable geometry, and predictable alignment; their state must not depend on decorative artwork.
2. Branded or illustrative icons use culturally grounded subjects only when the subject explains the object or action; use the joyally-imagegen workflow for new artwork.
3. Do not use generated artwork to replace a standard affordance such as close, search, menu, chevron, play, or retry.
4. Artwork has a bounded size budget and must not push title, label, or evidence content out of alignment.
5. Application menu items use object illustrations rather than character portraits. Keep generated object artwork in a stable 30px slot aligned with the existing illustrative menu family; utility glyph fallbacks remain 16–18px inside the same slot. Default and active assets share the same slot and optical scale, but the active drawing must change the object’s structure, pose, or meaningful components (closed/open book, sprout/branched leaves, folded/unfolded scroll); color changes and animation alone do not satisfy the selected-state contract. Selection may trigger one short object-specific motion (at most 1.2 seconds) before holding still; never animate every navigation item continuously. Reduced Motion keeps the active asset and selected surface but disables motion and crossfades. Retain the icon and accessible label in collapsed navigation. Character portraits remain available for page headers and conversation identity.
6. Related page headers use one shared circular role portrait geometry, with a 50% radius and a consistent size at each breakpoint; keep transparent portrait artwork free of an added circular background surface.
7. Functional illustration icons in those headers use a separate centered image slot with inner padding and no circular crop, so scrolls and other asymmetric objects remain complete. A functional page header reuses its navigation item’s selected-state artwork as a still image, keeping object structure and pose identical after the menu animation ends.
8. Keep the product brand mark distinct from character portraits: the shell identity, landing brand and static favicon share one small-size-tested mark; Chat messages and employee roles keep their character avatars. An animated favicon may add a restrained state-neutral pulse, but must stop in hidden tabs and under Reduced Motion.

## Contemporary Chinese visual language

1. Treat traditional references as selective brand cues inside a modern product grammar, without locking the system to one dynasty and while excluding Qing-dynasty aesthetics and characteristic symbols: quiet hierarchy, deliberate留白, ink-like text, celadon/lake actions, and rare cinnabar emphasis. Modern clarity and a youthful feel come first.
2. Keep modern sans-serif for body copy, controls, tables, and operational labels. Use a restrained Song-style serif only for display titles, report covers, or a small kicker.
3. Use seal, inkstone, bamboo, scroll, bronze mirror, or mountain-water motifs only when they explain the object or state. Functional icons retain stable geometry and accessibility; branded or illustrative artwork follows the joyally-imagegen workflow.
4. Keep paper grain, brush edges, and landscape silhouettes outside opaque content surfaces. Under narrow, print, reduced-transparency, or low-power modes, remove atmosphere and preserve Ant Design hierarchy.
5. Reject faux-ancient typography, palace-poster decoration, dense auspicious patterns, full red-and-gold palettes, and ornamental treatment that competes with evidence.

### Seasonal color and scene motion

1. Summer interactions use the saturated pond-cypress canopy green from the lake-landscape summer reference (for example `#2e7731`), with a deeper green for pressed states. Autumn interactions use a visibly more yellow, muted matcha green (for example `#687644`); red and gold stay in foliage and semantic status accents. Compare both seasons at the same material setting so translucency does not hide the hue difference.
2. Large application surfaces remain warm mist-white in both seasons. The loading scene uses an illustrated lake-landscape composition: distant mountains, clustered water-cypress groves, a calm lake and mist, with an open center for a compact loading subject and copy. Its summer and autumn plates share one layout; foliage changes with the season. Keep the painting stylized and the center readable, without binary streams, photographic scenery or large opaque shapes behind copy.
3. A character approach uses registered full-body walking frames with visible alternating leg steps and opposite arm swings, then holds a neutral final pose. Scale and depth travel use the same duration as the frame sequence; `prefers-reduced-motion` shows a still image. A walking decoration must synchronize step frames and horizontal travel on the same timeline, travel only in its facing direction, and keep its feet on the host surface baseline.
4. A swimming flock uses a few side-facing cutouts at staggered depths and sizes, with all travel following the facing direction. Keep body bobbing within 2px and 1 degree, stagger each bird’s cadence, and attach low-contrast wakes to its waterline. Keep the flock compact below the stationary loading copy; it is the waiting indicator, with no simulated progress bar or completion percentage. Fade the loop boundary rather than visibly snapping backward. Under `prefers-reduced-motion`, center a still flock and remove wake and mist motion.
5. Decorative branches belong at the perimeter and must never overlap labels or controls. Compact headers with action controls omit the foliage layer; do not rely on stacking buttons above decorative leaves. A chat thread title should not span the full document surface when the conversation rail already identifies the active thread.

### Semantic HTML and margin hygiene

Use semantic HTML without allowing browser defaults to destabilize compact layout geometry:

1. Use `<p>` for actual prose paragraphs that need paragraph semantics. Reset its margin in the owning scope when the component intentionally controls paragraph rhythm.
2. Use `<div>` or `<span>` for one-line previews, metadata, labels, tags, and truncated compact-row content. These are not prose paragraphs and must not inherit a global paragraph bottom margin.
3. Never fix compact-row overflow with ad-hoc negative margins. Keep line-height, gap, and truncation behavior explicit in the component contract.

### Tailwind and shadcn rules

1. Put shared semantic variables in the global theme and expose them through `@theme`; use utilities such as `bg-background`, `text-foreground`, `ring-ring`, and `border-border` at call sites.
2. Keep reusable primitives in `components/ui`. Prefer `cva` for finite variants and `cn` for safe composition; do not encode business terms in a base primitive.
3. A component may accept `className` and slots, but its default state, focus ring, disabled state, and size must remain correct without page-specific overrides.
4. Use component tokens for local density or geometry changes. Do not fork a global semantic token to fix one page.
5. Arbitrary Tailwind values are reserved for measured one-off geometry, imported media, or a documented visual exception; repeated values graduate into tokens.
6. Functional affordance icons must retain an accessible name and stable geometry. Branded, navigation, or illustrative icon artwork follows the project's joyally-imagegen workflow; do not replace that artwork with a generic utility icon.

### Magic UI component rules

1. Use Magic UI for suitable presentation components and emphasis motion; map color, typography, spacing, states, and focus treatment to project tokens. Keep operational controls on the shadcn/ui baseline.
2. Restrict shine/beam/shimmer/aurora effects to primary emphasis or an intentional brand moment; never animate every card, table row, sidebar item, or status badge.
3. Keep the effect outside the content reading surface so text and evidence remain opaque and stable.
4. Provide `prefers-reduced-motion`, `prefers-reduced-transparency`, and low-power fallbacks. The component must still communicate its state when animation is removed.

## Start with inventory

在改动前记录：

1. 现有 color、spacing、radius、shadow、typography tokens 及其来源。
2. 共享 Button、Input、Select、Card、Table、Dialog、Empty、Loading、Error 组件。
3. 页面级 layout、sidebar、toolbar、content measure 和响应式断点。
4. 键盘焦点、表单校验、loading、empty、error、retry、disabled、selected 状态。
5. 现有截图、视觉回归、Storybook、测试和无障碍检查入口。

不要先在页面里复制一组新颜色或新间距；先确认已有 token 和组件是否能够承载目标语义。

## Token contract

沿用由多参考系统共同约束的 `Seed → Map → Alias → Component` 四层映射：借鉴 Ant Design 的 token 分层、Material 3 的语义角色，并由 Tailwind/shadcn 承担实现；本项目的 `semantic` token group 对应 Alias tokens：

| Semantic role | React usage |
| --- | --- |
| `background` | 应用 canvas 和页面外围氛围 |
| `surface` / `surfaceStrong` | 主内容、表单、表格、长文本 |
| `surfaceMuted` | 辅助分组、筛选区、非主要信息 |
| `text` / `textSecondary` / `textTertiary` | 标题、正文、元数据 |
| `primary` / `primaryAction` | 选中、链接、焦点和主要操作 |
| `success` / `warning` / `error` | 状态语义，必须同时有文字、图标或形状 |
| `border` / `focus` | 分隔、输入边界和可见焦点 |

组件只消费 semantic role。需要调整品牌色时，优先改 token 映射，不要批量替换 JSX 中的 hex 值。

## Layout and breathing room

1. 页面主容器使用稳定的最大宽度和页面边距；长文本保持约 `68–78ch`，宽表格在独立容器内扩展。
2. 使用 8px rhythm：组件内常用 `8/12/16px`，区块之间常用 `24/32/48px`。
3. 一个页面保留一个主要阅读路径；不要把每个 section 都变成等大的卡片网格。
4. 高度由内容决定。避免 `min-height`、超大 padding 和空 hero 制造假呼吸感。
5. 外层 atmosphere 可以轻，内容 surface 要不透明且可读；长文本、代码、日志和表格不放在高对比装饰层上。
6. 窄屏优先保留内容顺序和可读字号；侧栏折叠或移入正常流，宽证据只在自己的容器内横向滚动。
7. 带角色图标的桌面侧栏默认约 `232px` 宽，菜单文字 `14px`、行高约 `46px`、图标约 `30–40px`，相邻菜单项留约 `8px` 净间距；当前路由用清晰的语义色填充和边缘标记，常驻强调入口只保留轻量材质，避免两者看起来同时被选中。
8. 聊天输入区可比正文阅读列稍宽，桌面端以约 `52–56rem` 为上限；通过输入面的宽度、约 `16px` 内边距和足够的首行书写空间形成主操作层级，窄屏仍占满可用宽度，不用放大整页工具栏或文字。
9. 侧栏与内容区之间保留一条可辨识的细分隔线；侧栏边缘不要叠加多层内阴影形成粗细不一的平行竖线。
10. 聊天输入区的发送按钮仅在可发送时使用实心主色；停止生成用主色描边与白底区分语义，禁用发送保持中性表面和可识别图标，不对整颗主色按钮施加低透明度。
11. 技能工作台的 Markdown 编辑器使用不透明阅读面、季节主色的浅色当前行和中性行号栏；浏览器未启动时用紧凑的季节色预览框与明确连接状态表达空状态，不使用灰蓝色通用骨架图或持续漂浮动画。

## Component contract

每个共享组件至少明确以下内容：

1. 默认、hover、pressed、focus-visible、disabled 和 selected 状态。
2. loading、empty、error 和 retry 路径，以及状态文字和恢复动作。
3. 内容变长时的换行、截断、滚动或扩展策略。
4. 键盘顺序、焦点可见性、屏幕阅读器名称和最小点击区域。
5. `prefers-reduced-motion`、`prefers-contrast` 和 `forced-colors` 下的可接受退化。

不要用颜色作为唯一状态信号，也不要让基础组件为单个页面加入不可复用的业务语义。

## Composition order

1. 先确定导航、上下文、控制、反馈、结果和下一步动作的关系。
2. 再建立页面区块和内容宽度。
3. 然后接入 semantic tokens 和共享组件状态。
4. 最后加入渐变、透明度、阴影和一次性的状态动效。

页面级样式只负责组合和局部布局；跨页面重复出现的视觉规则应回到 token、组件或 layout primitive。

## Migration checks

1. 对比迁移前后相同内容的 desktop、medium、390px 窄屏截图。
2. 检查最长标题、长表格、空状态、错误恢复和键盘焦点。
3. 检查新 token 是否被所有季节或 dark mode 正确解析。
4. 确认 React props、路由、事件、数据请求和业务文案没有被视觉迁移改坏。
5. 只把源代码、组件测试、构建产物、真实浏览器检查分别作为独立证据，不用其中一项代替用户验收。
