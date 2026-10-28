"""플레이 소감 (DESIGN §4.10). runs/<시각>/playtest_notes.md — 개선점 최대 3개, 근거 장면 없는 것은 버린다."""
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from meta_client import call_text, output_text

ROOT = Path(__file__).resolve().parent.parent
MAX_ITEMS = 3


@dataclass
class Improvement:
    problem: str
    step: int  # 몇 수째
    capture: str  # 캡처 경로
    genre: str  # 장르 비교: "같은 장르 게임은 보통 …"
    suggestion: str


def keep_grounded(items):
    """근거 장면(수 번호 > 0 + 실제 있는 캡처 파일)과 필수 칸이 다 있는 것만 남기고 3개까지 자른다."""
    kept = []
    for it in items:
        if not (it.problem.strip() and it.genre.strip() and it.suggestion.strip()):
            continue
        if it.step < 1 or not it.capture or not Path(it.capture).is_file():
            continue
        kept.append(it)
    return kept[:MAX_ITEMS]


def summarize(notes, moves):
    """Spark 1회로 note 목록 + 세션 기록을 개선점 후보로 정리한다. notes: [{step, capture, kind, what, why}]."""
    prompt = (
        "You are a game playtester. From the notes and move log below, list at most 3 improvements. "
        "Use only things actually experienced in this session; no generic advice. Reply with a JSON array only; each item has "
        '"problem", "step" (int, a step number from the notes), "capture" (path from the notes), '
        '"genre" (start with "Games of this genre usually"), "suggestion".\n'
        f"Notes: {json.dumps(notes)}\nMoves: {json.dumps(moves[-60:])}"
    )
    text = output_text(call_text(prompt))
    m = re.search(r"\[.*\]", text, re.S)
    raw = json.loads(m.group(0)) if m else []
    return [Improvement(str(d.get("problem", "")), int(d.get("step", 0)), str(d.get("capture", "")),
                        str(d.get("genre", "")), str(d.get("suggestion", ""))) for d in raw if isinstance(d, dict)]


def write_notes(run_dir, items):
    """근거 없는 것을 버린 뒤 playtest_notes.md 를 쓰고 (경로, 남긴 수, 버린 수) 를 돌려준다."""
    kept = keep_grounded(items)
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    lines = ["# Playtest notes", ""]
    if not kept:
        lines.append("(근거 장면이 있는 개선점 없음)")
    for i, it in enumerate(kept, 1):
        lines += [f"## {i}. {it.problem}", "", f"- 근거 장면: {it.step}수째 — {it.capture}",
                  f"- 장르 비교: {it.genre}", f"- 제안: {it.suggestion}", ""]
    path = run_dir / "playtest_notes.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path, len(kept), len(items) - len(kept)


def selftest():
    cap = str(ROOT / "captures" / "sample-d1-03.png")
    good = lambda n: Improvement(f"p{n}", n, cap, "Games of this genre usually show a hint", "add a hint")
    items = [good(1), good(2), Improvement("no step", 0, cap, "g", "s"), Improvement("missing file", 3, "/nope.png", "g", "s"),
             Improvement("no genre", 4, cap, " ", "s"), good(5), good(6)]
    assert [i.problem for i in keep_grounded(items)] == ["p1", "p2", "p5"]
    with tempfile.TemporaryDirectory() as d:
        path, kept, dropped = write_notes(Path(d) / "run1", items)
        text = path.read_text(encoding="utf-8")
        assert (kept, dropped) == (3, 4)
        for key in ("## 1. p1", "근거 장면: 1수째", "장르 비교", "제안", "## 3. p5"):
            assert key in text, key
        assert "no step" not in text and "missing file" not in text
        _, k0, _ = write_notes(Path(d) / "run2", [Improvement("x", 0, "", "g", "s")])
        assert k0 == 0 and "없음" in (Path(d) / "run2" / "playtest_notes.md").read_text(encoding="utf-8")
    print("notes selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]:
        selftest()
    else:
        print("usage: notes.py selftest")
