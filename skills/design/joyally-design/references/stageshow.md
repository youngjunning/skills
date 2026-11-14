# StageShow：产品界面演示素材

[StageShow](https://github.com/benjitaylor/skills/tree/main/stageshow) 是 Benji Taylor 制作的 Agent Skill，用 React 和 CSS 生成缩微产品界面、静帧、光标演示和 Bento 组合。2026-11-15 核对上游 `stageshow/SKILL.md` 版本 1.1.1，仓库 HEAD 为 `299140fafd08df55a9c234e610c3f64af3f45531`。上游 [MIT 许可](https://github.com/benjitaylor/skills/blob/main/stageshow/LICENSE)与[素材声明](https://github.com/benjitaylor/skills/blob/main/stageshow/NOTICE.md)分别适用；上游更新时重新核对。

## 何时使用

落地页 Hero、功能卡、文档封面或 Bento 需要表现产品界面及一段操作时，先按 Joyally Design 的[落地页](web-landing-page.md)、[反模板感检查](anti-ai-taste.md)与[动效](motion.md)确定产品主张、品牌、内容和展示位置，再参考 StageShow 的构图与演示流程。真实可操作页面继续使用项目组件、数据与交互；StageShow 场景是说明产品的演示素材。

## 接入步骤

1. 定义展示容器的实际尺寸、观看设备、主画面和要说明的一个产品动作。静帧要让读者一眼识别产品与结果；动效写出动作、可见反馈和停留画面。Bento 先确定主次卡片、跨卡关系与每张卡的职责。
2. 从目标产品读取品牌 tokens、图标、界面结构和获准内容，按 [上游 Skill](https://github.com/benjitaylor/skills/blob/main/stageshow/SKILL.md) 选择最接近的示例、构图与画面节奏。保留必要的真实文字和界面上下文；其他细节按展示尺寸简化。模拟内容要让读者能识别为演示，不暗示真实业务结果。
3. 需要 StageShow kit 或示例源码时，从上游仓库按项目依赖流程取得，记录版本与改动；使用前逐项核对图标、品牌、图片和字体的来源与许可。Joyally Design 只记录方法和上游入口，不随自身包分发上游代码或第三方素材。
4. 在实际页面尺寸预览静帧、完整动效与窄屏重排。检查裁切、文字、光标落点、动作因果、结果停留和循环接缝；在 reduced motion 下展示可独立说明结果的静帧。若要导出视频或截图，再核对最终文件与页面中的实际呈现。

StageShow 的作者和许可归属上游；采用它的构图方法不表示 Joyally Design 已安装其 kit，也不表示已经完成某个产品页面的视觉验收。
