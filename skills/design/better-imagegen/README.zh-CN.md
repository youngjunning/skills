# better-imagegen

**通用 GPT Image 2.6 生图 Skill** — 可接入支持 `SKILL.md` 的 Agent 运行时或直接复用其脚本；由 [apiyi](https://api.apiyi.com/register/?aff_code=ijv5) 驱动，通过 OpenAI 兼容图片接口，仅使用 GPT Image 2.6 高质量模式。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-blueviolet)](#)
[![apiyi](https://img.shields.io/badge/Powered_by-apiyi-orange)](https://api.apiyi.com/register/?aff_code=ijv5)

[English](README.md) · [中文](#)

---

## 能做什么

在任意接入该 Skill 的 Agent 中直接描述需求：

```
生成一张东京夜晚街头的电影感女性肖像
帮我做一个 App logo，深色主题，极简风格
并行生成 8 张产品图
做一个 Runcat 风格的菜单栏机器人跑步帧动画
做一张 Mac 动态壁纸，深海珊瑚礁，白天/夜晚切换
制作一个兼容 Codex 的宠物：湖獭、毛绒风格、带 16 个看向方向
把这篇技术文章中的架构、依赖和更新流程文字示意换成正式技术图
```

技能按图片类型选择工作流，统一使用 GPT Image 2.6 高质量模式，再完成后处理并保存到 `~/Pictures/better-imagegen/`。

生成前会先过一层提示词合规化：自动弱化平台 Logo、图片内精确文字、露骨内容、血腥暴力、模仿在世艺术家等高风险表达，减少正常创意需求被误拒的概率。

---

## 模型

| 模型 ID | 角色 | 说明 |
|---------|------|------|
| `gpt-image-2.6-sunburst` | 生成与编辑唯一模型 | 显式使用 `quality=high`；最多原模型重试一次，仍失败则停止并报告错误。实测范围见 `references/apiyi.md`。 |

**GPT 16:9 尺寸预设：**

| 档位 | 尺寸 |
|------|------|
| 1K | 1280×720 |
| 2K | 2048×1152 |
| 4K | 3840×2160 |

完整模型规格和尺寸约束见 `references/apiyi.md`。

---

## 使用场景

| 请求类型 | 模型 | 输出 |
|---------|-------------|------|
| 知识图谱 / 架构图 / 生命周期图 | GPT 无文字底图 + HTML/CSS/SVG 确定性语义层 | 3200×1800 PNG + WebP + 布局门禁报告 |
| 人像 / 插图 | GPT Image 2.6 | `.webp` q78，≤ 300 KB |
| Logo / favicon | GPT Image 2.6 | `.png`（pngquant），≤ 100 KB |
| Mac 静态壁纸（4K） | GPT Image 2.6 | `wallpaper.png`（无损 PNG） |
| Mac 动态壁纸 | 每帧 GPT Image 2.6 | `wallpaper-apr.heic`（2 帧，亮/暗模式切换） |
| Sprite loop 帧动画 | GPT Image 2.6 | 序列帧 PNG + `preview.gif` |
| Codex v2 宠物 | GPT Image 2.6 | 8×11 spritesheet + `pet.json` + QA 产物 |
| 批量生成（N 张） | 每张使用 GPT Image 2.6 | N × `.webp`，并行生成 |

---

## 技术图与插图密度

知识图谱、架构图、依赖图、构建流水线、发布流程和 Updater 状态机不让图片模型直接绘制文字和关系。模型只生成克制的无文字底图；节点、连线、箭头、标签、图例和生命周期状态全部由 HTML/CSS/SVG 确定性渲染，保证技术术语准确、箭头方向可验证。

长技术文章在交付前必须执行“可视化机会审计”，不设置插图数量上限。只要读者需要理解三步以上的顺序、分支、运行或所有权边界、依赖传播、状态变化、回滚或跨模块生命周期，就优先用图表达。ASCII/TXT 示意只能作为制图中间态，不能进入最终文章；可执行命令、配置、literal path 和短文件清单继续保留为 code block。

所有确定性技术图在导出和发布前必须通过真实浏览器几何门禁：

```bash
node scripts/validate_diagram_layout.mjs /absolute/path/diagram.html \
  --width 1600 --height 900 --min-gap 24 --boundary-clearance 16
```

门禁会在字体加载完成后读取 headless Chrome 的实际 DOM 几何，拒绝卡片重叠、gutter 过窄、标签压住卡片、连线穿越无关节点、箭头 marker 挤压卡片描边或阴影、文字贴近或穿过分隔线 / rail、文字裁切、元素越界和缺失布局标注。受保护的线标记 `data-layout-boundary`，相邻文字组标记 `data-layout-text`、`data-boundary-ref` 和 `data-boundary-side`。横向阶段图追加 `--min-gap 80 --edge-clearance 20 --marker-clearance 20 --label-clearance 8 --min-edge-length 56 --max-marker-size 16`。数值门禁通过后，还必须检查全尺寸和缩略预览，拦截“虽然没有相交，但视觉上仍然拥挤”的布局。

---

## Mac 动态壁纸

生成含 `apple_desktop:apr` 元数据的 2 帧 HEIC。系统外观切换到深色模式时，macOS 自动切换壁纸帧。

```
做一张动态壁纸，深夜星空下的山脉
```

**依赖：** `"$BETTER_IMAGEGEN_PYTHON" -m pip install pillow-heif`（安装到项目 `.venv`，内置 libheif，无需 Homebrew）

**输出路径：** `~/Pictures/better-imagegen/dynamic-wallpaper/wallpaper-apr.heic`

> **macOS Sonoma 说明：** 时间型（h24）HEIC 动态壁纸在 Sonoma 上已失效——苹果将该格式迁移到私有 `.madesktop` 体系。亮/暗模式切换（apr）完全可用。

---

## Sprite Loop 帧动画

用于 Runcat 类菜单栏动画、状态 mascot、loading loop、小型 App 动画。技能会先生成 sprite sheet，再切成编号 PNG 序列帧，写入 `manifest.json`，并打开 `preview.gif` 预览。

**输出路径：** `~/Pictures/better-imagegen/sprite-loop/{name}/`

## Codex 兼容宠物（可选目标格式）

这是通用宠物资产流程中的一个可选 adapter：面向 Codex 时，交付 `1536×2288` 的 8×11 v2 spritesheet、`spriteVersionNumber: 2` 的 `pet.json`、16 个连续 look directions，以及 contact sheet、motion preview、direction / chroma / validation QA 产物。技能先锁定宠物身份，再逐行生成和验收；不会自动安装到任何运行时目录，最终安装和动态验证由用户主动完成。

**输出路径：** `~/Pictures/better-imagegen/codex-pet/{pet-id}/`

---

## 输出规范

| 资产类型 | 格式 | 路径 |
|---------|------|------|
| 封面 / 插图 | 有损 WebP q78 | `~/Pictures/better-imagegen/{name}.webp` |
| Mac 静态壁纸 | 无损 PNG | `~/Pictures/better-imagegen/wallpaper.png` |
| Mac 动态壁纸 | 2 帧 HEIC | `~/Pictures/better-imagegen/dynamic-wallpaper/wallpaper-apr.heic` |
| Sprite loop 帧动画 | PNG 序列帧 + preview GIF | `~/Pictures/better-imagegen/sprite-loop/{name}/` |
| Codex v2 宠物 | spritesheet + `pet.json` + QA 产物 | `~/Pictures/better-imagegen/codex-pet/{pet-id}/` |
| Logo | PNG（pngquant） | 项目本地 |
| 元数据 | JSON | 与图片同目录 |

中间 PNG 写入 `/tmp/`，打包完成后自动清理。

---

## 安装配置

**1. 获取 API Key**

在 [apiyi.com](https://api.apiyi.com/register/?aff_code=ijv5) 注册，新用户有免费额度。

**2. 配置 Key**
```bash
export APIYI_API_KEY="your-key-here"
# 加到 ~/.zshrc 永久生效
```

**3. 安装到你的 Agent Skill 目录**
```bash
# 将目录放入你所用 Agent 的 skills 目录，并按该 Agent 的加载约定启用。
npx skills add youngjunning/skills --skill better-imagegen -g
```

**4. 安装核心本地依赖**
```bash
# 在安装工具给出的 better-imagegen 技能目录内执行。
eval "$(./scripts/ensure_venv.sh)"
# 依赖会安装到当前项目的 .venv，不会修改系统 Python
```

**5. 动态壁纸专用依赖**
```bash
"$BETTER_IMAGEGEN_PYTHON" -m pip install pillow-heif
```

---

## 文件结构

```
SKILL.md                      ← 技能入口与触发规则
references/
  apiyi.md                    ← API 鉴权、模型规格、尺寸约束、错误码
  generation.md               ← API Key 检查、模型别名、gen_image_apiyi、metadata helper
  prompt-compliance.md        ← 提示词合规化与拒绝重试策略
  post-process.md             ← WebP 转换、尺寸调整、PNG 压缩
  portrait.md                 ← 人像、封面、banner、通用单图
  knowledge-map.md            ← 精确技术图、插图密度审计、强制布局门禁
  high-allure.md              ← 高质感 romance / editorial 图片
  logo-icon.md                ← 透明 Logo、图标、favicon、抠图素材
  static-wallpaper.md         ← 静态壁纸 PNG 流程
  dynamic-wallpaper.md        ← Mac 动态壁纸：生成 + HEIC 打包
  sprite-loop.md              ← Runcat 类序列帧动画资产
  codex-pet.md                ← Codex v2 宠物：8×11 atlas、方向语义与 QA
scripts/
  validate_diagram_layout.mjs ← 真实 DOM 重叠、间距、穿线、溢出门禁
  test_validate_diagram_layout.mjs ← 正常与失败路径回归用例
```

---

## License

MIT — 见 [LICENSE](LICENSE)。
