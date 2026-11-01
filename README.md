# 俊宁的 Agent Skills

集中维护日常使用的工程、设计、写作与站点建设技能。每个技能保留独立的 `SKILL.md`、参考资料和辅助脚本，可按需安装，更新集中在一个仓库。

俊宁，阿里高级工程师、AI 开发者，拥有 10 年研发经验，现专注 AI 应用、AI 浏览器、Agent、AI Infra 与软件工程。

## 安装

选择需要的技能：

```bash
npx skills add youngjunning/skills
```

安装单个技能：

```bash
npx skills add youngjunning/skills --skill top-architect -g
```

`skills` CLI 的 Agent 选择与目标位置以安装时显示的选项为准。安装第三方工具不代表本仓库提供其服务、账号或额度。

维护者也可以使用同一个 checkout，通过软链接安装；以后 `git pull` 即可更新源文件：

```bash
git clone https://github.com/youngjunning/skills.git
cd skills
python3 scripts/link-skills.py --dest ~/.codex/skills --dry-run
python3 scripts/link-skills.py --dest ~/.codex/skills
```

已有同名安装时脚本默认停止；明确需要替换时加 `--replace`，旧内容会先移入本机备份目录。其他 Agent 可显式指定其技能目录，例如 `--dest ~/.claude/skills`。同一个 Agent 使用一种安装方式，避免重复加载。

## 技能目录

| 类别 | 技能 | 用途 |
| --- | --- | --- |
| Engineering | [top-architect](skills/engineering/top-architect/SKILL.md) | 架构讨论、决策与评审 |
| Engineering | [report-skill](skills/engineering/report-skill/SKILL.md) | 工程汇报与交付证据 |
| Engineering | [tauri-skills](skills/engineering/tauri-skills/SKILL.md) | Tauri 2 安全边界与 Node.js sidecar |
| Engineering | [windows-app-automation](skills/engineering/windows-app-automation/SKILL.md) | Windows 桌面自动化与状态验收 |
| Engineering | [browser-performance-audit](skills/engineering/browser-performance-audit/SKILL.md) | 加载、资源与长会话性能审查 |
| Design | [better-imagegen](skills/design/better-imagegen/SKILL.md) | 图像生成、编辑与素材校验 |
| Design | [qingshan-design](skills/design/qingshan-design/SKILL.md) | 青山湖跨平台设计系统 |
| Writing | [writting-skill](skills/writing/writting-skill/SKILL.md) | 中文与英文写作、博客与书稿 |
| Writing | [fiction-site-builder](skills/writing/fiction-site-builder/SKILL.md) | 小说创作与阅读站点建设 |
| Publishing | [adsense-site-builder](skills/publishing/adsense-site-builder/SKILL.md) | AdSense 站点规划、建设与就绪审查 |
| productivity | [memory-distill](skills/productivity/memory-distill/SKILL.md) | 独立整理个人记录、参考资料与概念笔记，按配置同步清单与统计 |
| productivity | [personal-records-reader](skills/productivity/personal-records-reader/SKILL.md) | 从显式配置的资料站读取记录、文章与收藏 |
| engineering | [qoderwork-cup](skills/engineering/qoderwork-cup/SKILL.md) | QoderWork Chat 的 Computer Use 验收 |
| engineering | [qwenwork-cup](skills/engineering/qwenwork-cup/SKILL.md) | 千问办公 Chat 的 Computer Use 验收 |
| Engineering | [macos-app-develop](skills/engineering/macos-app-develop/SKILL.md) | 原生 macOS、SwiftUI 与 Instruments 工作流（含许可改编） |
| engineering | [polyglot-service-deploy](skills/engineering/polyglot-service-deploy/SKILL.md) | 多运行时服务的构建、监督与部署诊断 |
| design | [lake-report-design](skills/design/lake-report-design/SKILL.md) | 可移植 HTML 报告、语义设计与可探索图表 |

机器可读目录位于 [catalog.json](catalog.json)。现有技能名保持不变，包括 `writting-skill` 的历史拼写。

## 使用与维护

按 Agent 支持的方式调用技能，例如 `$top-architect`，或描述任务让 Agent 按匹配条件选择。部分技能依赖浏览器、Computer Use、图像服务或额外工具，具体前提见对应入口；静态校验不代表这些外部能力已完成验收。

```bash
python3 scripts/validate.py
```

新增技能放在 `skills/<category>/<name>/`，更新目录与说明，运行相关脚本测试后提交。涉及行为变化的更新记录到 [CHANGELOG.md](CHANGELOG.md)。发布边界和贡献要求见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 公开范围与来源

通用技能在这里维护；依赖私有业务、内部系统、未公开协议或敏感数据的技能保留在各自私有仓库。目标地址、账号、密钥、个人安装记录应留在使用项目或本机配置中。

已安装的第三方技能继续跟随上游，不因本机安装而收录为原创。已有借鉴与改编的署名、许可和 `NOTICE` 随技能保留，参见 [THIRD_PARTY.md](THIRD_PARTY.md)。

目录组织与统一维护方式参考 [mattpocock/skills](https://github.com/mattpocock/skills)。本仓库使用分类目录、统一安装入口与本地链接，不要求额外控制服务或发布平台。

## 许可

MIT。根目录许可适用于本仓库新增的自有内容；各技能已有的 `LICENSE`、署名和第三方声明继续有效。
