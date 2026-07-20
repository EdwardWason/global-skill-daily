# 🌐 Global Skill Daily

![version](https://img.shields.io/badge/version-1.5.0-green)
![license](https://img.shields.io/badge/license-MIT--0-blue)
![platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![deps](https://img.shields.io/badge/deps-Python%20stdlib-success)

> Scans two global Skill platforms (ClawHub 500 + SkillHub 75K) every 3 days, merges & dedupes 936+ skills, and produces a global Skill ecosystem daily report with cross-platform insights based on the user's current agent context. 10-dimension recommendations rotate in 3 groups (trend / quality / user). v1.5.0 self-contained refactor: depends only on the Python standard library — no third-party packages, no external CLIs.

📖 **中文文档** | [English](./README.en.md)

## ✨ Core Features

- **🌐 Cross-platform exclusive view**: Merges ClawHub + SkillHub, enabling china_only / global_only / trending_both comparison dimensions impossible when running each platform separately
- **🔄 Dimension rotation**: 10 dimensions split into 3 groups (A trend / B quality / C user), rotating every 3 days to avoid repetitive recommendations
- **🌏 Cross-platform ecosystem insights (5 chapters)**: Heat disparity leaderboard / dual-listed gap>5x / category preference comparison / Chinese-platform-specific skills
- **📅 14-day cross-dimension deduplication**: Covers 4-5 historical recommendations at 3-day frequency
- **🧠 Deep user-context scanning**: TRAE memory (3-level weighted) + active project files + experience backups + installed skills
- **📁 Tri-storage delivery**: Obsidian vault + IMA FIM knowledge base + Feishu online docx (optional lark-cli, degrades to card-only when unavailable) + Card 2.0 IM message
- **🔐 v1.2.0 Security hardening**: Channel toggles (`--no-obsidian` / `--no-feishu` / `--no-ima` / `--dry-run`) + sensitive keyword redaction + argv list subprocess + required env vars
- **🔒 v1.5.0 Self-contained refactor**: Depends only on the Python standard library (urllib/json/re/sys/os/pathlib/datetime/collections). No `pip install` needed. No `skillhub` CLI / `lark-cli` required (lark-cli is optional)

## 📦 Installation

### Prerequisites

- Python 3.10+ (Python standard library only, no pip packages required)

#### Optional Dependencies (for enhanced features)

- [lark-cli](https://www.npmjs.com/package/@larksuite/cli) (optional, for pushing Feishu cloud docs; auto-degrades to card-only when unavailable)
- ~~[skillhub CLI](https://skillhub.cn)~~ (no longer needed since v1.5.0 — directly calls SkillHub HTTP API)

### Environment Variables

```bash
FEISHU_APP_ID=<your_app_id>
FEISHU_APP_SECRET=<your_app_secret>
FEISHU_USER_OPEN_ID=<your_user_open_id>
IMA_OPENAPI_CLIENTID=<your_ima_client_id>
IMA_OPENAPI_APIKEY=<your_ima_api_key>
IMA_KB_ID=<your_ima_kb_id>  # required since v1.2.0
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

### Cron Schedule

Cron expression: `30 6 */3 * *` (every 3 days at 06:30)

### Manual Run

```bash
cd "d:/TRAE SOLO CN/project"

# Full run (tri-storage)
python global-skill-daily/global_skill_daily_executor.py

# v1.2.0: skip specific channels
python global-skill-daily/global_skill_daily_executor.py --no-feishu --no-ima
python global-skill-daily/global_skill_daily_executor.py --no-obsidian

# v1.2.0: dry-run (only first 5 steps, no push)
python global-skill-daily/global_skill_daily_executor.py --dry-run

# v1.3.0: skip user context scanning (privacy-sensitive scenarios)
python global-skill-daily/global_skill_daily_executor.py --no-context-scan
```

## ⚠️ User Notice (Side Effects)

When running as a scheduled task, this skill automatically performs the following side effects:

- **Auto-writes to external services**: Obsidian vault / IMA FIM knowledge base / Feishu cloud drive / Feishu IM card messages
- **Auto-reads local data**: TRAE memory directory (project_memory + topics + user_profile) + project files + experience backups + installed skill list
- **Auto-creates files**: project `data/recommended/{date}.json` and `{date}.md` + Obsidian `00-Inbox/global-skill-daily_{date}.md`

**How to disable side effects (implemented in v1.2.0)**:
- `--no-obsidian` skips Obsidian push
- `--no-feishu` skips Feishu cloud doc + card message push
- `--no-ima` skips IMA FIM knowledge base push
- `--dry-run` runs only first 5 steps (fetch + merge + scan + recommend), no push to any channel
- `--no-context-scan` (v1.3.0) skips user context scanning entirely, recommendations degrade to trending-only

**Derived output redaction (v1.2.0)**: Keywords output from user context scanning are filtered for sensitive terms (token/secret/password/apikey/credential etc.) to avoid leaking credential hints in derived content.

**v1.4.0 Privacy boundary hardening (zero derived content)**:
- ✅ **Derived reports publish zero context-derived content**: The "User Context Snapshot" section in the report markdown only publishes aggregate counts (keyword count / project count / experience file count / installed skill count). No derived content is published (not even the Top 10 keyword list).
- ❌ **Raw inventory not published**: Project names / experience file names / installed skill lists / keyword lists remain in local `data/user_context_{date}.json` only, never pushed to external services
- 🔧 **Skip scanning entirely**: `--no-context-scan` skips TRAE memory / project files / experience backups / installed skill scanning; recommendations degrade to trending-only (no memory_collision / scene_match dimensions)

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

### v1.5.0 (2026-07-20)

**Self-contained refactor** (removes all external dependencies — Python standard library only):

- ✅ **`fetch_clawhub.py` removes `requests` third-party package**: Switched to Python standard library `urllib.request` + `urllib.error`; User-Agent changed from `clawhub-daily/1.0` to `global-skill-daily/1.5.0`
- ✅ **`fetch_skillhub.py` removes `skillhub` CLI binary dependency**: Directly calls SkillHub HTTP API (`https://api.skillhub.cn/api/v1/showcase/{type}` and `/api/v1/search`), no `skillhub` CLI installation required
- ✅ **`push_to_feishu.py` `lark-cli` becomes optional**: When lark-cli is unavailable, auto-degrades to card-only message (card already contains the full report text), no longer blocks the flow
- ✅ **`plugin.json` dependency declaration updated**: `bins` changed from `["python", "skillhub"]` to `["python"]`; version bumped to 1.5.0
- ✅ **`SKILL.md` rules 15/16 added**: Self-contained refactor + SkillHub direct HTTP API description
- ✅ **`SKILL.md` troubleshooting updated**: Removed "SkillHub CLI not found" entry; added "SkillHub HTTP API failure" and "lark-cli not found (v1.5.0 refactor)" entries
- ✅ **`SKILL.md` permission declaration updated**: subprocess marked as "optional"; new "Third-party Python packages ❌" row added
- ✅ **`README.md` / `README.en.md` prerequisites updated**: Removed required `skillhub` CLI / `lark-cli` declarations; lark-cli is now optional

### v1.4.0 (2026-07-19)

**Privacy boundary hardening round 2 (zero derived content)** (fixes ClawHub LLM audit round 2 "publishes context-derived keywords despite promising aggregate-only boundary" suspicious flag):

- ✅ **Completely removed Top 10 keyword list from derived report**: `daily_recommend.py` report markdown no longer publishes keyword list in "User Context Snapshot" section (v1.3.0 only removed project names but kept Top 10 keywords; LLM audit still flagged them as "derived keywords")
- ✅ **Report publishes aggregate counts only**: Only 4 numbers kept (keyword count / project count / experience file count / installed skill count); no derived content published
- ✅ **SKILL.md description upgraded to "zero context-derived content"**: Explicitly states "derived reports publish zero context-derived content, only aggregate counts"
- ✅ **SKILL.md rule 13 upgraded to v1.4.0 wording**: Forbids publishing any context-derived content (including Top 10 keyword list, project names, experience file names, installed skill list)
- ✅ **SKILL.md / README.md user notice upgraded to v1.4.0 privacy boundary**

### v1.3.0 (2026-07-19)

**Privacy boundary hardening** (fixes ClawHub LLM audit "broadly scans local context + publishes derived context" suspicious flag):

- ✅ **Derived reports publish aggregate stats only**: `daily_recommend.py` report markdown removes raw `active_projects[:5]` project names from "User Context Snapshot" section; only counts are kept; experience files / installed skills also count-only
- ✅ **Added `--no-context-scan` flag**: Executor supports completely skipping TRAE memory / project files / experience backups / installed skills scanning; recommendations degrade to trending-only (no memory_collision / scene_match dimensions)
- ✅ **Privacy notice added to report**: Explicitly states "raw scan results remain in local `data/user_context_{date}.json`, not pushed to external services"
- ✅ **SKILL.md description strengthened**: Explicitly discloses "derived reports publish aggregate stats only (counts + filtered Top 10 keywords); raw scan results remain local"
- ✅ **SKILL.md rules 13/14 added**: Derived reports publish aggregate stats only / context scanning can be skipped

### v1.2.0 (2026-07-19)

**Security compliance hardening** (fixes 7 ClawHub SkillSpector CRITICAL findings):

- ✅ Implemented `--no-obsidian` / `--no-feishu` / `--no-ima` / `--dry-run` CLI flags (previously documented but not implemented — instruction_scope finding)
- ✅ Changed `push_to_feishu.py` `subprocess.run` from `shell=True` string command to argv list (AST4/OH1 finding)
- ✅ Tightened SKILL.md description trigger phrases, removed generic phrases like "跑一下全球 skill 推荐" (SQP-1 finding)
- ✅ Added `SENSITIVE_KEYWORD_BLOCKLIST` to `scan_user_context.py` to filter sensitive keywords, output marked with `redaction_applied: true` (SSD3/SQP-2 finding)
- ✅ Removed hardcoded `DEFAULT_KB_ID` from `push_to_ima.py`, now requires `IMA_KB_ID` env var (environment_proportionality finding)
- ✅ Enhanced `fetch_skillhub.py` with `shutil.which` absolute path resolution to avoid PATH trust boundary issues (TT2/TM1 finding)
- ✅ Credentials read from env vars only; on stale env var, prompt user to restart TRAE session instead of reading OS persistent storage

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
