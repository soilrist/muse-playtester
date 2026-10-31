# PlayTester

An AI agent that plays your game like a human — watching the screen, pressing keys — and writes reproducible bug reports.

Built from scratch during Meta Global AI Developer Hackathon (Oct 28 – Nov 4, 2026). All product code lives in `src/` and was written during the event; `loop/`, `docs/`, `tools/` are my open-source dev-process template (soilrist/loop-starter-kit) used to run the build.

## Meta models used
- **SAM 3.1** — perception: finds people, HP bars, doors, chests and dialog boxes on each screenshot. PlayTester works out which person box is the player by watching which one moved after a move key, then hands Spark every other object as an offset from the player ("74px right, 30px down").
- **Muse Spark 1.3** — decision: picks the next action via tool calling (`press`, `wait`, `note`, `report_bug`, `done`, plus `click` for mouse-driven games).

Bugs are flagged two ways: Spark calls `report_bug` when it sees something wrong, and fixed rules catch what a model can miss — `same_screen` (keys pressed, screen frozen) and `player_stuck` (SAM-tracked player did not move after three move keys in two or more directions, with no dialog open).

## Game under test
Breath of the Abyss — my own unfinished Godot 4 top-down RPG, tested on a pinned snapshot of the private dev build (an older public version lives at [soilrist/breath-of-the-abyss](https://github.com/soilrist/breath-of-the-abyss)). PlayTester never reads its code; it only sees the screen and presses keys.

Second game, different engine: **Snarehaven**, my Unreal Engine 5 mobile monster-capture action game, packaged for Win64 and played offline (`-SnareOffline`) with keys plus real mouse clicks (left attacks, right captures). Same agent, no game-specific code beyond the launch command and window title: `PT_GAME=snarehaven tools/vm/run_in_vm.sh`.

## How to run
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
echo "<your Meta API key>" > ~/.meta-api-key && chmod 600 ~/.meta-api-key   # or set META_API_KEY
.venv/bin/python src/run.py   # 60-move session, writes runs/<timestamp>/
```
Open `viewer/index.html` in a browser to browse sessions and bug reports (regenerate it with `.venv/bin/python src/viewer_build.py build`; open it from the repository root so the relative links work).

On macOS, grant the terminal Screen Recording and Accessibility permission (needed to capture the game window and send keys).

## Status
Working pieces, each with a self-check: `src/report.py selftest`, `src/notes.py selftest`, `src/viewer_build.py selftest`, `src/run.py selftest`, `src/capture.py` (saves a screenshot). `src/perceive.py` (SAM), `src/decide.py` (Spark tool calls) and `src/act.py` (key presses) are chained by `src/run.py` into a session loop (log, captures, `summary.md`, `playtest_notes.md`). A full 60-move run on the real game has completed inside a Windows VM (so the agent does not take over the developer's own screen); more runs and bug reports are in progress.

## Demo video
_Coming soon._

## Bug reports
See [`bugs/INDEX.md`](bugs/INDEX.md).
