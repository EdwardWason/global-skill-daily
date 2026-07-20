# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-07-20

### Changed
- **`fetch_clawhub.py` 移除 `requests` 第三方包**：改用 Python 标准库 `urllib.request` + `urllib.error`。`call_list_public_page()` 函数从 `requests.post` 改为 `urllib.request.Request` + `urllib.request.urlopen`；异常处理从 `requests.exceptions.Timeout` 改为 `urllib.error.HTTPError` / `urllib.error.URLError`；User-Agent 从 `clawhub-daily/1.0` 改为 `global-skill-daily/1.5.0`
- **`fetch_skillhub.py` 移除 `skillhub` CLI 二进制依赖**：改为直连 SkillHub HTTP API。移除 `import shutil` / `import subprocess` / `import os` 和 `_SKILLHUB_RESOLVED` / `SKILLHUB_BIN` CLI 路径解析逻辑；移除 `run_cli()` 和 `parse_json_output()` 函数；新增 `_http_get_json()` 辅助函数；重写 `fetch_rankings()` / `fetch_category_search()` / `fetch_keyword_search()` 三个函数。API 端点：`GET https://api.skillhub.cn/api/v1/showcase/{type}`（6 种类型：hot/featured/newest/recommended/trending/paid）和 `GET https://api.skillhub.cn/api/v1/search?q={kw}&limit={n}`
- **`push_to_feishu.py` `lark-cli` 改为可选依赖**：lark-cli 不可用时自动降级为仅卡片消息（卡片已含完整简报文本），不再阻断流程。`push()` 函数在 `upload_to_drive_via_lark_cli` 失败时打印 v1.5.0 降级模式提示并继续发卡片
- **`plugin.json` 依赖声明更新**：`bins` 从 `["python", "skillhub"]` 改为 `["python"]`；版本号从 1.1.0 升到 1.5.0；`tags` 追加 `self-contained`；`triggers.keywords` 精简为 2 个核心触发词
- **`SKILL.md` description 升级**：明确声明 v1.5.0 自依赖改造，lark-cli 改为可选降级
- **`SKILL.md` 任务段更新**：Step 1 SkillHub CLI → SkillHub HTTP API；Step 7 飞书云文档标注「可选 lark-cli，不可用时降级为仅卡片」
- **`SKILL.md` 三处存放路径表更新**：飞书云文档行标注「v1.5.0 起 lark-cli 可选」；飞书卡片行标注「云文档不可用时按钮省略」
- **`SKILL.md` 规则段新增 15/16**：自依赖改造 + SkillHub 直连 HTTP API
- **`SKILL.md` 故障排除更新**：移除「SkillHub CLI 找不到」条目；新增「SkillHub HTTP API 失败（v1.5.0 改造）」「lark-cli 找不到（v1.5.0 改造）」条目
- **`SKILL.md` 权限声明更新**：subprocess 标记为「可选」；新增「第三方 Python 包 ❌」行
- **`README.md` / `README.en.md` 前置依赖更新**：移除 skillhub CLI / lark-cli 必需声明；lark-cli 改为可选；新增 `deps` badge 标注「Python 标准库」

### Removed
- **`fetch_clawhub.py` `import requests`**：第三方包依赖移除
- **`fetch_skillhub.py` CLI 调用逻辑**：`shutil.which("skillhub")` / `subprocess.run` / `SKILLHUB_BIN` / `_SKILLHUB_RESOLVED` / `run_cli()` / `parse_json_output()` 全部移除
- **`fetch_skillhub.py` `RANKING_TYPES` 中的 "all" 类型**：无对应 HTTP API 端点，从 7 个改为 6 个

### Added
- **`fetch_skillhub.py` `SKILLHUB_API_HOST` 和 `RANKING_ENDPOINTS` 常量**：直接 HTTP API 端点定义
- **`fetch_skillhub.py` `_http_get_json()` 辅助函数**：用 `urllib.request` 封装 GET 请求
- **`fetch_skillhub.py` `normalize_skill()` 新增 `displayName` fallback**：适配新 API 返回字段
- **`SKILL.md` 规则 15（自依赖改造）**：所有 Python 脚本仅依赖标准库，禁止 `pip install` 第三方包
- **`SKILL.md` 规则 16（SkillHub 直连 HTTP API）**：6 个排行榜类型说明

## [1.4.0] - 2026-07-19

### Changed
- **`daily_recommend.py` 报告 markdown 完全移除 Top 10 关键词列表**：「用户上下文快照」段不再发布任何关键词列表（v1.3.0 仅移除项目名但保留 Top 10 关键词，LLM audit 第二轮仍标记为"派生关键词"）
- **`daily_recommend.py` `_build_chinese_summary` 移除推荐理由中的关键词字面量**：当 `matched_memory` 有匹配时，推荐理由从「匹配你的 N 个上下文关键词（关键词1, 关键词2, 关键词3）」改为「匹配你的 N 个上下文关键词（关键词已脱敏，仅本地保留）」
- **`daily_recommend.py` `memory_match` 结构化字段移除 `matched_keywords`**：JSON 输出中 `memory_match.matched_keywords`（前 10 个关键词）改为 `memory_match.matched_count`（仅计数）
- **`daily_recommend.py` markdown 「记忆命中」行移除关键词字面量**：从「N 权重 — 关键词1, 关键词2...」改为「N 权重，匹配 M 个关键词（关键词已脱敏，仅本地保留）」
- **报告「用户上下文快照」段只发布 4 个聚合计数**：关键词数 / 项目数 / 经验文件数 / 已装 skill 数。不发布任何上下文派生内容
- **SKILL.md description 升级为"零上下文派生内容"**：明确声明「派生报告零上下文派生内容，只发布聚合计数」
- **SKILL.md 规则 13 升级到 v1.4.0 措辞**：禁止发布任何上下文派生内容（含 Top 10 关键词列表、项目名、经验文件名、已装 skill 列表）
- **SKILL.md / README.md / README.en.md 用户须知升级为 v1.4.0 隐私边界**

### Fixed
- **ClawHub LLM audit 第二轮 suspicious 标记**：v1.3.0 修复了第一轮 LLM audit 标记，但第二轮 LLM audit 仍标记 `suspicious`，原因是「publishes context-derived keywords to external services despite promising aggregate-only boundary」。v1.4.0 通过完全移除用户上下文关键词字面量修复——共 4 处泄露点：
  - 「用户上下文快照」段的 Top 10 关键词列表（v1.3.0 遗留）
  - 推荐理由（`_build_chinese_summary`）中的 `matched_memory[:3]` 字面量
  - JSON 结构化输出的 `memory_match.matched_keywords` 字段（前 10 个）
  - markdown「记忆命中」行的关键词列表（前 5 个）
  修复后「零上下文派生内容」承诺字面成立


## [1.3.0] - 2026-07-19

### Added
- **`--no-context-scan` CLI flag**：主执行器支持完全跳过用户上下文扫描（TRAE memory + 项目文件 + 经验备份 + 已装 skill），推荐降级为 trending-only。用于隐私敏感场景或调度器环境
- **报告中隐私声明段落**：明确告知「原始扫描结果仅存本地 `data/user_context_{date}.json`，不推送至外部服务」

### Changed
- **`daily_recommend.py` 报告 markdown 移除原始项目名**：「用户上下文快照」段不再发布 `active_projects[:5]` 项目名，只保留计数；经验文件/已装 skill 也只保留计数
- **SKILL.md description 强化隐私边界披露**：明确说明「派生报告只发布聚合统计量（计数+已过滤 Top 10 关键词），原始扫描结果仅存本地」
- **SKILL.md 新增规则 13/14**：派生报告只发布聚合统计量 / 上下文扫描可跳过
- **README.md / README.en.md 同步 v1.3.0 隐私边界说明**：用户须知段新增「v1.3.0 隐私边界强化」子段

### Fixed
- **ClawHub LLM audit suspicious 标记**：v1.2.0 修复了 7 项 SkillSpector CRITICAL finding，但 LLM audit 仍标记 `suspicious`，原因是「broadly scans local agent/project context and can regularly publish derived context to external services」。v1.3.0 通过以下措施修复：
  - 派生报告不再发布原始项目名/经验文件名/已装 skill 列表
  - 提供 `--no-context-scan` 完全跳过扫描
  - description 显式披露隐私边界

## [1.2.0] - 2026-07-19

### Added
- **`--no-obsidian` / `--no-feishu` / `--no-ima` / `--dry-run` CLI flags**：主执行器实现渠道开关参数（v1.1 文档已声明但代码未实现，被 SkillSpector 标记为 instruction_scope finding）
- **`SENSITIVE_KEYWORD_BLOCKLIST` 敏感词黑名单**：`scan_user_context.py` 输出 keywords 时过滤凭证/密钥相关词汇，派生输出标记 `redaction_applied: true`
- **`IMA_KB_ID` 环境变量必填校验**：未设置时返回失败并提示用户

### Changed
- **`push_to_feishu.py` subprocess 改为 argv list 模式**：移除 `shell=True` 字符串命令拼接，使用 `["lark-cli", "drive", "+import", ...]` argv list，避免 shell 注入风险（AST4/OH1 finding）
- **`push_to_ima.py` 移除硬编码 `DEFAULT_KB_ID`**：改为 `IMA_KB_ID` 环境变量必填，避免 environment_proportionality finding
- **`fetch_skillhub.py` 增强 `shutil.which` 解析**：强制将 SKILLHUB_BIN 解析为绝对路径，避免 PATH 信任边界问题（TT2/TM1 finding）
- **SKILL.md description 精简触发词**：删除「跑一下全球 skill 推荐」「每 3 天 skill 推荐」等宽泛短语，仅保留「全球 skill 日报」「global skill daily」两个核心触发词（SQP-1 finding）
- **凭证读取策略**：所有凭证仅从环境变量读取，环境变量 stale 时提示用户重启 TRAE session，不读 OS 持久存储（v5.17 SkillSpector 约束）

### Fixed
- **ClawHub SkillSpector CRITICAL 7 项 finding 全部修复**：
  - [instruction_scope] `--no-obsidian/--no-feishu/--no-ima` 文档声明但代码未实现 → 已实现
  - [AST4] `push_to_feishu.py` shell=True 命令构造风险 → 改为 argv list
  - [OH1] shell-string 命令构造应改为 argv-based → 已改
  - [SQP-1] 触发词过宽 → 精简到核心短语
  - [SSD-3] 派生输出含敏感关键词 → 加 BLOCKLIST 过滤
  - [SQP-2] 持久化派生内容=隐私问题 → 加 redaction
  - [environment_proportionality] 默认 kb_id 硬编码 → 改为环境变量必填
  - [TT2/TM1] CLI 参数约束不够 → shutil.which 绝对路径解析

## [1.1.0] - 2026-07-19

### Added
- **维度轮换机制**：10 维度分 3 组（A 趋势 / B 质量 / C 用户），每 3 天 1 周期，避免每次推荐角度雷同
- **跨平台生态洞察模块（5 章节）**：
  - A. 热度差异榜 — 国内独火 Top 5（SkillHub 高 / ClawHub 低）
  - B. 热度差异榜 — 全球独火 Top 5（ClawHub 高 / SkillHub 低）
  - C. 双榜共有但热度差 >5x — 中英文开发者偏好分化
  - D. 中英文开发者品类偏好对比
  - E. 中文平台特色 skill（bilibili/douyin/wechat 等）
- **卡片新增「跨平台生态洞察」区块**（yellow-50 亮点背景，展示 4 条 insights_summary）
- **卡片 TL;DR 新增维度组 + 去重窗口字段**
- **JSON 输出新增字段**：`dedup_window_days` / `dimension_group` / `dimension_group_name` / `dimension_group_desc` / `cross_platform_insights`

### Changed
- **频率从每日改为每 3 天**：cron `30 6 * * *` → `30 6 */3 * *`（用户反馈：每日扫描重复太多，意义不大）
- **去重窗口从 7 天延长到 14 天**：配合每 3 天 1 次频率可覆盖 4-5 次历史推荐
- **newcomers 维度过滤放宽**：年龄阈值 60→90 天，最低安装 10→5（避免候选不足）
- **verified 维度改用质量代理**：原 verified badge 全空，改用 `versions>=3 + stars>=30 + 非 suspicious`
- **飞书存储从 `+upload` 切换到 `+import --type docx`**：转为在线 docx 文档，用户点击按钮可直接查看内容

### Fixed
- **按钮点击不能查看问题**（用户反馈）：`+upload` 只存原文件（点击只能下载），改用 `+import --type docx` 转为在线 docx（点击可查看）
- **JSON 含 `Infinity` 非标准问题**：`gap_ratio` 为 inf 时写 null，markdown 显示为 `∞`，避免下游 JSON 解析失败

### User Feedback Addressed
- 用户反馈 #1（按钮不能查看）：✅ 修复（+upload → +import）
- 用户反馈 #2（频率与去重）：✅ 修复（每 3 天 + 14 天去重 + 维度轮换）
- 用户反馈 #3（跨平台对比太少）：✅ 修复（新增 5 章节洞察模块 + 卡片展示头条）

## [1.0.0] - 2026-07-19

### Added
- 合并 ClawHub Daily (v2.0.9) 和 SkillHub Daily (v7.0.1) 为单一技能
- 10 维度 12 个推荐引擎：trending_both / quality / newcomers / china_only / global_only / active_developer / memory_collision / scene_match / verified / panorama
- 用户上下文深度扫描：TRAE memory (3级权重) + 项目活跃文件 + 经验备份 + 已装 skill
- 跨平台对比独占维度：china_only / global_only / trending_both
- 统一 normalize 层：合并 ClawHub + SkillHub 数据为统一 schema
- 飞书 Card 2.0 卡片：schema=2.0，markdown 元素（替代旧版 lark_md），标题含具体数字
- 飞书存储用 lark-cli drive +upload 用户身份（替代 create_document 应用身份）
- 三处存放失败隔离 + Obsidian 三级 fallback

### Fixed
- 飞书卡片 Markdown 不渲染问题（升级到 Card 2.0 markdown 元素）
- 卡片标题无区分度问题（标题含具体数字）
- 飞书文档归属应用而非用户问题（改用 lark-cli drive +upload）
- 去重窗口文档不一致问题（统一 7 天）

### Security
- 凭证优先级：CLI 参数 > 环境变量 > references/config.json
- 凭证仅从环境变量读取，stale 时提示用户重启 TRAE session（v1.2.0 起强制）
