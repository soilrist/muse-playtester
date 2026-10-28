"""세션 (DESIGN §4.8). 게임을 띄우고 perceive → decide → act → judge 를 상한까지 돌린다."""
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from judge import Judge, Step
from report import Bug, write_report

ROOT = Path(__file__).resolve().parent.parent
GODOT = Path.home() / "Applications/Godot.app/Contents/MacOS/Godot"
GAME = Path.home() / "Git Project/breath-of-the-abyss"
SEE = ["player character", "health bar"]  # judge 규칙이 쓰는 둘만 묻는다 (SAM 상한 120 = 60수 x 2장)
GOAL = "explore the game and look for bugs"
BOOT_SEC = 6


def _limit(name, default):
    return int(float(os.environ.get(name, default)))


def default_ports():
    """실제 캡처·SAM·Spark·키 입력. 자체검사는 이 자리를 가짜로 바꿔 부른다."""
    import act
    import capture
    import decide
    import perceive
    return {"capture": capture.capture, "perceive": lambda p: perceive.perceive(p, SEE),
            "decide": decide.decide, "press": act.press, "wait": act.wait}


def launch_game():
    return subprocess.Popen([str(GODOT), "--path", str(GAME)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_session(ports, run_dir, max_actions=None, max_spark=None, max_sam=None, goal=GOAL, clock=time.monotonic):
    """한 세션을 돌려 (종료 이유, 수) 를 돌려준다. 이상은 bugs/ 에 리포트로, 기록은 run_dir/summary.md 에 남긴다."""
    max_actions = max_actions or _limit("PT_MAX_ACTIONS", 60)
    max_spark = max_spark or _limit("PT_MAX_SPARK_CALLS", 80)
    max_sam = max_sam or _limit("PT_MAX_SAM_CALLS", 120)
    run_dir = Path(run_dir)
    (run_dir / "frames").mkdir(parents=True, exist_ok=True)
    judge, moves, bug_paths, spark, sam = Judge(), [], [], 0, 0
    t0, reason, n = clock(), "action limit", 0
    try:
        for n in range(1, max_actions + 1):
            if spark + 1 > max_spark:
                reason = "spark call limit"
                n -= 1
                break
            if sam + len(SEE) > max_sam:
                reason = "sam call limit"
                n -= 1
                break
            shot = ports["capture"](run_dir / "frames" / f"{n:03d}.png")
            scene = ports["perceive"](shot)
            sam += len(SEE)
            tool, args = ports["decide"](scene.summary(), moves, goal)
            spark += 1
            keys = ()
            if tool == "press":
                ports["press"](args["key"], args["hold_ms"])
                keys = (args["key"],)
                moves.append(f"{args['key']} {args['hold_ms']}ms")
            elif tool == "wait":
                ports["wait"](args["ms"])
                moves.append(f"wait {args['ms']}ms")
            elif tool == "done":
                reason = f"done: {args.get('reason', '')}"
                break
            elif tool == "report_bug":
                moves.append(f"report_bug {args.get('title', '')}")
                bug_paths.append(_report(Bug(args["title"], args["severity"], list(moves), "game behaves normally",
                                             args["title"], f"Spark: {args['why']}", [str(shot)], run_dir.name)))
            else:
                moves.append(f"{tool} (ignored)")
            for f in judge.check(Step(clock() - t0, shot, keys, scene)):
                bug_paths.append(_report(Bug(f"{f.rule} at step {n}", "medium", list(moves), "game keeps responding",
                                             f.why, f"judge rule {f.rule}", f.frames, run_dir.name)))
    except Exception as e:  # BudgetExceeded 포함 — 어떤 이유든 기록은 남기고 끝낸다
        reason = f"stopped: {type(e).__name__}: {e}"
    _summary(run_dir, reason, n, spark, sam, bug_paths)
    return reason, n


def _report(bug):
    return write_report(bug, ROOT / "bugs")


def _summary(run_dir, reason, n, spark, sam, bug_paths):
    lines = ["# Session summary", "", f"- 종료 이유: {reason}", f"- 수: {n}", f"- Spark 호출: {spark}", f"- SAM 이미지: {sam}",
             f"- 리포트: {len(bug_paths)}", *[f"  - {p}" for p in bug_paths], ""]
    (Path(run_dir) / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    run_dir = ROOT / "runs" / datetime.now().strftime("%Y%m%d-%H%M%S")
    game = launch_game()
    try:
        time.sleep(BOOT_SEC)
        reason, n = run_session(default_ports(), run_dir)
    finally:
        game.terminate()
    print(f"session end: {reason} ({n} steps) -> {run_dir}")


def selftest():
    import report
    from perceive import Scene
    shot = ROOT / "captures" / "sample-d1-03.png"
    script = [("press", {"key": "down", "hold_ms": 100}), ("wait", {"ms": 1}), ("done", {"reason": "enough"})]
    log = []

    def ports(tools):
        it = iter(tools)
        return {"capture": lambda p: shot, "perceive": lambda p: Scene(p), "decide": lambda s, r, g: next(it),
                "press": lambda k, h: log.append(("press", k, h)), "wait": lambda ms: log.append(("wait", ms))}

    old = report.ROOT
    with tempfile.TemporaryDirectory() as d:
        globals()["ROOT"] = Path(d)
        try:
            r, n = run_session(ports(script), Path(d) / "r1")
            assert (r, n) == ("done: enough", 3), (r, n)
            assert log == [("press", "down", 100), ("wait", 1)], log
            assert "done: enough" in (Path(d) / "r1" / "summary.md").read_text(encoding="utf-8")
            r, n = run_session(ports([("wait", {"ms": 1})] * 9), Path(d) / "r2", max_actions=4)
            assert (r, n) == ("action limit", 4), (r, n)
            r, n = run_session(ports([("wait", {"ms": 1})] * 9), Path(d) / "r3", max_spark=2)
            assert (r, n) == ("spark call limit", 2), (r, n)
            r, n = run_session(ports([("wait", {"ms": 1})] * 9), Path(d) / "r4", max_sam=5)
            assert (r, n) == ("sam call limit", 2), (r, n)
            r, n = run_session(ports([("report_bug", {"title": "Door", "severity": "low", "why": "w"})] + script), Path(d) / "r5")
            assert (Path(d) / "bugs" / "INDEX.md").is_file() and "Door" in (Path(d) / "bugs" / "INDEX.md").read_text(encoding="utf-8")
            r, n = run_session(ports([]), Path(d) / "r6")  # decide 가 StopIteration → 기록 남기고 끝
            assert r.startswith("stopped:") and (Path(d) / "r6" / "summary.md").is_file(), r
        finally:
            globals()["ROOT"] = old
    print("run selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]:
        selftest()
    else:
        main()
