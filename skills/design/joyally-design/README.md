# Joyally Design

按产品任务选择 Oil UI Pro 的设计与走查方法，按需使用 Joyally 的语义 tokens、跨平台状态、主题资产、报告与交互图表；主题和组件预设均不代替当前产品的品牌与既有设计。选择依据见[融合方法](references/fused-method.md)。

统一的跨平台设计 Skill：从产品与品牌建立视觉语言，覆盖原生平台适配、React 组件契约、可移植 HTML 报告、演示与交互图表。六套并列主题为「青山湖」「西湖」「苏州园林」「马尔代夫」「阿尔卑斯雪山」与[小香风](references/fashion-xiaoxiang.md)；青山湖正在补齐四季参考，其余五套各有 20 张可追溯的参考画面。前五套的[景观视觉规则](references/visual-language.md)从地点取景，小香风从服装廓形、细节与编辑式呈现取材；粗花呢只是材质线索。小香风另有[浅色与深色 token 样本](assets/xiaoxiang-theme.tokens.json)，现有平台 tokens 与四季预设是青山湖主题的实现样本。参考画面保存在[青山湖](assets/references/qingshan-lake/README.md)、[西湖](assets/references/west-lake/README.md)、[苏州园林](assets/references/suzhou-gardens/README.md)、[马尔代夫](assets/references/maldives/README.md)、[阿尔卑斯雪山](assets/references/alpine-snow-mountains/README.md)与[小香风](assets/references/xiaoxiang/README.md)目录；苏州园林也使用[留园照片](assets/references/lingering-garden/README.md)。

```bash
npx skills add youngjunning/skills --skill joyally-design -g
```

使用 `$joyally-design`，说明产品、目标平台和要完成的任务。入口与按需参考见 [SKILL.md](SKILL.md)。Joyally Design 以[完整设计流程](DESIGN_PROCESS.md)与[融合方法](references/fused-method.md)把方向探索、各类页面方法、存量改造、素材、动效、对比页、截图、评审和规范工具落到共享的语义变量、组件状态与验收契约；按任务选用[景观视觉主题](references/visual-language.md)或[小香风主题](references/fashion-xiaoxiang.md)。全部方法、工具和素材位于本目录，按[能力路由](references/capability-routing.md)读取。更新源包时运行 `python3 scripts/sync-upstream.py <压缩包> --check`，确认后用 `--apply` 导入；已有本地修改会报告冲突，不会被覆盖。

## 快速上手

安装后，在支持 Skills 的对话里输入 `$joyally-design`，接着写任务、使用者、要保留的约束和预期交付。

| 场景 | 可复制的提问 | 预期交付 |
| --- | --- | --- |
| 新建官网 | `$joyally-design 给团队设计系统做一个 React 官网。访客需要找到视觉规范、组件和安装方式。先实现首页，验证桌面、手机和键盘导航。` | 可运行页面与验收截图 |
| 精修已有表单 | `$joyally-design 精修截图里的项目设置表单。保留字段、保存逻辑和组件库，核对校验失败、提交中和提交成功三种状态。` | 改动与前后对比 |
| 实现中后台组件 | `$joyally-design 在现有 React 工作台实现任务列表。先检查组件来源，选用 Button、Input、Select、Table 与反馈组件；保留数据层，验证搜索、筛选、空状态、窄屏和键盘操作。` | 本地组件源码、可操作页面和验证结果 |
| 生成 HTML 周报 | `$joyally-design 把附上的工单数据整理成可离线打开和打印的 HTML 周报，给运营同学看。先写响应时长的变化，再列数据和下一步。` | 报告 HTML 和资源目录 |
| 绘制交互流程图 | `$joyally-design 把工具调用审批流程画成可缩放的交互图，区分审批通过与返回修改两条路径，交付 JSON 源文件和 HTML。` | 流程定义、交互 HTML 和校验结果 |

也可以在 macOS 或 Linux 终端进入 Skill 目录，运行下面的示例。命令会打印可用浏览器打开的产物路径。

编码 Agent 的组件选择、官方源码安装、Joyally tokens 映射和验收顺序见 [React 组件工作流](references/component-workflow.md)。跨项目实现按目标项目和官方 CLI 获取源码。

```bash
output_dir=$(mktemp -d)
node scripts/design-engine.mjs report "$output_dir/joyally-report" --title "工单响应周报"
printf "%s\n" "$output_dir/joyally-report/index.html"
```

```bash
output_dir=$(mktemp -d)
example="runtime/diagram/examples/agent-tool-call.workflow.json"
node scripts/design-engine.mjs diagram validate workflow "$example" &&
  node scripts/design-engine.mjs diagram deliver workflow "$example" "$output_dir/agent-workflow.html" &&
  printf "%s\n" "$output_dir/agent-workflow.html"
```

## 视觉与许可

报告、原生示例与图表遵循 [token 契约](references/token-contract.md)。交互图表的四种样式 共用语义颜色，保留构图、线条与动效特点。旧项目已复制的源码不自动重写；原生 CSS 统一使用 `joyally-` 前缀。

默认本地交付，托管使用调用项目已授权的服务。公开包不依赖内部上传工具。Joyally Design 自身源码采用 [PolyForm Noncommercial 1.0.0](LICENSE)，允许非商业使用、修改和分发；商业使用需另行授权。从 `node scripts/design-engine.mjs --help` 查看报告、演示和图表命令。
