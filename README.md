# PlayTester

An AI agent that plays your game like a human — watching the screen, pressing keys — and writes reproducible bug reports.

Built from scratch during Meta Global AI Developer Hackathon (Oct 28 – Nov 4, 2026). All product code lives in `src/` and was written during the event; `loop/`, `docs/`, `tools/` are my open-source dev-process template (soilrist/loop-starter-kit) used to run the build.

## Meta models used
- **SAM 3.1** — perception: finds the player, enemies, HP bar, doors, chests, NPCs and dialog boxes on each screenshot.
- **Muse Spark 1.3** — decision: picks the next action via tool calling (`press`, `wait`, `report_bug`, `done`).

## Game under test
Breath of the Abyss — my own unfinished Godot 4 top-down RPG, tested on a pinned snapshot of the private dev build (an older public version lives at [soilrist/breath-of-the-abyss](https://github.com/soilrist/breath-of-the-abyss)). PlayTester never reads its code; it only sees the screen and presses keys.

## How to run
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
echo "<your Meta API key>" > ~/.meta-api-key && chmod 600 ~/.meta-api-key   # or set META_API_KEY
.venv/bin/python -m src.run   # 60-move session, writes runs/<timestamp>/
```
Open `viewer/index.html` in a browser to browse sessions and bug reports (regenerate it with `.venv/bin/python src/viewer_build.py build`; open it from the repository root so the relative links work).

On macOS, grant the terminal Screen Recording and Accessibility permission (needed to capture the game window and send keys).

## Status
Working pieces, each with a self-check: `src/report.py selftest`, `src/notes.py selftest`, `src/viewer_build.py selftest`, `src/capture.py` (saves a screenshot). `src/perceive.py` (SAM), `src/decide.py` (Spark tool calls) and `src/act.py` (key presses) are written, and `src/run.py` chains them into a session loop (log, captures, `summary.md`, `playtest_notes.md`). Its self-check passes on fake input; a full 60-move run on the real game is not verified yet (key injection into the Godot window is still being debugged).

## Demo video
_Coming soon._

## Bug reports
See [`bugs/INDEX.md`](bugs/INDEX.md).
