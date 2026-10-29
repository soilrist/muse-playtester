"""세션 (DESIGN §4.8). 게임을 띄우고 perceive → decide → act → judge 를 상한까지 돌린다."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from capture import Interrupted, human_idle_seconds
from judge import Judge, Step, frames_same
from notes import summarize, write_notes
from report import Bug, write_report

ROOT = Path(__file__).resolve().parent.parent
if sys.platform == "win32":  # Parallels Windows VM — tools/vm/bootstrap.ps1 이 깐 자리. 세이브는 VM 안 것이라 사람 세이브와 무관
    GODOT = Path(r"C:\pt\godot\godot.exe")
    GAME = Path(r"C:\pt\game")
    SAVE_DIR = Path(os.environ.get("APPDATA", "")) / "Godot/app_userdata/심연의 숨결"
else:
    GODOT = Path.home() / "Applications/Godot.app/Contents/MacOS/Godot"
    GAME = Path.home() / "Git Project/zerostudyrpg-snapshot"
    SAVE_DIR = Path.home() / "Library/Application Support/Godot/app_userdata/심연의 숨결"  # 사람 세이브와 공유
SEE = ["person", "health bar"]  # judge 규칙이 쓰는 둘만 묻는다 (SAM 상한 120 = 60수 x 2장)
GOAL = "explore the game and look for bugs"
BOOT_SEC = 6
PROBE_KEYS = ["up", "down", "left", "right", "w", "s", "a", "d"]  # 반대 방향이 이웃하게 — 벽에 막힌 쪽과 열린 쪽이 표에서 갈린다
INTERACT_PROBE_KEYS = ["enter", "space", "z", "e", "x"]  # 통하는 키가 나오면 거기서 멈춘다 (대화창이 열렸는데 또 누르면 넘어가 버린다)
PROBE_HOLD_MS = 300
PROBE_SETTLE_MS = 200
IDLE_MIN_SEC = 300  # 사람이 이보다 최근에 맥을 만졌으면 실측하지 않는다 (게임은 창 포커스를 잃으면 스스로 일시정지한다)
HUMAN_BACK = "사람이 돌아옴"


def _limit(name, default):
    return int(float(os.environ.get(name, default)))


def default_ports():
    """실제 캡처·SAM·Spark·키 입력. 자체검사는 이 자리를 가짜로 바꿔 부른다."""
    import act
    import capture
    import decide
    import perceive
    return {"capture": capture.capture, "perceive": lambda p: perceive.perceive(p, SEE),
            "decide": decide.decide, "press": act.press, "wait": act.wait,
            "summarize": summarize}


def backup_saves(src, dst):
    """세이브 폴더를 dst 로 통째 복사한다. 폴더가 없으면 None."""
    src = Path(src)
    if not src.is_dir():
        return None
    shutil.copytree(src, dst)
    return Path(dst)


def restore_saves(src, backup):
    """세이브 폴더를 백업 시점 그대로 되돌린다 (백업 뒤에 생긴 파일은 지운다). backup 이 None 이면 폴더가 원래 없었던 것."""
    src = Path(src)
    if src.exists():
        shutil.rmtree(src)
    if backup is not None:
        shutil.copytree(backup, src)


def launch_game():
    return subprocess.Popen([str(GODOT), "--path", str(GAME)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_session(ports, run_dir, max_actions=None, max_spark=None, max_sam=None, goal=GOAL, clock=time.monotonic):
    """한 세션을 돌려 (종료 이유, 수) 를 돌려준다. 이상은 bugs/ 에 리포트로, 기록은 run_dir/summary.md 에 남긴다."""
    max_actions = max_actions or _limit("PT_MAX_ACTIONS", 60)
    max_spark = max_spark or _limit("PT_MAX_SPARK_CALLS", 80)
    max_sam = max_sam or _limit("PT_MAX_SAM_CALLS", 120)
    run_dir = Path(run_dir)
    (run_dir / "frames").mkdir(parents=True, exist_ok=True)
    judge, moves, bug_paths, spark, sam, notes = Judge(), [], [], 0, 0, []
    stuck = {}
    hint, same_reported, want_note = "", False, False  # hint: 키별 확인에서 알아낸 관찰 결과를 이후 decide 입력에 붙인다
    t0, reason, n, entry = clock(), "action limit", 0, None
    try:
        for n in range(1, max_actions + 1):
            entry = None
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
            tool, args = ports["decide"](scene.summary(), moves, goal + hint, shot, **({"only_note": True} if want_note else {}))
            want_note = False
            spark += 1
            why = args.get("why") if tool in ("report_bug", "note") else args.pop("why", None)  # press·wait·done 의 why 는 로그 칸으로 옮긴다
            keys, entry = (), {"step": n, "t": round(clock() - t0, 1), "scene": scene.summary(), "tool": tool,
                               "args": args, "why": why or "(no reason given)", "capture": _rel(run_dir, shot), "findings": []}
            if tool == "press":
                ports["press"](args["key"], args["hold_ms"])
                keys = (args["key"],)
                moves.append(f"{args['key']} {args['hold_ms']}ms")
            elif tool == "wait":
                ports["wait"](args["ms"])
                moves.append(f"wait {args['ms']}ms")
            elif tool == "done":
                reason = f"done: {args.get('reason', '')}"
                _log(run_dir, entry)
                break
            elif tool == "report_bug":
                moves.append(f"report_bug {args.get('title', '')}")
                bug_paths.append(_report(Bug(args["title"], args["severity"], list(moves), "game behaves normally",
                                             args["title"], f"Spark: {args['why']}", [str(shot)], run_dir.name)))
            elif tool == "note":
                moves.append(f"note {args.get('kind', '')}")
                notes.append({"step": n, "capture": _rel(run_dir, shot), "kind": args.get("kind", ""),
                              "what": args.get("what", ""), "why": args.get("why", "")})
            else:
                moves.append(f"{tool} (ignored)")
            for f in judge.check(Step(clock() - t0, shot, keys, scene)):
                table, sev, expect = [], "medium", "game keeps responding"
                if f.rule == "same_screen":
                    want_note = True  # 다음 수는 note 만 고르게 한다 — 프롬프트 권유로는 3회 내내 0번이었다
                    table = probe_keys(ports, run_dir, n)
                    hint = probe_hint(table) or hint
                    for k in keys:  # probe 의 '바뀜'은 방향만 바뀐 것일 수 있다 — 같은 키로 두 번 막히면 벽·맵 끝이다
                        stuck[k] = stuck.get(k, 0) + 1
                        if stuck[k] == 2:
                            hint += blocked_hint(k)
                elif f.rule == "interact_stuck":
                    table = probe_keys(ports, run_dir, n, INTERACT_PROBE_KEYS, True)
                    sev, expect = "low", "an interaction key opens a dialog or inspects something"
                    worked = [k for k, changed, _, _ in table if changed]
                    moves.append(f"hint: '{worked[0]}' changes the screen when interacting — use it" if worked else
                                 "hint: none of enter/space/z/e/x changed the screen here — move closer or try another goal")
                if f.rule == "same_screen" and same_reported:  # 같은 원인(키 무반응) 리포트는 세션당 1개
                    entry["findings"].append(f.rule)
                    entry.setdefault("probe", {}).update({k: changed for k, changed, _, _ in table})
                    continue
                same_reported = same_reported or f.rule == "same_screen"
                bug_paths.append(_report(Bug(f"{f.rule} at step {n}", sev, list(moves), expect,
                                             f.why, f"judge rule {f.rule}", f.frames, run_dir.name, table)))
                entry["findings"].append(f.rule)
                if table:
                    entry.setdefault("probe", {}).update({k: changed for k, changed, _, _ in table})
            _log(run_dir, entry)
    except Interrupted as e:  # 다른 앱이 앞으로 왔다 — 판정하지 않고, 창을 되찾지 않고, 정상 종료
        reason = HUMAN_BACK
        _log(run_dir, {**(entry or {"step": n, "capture": ""}), "interrupted": True, "interrupt_detail": str(e)})
    except Exception as e:  # BudgetExceeded 포함 — 어떤 이유든 기록은 남기고 끝낸다
        reason = f"stopped: {type(e).__name__}: {e}"
    if notes and "summarize" in ports:  # 세션 끝에 Spark 1회로 소감 정리 (DESIGN §4.10)
        try:
            write_notes(run_dir, ports["summarize"](notes, moves))
            spark += 1
        except Exception as e:
            reason += f" (notes failed: {type(e).__name__})"
    _summary(run_dir, reason, n, spark, sam, bug_paths)
    return reason, n


def probe_keys(ports, run_dir, n, keys=PROBE_KEYS, stop_on_change=False):
    """걸린 자리에서 후보 키를 하나씩 눌러 키마다 화면이 바뀌었는지 본다. [(키, 바뀜, 전 그림, 후 그림)]."""
    table = []
    for key in keys:
        before = ports["capture"](Path(run_dir) / "frames" / f"probe-{n:03d}-{key}-before.png")
        ports["press"](key, PROBE_HOLD_MS)
        ports["wait"](PROBE_SETTLE_MS)
        after = ports["capture"](Path(run_dir) / "frames" / f"probe-{n:03d}-{key}-after.png")
        table.append((key, not frames_same(before, after), str(before), str(after)))
        if stop_on_change and table[-1][1]:
            break
    return table


def probe_hint(table):
    """키별 확인 표에서 안 바뀐 키와 바뀐 키를 decide 가 읽을 문장으로. 바뀐 키가 없거나 안 바뀐 키가 없으면 ''."""
    dead = [k for k, changed, _, _ in table if not changed]
    live = [k for k, changed, _, _ in table if changed]
    if not dead or not live:
        return ""
    return (f" Observed: keys {', '.join(dead)} did NOT change the screen here (no response) — do not press them again; "
            f"use keys that did change it: {', '.join(live)}.")


def blocked_hint(key):
    """같은 키로 same_screen 이 두 번 났을 때 decide 에 붙일 문장."""
    return f" '{key}' pressed here twice, screen unchanged — blocked (wall/map edge) here; go the other way."


def _rel(run_dir, shot):
    """run 폴더 기준 상대경로(frames/012.png). VM 의 \\\\Mac\\… 절대경로가 로그에 남지 않게 — Mac 에서 그대로 열린다."""
    parts = Path(str(shot).replace("\\", "/")).parts
    return "/".join(parts[parts.index("frames"):]) if "frames" in parts else str(shot)


def _rel_to(path, anchor):
    """리포트 경로를 bugs/0047-x/report.md 꼴 상대경로로 — summary 에 VM 의 \\\\Mac\\… 절대경로가 남지 않게."""
    parts = Path(str(path).replace("\\", "/")).parts
    return "/".join(parts[len(parts) - 1 - parts[::-1].index(anchor):]) if anchor in parts else str(path)


def _log(run_dir, entry):
    """수마다 한 줄: 수 번호·Scene 요약·Spark 툴 호출(이름+인자)·Spark 이유(why)·누른 키와 시간(args)·캡처 경로·judge 결과."""
    with (Path(run_dir) / "log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _report(bug):
    return write_report(bug, ROOT / "bugs")


def _summary(run_dir, reason, n, spark, sam, bug_paths):
    lines = ["# Session summary", "", f"- 종료 이유: {reason}", f"- 수: {n}", "- 수별 로그: [log.jsonl](log.jsonl)", f"- Spark 호출: {spark}", f"- SAM 이미지: {sam}",
             f"- 리포트: {len(bug_paths)}", *[f"  - {_rel_to(p, 'bugs')}" for p in bug_paths], ""]
    (Path(run_dir) / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def human_busy(idle_fn=human_idle_seconds, min_sec=IDLE_MIN_SEC):
    """사람이 맥을 쓰는 중이면 유휴 초(문자열 설명용), 아니면 None. 유휴를 못 읽으면 쓰는 중이 아닌 것으로 본다."""
    idle = idle_fn()
    return idle if idle is not None and idle < min_sec else None


def main():
    idle = human_busy()
    if idle is not None:
        print(f"사람 사용 중, 실측 미룸 (유휴 {idle:.0f}초 < {IDLE_MIN_SEC}초)")
        return
    run_dir = ROOT / "runs" / datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = backup_saves(SAVE_DIR, ROOT / "backups" / ("userdata-" + datetime.now().strftime("%Y%m%d-%H%M%S")))
    try:
        game = launch_game()
        try:
            time.sleep(BOOT_SEC)
            import act
            act.focus_game()  # 세션 시작 때 단 한 번만 창을 올린다 — 이후엔 빼앗지 않는다
            reason, n = run_session(default_ports(), run_dir)
        finally:
            game.terminate()
            game.wait()
    finally:
        restore_saves(SAVE_DIR, backup)
    print(f"session end: {reason} ({n} steps) -> {run_dir}")


def selftest():
    import report
    from perceive import Scene
    shot = ROOT / "captures" / "sample-d1-03.png"
    script = [("press", {"key": "down", "hold_ms": 100, "why": "see door"}), ("wait", {"ms": 1, "why": "let it settle"}), ("done", {"reason": "enough", "why": "seen enough"})]
    log = []

    def ports(tools):
        it = iter(tools)
        return {"capture": lambda p: (Path(p).parent.mkdir(parents=True, exist_ok=True), shutil.copy(shot, p), Path(p))[2], "perceive": lambda p: Scene(p), "decide": lambda s, r, g, i=None, **kw: next(it),
                "press": lambda k, h: log.append(("press", k, h)), "wait": lambda ms: log.append(("wait", ms))}

    old = report.ROOT
    with tempfile.TemporaryDirectory() as d:
        globals()["ROOT"] = Path(d)
        try:
            assert _rel_to("\\\\Mac\\Home\\p\\bugs\\0047-x\\report.md", "bugs") == "bugs/0047-x/report.md"
            assert _rel("x", "\\\\Mac\\Home\\p\\runs\\r\\frames\\012.png") == "frames/012.png"
            r, n = run_session(ports(script), Path(d) / "r1")
            assert (r, n) == ("done: enough", 3), (r, n)
            assert log == [("press", "down", 100), ("wait", 1)], log
            assert "done: enough" in (Path(d) / "r1" / "summary.md").read_text(encoding="utf-8")
            rows = [json.loads(x) for x in (Path(d) / "r1" / "log.jsonl").read_text(encoding="utf-8").splitlines()]
            assert [x["step"] for x in rows] == [1, 2, 3] and rows[0]["tool"] == "press" and rows[0]["args"]["key"] == "down", rows
            assert all(x["capture"].startswith("frames/") and (Path(d) / "r1" / x["capture"]).is_file() and x["scene"] for x in rows), rows
            assert [x["why"] for x in rows] == ["see door", "let it settle", "seen enough"] and "why" not in rows[0]["args"], rows
            r, n = run_session(ports([("wait", {"ms": 1})] * 9), Path(d) / "r2", max_actions=4)
            assert (r, n) == ("action limit", 4), (r, n)
            r, n = run_session(ports([("wait", {"ms": 1})] * 9), Path(d) / "r3", max_spark=2)
            assert (r, n) == ("spark call limit", 2), (r, n)
            r, n = run_session(ports([("wait", {"ms": 1})] * 9), Path(d) / "r4", max_sam=5)
            assert (r, n) == ("sam call limit", 2), (r, n)
            r, n = run_session(ports([("report_bug", {"title": "Door", "severity": "low", "why": "w"})] + script), Path(d) / "r5")
            assert (Path(d) / "bugs" / "INDEX.md").is_file() and "Door" in (Path(d) / "bugs" / "INDEX.md").read_text(encoding="utf-8")
            from notes import Improvement
            note = ("note", {"kind": "ux", "what": "no hint", "why": "lost"})
            p7 = ports([note] + script)
            p7["summarize"] = lambda ns, mv: [Improvement("no hint", ns[0]["step"], ns[0]["capture"], "Games of this genre usually hint", "add hint")]
            run_session(p7, Path(d) / "r7")
            text = (Path(d) / "r7" / "playtest_notes.md").read_text(encoding="utf-8")
            assert "1수째" in text and "no hint" in text, text
            assert not (Path(d) / "r1" / "playtest_notes.md").exists()
            # same_screen 시나리오: 1수만 다른 화면, 이후 같은 화면, 시계는 호출마다 3초
            seq = {"n": 0}

            def cap(p):
                seq["n"] += 1
                shutil.copy2(Path(shot).with_name("priv-b0.png") if seq["n"] == 1 else shot, p)
                return p
            tick = {"t": 0}

            def clock():
                tick["t"] += 3
                return tick["t"]
            forced = []
            p8 = ports([("press", {"key": "down", "hold_ms": 100})] * 6)
            p8["decide"] = (lambda it: lambda s, r, g, i=None, **kw: (forced.append(kw.get("only_note", False)), next(it))[1])(iter([("press", {"key": "down", "hold_ms": 100})] * 6))
            p8["capture"] = lambda p: (Path(p).parent.mkdir(parents=True, exist_ok=True), cap(p))[1]
            run_session(p8, Path(d) / "r8", max_actions=6, clock=clock)
            rows = [json.loads(x) for x in (Path(d) / "r8" / "log.jsonl").read_text(encoding="utf-8").splitlines()]
            hit = [x for x in rows if "same_screen" in x["findings"]]
            assert True in forced and forced[0] is False and forced[rows.index(hit[0]) + 1] is True, forced
            assert hit and set(hit[0]["probe"]) == set(PROBE_KEYS) and not any(hit[0]["probe"].values()), rows
            assert all(x["why"] == "(no reason given)" for x in rows), rows
            rep = next((Path(d) / "bugs").glob("*same-screen*/report.md")).read_text(encoding="utf-8")
            assert "## 키별 확인" in rep and "| up | 그대로 |" in rep and "| d | 그대로 |" in rep, rep
            assert any((next((Path(d) / "bugs").glob("*same-screen*")) / "frames").glob("probe-*-up-before.png"))
            # probe 결과가 다음 decide 입력에 들어가고, same_screen 리포트는 세션당 1개
            assert probe_hint([("right", False, "", ""), ("a", True, "", "")]).count("right") == 1 and "a." in probe_hint([("right", False, "", ""), ("a", True, "", "")])
            assert probe_hint([("right", False, "", "")]) == ""
            assert "pressed here twice" in blocked_hint("a") and "'a'" in blocked_hint("a")
            assert len(list((Path(d) / "bugs").glob("*same-screen*"))) == 1
            seen, seq["n"] = [], 0
            probed = {"n": 0}

            def cap2(p):  # 1수 다른 화면, 이후 같은 화면. 'a' 를 누른 뒤 그림만 바꿔 a 만 '바뀜'으로 만든다
                probed["n"] += 1
                shutil.copy2(Path(shot).with_name("priv-b0.png") if probed["n"] == 1 or str(p).endswith("probe-004-a-after.png") or str(p).endswith("probe-005-a-after.png") or str(p).endswith("probe-006-a-after.png") else shot, p)
                return p
            p11 = ports([("press", {"key": "right", "hold_ms": 100})] * 8)
            p11["capture"] = lambda p: (Path(p).parent.mkdir(parents=True, exist_ok=True), cap2(p))[1]
            p11["decide"] = (lambda it: lambda s, r, g, i=None, **kw: (seen.append(g), next(it))[1])(iter([("press", {"key": "right", "hold_ms": 100})] * 8))
            run_session(p11, Path(d) / "r11", max_actions=8, clock=clock)
            rows = [json.loads(x) for x in (Path(d) / "r11" / "log.jsonl").read_text(encoding="utf-8").splitlines()]
            assert any("same_screen" in x["findings"] for x in rows) and any("did NOT change" in g and "right" in g for g in seen), (seen, rows)
            # interact_stuck: enter 를 계속 눌러도 화면이 그대로 — 후보 키 5개를 다 시도하고 리포트에 표
            seq["n"] = 0
            p10 = ports([("press", {"key": "enter", "hold_ms": 100})] * 6)
            p10["capture"] = p8["capture"]
            run_session(p10, Path(d) / "r10", max_actions=6, clock=clock)
            rows = [json.loads(x) for x in (Path(d) / "r10" / "log.jsonl").read_text(encoding="utf-8").splitlines()]
            hit = [x for x in rows if "interact_stuck" in x["findings"]]
            assert hit and set(hit[0]["probe"]) == set(INTERACT_PROBE_KEYS) and not any(hit[0]["probe"].values()), rows
            rep = next((Path(d) / "bugs").glob("*interact-stuck*/report.md")).read_text(encoding="utf-8")
            assert "## 키별 확인" in rep and "| enter | 그대로 |" in rep and "| x | 그대로 |" in rep and "none of enter/space/z/e/x" in rep, rep
            # 사람이 돌아옴: 3번째 수의 press 중 다른 앱이 앞으로 옴 → interrupted 로그, judge·리포트 없음, 정상 종료
            def rude(k, h):
                if len(log) >= 2:
                    raise Interrupted("Claude 가 앞으로 왔다")
                log.append(("press", k, h))
            log.clear()
            p9 = ports([("press", {"key": "down", "hold_ms": 100})] * 6)
            p9["press"] = rude
            before = len(list((Path(d) / "bugs").glob("*/report.md")))
            r, n = run_session(p9, Path(d) / "r9")
            rows = [json.loads(x) for x in (Path(d) / "r9" / "log.jsonl").read_text(encoding="utf-8").splitlines()]
            assert (r, n) == (HUMAN_BACK, 3) and rows[-1].get("interrupted") and rows[-1]["step"] == 3 and not rows[-1]["findings"] and len(rows) == 3, (r, n, rows)
            assert "사람이 돌아옴" in (Path(d) / "r9" / "summary.md").read_text(encoding="utf-8")
            assert len(list((Path(d) / "bugs").glob("*/report.md"))) == before
            assert human_busy(lambda: 60.0) == 60.0 and human_busy(lambda: 301.0) is None and human_busy(lambda: None) is None
            r, n = run_session(ports([]), Path(d) / "r6")  # decide 가 StopIteration → 기록 남기고 끝
            assert r.startswith("stopped:") and (Path(d) / "r6" / "summary.md").is_file(), r
        finally:
            globals()["ROOT"] = old
    with tempfile.TemporaryDirectory() as d:
        save, bak = Path(d) / "save", Path(d) / "bak"
        save.mkdir()
        (save / "slot1.json").write_text("orig", encoding="utf-8")
        b = backup_saves(save, bak)
        (save / "slot1.json").write_text("changed", encoding="utf-8")
        (save / "new.json").write_text("x", encoding="utf-8")
        restore_saves(save, b)
        assert (save / "slot1.json").read_text(encoding="utf-8") == "orig" and not (save / "new.json").exists()
        assert subprocess.run(["diff", "-r", str(save), str(bak)]).returncode == 0
        assert backup_saves(Path(d) / "none", Path(d) / "bak2") is None
    print("run selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]:
        selftest()
    else:
        main()
