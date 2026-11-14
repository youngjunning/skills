# 三级质量门禁

Joyally Design 把可观察的界面风险分成 Floor、Reflex 和 Finish。门禁用于让默认选择可检查、例外可解释，不是审美评分，也不替代真实任务、品牌规范、组件约束、截图评审和可访问性测试。

## 三层含义

| 层级 | 含义 | 当前自动检查 | 处理方式 |
| --- | --- | --- | --- |
| Floor | 不应带着交付的基础故障 | 文字对比度过低；首屏内容停在透明状态 | 必须修复；不能用样式例外绕过 |
| Reflex | 容易形成模板感或职责不清的默认手法 | 过小正文、过紧行高、标题前重复短标签、小号全大写宽字距标签、渐变文字、卡片套卡片、无语义粗侧条、Emoji 功能图标、标题单词单独强调、文字末尾粘箭头 | 优先修复；确有品牌、状态或任务依据时写明理由后保留 |
| Finish | 不一定阻塞，但交付前应回答 | 标题层级跳级；页面语言、标题或摘要元数据缺失 | 修复或记录回答，不阻塞自动命令 |

检查只覆盖能从真实浏览器 DOM 与 computed style 稳定观察到的项目。自动规则没报错不等于设计通过；颜色、卡片、渐变、侧条或大写本身也不是错误，仍按[反模板感检查](anti-ai-taste.md)判断其职责。

## 启用与解释

普通截图会把发现写入 `report.json` 的 `lint`，不改变返回码。交付或 CI 使用 `--gates`：存在未处理的 Floor 或 Reflex 时返回 1；Finish 只提示。

Reflex 的有依据例外写在最小可解释容器上，格式为 `规则:理由`，多项用分号分隔。理由至少 4 个字：

```html
<section data-joyally-waive="eyebrow:品牌章节索引;trackedCaps:品牌字标规范">
  <p class="eyebrow">RESEARCH NOTES</p>
  <h2>研究记录</h2>
</section>
```

Finish 的明确回答使用 `data-joyally-answer`：

```html
<main data-joyally-answer="headingSkip:嵌入外部组件保留原层级">…</main>
```

不要为了过门禁而批量加例外。报告会保留 `tier`、`status`、命中位置和理由，评审时应能从产品事实验证理由。

## 存量页面保真

重设计前用 `--before` 记录链接、表单、字段、ID、测试钩子、标题和媒体的结构契约；修改后用 `--kept` 对照。它比较接线与内容骨架，不做像素冻结：

```text
node <skill>/scripts/shoot.mjs page.html --size desktop --before .joyally-design/account-before.json --out .joyally-design/before
node <skill>/scripts/shoot.mjs page.html --size desktop --kept .joyally-design/account-before.json --gates --out .joyally-design/after
```

链接、表单、字段、ID 和测试钩子缺失属于 Floor，返回 1；标题和媒体缺失作为 Reflex 证据写进报告，但不单独阻塞。契约只证明被记录的 DOM 能力仍在，不证明业务请求成功、权限正确、部署生效或用户流程已经验收，这些仍需从真实入口操作并回读。

### 第二期：结构关系指纹

`--before` 同时记录语义关系，不新增另一套页面模型：landmark 顺序与嵌套、导航链接顺序、表单字段分组、表格列顺序，以及带 `aria-controls` 的动作与目标。`--kept --gates` 发现这些关系变化时按 Reflex 阻塞；重设计可以改变关系，但必须说明为什么新结构更适合任务。

尽量在具体关系上解释，格式仍沿用 `data-joyally-waive`：

```html
<main data-joyally-waive="structure.navigation:主任务改为报告优先;structure.tableStructure:状态成为首要判断依据">
  …
</main>
```

可用关系名为 `landmarkStructure`、`navigation`、`formStructure`、`tableStructure` 与 `actionTarget`。确实是同一次整体信息架构调整时才使用 `structure:理由`；它会解释当前页面全部结构关系变化。结构指纹不比较 CSS、像素位置或组件实现，因此不会要求存量页面保持原布局。

## 第二期：真实素材清单

素材清单把[素材流程](media.md)已有的来源、许可、用途和页面接线变成浏览器证据，不替代素材选择与画面评审。只有页面确实使用主视觉、品牌图、对象图片、视频或其他内容媒体时才启用；纯数据任务不为过门禁硬塞素材。

在页面上给需要追溯的素材标稳定 ID：

```html
<img data-joyally-material="hero" src="assets/hero.webp" alt="产品主体的正面实拍">
```

再写一份符合 [material-manifest.schema.json](material-manifest.schema.json) 的清单：

```json
{
  "version": 1,
  "assets": [{
    "id": "hero",
    "expected": "assets/hero.webp",
    "purpose": "展示真实产品主体",
    "source": { "kind": "owned", "reference": "产品团队原始摄影" },
    "license": "项目自有"
  }]
}
```

`source.kind` 可按项目写 `owned`、`generated`、`licensed`、`public-domain` 或 `user-supplied`；`reference` 写可回查的原图、生成记录、来源页或项目材料，不把分类名本身当来源。`license` 写实际许可或明确的项目使用边界。素材暂不要求在某个状态出现时可写 `required: false`。

```text
node <skill>/scripts/shoot.mjs page.html --size desktop --materials materials.json --gates --out .joyally-design/material-check
```

清单素材未接入、ID 未声明、路径不一致或加载失败属于 Floor；明显占位路径属于 Reflex；替代文本缺失和未标记的大幅内容媒体属于 Finish。检查只在显式 `--materials` 时运行，继续复用现有 `--gates`、`report.json` 和真实浏览器，不扫描项目目录猜素材归属。

灰盒评审确需临时素材时，可在对应元素写 `data-joyally-waive="materialPlaceholder:灰盒评审阶段的临时素材"`；缺少替代文本或暂不纳入清单的内容媒体用 `data-joyally-answer` 说明。Floor 级的来源接线、路径和加载问题不能豁免。

## 来源边界

三级命名、默认反模式和“先记录再保留”的机制受到 Hallmark 的启发。Joyally Design 只选取与现有任务评审、真实浏览器证据链相容的部分，规则、浏览器实现、例外格式和存量契约均在本项目独立实现；没有引入 Hallmark 的主题目录或页面资产。来源与许可见 `legal/hallmark/`。
