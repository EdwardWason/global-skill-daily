"""
global_skill_daily_executor.py — 主执行器

管线：
  1. fetch_clawhub.py    → data/snapshots/{date}.clawhub.json
  2. fetch_skillhub.py   → data/snapshots/{date}.skillhub.json
  3. normalize.py        → data/snapshots/{date}.merged.json
  4. scan_user_context.py → data/user_context_{date}.json
  5. daily_recommend.py  → data/recommended/{date}.json + .md
  6. push_to_obsidian.py → vault
  7. push_to_ima.py      → IMA FIM
  8. push_to_feishu.py   → 飞书云文档 + Card 2.0

三处存放失败隔离：每个推送独立 try/except。
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DATA_DIR = PROJECT_ROOT / "data"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
RECOMMENDED_DIR = DATA_DIR / "recommended"


def _run_step(name: str, cmd: list[str], cwd: Path | None = None) -> tuple[bool, str, float]:
    """运行一个步骤，返回 (success, output, elapsed_seconds)。"""
    print(f"\n{'='*60}")
    print(f"[STEP] {name}")
    print(f"[CMD]  {' '.join(cmd)}")
    print(f"{'='*60}")
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=600,
            encoding="utf-8", errors="replace",
            cwd=str(cwd) if cwd else None,
        )
        elapsed = time.time() - start
        output = result.stdout + ("\n" + result.stderr if result.stderr else "")
        if result.returncode == 0:
            print(f"[OK] {name} ({elapsed:.1f}s)")
            if output.strip():
                print(output[-1500:])
            return True, output, elapsed
        else:
            print(f"[FAIL] {name} returncode={result.returncode} ({elapsed:.1f}s)")
            print(output[-2000:])
            return False, output, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"[FAIL] {name} timeout ({elapsed:.1f}s)")
        return False, "timeout", elapsed
    except (OSError, FileNotFoundError) as e:
        elapsed = time.time() - start
        print(f"[FAIL] {name} exception: {e}")
        return False, str(e), elapsed


def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    start_time = time.time()

    print(f"🌐 Global Skill Daily Executor — {date_str}")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")

    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    RECOMMENDED_DIR.mkdir(parents=True, exist_ok=True)

    python = sys.executable
    report = {
        "date": date_str,
        "started_at": datetime.now().isoformat(),
        "steps": [],
        "push_results": {},
    }

    # Step 1: fetch_clawhub
    clawhub_output = SNAPSHOTS_DIR / f"{date_str}.clawhub.json"
    ok, out, t = _run_step(
        "fetch_clawhub",
        [python, str(SCRIPTS_DIR / "fetch_clawhub.py"), "--num", "500", "--date", date_str, "--output", str(SNAPSHOTS_DIR)]
    )
    report["steps"].append({"step": "fetch_clawhub", "ok": ok, "elapsed": t})

    # Step 2: fetch_skillhub
    skillhub_output = SNAPSHOTS_DIR / f"{date_str}.skillhub.json"
    ok2, out2, t2 = _run_step(
        "fetch_skillhub",
        [python, str(SCRIPTS_DIR / "fetch_skillhub.py"), "--output", str(SNAPSHOTS_DIR)]
    )
    report["steps"].append({"step": "fetch_skillhub", "ok": ok2, "elapsed": t2})

    # Step 3: normalize
    merged_output = SNAPSHOTS_DIR / f"{date_str}.merged.json"
    ok3, out3, t3 = _run_step(
        "normalize",
        [python, str(SCRIPTS_DIR / "normalize.py"), str(clawhub_output), str(skillhub_output), str(merged_output)]
    )
    report["steps"].append({"step": "normalize", "ok": ok3, "elapsed": t3})

    # Step 4: scan_user_context
    context_output = DATA_DIR / f"user_context_{date_str}.json"
    ok4, out4, t4 = _run_step(
        "scan_user_context",
        [python, str(SCRIPTS_DIR / "scan_user_context.py"), "--output", str(context_output)]
    )
    report["steps"].append({"step": "scan_user_context", "ok": ok4, "elapsed": t4})

    # Step 5: daily_recommend
    recommend_json = RECOMMENDED_DIR / f"{date_str}.json"
    recommend_md = RECOMMENDED_DIR / f"{date_str}.md"
    ok5, out5, t5 = _run_step(
        "daily_recommend",
        [python, str(SCRIPTS_DIR / "daily_recommend.py"), str(merged_output), str(context_output), str(RECOMMENDED_DIR)]
    )
    report["steps"].append({"step": "daily_recommend", "ok": ok5, "elapsed": t5})

    # Step 6-8: 三处存放（失败隔离）
    print(f"\n{'='*60}")
    print("[STEP] 三处存放推送（失败隔离）")
    print(f"{'='*60}")

    # 6. push_to_obsidian
    try:
        ok6, out6, t6 = _run_step(
            "push_to_obsidian",
            [python, str(SCRIPTS_DIR / "push_to_obsidian.py"), str(recommend_md), date_str]
        )
        report["push_results"]["obsidian"] = {"ok": ok6, "elapsed": t6, "output": out6[-500:]}
    except Exception as e:
        report["push_results"]["obsidian"] = {"ok": False, "error": str(e)}

    # 7. push_to_ima
    try:
        ok7, out7, t7 = _run_step(
            "push_to_ima",
            [python, str(SCRIPTS_DIR / "push_to_ima.py"), str(recommend_md), date_str]
        )
        report["push_results"]["ima"] = {"ok": ok7, "elapsed": t7, "output": out7[-500:]}
    except Exception as e:
        report["push_results"]["ima"] = {"ok": False, "error": str(e)}

    # 8. push_to_feishu
    try:
        ok8, out8, t8 = _run_step(
            "push_to_feishu",
            [python, str(SCRIPTS_DIR / "push_to_feishu.py"), str(recommend_json), str(recommend_md), date_str]
        )
        report["push_results"]["feishu"] = {"ok": ok8, "elapsed": t8, "output": out8[-500:]}
    except Exception as e:
        report["push_results"]["feishu"] = {"ok": False, "error": str(e)}

    # 总结报告
    elapsed_total = time.time() - start_time
    report["elapsed_total"] = elapsed_total
    report["finished_at"] = datetime.now().isoformat()

    print(f"\n{'='*60}")
    print(f"[DONE] Global Skill Daily — {date_str}")
    print(f"[TIME] Total: {elapsed_total:.1f}s")
    print(f"{'='*60}")

    print("\n📊 执行摘要:")
    for step in report["steps"]:
        status = "✓" if step["ok"] else "✗"
        print(f"  {status} {step['step']:25s} {step['elapsed']:.1f}s")

    print("\n📤 三处存放:")
    for channel, res in report["push_results"].items():
        status = "✓" if res.get("ok") else "✗"
        print(f"  {status} {channel:10s} {res.get('elapsed', 0):.1f}s")

    # 保存执行报告
    report_path = DATA_DIR / f"executor_report_{date_str}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📝 Report: {report_path}")

    # 如果推荐成功，打印推荐摘要
    if recommend_json.exists():
        try:
            rec_data = json.loads(recommend_json.read_text(encoding="utf-8"))
            print(f"\n🎯 推荐摘要:")
            print(f"  - 双榜扫描: ClawHub={rec_data['clawhub_count']} + SkillHub={rec_data['skillhub_count']} → merged={rec_data['merged_count']} (both={rec_data['both_count']})")
            print(f"  - 今日推荐: {rec_data['recommendations_count']} 个")
            print(f"  - 跨平台对比: {rec_data['cross_platform_count']} 个")
            print(f"  - 去重跳过: {rec_data['dedup_skipped_count']} 个")
            print(f"\n  推荐列表:")
            for rec in rec_data["recommendations"]:
                print(f"    {rec['dimension_label']:30s} {rec['name']}")
        except json.JSONDecodeError:
            pass


if __name__ == "__main__":
    main()
