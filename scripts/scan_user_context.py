"""
scan_user_context.py — 强化版用户上下文扫描（前置依赖，不是普通维度）

扫描 4 个来源：
  1. TRAE memory（3 级权重）
     - project_memory.md × 3
     - 最近 1 天 topics.md × 2
     - user_profile.md × 1
  2. 项目活跃文件（最近 7 天修改过的子目录）
     - 提取目录名作为关键词
  3. 经验备份（docs/knowledge/ 下的 patterns/pitfalls/technical-decisions）
     - 提取文件名作为关键词
  4. 已安装 skill 清单（~/.trae-cn/skills/ 下目录）

输出：
  data/user_context_{date}.json
    {
      "scan_date": "YYYY-MM-DD",
      "keywords": [
        {"word": "python", "weight": 9, "sources": ["project_memory×3", "topics×2", "user_profile×1", "active_projects"]},
        ...
      ],
      "active_projects": ["clawhub-daily", "skillhub-cn-daily", ...],
      "experience_files": ["2026-07-17-clawhub-publish-phantom-success.md", ...],
      "installed_skills": ["clawhub-daily", "skillhub-cn-daily", ...],
      "memory_summary": {
        "project_memory_words": N,
        "topics_words": N,
        "user_profile_words": N,
      }
    }
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


# 技术关键词词典（用于从 memory 中提取）
TECH_KEYWORDS = {
    # 编程语言
    "python", "javascript", "typescript", "java", "go", "rust", "c++", "c#", "ruby",
    # 框架/库
    "react", "vue", "angular", "nextjs", "django", "flask", "fastapi", "express",
    "node", "deno", "bun",
    # 工具
    "docker", "kubernetes", "git", "github", "gitlab", "vscode", "vim", "emacs",
    # AI/LLM
    "openai", "anthropic", "claude", "gpt", "gemini", "llm", "rag", "embedding",
    "agent", "mcp", "prompt", "fine-tuning", "llama", "mistral",
    # 数据
    "pandas", "numpy", "matplotlib", "plotly", "jupyter", "spark", "airflow",
    # 飞书/国内
    "feishu", "lark", "dingtalk", "wechat", "weixin", "xiaohongshu", "douyin", "bilibili",
    # 平台
    "clawhub", "skillhub", "openclaw", "trae",
    # 文档/内容
    "markdown", "html", "css", "pdf", "word", "excel", "ppt",
    # 业务
    "audit", "tax", "finance", "accounting", "treasury",
    "ocr", "nlp", "sentiment", "classification",
    "webhook", "api", "rest", "graphql", "grpc",
    "cron", "scheduler", "automation",
    "obsidian", "notion",
    # 中文关键词
    "飞书", "微信", "钉钉", "小红书", "抖音", "B站",
    "审计", "税务", "财务", "会计", "券商", "投行",
    "公众号", "图文", "视频", "转录",
    "技能", "日报", "周报", "月报",
}


def _extract_keywords(text: str, weight: int, source_name: str, counter: dict, source_map: dict) -> int:
    """从文本中提取关键词，按权重累加。返回提取的关键词数量。"""
    if not text:
        return 0

    text_lower = text.lower()
    found = 0

    # 英文关键词：词边界匹配
    for kw in TECH_KEYWORDS:
        if re.match(r"^[a-z]", kw):
            # 英文：词边界
            pattern = r"\b" + re.escape(kw) + r"\b"
            matches = re.findall(pattern, text_lower)
            if matches:
                counter[kw] += weight * len(matches)
                if kw not in source_map:
                    source_map[kw] = []
                source_map[kw].append(f"{source_name}×{weight}")
                found += len(matches)
        else:
            # 中文：直接子串
            count = text_lower.count(kw)
            if count > 0:
                counter[kw] += weight * count
                if kw not in source_map:
                    source_map[kw] = []
                source_map[kw].append(f"{source_name}×{weight}")
                found += count

    return found


def _scan_memory(memory_root: Path, project_dir: Path, counter: dict, source_map: dict) -> dict:
    """扫描 TRAE memory，3 级权重。"""
    summary = {"project_memory_words": 0, "topics_words": 0, "user_profile_words": 0}

    # 1. project_memory.md × 3
    pm = memory_root / "projects" / "-d-TRAE-SOLO-CN-project" / "project_memory.md"
    if pm.exists():
        text = pm.read_text(encoding="utf-8")
        summary["project_memory_words"] = _extract_keywords(text, 3, "project_memory", counter, source_map)

    # 2. 最近 1 天 topics.md × 2
    today = datetime.now().strftime("%Y%m%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    for date_str in [today, yesterday]:
        topics = memory_root / "projects" / "-d-TRAE-SOLO-CN-project" / date_str / "topics.md"
        if topics.exists():
            text = topics.read_text(encoding="utf-8")
            summary["topics_words"] += _extract_keywords(text, 2, "topics", counter, source_map)

    # 3. user_profile.md × 1
    up = memory_root / "user_profile.md"
    if up.exists():
        text = up.read_text(encoding="utf-8")
        summary["user_profile_words"] = _extract_keywords(text, 1, "user_profile", counter, source_map)

    return summary


def _scan_active_projects(project_dir: Path, days: int = 7) -> tuple[list[str], dict, dict]:
    """扫描项目目录下最近 N 天修改过的子目录。"""
    cutoff = datetime.now() - timedelta(days=days)
    active = []
    counter: dict = defaultdict(int)
    source_map: dict = defaultdict(list)

    if not project_dir.exists():
        return active, counter, source_map

    for item in project_dir.iterdir():
        if not item.is_dir():
            continue
        if item.name.startswith(".") or item.name in {"docs", "data", "node_modules", "__pycache__"}:
            continue
        # 检查目录的最近修改时间
        try:
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            if mtime >= cutoff:
                active.append(item.name)
                # 目录名作为关键词（拆分为单词）
                parts = re.split(r"[-_]", item.name.lower())
                for p in parts:
                    if len(p) >= 3 and p.isalpha():
                        counter[p] += 2
                        source_map[p].append("active_projects×2")
        except OSError:
            continue

    return active, counter, source_map


def _scan_experience(project_dir: Path, counter: dict, source_map: dict) -> list[str]:
    """扫描 docs/knowledge/ 下的经验文件。"""
    files = []
    knowledge_root = project_dir / "docs" / "knowledge"
    if not knowledge_root.exists():
        return files

    for sub in ["patterns", "pitfalls", "technical-decisions"]:
        sub_dir = knowledge_root / sub
        if not sub_dir.exists():
            continue
        for f in sub_dir.glob("*.md"):
            files.append(f.name)
            # 文件名作为关键词
            stem = f.stem.lower()
            # 去日期前缀
            stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
            parts = re.split(r"[-_]", stem)
            for p in parts:
                if len(p) >= 3 and p.isalpha():
                    counter[p] += 1
                    source_map[p].append(f"experience:{sub}×1")
            # 文件内容也扫一遍
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                _extract_keywords(text, 1, f"experience:{sub}", counter, source_map)
            except OSError:
                pass

    return files


def _scan_installed_skills(home: Path) -> list[str]:
    """扫描已安装 skill 清单。"""
    skills_dir = home / ".trae-cn" / "skills"
    if not skills_dir.exists():
        return []
    return sorted([d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith(".")])


def scan(memory_root: Path, project_dir: Path, output_path: Path, home: Path | None = None) -> dict:
    """执行完整扫描。"""
    home = home or Path.home()

    counter: dict = defaultdict(int)
    source_map: dict = defaultdict(list)

    # 1. TRAE memory
    memory_summary = _scan_memory(memory_root, project_dir, counter, source_map)

    # 2. 项目活跃文件
    active_projects, proj_counter, proj_source_map = _scan_active_projects(project_dir)
    for k, v in proj_counter.items():
        counter[k] += v
    for k, v in proj_source_map.items():
        source_map[k].extend(v)

    # 3. 经验备份
    experience_files = _scan_experience(project_dir, counter, source_map)

    # 4. 已安装 skill
    installed_skills = _scan_installed_skills(home)
    for skill in installed_skills:
        parts = re.split(r"[-_]", skill.lower())
        for p in parts:
            if len(p) >= 3 and p.isalpha():
                counter[p] += 2
                source_map[p].append("installed_skills×2")

    # 输出关键词列表（按权重降序）
    keywords = [
        {
            "word": w,
            "weight": c,
            "sources": sorted(set(source_map.get(w, []))),
        }
        for w, c in sorted(counter.items(), key=lambda x: -x[1])
        if c >= 2  # 至少 2 权重才入选
    ]

    result = {
        "scan_date": datetime.now().strftime("%Y-%m-%d"),
        "scanned_at": datetime.now(tz=timezone.utc).isoformat(),
        "keywords": keywords,
        "keywords_top20": [k["word"] for k in keywords[:20]],
        "active_projects": active_projects,
        "experience_files": experience_files,
        "installed_skills": installed_skills,
        "memory_summary": memory_summary,
        "total_unique_keywords": len(keywords),
    }

    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Scan user context for global-skill-daily")
    parser.add_argument("--memory-root", default=r"c:\Users\Administrator\.trae-cn\memory",
                        help="TRAE memory root path")
    parser.add_argument("--project-dir", default=r"d:\TRAE SOLO CN\project",
                        help="Project working directory")
    parser.add_argument("--output", default=None,
                        help="Output JSON path (default: data/user_context_{date}.json)")
    args = parser.parse_args()

    memory_root = Path(args.memory_root)
    project_dir = Path(args.project_dir)
    date_str = datetime.now().strftime("%Y-%m-%d")

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(__file__).parent.parent / "data" / f"user_context_{date_str}.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    result = scan(memory_root, project_dir, output_path)

    print(f"[scan_user_context] scanned: keywords={result['total_unique_keywords']}, "
          f"active_projects={len(result['active_projects'])}, "
          f"experience_files={len(result['experience_files'])}, "
          f"installed_skills={len(result['installed_skills'])}")
    print(f"[scan_user_context] top 10 keywords: {result['keywords_top20'][:10]}")
    print(f"[scan_user_context] output: {output_path}")


if __name__ == "__main__":
    main()
