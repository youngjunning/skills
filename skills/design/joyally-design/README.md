# Joyally Design

统一的跨平台设计 Skill：从产品与品牌建立视觉语言，覆盖原生平台适配、React 组件契约、可移植 HTML 报告、演示与交互图表。自身的[中国风审美视觉体系](references/visual-language.md)先定义共同规则，再以「疏林静水」「长桥远望」「游廊框景」作为平等的视觉主题。青山湖水上森林、西湖和苏州园林分别是三个主题当前的取景地；取景地只是主题的来源属性，主题还包括构图、色彩、材质、节奏及语义映射。现有 tokens 与四季预设是取景于青山湖水上森林的「疏林静水」实现样本。[青山湖参考画面](assets/references/qingshan-lake/README.md)用于观察水杉、湖面层次与季节光影。具体产品界面按品牌和任务决定主题与地名是否出现。

```bash
npx skills add youngjunning/skills --skill joyally-design -g
```

使用 `$joyally-design`，说明产品、目标平台和要完成的任务。入口与按需参考见 [SKILL.md](SKILL.md)。Joyally Design 以[完整设计流程](DESIGN_PROCESS.md)与[融合方法](references/fused-method.md)把方向探索、各类页面方法、存量改造、素材、动效、对比页、截图、评审和规范工具落到同一套[中国风审美视觉体系](references/visual-language.md)、语义变量、组件状态与验收契约。全部方法、工具和素材位于本目录，按[能力路由](references/capability-routing.md)读取。更新源包时运行 `python3 scripts/sync-upstream.py <压缩包> --check`，确认后用 `--apply` 导入；已有本地修改会报告冲突，不会被覆盖。

## 快速上手

安装后，在支持 Skills 的对话里输入 `$joyally-design`，接着写任务、使用者、要保留的约束和预期交付。

| 场景 | 可复制的提问 | 预期交付 |
| --- | --- | --- |
| 新建官网 | `$joyally-design 给团队设计系统做一个 React 官网。访客需要找到视觉规范、组件和安装方式。先实现首页，验证桌面、手机和键盘导航。` | 可运行页面与验收截图 |
| 精修已有表单 | `$joyally-design 精修截图里的项目设置表单。保留字段、保存逻辑和组件库，核对校验失败、提交中和提交成功三种状态。` | 改动与前后对比 |
| 生成 HTML 周报 | `$joyally-design 把附上的工单数据整理成可离线打开和打印的 HTML 周报，给运营同学看。先写响应时长的变化，再列数据和下一步。` | 报告 HTML 和资源目录 |
| 绘制交互流程图 | `$joyally-design 把工具调用审批流程画成可缩放的交互图，区分审批通过与返回修改两条路径，交付 JSON 源文件和 HTML。` | 流程定义、交互 HTML 和校验结果 |

也可以在 macOS 或 Linux 终端进入 Skill 目录，运行下面的示例。命令会打印可用浏览器打开的产物路径。

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
