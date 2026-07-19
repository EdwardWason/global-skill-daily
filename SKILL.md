---
name: "global-skill-daily"
slug: "global-skill-daily"
displayName: "Global Skill Daily"
description: "每 3 天扫描全球两大 Skill 平台（ClawHub 500 + SkillHub 7.5万）合并去重，基于用户当前 agent 上下文（memory/topics/profile + 项目文件 + 经验备份 + 已装 skill）做 10 维度推荐（3 组轮换：趋势/质量/用户），生成含跨平台生态洞察（5 章节）的全球 Skill 生态日报并三处存放推送（Obsidian + IMA FIM + 飞书 Card 2.0 在线 docx）。14 天跨维度去重避免多日推荐重合。当用户说「全球 skill 日报」「global skill daily」「跑一下全球 skill 推荐」时触发。Do NOT use for 发布新 skill / 修改已装 skill / skill 安全审计 / 本地 skill 生态分析 / 被动 skill 发现。"
version: "1.1.0"
license: "MIT-0"
summary: "合并 ClawHub Daily + SkillHub Daily 的全球 Skill 生态日报，v1.1 强化跨平台洞察 + 维度轮换 + 14 天去重。"
allowed-tools: "Read, Write, Edit, Glob, Grep, RunCommand"
metadata:
  openclaw:
    skillKey: "global-skill-daily"
    emoji: "🌐"
    homepage: "https://github.com/trae-solo/global-skill-daily"
    os: ["windows", "macos", "linux"]
    requires:
      bins: ["python", "skillhub"]
      env: ["FEISHU_APP_ID", "FEISHU_APP_SECRET", "FEISHU_USER_OPEN_ID", "IMA_OPENAPI_CLIENTID", "IMA_OPENAPI_APIKEY"]
    primaryEnv: "FEISHU_APP_ID"
    envVars:
      - name: "FEISHU_APP_ID"
        description: "飞书应用 App ID"
        required: true
      - name: "FEISHU_APP_SECRET"
        description: "飞书应用 App Secret"
        required: true
      - name: "FEISHU_USER_OPEN_ID"
        description: "接收卡片消息的用户 open_id"
        required: true
      - name: "IMA_OPENAPI_CLIENTID"
        description: "IMA OpenAPI Client ID"
        required: true
      - name: "IMA_OPENAPI_APIKEY"
        description: "IMA OpenAPI API Key"
        required: true
      - name: "OBSIDIAN_VAULT_PATH"
        description: "Obsidian vault 路径（默认 E:\\Obsidian-Vault\\00-Inbox）"
        required: false
    always: false
---

# 🌐 Global Skill Daily

> 每 3 天扫描全球两大 Skill 平台，基于用户当前 agent 上下文做精准推荐，展现中英文生态全貌。

## 任务

每 3 天 06:30 自动执行（或用户手动触发），完成以下管线：

1. **抓取**：ClawHub Convex API（500 个）+ SkillHub CLI（7 排行榜 + 11 分类 + 6 记忆关键词，去重后 ~550 个）
2. **统一 schema**：`normalize.py` 将两源数据归一化为统一格式，标记 `source = clawhub / skillhub / both`
3. **用户上下文扫描**：`scan_user_context.py` 扫描 TRAE memory（project_memory×3 + topics×2 + user_profile×1）+ 项目活跃文件 + 经验备份 + 已装 skill 清单，提取关键词集合
4. **10 维度推荐（v1.1 维度轮换）**：`daily_recommend.py` 根据日期选择 3 组之一（A 趋势 / B 质量 / C 用户），出 7-12 个推荐
5. **跨平台生态洞察（v1.1 核心）**：5 章节分析 — 热度差异榜 / 双榜共有 gap>5x / 品类偏好对比 / 中文平台特色 skill
6. **简报生成**：生成 markdown 简报（篇幅不限，趋势/热点/聚焦领域充分展开）
7. **三处存放**：Obsidian（vault）+ IMA FIM 知识库 + 飞书云文档（在线 docx，可点击查看）+ Card 2.0 卡片消息

## 输出格式

### 简报结构（markdown）

```
# 🌐 全球 Skill 生态日报 | {date}

## TL;DR
- 双榜扫描：ClawHub 500 + SkillHub 7.5万 → 合并去重后 N 个独立 skill
- 今日推荐 7-12 个（按维度组），跨平台对比 X 个
- 跳过 14 天去重 Y 个（v1.1 升级）
- 今日维度组：趋势组 / 质量组 / 用户组（3 天 1 周期）

## 👤 用户上下文快照
- 今日扫描关键词：[列表]
- 活跃项目：[列表]
- 经验命中：[列表]

## 🌏 跨平台生态洞察（v1.1 核心特色）
### 🎯 数据洞察
### 📊 A. 热度差异榜 — 国内独火 Top 5
### 📊 B. 热度差异榜 — 全球独火 Top 5
### 🔄 C. 双榜共有但热度差 >5x — 中英文开发者偏好分化
### 🏷️ D. 中英文开发者品类偏好对比
### 🇨🇳 E. 中文平台特色 skill（bilibili/douyin/wechat 等）

## 📊 跨平台趋势速览
- 双榜共有 Top 3

## 🔥 今日推荐（按维度组）
### 🔥 trending_both × N  / ⭐ quality × N  / 🚀 newcomers × N
### 🇨🇳 china_only × N  / 🌍 global_only × N  / 👤 active_developer × N
### 🧠 memory_collision × N  / 🎯 scene_match × N  / 🛡️ verified × N  / 🏆 panorama × N

## 📌 数据说明
- ClawHub API v4 / SkillHub CLI / 抓取耗时 / 推荐算法版本
- 去重窗口：14 天跨维度去重（v1.1）
- 维度轮换：10 维度分 3 组，每 3 天 1 周期（v1.1）
```

### 三处存放路径

| 渠道 | 路径 |
|------|------|
| Obsidian | `E:\Obsidian-Vault\00-Inbox\global-skill-daily_{date}.md` |
| IMA FIM | `kb_id=aFEGG-4YH3z_CaCSNVNC5dSJR5cutjlatcEQcNZjtlA=` |
| 飞书云文档 | `lark-cli drive +import --type docx` 用户身份（在线 docx，可点击查看） |
| 飞书卡片 | Card 2.0 schema，`template=green`，标题含具体数字，按钮链接到在线 docx |

## 规则

1. **用户上下文扫描是前置依赖**，不是普通维度。没有这个，找 skill 就是抓瞎。
2. **跨平台对比是独占价值**：`china_only` / `global_only` / `trending_both` 三个维度只能在合并后实现，单独跑永远做不到。
3. **去重窗口 14 天（v1.1）**：跨维度去重，slug 优先精确匹配，回退 fuzzy（去掉 `-cn`/`-zh` 后缀）。配合每 3 天 1 次频率可覆盖 4-5 次历史推荐。
4. **维度轮换（v1.1）**：10 维度分 3 组（A 趋势 / B 质量 / C 用户），每 3 天 1 周期，避免每次推荐角度雷同。日期 → 组映射：`(days_offset // 3) % 3`。
5. **跨平台生态洞察是核心特色（v1.1）**：5 章节分析（热度差异榜 / 双榜共有 gap>5x / 品类偏好对比 / 中文平台特色 skill），不算"可选模块"，必须充分展开。
6. **三处存放失败隔离**：每个渠道独立 try/except，一处失败不阻断其他。
7. **凭证优先级**：CLI 参数 > 环境变量（必要时读 Windows registry 绕过 TRAE session 缓存）> `references/config.json`。
8. **报告篇幅不限制**：趋势/热点/聚焦领域充分展开，避免信息密度过低。
9. **飞书卡片用 Card 2.0**：`schema=2.0`，`markdown` 元素（非旧版 `lark_md`），按钮 `behaviors`，标题含具体数字（如 `20260719-全球Skill日报-推荐7个-跨平台6个`）。
10. **飞书存储用 `+import --type docx`（v1.1 修复）**：将 .md 转为在线 docx 文档，用户点击按钮可直接查看内容。**禁止用 `+upload`**（只存原文件，点击只能下载，用户无法在线查看）。

## 示例

### 触发示例

```
用户：跑一下全球 skill 日报
用户：global skill daily
用户：今天的 skill 推荐跑一下
```

### cron 触发命令

```bash
cd "d:/TRAE SOLO CN/project" && python global-skill-daily/global_skill_daily_executor.py
```

### 输出示例（摘要）

```
🌐 全球 Skill 生态日报 | 2026-07-19

TL;DR
- 双榜扫描：ClawHub 492 + SkillHub 555 → 合并去重后 936 个独立 skill
- 今日推荐 7 个，跨平台对比 6 个
- 跳过 14 天去重 10 个（v1.1）
- 今日维度组：趋势组（聚焦双榜热度与跨平台差异）

🌏 跨平台生态洞察
- 发现 30 个双榜共有但热度差 >5x 的 skill，反映中英文开发者偏好分化
- 国内独火 skill 集中在「office-efficiency」品类（23 个）
- 全球独火 skill 集中在「integrations」品类（77 个）
- 识别出 77 个中文平台特色 skill（bilibili/douyin/wechat 等）

📊 A. 热度差异榜 — 国内独火 Top 5
| Skill | SkillHub 安装 | ClawHub 安装 | 差距倍数 |
| Find Skills | 75,956 | 0 | ∞ |
| Agent Memory | 25,555 | 1,014 | 25.2x |

🔥 今日推荐（趋势组）
1. 🔥 trending_both × 2: ontology, Proactive Agent
2. 🇨🇳 china_only × 2: Summarize, Agent Browser
3. 🌍 global_only × 2: Multi Search Engine, PollyReach
4. 🏆 panorama × 1: Free Ride
```

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| ClawHub API 限流（429） | 已内置退避 5s × 3 重试 |
| SkillHub CLI 找不到 | 检查 PATH 或设置 `SKILLHUB_BIN` 环境变量 |
| 飞书 token 失效 | 重启 TRAE session 或读 registry |
| IMA 笔记标题重复 | 已 strip YAML frontmatter |
| Obsidian 写入 PermissionError | 三级 fallback：重试 → ASCII 文件名 → saved/ |
| 卡片 Markdown 不渲染 | 已用 Card 2.0 `markdown` 元素，非 `lark_md` |
| 按钮点击只能下载不能查看（v1.1 修复） | 已从 `+upload` 切换到 `+import --type docx`，转为在线 docx 可点击查看 |
| JSON 含 `Infinity` 非标准（v1.1 修复） | `gap_ratio` 为 inf 时写 null，markdown 显示为 `∞` |

## 权限声明

| 能力类别 | 是否使用 | 说明 |
|---------|---------|------|
| 网络访问 | ✅ | ClawHub API（抓取 skill）+ SkillHub API（抓取 skill）+ IMA API（推送笔记到知识库）+ 飞书 OpenAPI（推送卡片）|
| 文件读写 | ✅ | 读：TRAE memory + 项目文件 + 经验备份 + 已装 skill 清单。写：Obsidian vault（`E:\Obsidian-Vault\00-Inbox\`）+ 项目 `data/` 目录 |
| 环境变量 | ✅ | `FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_USER_OPEN_ID` / `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY` / `OBSIDIAN_VAULT_PATH` |
| subprocess | ✅ | `lark-cli drive +import --type docx`（推送云文档）+ `skillhub` CLI（抓取排行榜）|
| 外部 API | ✅ | ClawHub Convex API v4 + SkillHub OpenAPI + IMA OpenAPI + 飞书 OpenAPI |

### 用户须知（副作用声明）

⚠️ 本技能作为定时任务运行时会自动执行以下副作用：
- 自动写入外部服务：Obsidian vault / IMA FIM 知识库 / 飞书云盘 / 飞书 IM 卡片消息
- 自动读取本地数据：TRAE memory 目录（project_memory + topics + user_profile）+ 项目文件 + 经验备份 + 已装 skill 清单
- 自动创建文件：项目 `data/recommended/{date}.json` 和 `{date}.md` + Obsidian `00-Inbox/global-skill-daily_{date}.md`

**如何禁用副作用**：手动运行时可加 `--no-obsidian` / `--no-feishu` / `--no-ima` 参数跳过对应渠道
