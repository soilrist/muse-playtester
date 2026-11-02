# PlayTester

An AI agent that plays your game like a human — watching the screen, pressing keys — and writes reproducible bug reports.

Built from scratch during Meta Global AI Developer Hackathon (Oct 28 – Nov 4, 2026). All product code lives in `src/` and was written during the event; `loop/`, `docs/`, `tools/` are my open-source dev-process template (soilrist/loop-starter-kit) used to run the build.

## Meta models used
- **SAM 3.1** — perception: finds people, HP bars, doors, chests and dialog boxes on each screenshot. PlayTester works out which person box is the player by watching which one moved after a move key, then hands Spark every other object as an offset from the player ("74px right, 30px down").
- **Muse Spark 1.3** — decision: picks the next action via tool calling (`press`, `wait`, `note`, `report_bug`, `done`, plus `click` for mouse-driven games).

Bugs are flagged two ways: Spark calls `report_bug` when it sees something wrong, and fixed rules catch what a model can miss — `same_screen` (keys pressed, screen frozen) and `player_stuck` (SAM-tracked player did not move after three move keys in two or more directions, with no dialog open). After the session, `src/gamelog.py` reads the log files the engine already writes (UE `Saved/Logs`, Godot `user://logs`) and files a report per rule — assets missing from the build, crashes, script errors — with the log file attached. A game that dies while booting still gets a crash report.

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
Working pieces, each with a self-check: `src/report.py selftest`, `src/notes.py selftest`, `src/viewer_build.py selftest`, `src/run.py selftest`, `src/gamelog.py selftest`, `src/capture.py` (saves a screenshot). `src/perceive.py` (SAM), `src/decide.py` (Spark tool calls) and `src/act.py` (key presses) are chained by `src/run.py` into a session loop (log, captures, `summary.md`, `playtest_notes.md`). A full 60-move run on the real game has completed inside a Windows VM (so the agent does not take over the developer's own screen); more runs and bug reports are in progress.

Snarehaven (UE5, Win64 build in the same VM): sessions with real mouse clicks and keys — title screen, intro and tutorial cleared, then walking around the first field (`runs/20261101-091910`, `runs/20261102-152538`). Findings: conflicting server status in offline mode ("서버에 연결 중..." and "서버 연결 안 됨" shown at once, no retry); eight sound packages missing from the packaged build (`SFX_Amb_Rain_02`, `_Ocean_02`, `_Wind_02`, `_Night_02`, `_Swamp_02`, `SFX_Bird_07`, `SFX_Footstep_Grass_06`, `SFX_Swing_04` — [bugs/0059](bugs/0059-8-packages-missing-from-the-build/report.md), filed from the game log); and an intermittent startup crash (`Assertion failed: IsSet()` — [bugs/0055](bugs/0055-crash-assertion-failed-isset/report.md)), which PlayTester reports and survives by relaunching the game. VM note: UE5's default anti-aliasing (TSR) turned the whole 3D view black on the Parallels virtual GPU, so PlayTester launches the game with FXAA (`-dpcvars=r.AntiAliasingMethod=1`); a few objects still flicker black there (the virtual GPU drops some draws — the same objects also go black with lighting off), and Spark flagged them as rendering errors on its own.

## Demo video
2.5-minute draft: Godot run, Unreal run, judge and bug report. Built from real runs by `.venv/bin/python tools/demo/make_video.py` (writes `demo/playtester-demo.mp4`, narration via edge-tts).

## Bug reports
See [`bugs/INDEX.md`](bugs/INDEX.md).
