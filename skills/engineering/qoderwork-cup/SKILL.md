---
name: qoderwork-cup
description: 通过 macOS Computer Use 验收 QoderWork Chat 的技能加载、消息、确认入口、进度和结果展示，处理窗口绑定与可访问性索引问题；不代替被测技能的服务端协议验收。
---

# QoderWork Computer Use

使用当前环境暴露的 Computer Use 文档绑定应用。先按已核验的 bundle ID `com.qoder.work` 获取 App；宿主 API 与旧示例不同或绑定失败时，先核对当前可用应用与 API，再继续。

```js
const app = await cua.getApp('com.qoder.work');
const state = await app.getAXState({ disableDiffing: true });
```

读取可访问性树使用 `getAXState()`，绑定应用使用 `getApp()`；不假定存在 `app.getState()`、`app.getWindow()` 或 `cua.computer.launch_app`。按当前文档约定提交回车，不能将 `ENTER` 当作通用键名。

1. 每次操作或等待状态变化后重新读取 UI 并定位；Accessibility index 只对最近一次状态有效。
2. 优先使用 AX 操作；需要坐标时以当前截图定位，截图到点击之间不插入改变窗口状态的操作。
3. 瞬时无窗口时，重新读取全局状态并绑定一次；仍不可用则记录 UI 阶段未验收。
4. 发送消息或确认执行后，先检查是否已提交再重试，避免重复触发任务。普通 UI 动作至多重试一次。

验收前从被测项目读取技能名称、安装方式、测试目标和允许的副作用；不覆盖已有技能安装。UI 检查按真实显示记录：技能是否加载，消息原文是否完整，确认入口是否出现，进度与结果是否可见。

UI 中的运行状态不证明远端任务仍在执行，也不证明结果正确。服务端任务 ID、事件、终态和产物由被测项目自己的协议测试对照；本技能不携带具体服务协议、环境地址或账号读取逻辑。真实执行需要项目授权；没有目标环境或执行授权时，只做不会触发远端任务的本地检查。

窗口、AX 与 Computer Use 故障记录在 UI 层；被测业务的失败另行记录。完成后分别报告本地接入、UI 验收、协议结果和目标设备的未验证项。
