# Joyally Design 应用广场

[index.html](index.html) 展示已完成并经过真实页面检查的应用。当前收录「日日有数」H5 记账应用，提供手机与桌面画面预览；点击画面或“打开完整应用”可在独立窗口操作。包内的 `ledger-h5/` 是从该项目的生产构建复制的演示制品，演示账单均为虚构数据。

应用中包含 ES modules。请在 Joyally Design 目录运行本地静态服务，再打开 `http://localhost:8123/assets/apps/`：

```bash
python3 -m http.server 8123
```

直接打开 `index.html` 时也可浏览截图；运行完整应用需要上述服务。应用使用浏览器 `localStorage`；清除浏览器数据会删除新增账目。新示例应先确认公开受众、实际功能与截图，再把可独立运行的应用放入单独目录，更新广场中的真实数量与入口。
