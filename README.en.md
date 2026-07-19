# 🌐 Global Skill Daily

![version](https://img.shields.io/badge/version-1.1.0-green)
![license](https://img.shields.io/badge/license-MIT--0-blue)
![platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

> Scans two global Skill platforms (ClawHub 500 + SkillHub 75K) every 3 days, merges & dedupes 936+ skills, and produces a global Skill ecosystem daily report with cross-platform insights based on the user's current agent context. 10-dimension recommendations rotate in 3 groups (trend / quality / user).

📖 **中文文档** | [English](./README.en.md)

## ✨ Core Features

- **🌐 Cross-platform exclusive view**: Merges ClawHub + SkillHub, enabling china_only / global_only / trending_both comparison dimensions impossible when running each platform separately
- **🔄 Dimension rotation**: 10 dimensions split into 3 groups (A trend / B quality / C user), rotating every 3 days to avoid repetitive recommendations
- **🌏 Cross-platform ecosystem insights (5 chapters)**: Heat disparity leaderboard / dual-listed gap>5x / category preference comparison / Chinese-platform-specific skills
- **📅 14-day cross-dimension deduplication**: Covers 4-5 historical recommendations at 3-day frequency
- **🧠 Deep user-context scanning**: TRAE memory (3-level weighted) + active project files + experience backups + installed skills
- **📁 Tri-storage delivery**: Obsidian vault + IMA FIM knowledge base + Feishu online docx + Card 2.0 IM message

## 📦 Installation

### Prerequisites

- Python 3.10+
- [skillhub CLI](https://skillhub.cn) (for fetching SkillHub rankings)
- [lark-cli](https://www.npmjs.com/package/@larksuite/cli) (for pushing Feishu cloud docs)

### Environment Variables

```bash
FEISHU_APP_ID=<your_app_id>
FEISHU_APP_SECRET=<your_app_secret>
FEISHU_USER_OPEN_ID=<your_user_open_id>
IMA_OPENAPI_CLIENTID=<your_ima_client_id>
IMA_OPENAPI_APIKEY=<your_ima_api_key>
OBSIDIAN_VAULT_PATH=E:\Obsidian-Vault\00-Inbox  # optional
```

### Install

```bash
# ClawHub
clawhub install global-skill-daily

# SkillHub
skillhub install global-skill-daily
```

## 🚀 Usage

### Trigger Phrases

- "全球 skill 日报"
- "global skill daily"
- "跑一下全球 skill 推荐"
- "每 3 天 skill 推荐"

### Cron Schedule

Cron expression: `30 6 */3 * *` (every 3 days at 06:30)

### Manual Run

```bash
cd "d:/TRAE SOLO CN/project"
python global-skill-daily/global_skill_daily_executor.py
```

## ⚠️ User Notice (Side Effects)

When running as a scheduled task, this skill automatically performs the following side effects:

- **Auto-writes to external services**: Obsidian vault / IMA FIM knowledge base / Feishu cloud drive / Feishu IM card messages
- **Auto-reads local data**: TRAE memory directory (project_memory + topics + user_profile) + project files + experience backups + installed skill list
- **Auto-creates files**: project `data/recommended/{date}.json` and `{date}.md` + Obsidian `00-Inbox/global-skill-daily_{date}.md`

**How to disable side effects**: When running manually, add `--no-obsidian` / `--no-feishu` / `--no-ima` parameters to skip the corresponding channels.

## 📋 Output Example

```
🌐 Global Skill Ecosystem Daily | 2026-07-19

TL;DR
- Dual-list scan: ClawHub 492 + SkillHub 555 → 936 unique skills after merge
- Today's recommendations: 7 (cross-platform: 6)
- Skipped via 14-day dedup: 10 (v1.1)
- Today's dimension group: Trend (focused on dual-list heat & cross-platform gaps)

🌏 Cross-Platform Ecosystem Insights
- Found 30 dual-listed skills with heat gap >5x — reflects CN vs global developer preference divergence
- CN-exclusive hot skills cluster in "office-efficiency" category (23)
- Global-exclusive hot skills cluster in "integrations" category (77)
- Identified 77 Chinese-platform-specific skills (bilibili/douyin/wechat etc.)
```

## 📊 Recommendation Dimensions (10 dimensions, 3 rotating groups)

| Group | Dimension | Count | Description |
|-------|-----------|-------|-------------|
| A Trend | trending_both | ×2 | Hot on both lists |
| A Trend | china_only | ×2 | CN-exclusive hot |
| A Trend | global_only | ×2 | Global-exclusive hot |
| A Trend | panorama | ×1 | Panoramic view |
| B Quality | quality | ×2 | Top-rated |
| B Quality | newcomers | ×2 | Newcomers |
| B Quality | active_developer | ×2 | Active developers |
| B Quality | verified | ×1 | Quality certified |
| C User | memory_collision | ×3 | Memory collision |
| C User | scene_match | ×4 | Pain-point match |
| C User | trending_both | ×1 | Dual-hot (fallback) |

## 📁 Repository Structure

```
global-skill-daily/
├── SKILL.md                          # Main entry (≤200 lines)
├── README.md                         # Chinese docs
├── README.en.md                      # English docs (this file)
├── CHANGELOG.md                      # Version log
├── LICENSE                           # MIT-0
├── .gitignore                        # Git ignore
├── .clawhubignore                    # ClawHub ignore
├── .claude-plugin/
│   └── plugin.json                   # Plugin metadata
├── references/
│   └── pain-points.md                # Pain-point scenario library
├── scripts/
│   ├── fetch_clawhub.py              # Fetch ClawHub
│   ├── fetch_skillhub.py             # Fetch SkillHub
│   ├── normalize.py                  # Merge & dedupe
│   ├── scan_user_context.py          # User context scanner
│   ├── daily_recommend.py            # 10-dimension engine
│   ├── push_to_obsidian.py           # Obsidian pusher
│   ├── push_to_ima.py                # IMA pusher
│   └── push_to_feishu.py             # Feishu pusher
└── global_skill_daily_executor.py    # Main executor
```

## 📝 Changelog

### v1.1.0 (2026-07-19)

- Dimension rotation mechanism (3 groups, 3-day cycle)
- Cross-platform ecosystem insights module (5 chapters)
- Frequency changed from daily to every 3 days
- Dedup window extended from 7 to 14 days
- Feishu storage switched from `+upload` to `+import --type docx` (fixes button-only-downloads bug)
- IMA API endpoint fix (openapi.yixin.im → ima.qq.com)

### v1.0.0 (2026-07-19)

- Merged ClawHub Daily + SkillHub Daily into a single skill
- 10-dimension recommendation engine
- Deep user-context scanning (3-level weighted)
- Tri-storage failure isolation + Obsidian 3-tier fallback

## 📄 License

MIT-0

## 🔗 Related Links

- [ClawHub](https://clawhub.ai) — Global Skill platform
- [SkillHub](https://skillhub.cn) — Chinese Skill platform
- [TRAE](https://trae.cn) — AI coding assistant
