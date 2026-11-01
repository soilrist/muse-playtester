"""게임 로그 검사 — 세션 동안 게임이 남긴 로그에서 화면으론 안 보이는 것(빠진 에셋·크래시·스크립트 오류)을 찾아 리포트로.
게임 코드는 안 읽는다. 엔진이 원래 쓰는 로그 파일만 읽는다 (UE: Saved/Logs/*.log, Godot: user://logs/*.log)."""
import re
import sys
import tempfile
from pathlib import Path

from report import Bug, write_report

MAX_LINES = 10  # 리포트에 붙이는 로그 줄 상한
# (규칙, 정규식 — 첫 그룹이 같으면 같은 것, 제목, 심각도, 기대)
RULES = [
    ("missing_asset", re.compile(r"LoadPackage: SkipPackage: (\S+) .*does not exist"),
     "{n} packages missing from the build", "medium", "every asset the game loads is in the packaged build"),
    ("crash", re.compile(r"LogWindows: Error: (Assertion failed: .+?) \[File:"),
     "Crash: {first}", "high", "the game keeps running"),
    ("script_error", re.compile(r"^(?:SCRIPT )?ERROR: (.+)$", re.M),
     "{n} script errors in the game log", "medium", "no engine or script errors while playing"),
]


def read_log(p):
    b = Path(p).read_bytes()
    return b.decode("utf-16") if b[:2] in (b"\xff\xfe", b"\xfe\xff") else b.decode("utf-8", "replace")


def logs_since(log_dir, t0):
    """t0(epoch 초) 뒤에 쓰인 로그 파일. UE 는 재실행 때 지난 로그를 *-backup-*.log 로 돌리므로 부팅 크래시 로그도 여기 걸린다."""
    d = Path(log_dir)
    return sorted((p for p in d.glob("*.log") if p.stat().st_mtime >= t0), key=lambda p: p.stat().st_mtime) if d.is_dir() else []


def scan(texts):
    """texts: [(파일 이름, 내용)]. {규칙: (같은 것 묶은 순서 목록, 전체 횟수, 근거 줄들, 걸린 파일들)} — 걸린 규칙만."""
    out = {}
    for name, rx, *_ in RULES:
        keys, lines, files, count = [], [], [], 0
        for fname, t in texts:
            for m in rx.finditer(t):
                count += 1
                if fname not in files:
                    files.append(fname)
                if m[1] not in keys:
                    keys.append(m[1])
                    end = t.find("\n", m.end())
                    lines.append(t[t.rfind("\n", 0, m.start()) + 1:end if end >= 0 else None].strip())
        if count:
            out[name] = (keys, count, lines, files)
    return out


def report_logs(log_dir, t0, frame, session, bugs_dir):
    """로그를 읽어 규칙마다 리포트 1개. 만든 report.md 경로 목록. 근거로 화면 한 장(있으면)과 걸린 로그 파일 원본을 붙인다."""
    files = logs_since(log_dir, t0)
    found = scan([(p.name, read_log(p)) for p in files])
    paths = []
    for name, rx, title, sev, expected in RULES:
        if name not in found:
            continue
        keys, count, lines, hit = found[name]
        actual = f"{count} occurrence(s) in the game log, {len(keys)} distinct:\n\n```\n" + "\n".join(lines[:MAX_LINES]) + "\n```"
        paths.append(write_report(Bug(
            title.format(n=len(keys), first=keys[0][:60]), sev,
            ["Launch the game", f"Play the session runs/{session} (actions in log.jsonl)", "Read the game log after the session"],
            expected, actual, f"game log rule {name}: {', '.join(hit)}", [str(frame)] * bool(frame) + [str(Path(log_dir) / h) for h in hit], session), bugs_dir))
    return paths


def selftest():
    import os
    import time
    ue = ("[0]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/SFX/Rain (0x1) - The package to load does not exist on disk\n"
          "[0]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/SFX/Rain (0x1) - The package to load does not exist on disk\n"
          "[0]LogStreaming: Warning: LoadPackage: SkipPackage: /Game/SFX/Bird (0x2) - The package to load does not exist on disk\n")
    crash = ("[0]LogWindows: Error: appError called: Assertion failed: IsSet() [File:Optional.h] [Line: 372]\n"
             "[0]LogWindows: Error: Assertion failed: IsSet() [File:Optional.h] [Line: 372]\n")
    godot = "ERROR: Condition \"!p\" is true.\nSCRIPT ERROR: Invalid get index 'hp'\n"
    f = scan([("a.log", ue), ("b.log", crash), ("c.log", godot)])
    assert f["missing_asset"][:2] == (["/Game/SFX/Rain", "/Game/SFX/Bird"], 3), f
    assert f["crash"][:2] == (["Assertion failed: IsSet()"], 1), f  # appError 줄은 같은 크래시를 두 번 세지 않는다
    assert f["script_error"][1] == 2 and f["script_error"][2][1].startswith("SCRIPT ERROR"), f
    assert f["crash"][3] == ["b.log"] and "[Line: 372]" in f["crash"][2][0], f
    assert scan([("a.log", "LogInit: all good\n")]) == {}
    with tempfile.TemporaryDirectory() as d:
        logs, bugs = Path(d) / "Logs", Path(d) / "bugs"
        logs.mkdir()
        (logs / "Game-backup.log").write_text(crash, encoding="utf-16")  # 인코딩이 달라도 읽는다
        (logs / "Game.log").write_text(ue, encoding="utf-8")
        old = logs / "old.log"
        old.write_text(crash)
        os.utime(old, (0, 0))
        frame = Path(__file__).resolve().parent.parent / "captures" / "sample-d1-03.png"
        paths = report_logs(logs, time.time() - 60, frame, "s1", bugs)
        assert len(paths) == 2, paths
        text = "".join(p.read_text(encoding="utf-8") for p in paths)
        for k in ("2 packages missing", "Crash: Assertion failed: IsSet()", "- 심각도: high", "/Game/SFX/Bird", "rule crash: Game-backup.log\n"):
            assert k in text, k
        assert "old.log" not in text
        assert "frames/Game-backup.log" in text and "frames/sample-d1-03.png" in text
        p = report_logs(logs, time.time() - 60, None, "s2", bugs)[1]  # 부팅 크래시 — 화면이 없어도 로그만으로 리포트
        assert sorted(x.name for x in (p.parent / "frames").iterdir()) == ["Game-backup.log"], p
        assert report_logs(Path(d) / "none", 0, frame, "s1", bugs) == []
    print("gamelog selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]:
        selftest()
    else:
        print("usage: gamelog.py selftest")
