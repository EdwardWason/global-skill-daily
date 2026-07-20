# 🌐 Global Skill Daily | 全球 Skill 生态日报

![version](https://img.shields.io/badge/版本-1.5.0-green)
![license](https://img.shields.io/badge/license-MIT--0-blue)
![platform](https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![deps](https://img.shields.io/badge/依赖-Python%20标准库-success)

> 每 3 天扫描全球两大 Skill 平台（ClawHub 500 + SkillHub 7.5万），合并去重 936+ skill，基于用户当前 agent 上下文做 10 维度推荐（3 组轮换：趋势/质量/用户），生成含跨平台生态洞察的全球 Skill 生态日报并三处存放推送。v1.5.0 自依赖改造：仅依赖 Python 标准库，无需第三方包或外部 CLI。

## ✨ 核心特性

- **🌐 跨平台独占视角**：合并 ClawHub + SkillHub，独占 china_only / global_only / trending_both 三个对比维度
- **🔄 维度轮换机制**：10 维度分 3 组（A 趋势 / B 质量 / C 用户），每 3 天 1 周期，避免推荐雷同
- **🌏 跨平台生态洞察（5 章节）**：热度差异榜 / 双榜共有 gap>5x / 品类偏好对比 / 中文平台特色 skill
- **📅 14 天跨维度去重**：配合每 3 天 1 次频率，覆盖 4-5 次历史推荐
- **🧠 用户上下文深度扫描**：TRAE memory（3 级权重）+ 项目活跃文件 + 经验备份 + 已装 skill 清单
- **📁 三处存放**：Obsidian vault + IMA FIM 知识库 + 飞书云文档（可选 lark-cli，不可用时降级为仅卡片）+ Card 2.0 卡片消息
- **🔒 v1.5.0 自依赖改造**：仅依赖 Python 标准库（urllib/json/re/sys/os/pathlib/datetime/collections），无需 `pip install` 任何第三方包，无需安装 `skillhub` CLI / `lark-cli`（lark-cli 改为可选）

## 📦 安装

### 前置依赖

- Python 3.10+（仅依赖 Python 标准库，无需 pip 安装任何包）

#### 可选依赖（用于增强功能）

- [lark-cli](https://www.npmjs.com/package/@larksuite/cli)（可选，用于推送飞书云文档；不可用时自动降级为仅卡片消息）
- ~~[skillhub CLI](https://skillhub.cn)~~（v1.5.0 起不再需要，改为直连 SkillHub HTTP API）

### 环境变量

```bash
FEISHU_APP_ID=<your_app_id>
FEISHU_APP_SECRET=<your_app_secret>
FEISHU_USER_OPEN_ID=<your_user_open_id>
IMA_OPENAPI_CLIENTID=<your_ima_client_id>
IMA_OPENAPI_APIKEY=<your_ima_api_key>
IMA_KB_ID=<your_ima_kb_id>  # v1.2.0 起必填
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

### 定时任务

cron 表达式：`30 6 */3 * *`（每 3 天 06:30 执行）

### 手动运行

```bash
cd "d:/TRAE SOLO CN/project"

# 完整运行（三处存放）
python global-skill-daily/global_skill_daily_executor.py

# v1.2.0 新增：跳过指定渠道
python global-skill-daily/global_skill_daily_executor.py --no-feishu --no-ima
python global-skill-daily/global_skill_daily_executor.py --no-obsidian

# v1.2.0 新增：dry-run（只跑前 5 步，不推送任何渠道）
python global-skill-daily/global_skill_daily_executor.py --dry-run

# v1.3.0 新增：隐私敏感场景跳过上下文扫描
python global-skill-daily/global_skill_daily_executor.py --no-context-scan
```

## ⚠️ 用户须知（副作用声明）

本技能作为定时任务运行时会自动执行以下副作用：

- **自动写入外部服务**：Obsidian vault / IMA FIM 知识库 / 飞书云盘 / 飞书 IM 卡片消息
- **自动读取本地数据**：TRAE memory 目录（project_memory + topics + user_profile）+ 项目文件 + 经验备份 + 已装 skill 清单
- **自动创建文件**：项目 `data/recommended/{date}.json` 和 `{date}.md` + Obsidian `00-Inbox/global-skill-daily_{date}.md`

**如何禁用副作用（v1.2.0 已实现）**：
- `--no-obsidian` 跳过 Obsidian 推送
- `--no-feishu` 跳过飞书云文档 + 卡片消息推送
- `--no-ima` 跳过 IMA FIM 知识库推送
- `--dry-run` 只跑前 5 步（抓取+合并+扫描+推荐），不推送任何渠道
- `--no-context-scan`（v1.3.0）跳过用户上下文扫描，推荐降级为 trending-only

**派生输出脱敏（v1.2.0）**：扫描用户上下文后输出的 keywords 已过滤敏感词（token/secret/password/apikey/credential 等），避免派生内容暴露凭证线索。

**v1.4.0 隐私边界强化（零派生内容发布）**：
- ✅ **派生报告零上下文派生内容**：报告 markdown 中「用户上下文快照」段只发布聚合计数（关键词数/项目数/经验文件数/已装 skill 数），不发布任何派生内容（连 Top 10 关键词列表也不发布）
- ❌ **不会发布原始清单**：项目名/经验文件名/已装 skill 列表/关键词列表仅存本地 `data/user_context_{date}.json`，不推送至外部服务
- 🔧 **完全跳过扫描**：`--no-context-scan` 完全跳过 TRAE memory / 项目文件 / 经验备份 / 已装 skill 扫描，推荐降级为 trending-only（无 memory_collision / scene_match 维度）

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

### v1.5.0 (2026-07-20)

**自依赖改造**（移除所有外部依赖，仅依赖 Python 标准库）：

- ✅ **`fetch_clawhub.py` 移除 `requests` 第三方包**：改用 Python 标准库 `urllib.request` + `urllib.error`，User-Agent 从 `clawhub-daily/1.0` 改为 `global-skill-daily/1.5.0`
- ✅ **`fetch_skillhub.py` 移除 `skillhub` CLI 二进制依赖**：改为直连 SkillHub HTTP API（`https://api.skillhub.cn/api/v1/showcase/{type}` 和 `/api/v1/search`），无需安装 skillhub CLI
- ✅ **`push_to_feishu.py` 中 `lark-cli` 改为可选依赖**：lark-cli 不可用时自动降级为仅卡片消息（卡片已含完整简报文本），不再阻断流程
- ✅ **`plugin.json` 依赖声明更新**：`bins` 从 `["python", "skillhub"]` 改为 `["python"]`，版本号到 1.5.0
- ✅ **`SKILL.md` 新增规则 15/16**：自依赖改造 + SkillHub 直连 HTTP API 说明
- ✅ **`SKILL.md` 故障排除更新**：移除「SkillHub CLI 找不到」条目，新增「SkillHub HTTP API 失败」「lark-cli 找不到（v1.5.0 改造）」条目
- ✅ **`SKILL.md` 权限声明更新**：subprocess 标记为「可选」，新增「第三方 Python 包 ❌」行
- ✅ **`README.md` / `README.en.md` 前置依赖更新**：移除 skillhub CLI / lark-cli 必需声明，lark-cli 改为可选

### v1.4.0 (2026-07-19)

**隐私边界再次强化（零派生内容发布）**（修复 ClawHub LLM audit 第二轮 "publishes context-derived keywords despite promising aggregate-only boundary" suspicious 标记）：

- ✅ **派生报告完全移除 Top 10 关键词列表**：`daily_recommend.py` 报告 markdown 中「用户上下文快照」段不再发布关键词列表（v1.3.0 仅移除项目名但保留 Top 10 关键词，LLM audit 仍标记为"派生关键词"）
- ✅ **报告只发布聚合计数**：仅保留 4 个数字（关键词数/项目数/经验文件数/已装 skill 数），不发布任何派生内容
- ✅ **SKILL.md description 升级为"零上下文派生内容"**：明确声明"派生报告零上下文派生内容，只发布聚合计数"
- ✅ **SKILL.md 规则 13 升级到 v1.4.0 措辞**：禁止发布任何上下文派生内容（含 Top 10 关键词列表、项目名、经验文件名、已装 skill 列表）
- ✅ **SKILL.md/README.md 用户须知升级为 v1.4.0 隐私边界**

### v1.3.0 (2026-07-19)

**隐私边界强化**（修复 ClawHub LLM audit "broadly scans local context + publishes derived context" suspicious 标记）：

- ✅ **派生报告只发布聚合统计量**：`daily_recommend.py` 报告 markdown 中「用户上下文快照」段移除原始 `active_projects[:5]` 项目名，只保留计数；经验文件/已装 skill 也只保留计数
- ✅ **新增 `--no-context-scan` flag**：主执行器支持完全跳过 TRAE memory / 项目文件 / 经验备份 / 已装 skill 扫描，推荐降级为 trending-only（无 memory_collision / scene_match 维度）
- ✅ **报告中增加隐私声明**：明确告知「原始扫描结果仅存本地 `data/user_context_{date}.json`，不推送至外部服务」
- ✅ **SKILL.md description 强化披露**：明确说明「派生报告只发布聚合统计量（计数+已过滤 Top 10 关键词），原始扫描结果仅存本地」
- ✅ **SKILL.md 新增规则 13/14**：派生报告只发布聚合统计量 / 上下文扫描可跳过

### v1.2.0 (2026-07-19)

**安全合规强化**（修复 ClawHub SkillSpector CRITICAL 7 项 finding）：

- ✅ 实现 `--no-obsidian` / `--no-feishu` / `--no-ima` / `--dry-run` 命令行参数（之前文档声明但代码未实现，instruction_scope finding）
- ✅ `push_to_feishu.py` 的 `subprocess.run` 从 `shell=True` 字符串命令改为 argv list（AST4/OH1 finding）
- ✅ SKILL.md description 精简触发词，删除"跑一下全球 skill 推荐"等宽泛短语（SQP-1 finding）
- ✅ `scan_user_context.py` 增加 `SENSITIVE_KEYWORD_BLOCKLIST` 过滤敏感关键词，派生输出标记 `redaction_applied: true`（SSD3/SQP-2 finding）
- ✅ `push_to_ima.py` 移除硬编码 `DEFAULT_KB_ID`，改为 `IMA_KB_ID` 环境变量必填（environment_proportionality finding）
- ✅ `fetch_skillhub.py` 增强 `shutil.which` 解析为绝对路径，避免 PATH 信任边界问题（TT2/TM1 finding）
- ✅ 凭证仅从环境变量读取，环境变量 stale 时提示用户重启 TRAE session，不读 OS 持久存储

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
