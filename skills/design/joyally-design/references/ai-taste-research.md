# 界面“AI 味”：证据与检查边界

整理于 2026-11-13。“AI 味”是对模板化结果的主观简称，不能据此判断界面是否由 AI 制作。NN/g 对 AI 原型的实测指出：宽泛提示容易产生杂乱、重复、内容顺序不合理和占空间却缺少信息的容器；具体任务、设计约束、参考画面和真实语境的数据能改善结果。[NN/g：AI 原型实测](https://www.nngroup.com/articles/vague-prototyping/)、[NN/g：真实设计情境](https://www.nngroup.com/articles/ai-prototyping/)

## 可以转成设计检查的发现

| 现象 | 证据与检查办法 | 示例（为规则说明编写，并非来源原图） |
| --- | --- | --- |
| 视觉重点与任务重点错位 | NN/g 发现 AI 原型常让次要进度环或单数字容器占据最大面积。先列出用户要判断的对象、依据和动作，再检查首屏视觉重量是否与之相符。[来源](https://www.nngroup.com/articles/vague-prototyping/) | 工单页让“累计 128 条”占据首屏，待处理工单和下一步藏在下方；把列表、异常原因和处理入口置前。 |
| 重复模块与无职责容器 | NN/g 观察到重复进度组件与低信息密度的大容器。USWDS 规定卡片应是可独立理解的内容集合入口，不能只为画边框而使用，也不适合替代表格行或连续正文。[NN/g](https://www.nngroup.com/articles/vague-prototyping/)、[USWDS Card](https://designsystem.digital.gov/components/card/) | “运行日志”卡片中再套“本次日志”卡片、每条日志又套小卡片；改为一个清楚的日志区域与行分隔。 |
| 无语义强调与泛化装饰 | NN/g 的信噪比与最简设计原则要求视觉重量服务重要内容。由此推论：同级卡片边缘重复的醒目竖条若没有状态、类别、当前位置或操作范围的职责，就应去掉；它的颜色不是判定依据。[信噪比](https://www.nngroup.com/articles/signal-noise-ratio/)、[可用性原则](https://www.nngroup.com/articles/ten-usability-heuristics/) | 两个普通分组都有粗侧条，标题和边框已足够分组；删除侧条。若侧条标示“当前步骤”，保留并同时给出文字。 |
| 通用风格套用具体产品 | NN/g 观察到未指定视觉语境时，AI 原型容易落回中性底色加亮色点缀的通用样式，或误套与任务不符的页面模式。核对既有品牌、真实对象和任务，而不是按颜色、圆角或渐变本身定罪。[来源](https://www.nngroup.com/articles/ai-prototyping/) | 航班处置工作区套社交主页大头像和欢迎语，挤走航班状态与操作；用任务对象和现有产品语言组织首屏。 |
| 空泛文案与不真实示例 | NN/g 建议以贴近实际的内容和数据驱动原型，并在获得真实数据前先制作可检验的 mock data。检查名称、长短、空值、异常和动作文字是否足以验证布局与流程；mock data 应明确是示例。[来源](https://www.nngroup.com/articles/vague-prototyping/) | 每行都写“示例项目 · 100% · 了解更多”；改成能区分状态、长度和下一步的模拟记录，且不冒充真实业务结果。 |
| 装饰代替状态反馈 | NN/g 要求及时呈现系统状态、错误原因和恢复办法；WCAG 1.4.1 要求颜色不能是传达信息的唯一视觉方式。核对 loading、success、error、disabled 的文字与可操作结果。[NN/g](https://www.nngroup.com/articles/ten-usability-heuristics/)、[W3C WCAG 1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) | 仅把边框变绿表示成功；同时显示“已保存”及时间，失败时说明原因和重试入口。 |

## 边界

- 这些是审核线索，不是“AI 生成检测器”。同一种视觉结果也可能由人工设计；优秀的 AI 辅助界面同样可能通过检查。[NN/g：真实设计情境](https://www.nngroup.com/articles/ai-prototyping/)
- 颜色、圆角、卡片、渐变、插画和侧边标记都有正当用途。要问它是否表达品牌、信息、状态、分组或反馈；保留有职责的设计，删除只增加噪声的重复层。[NN/g：视觉层级](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)、[USWDS Card](https://designsystem.digital.gov/components/card/)
- 有语义的颜色标记需要可见的文字、形状等辅助线索；只换颜色既不能修复信息层级，也不能满足状态传达。[W3C WCAG 1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)
