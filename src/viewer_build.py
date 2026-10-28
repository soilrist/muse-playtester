"""viewer (DESIGN §4.9). runs/·bugs/ 를 읽어 서버 없이 열리는 viewer/index.html 한 장을 만든다."""
import html
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROW = re.compile(r"^\|\s*(\d{4})\s*\|\s*\[(.+?)\]\((.+?)\)\s*\|\s*(\w+)\s*\|\s*(.*?)\s*\|$")
STYLE = ("body{font:15px/1.5 system-ui,sans-serif;max-width:860px;margin:2rem auto;padding:0 1rem;color:#222}"
         "table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;padding:.4rem;text-align:left}"
         ".high{color:#b00020;font-weight:600}.medium{color:#b26a00}.low{color:#555}"
         "pre{background:#f5f5f5;padding:.6rem;white-space:pre-wrap}")


def read_bugs(bugs_dir):
    """bugs/INDEX.md 표 줄을 (번호, 제목, 리포트 상대경로, 심각도, 세션) 로 읽는다."""
    index = Path(bugs_dir) / "INDEX.md"
    if not index.is_file():
        return []
    rows = (ROW.match(line) for line in index.read_text(encoding="utf-8").splitlines())
    return [m.groups() for m in rows if m]


def read_sessions(runs_dir):
    """runs/<시각>/ 폴더를 이름 역순(최근 먼저)으로 (이름, summary 본문 또는 None, notes 있나) 로 읽는다."""
    runs_dir = Path(runs_dir)
    if not runs_dir.is_dir():
        return []
    out = []
    for d in sorted((p for p in runs_dir.iterdir() if p.is_dir()), key=lambda p: p.name, reverse=True):
        summary = d / "summary.md"
        text = summary.read_text(encoding="utf-8") if summary.is_file() else None
        out.append((d.name, text, (d / "playtest_notes.md").is_file()))
    return out


def render(bugs, sessions):
    e = html.escape
    parts = ["<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><title>PlayTester viewer</title>",
             f"<style>{STYLE}</style><h1>PlayTester</h1>",
             f"<h2>Bug reports ({len(bugs)})</h2>"]
    if bugs:
        parts.append("<table><tr><th>#</th><th>Title</th><th>Severity</th><th>Session</th></tr>")
        for num, title, path, sev, session in bugs:
            parts.append(f"<tr><td>{e(num)}</td><td><a href=\"../bugs/{e(path)}\">{e(title)}</a></td>"
                         f"<td class=\"{e(sev)}\">{e(sev)}</td><td>{e(session)}</td></tr>")
        parts.append("</table>")
    else:
        parts.append("<p>No bug reports yet.</p>")
    parts.append(f"<h2>Sessions ({len(sessions)})</h2>")
    if not sessions:
        parts.append("<p>No sessions yet.</p>")
    for name, text, has_notes in sessions:
        notes = f" · <a href=\"../runs/{e(name)}/playtest_notes.md\">playtest notes</a>" if has_notes else ""
        body = f"<pre>{e(text)}</pre>" if text else "<p>(no summary.md)</p>"
        parts.append(f"<details><summary>{e(name)}{notes}</summary>{body}</details>")
    return "\n".join(parts) + "\n"


def build(root=None):
    """viewer/index.html 을 쓰고 경로를 돌려준다."""
    root = Path(root or ROOT)
    out = root / "viewer" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(render(read_bugs(root / "bugs"), read_sessions(root / "runs")), encoding="utf-8")
    return out


def selftest():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        empty = build(root).read_text(encoding="utf-8")
        assert "No bug reports yet." in empty and "No sessions yet." in empty
        (root / "bugs").mkdir()
        (root / "bugs" / "INDEX.md").write_text(
            "# Bug reports\n\n| # | Title | Severity | Session |\n|---|---|---|---|\n"
            "| 0001 | [Stuck <in> wall](0001-stuck/report.md) | high | s1 |\n", encoding="utf-8")
        for name, notes in (("20261101-0900", False), ("20261101-1000", True)):
            (root / "runs" / name).mkdir(parents=True)
            (root / "runs" / name / "summary.md").write_text(f"steps: 60 <{name}>", encoding="utf-8")
            if notes:
                (root / "runs" / name / "playtest_notes.md").write_text("n", encoding="utf-8")
        text = build(root).read_text(encoding="utf-8")
        assert "Bug reports (1)" in text and "Sessions (2)" in text
        assert '<a href="../bugs/0001-stuck/report.md">Stuck &lt;in&gt; wall</a>' in text
        assert text.index("20261101-1000") < text.index("20261101-0900"), "최근 세션이 위"
        assert text.count("playtest_notes.md") == 1 and "steps: 60 &lt;20261101-0900&gt;" in text
    print("viewer_build selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]:
        selftest()
    elif sys.argv[1:] == ["build"]:
        print(build())
    else:
        print("usage: viewer_build.py selftest|build")
