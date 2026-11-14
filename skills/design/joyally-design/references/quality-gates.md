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

## 来源边界

三级命名、默认反模式和“先记录再保留”的机制受到 Hallmark 的启发。Joyally Design 只选取与现有任务评审、真实浏览器证据链相容的部分，规则、浏览器实现、例外格式和存量契约均在本项目独立实现；没有引入 Hallmark 的主题目录或页面资产。来源与许可见 `legal/hallmark/`。
