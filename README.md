# 🌐 Global Skill Daily | 全球 Skill 生态日报

![version](https://img.shields.io/badge/版本-1.1.0-green)
![license](https://img.shields.io/badge/license-MIT--0-blue)
![platform](https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

> 每 3 天扫描全球两大 Skill 平台（ClawHub 500 + SkillHub 7.5万），合并去重 936+ skill，基于用户当前 agent 上下文做 10 维度推荐（3 组轮换：趋势/质量/用户），生成含跨平台生态洞察的全球 Skill 生态日报并三处存放推送。

## ✨ 核心特性

- **🌐 跨平台独占视角**：合并 ClawHub + SkillHub，独占 china_only / global_only / trending_both 三个对比维度
- **🔄 维度轮换机制**：10 维度分 3 组（A 趋势 / B 质量 / C 用户），每 3 天 1 周期，避免推荐雷同
- **🌏 跨平台生态洞察（5 章节）**：热度差异榜 / 双榜共有 gap>5x / 品类偏好对比 / 中文平台特色 skill
- **📅 14 天跨维度去重**：配合每 3 天 1 次频率，覆盖 4-5 次历史推荐
- **🧠 用户上下文深度扫描**：TRAE memory（3 级权重）+ 项目活跃文件 + 经验备份 + 已装 skill 清单
- **📁 三处存放**：Obsidian vault + IMA FIM 知识库 + 飞书云文档（在线 docx）+ Card 2.0 卡片消息

## 📦 安装

### 前置依赖

- Python 3.10+
- [skillhub CLI](https://skillhub.cn)（用于抓取 SkillHub 排行榜）
- [lark-cli](https://www.npmjs.com/package/@larksuite/cli)（用于推送飞书云文档）

### 环境变量

```bash
FEISHU_APP_ID=<your_app_id>
FEISHU_APP_SECRET=<your_app_secret>
FEISHU_USER_OPEN_ID=<your_user_open_id>
IMA_OPENAPI_CLIENTID=<your_ima_client_id>
IMA_OPENAPI_APIKEY=<your_ima_api_key>
OBSIDIAN_VAULT_PATH=E:\Obsidian-Vault\00-Inbox  # 可选
```

### 安装方式

```bash
# ClawHub
clawhub install global-skill-daily

# SkillHub
skillhub install global-skill-daily
```

## 🚀 使用

### 触发词

- "全球 skill 日报"
- "global skill daily"
- "跑一下全球 skill 推荐"
- "每 3 天 skill 推荐"

### 定时任务

cron 表达式：`30 6 */3 * *`（每 3 天 06:30 执行）

### 手动运行

```bash
cd "d:/TRAE SOLO CN/project"
python global-skill-daily/global_skill_daily_executor.py
```

## ⚠️ 用户须知（副作用声明）

本技能作为定时任务运行时会自动执行以下副作用：

- **自动写入外部服务**：Obsidian vault / IMA FIM 知识库 / 飞书云盘 / 飞书 IM 卡片消息
- **自动读取本地数据**：TRAE memory 目录（project_memory + topics + user_profile）+ 项目文件 + 经验备份 + 已装 skill 清单
- **自动创建文件**：项目 `data/recommended/{date}.json` 和 `{date}.md` + Obsidian `00-Inbox/global-skill-daily_{date}.md`

**如何禁用副作用**：手动运行时可加 `--no-obsidian` / `--no-feishu` / `--no-ima` 参数跳过对应渠道

## 📋 输出示例

```
🌐 全球 Skill 生态日报 | 2026-07-19

TL;DR
- 双榜扫描：ClawHub 492 + SkillHub 555 → 合并去重 936 个独立 skill
- 今日推荐 7 个，跨平台对比 6 个
- 跳过 14 天去重 10 个（v1.1）
- 今日维度组：趋势组（聚焦双榜热度与跨平台差异）

🌏 跨平台生态洞察
- 发现 30 个双榜共有但热度差 >5x 的 skill
- 国内独火 skill 集中在「office-efficiency」品类（23 个）
- 全球独火 skill 集中在「integrations」品类（77 个）
- 识别出 77 个中文平台特色 skill（bilibili/douyin/wechat 等）
```

## 📊 推荐维度（10 维度 3 组轮换）

| 组 | 维度 | 推荐数 | 描述 |
|----|------|--------|------|
| A 趋势组 | trending_both | ×2 | 双榜都火 |
| A 趋势组 | china_only | ×2 | 国内独火 |
| A 趋势组 | global_only | ×2 | 全球独火 |
| A 趋势组 | panorama | ×1 | 全景视角 |
| B 质量组 | quality | ×2 | 口碑精品 |
| B 质量组 | newcomers | ×2 | 新星上线 |
| B 质量组 | active_developer | ×2 | 活跃开发者 |
| B 质量组 | verified | ×1 | 质量认证 |
| C 用户组 | memory_collision | ×3 | 记忆碰撞 |
| C 用户组 | scene_match | ×4 | 痛点匹配 |
| C 用户组 | trending_both | ×1 | 双榜热装（兜底） |

## 📁 仓库结构

```
global-skill-daily/
├── SKILL.md                          # 主入口（≤200行）
├── README.md                         # 中文说明（本文件）
├── README.en.md                      # 英文说明
├── CHANGELOG.md                      # 版本日志
├── LICENSE                           # MIT-0
├── .gitignore                        # Git 忽略
├── .clawhubignore                    # ClawHub 忽略
├── .claude-plugin/
│   └── plugin.json                   # 插件元数据
├── references/
│   └── pain-points.md                # 痛点场景库
├── scripts/
│   ├── fetch_clawhub.py              # 抓取 ClawHub
│   ├── fetch_skillhub.py             # 抓取 SkillHub
│   ├── normalize.py                  # 合并去重
│   ├── scan_user_context.py          # 用户上下文扫描
│   ├── daily_recommend.py            # 10 维度推荐引擎
│   ├── push_to_obsidian.py           # Obsidian 推送
│   ├── push_to_ima.py                # IMA 推送
│   └── push_to_feishu.py             # 飞书推送
└── global_skill_daily_executor.py    # 主执行器
```

## 📝 版本日志

### v1.1.0 (2026-07-19)

- 维度轮换机制（3 组，每 3 天 1 周期）
- 跨平台生态洞察模块（5 章节）
- 频率从每日改为每 3 天
- 去重窗口从 7 天延长到 14 天
- 飞书存储从 `+upload` 切换到 `+import --type docx`（修复按钮不能查看）
- IMA API 端点修复（openapi.yixin.im → ima.qq.com）

### v1.0.0 (2026-07-19)

- 合并 ClawHub Daily + SkillHub Daily 为单一技能
- 10 维度 12 个推荐引擎
- 用户上下文深度扫描（3 级权重）
- 三处存放失败隔离 + Obsidian 三级 fallback

## 📄 License

MIT-0

## 🔗 相关链接

- [ClawHub](https://clawhub.ai) — 全球 Skill 平台
- [SkillHub](https://skillhub.cn) — 中文 Skill 平台
- [TRAE](https://trae.cn) — AI 编程助手
