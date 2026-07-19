# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- 必要时读 Windows registry 绕过 TRAE session 缓存
