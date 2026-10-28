"""버그 리포트 (DESIGN §4.7). bugs/<번호 4자리>-<slug>/report.md + frames/ + bugs/INDEX.md 한 줄."""
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEVERITIES = ("low", "medium", "high")
INDEX_HEAD = "# Bug reports\n\n| # | Title | Severity | Session |\n|---|---|---|---|\n"


@dataclass
class Bug:
    title: str
    severity: str
    steps: list  # 재현 순서: 누른 입력 목록 (예: "down 300ms")
    expected: str
    actual: str
    why: str  # judge 규칙 또는 Spark why
    frames: list = field(default_factory=list)
    session: str = ""
    key_table: list = field(default_factory=list)  # 키별 확인: (키, 화면이 바뀌었나, 누르기 전 그림, 누른 뒤 그림)


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:40].strip("-") or "bug"


def next_number(bugs_dir):
    nums = [int(p.name[:4]) for p in bugs_dir.glob("[0-9][0-9][0-9][0-9]-*") if p.is_dir()]
    return max(nums, default=0) + 1


def write_report(bug, bugs_dir=None):
    """리포트 폴더를 만들고 report.md 경로를 돌려준다. 필수 칸이 비면 ValueError."""
    bugs_dir = Path(bugs_dir or ROOT / "bugs")
    if bug.severity not in SEVERITIES:
        raise ValueError(f"severity must be one of {SEVERITIES}: {bug.severity!r}")
    for name in ("title", "steps", "expected", "actual", "why", "frames"):
        if not getattr(bug, name):
            raise ValueError(f"required field is empty: {name}")
    bugs_dir.mkdir(parents=True, exist_ok=True)
    num = next_number(bugs_dir)
    folder = bugs_dir / f"{num:04d}-{slugify(bug.title)}"
    (folder / "frames").mkdir(parents=True)
    rels = []
    for f in bug.frames:
        dst = folder / "frames" / Path(f).name
        shutil.copy2(f, dst)
        rels.append(f"frames/{dst.name}")
    lines = [f"# {bug.title}", "", f"- 심각도: {bug.severity}", f"- 세션: {bug.session or '-'}", "",
             "## 재현 순서", *[f"{i}. {s}" for i, s in enumerate(bug.steps, 1)], "",
             "## 기대", bug.expected, "", "## 실제", bug.actual, "", "## 근거 프레임", *[f"- {r}" for r in rels], "",
             "## 판단 근거", bug.why, ""]
    if bug.key_table:
        lines += _key_section(bug.key_table, folder)
    (folder / "report.md").write_text("\n".join(lines), encoding="utf-8")
    index = bugs_dir / "INDEX.md"
    if not index.exists():
        index.write_text(INDEX_HEAD, encoding="utf-8")
    with index.open("a", encoding="utf-8") as fh:
        fh.write(f"| {num:04d} | [{bug.title}]({folder.name}/report.md) | {bug.severity} | {bug.session or '-'} |\n")
    return folder / "report.md"


def _key_section(table, folder):
    """## 키별 확인 — 이동 후보 키를 하나씩 눌렀을 때 화면이 바뀌었는지 표로. 그림은 리포트 폴더로 복사한다."""
    rows = []
    for key, changed, before, after in table:
        rels = []
        for f in (before, after):
            dst = folder / "frames" / Path(f).name
            shutil.copy2(f, dst)
            rels.append(f"frames/{dst.name}")
        rows.append(f"| {key} | {'바뀜' if changed else '그대로'} | {rels[0]} | {rels[1]} |")
    moved = [k for k, c, _, _ in table if c]
    still = [k for k, c, _, _ in table if not c]
    return ["## 키별 확인", "", "| 키 | 화면 | 누르기 전 | 누른 뒤 |", "|---|---|---|---|", *rows, "",
            f"- 화면이 바뀐 키: {', '.join(moved) or '없음'}", f"- 안 바뀐 키: {', '.join(still) or '없음'}", ""]


def selftest():
    src = ROOT / "captures" / "sample-d1-03.png"
    with tempfile.TemporaryDirectory() as d:
        b = Bug("Player stuck in wall", "high", ["down 300ms", "down 300ms"], "player moves", "screen unchanged 11s",
                "judge rule same_screen", [str(src)], "s1")
        p1 = write_report(b, d)
        p2 = write_report(b, d)
        assert p1.parent.name == "0001-player-stuck-in-wall" and p2.parent.name == "0002-player-stuck-in-wall"
        text = p1.read_text(encoding="utf-8")
        for key in ("## 재현 순서", "1. down 300ms", "## 기대", "## 실제", "frames/sample-d1-03.png", "## 판단 근거", "same_screen"):
            assert key in text, key
        assert (p1.parent / "frames" / "sample-d1-03.png").exists()
        assert "## 키별 확인" not in text
        b.key_table = [("up", False, str(src), str(src)), ("left", True, str(src), str(ROOT / "captures" / "priv-b0.png"))]
        t3 = write_report(b, d).read_text(encoding="utf-8")
        for key in ("## 키별 확인", "| up | 그대로 |", "| left | 바뀜 |", "화면이 바뀐 키: left", "안 바뀐 키: up", "frames/priv-b0.png"):
            assert key in t3, key
        assert (p1.parent.parent / "0003-player-stuck-in-wall" / "frames" / "priv-b0.png").exists()
        rows = [l for l in (Path(d) / "INDEX.md").read_text(encoding="utf-8").splitlines() if l.startswith("| 000")]
        assert len(rows) == 3
        for bad in (Bug("t", "urgent", ["a"], "e", "a", "w", [str(src)]), Bug("t", "low", [], "e", "a", "w", [str(src)])):
            try:
                write_report(bad, d)
                raise AssertionError("검증 실패해야 함")
            except ValueError:
                pass
    print("report selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]:
        selftest()
    else:
        print("usage: report.py selftest")
