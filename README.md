# PlayTester

An AI agent that plays your game like a human — watching the screen, pressing keys — and writes reproducible bug reports.

Built from scratch during Meta Global AI Developer Hackathon (Oct 28 – Nov 4, 2026). All product code lives in `src/` and was written during the event; `loop/`, `docs/`, `tools/` are my open-source dev-process template (soilrist/loop-starter-kit) used to run the build.

## Meta models used
- **SAM 3.1** — perception: finds the player, enemies, HP bar, doors, chests, NPCs and dialog boxes on each screenshot.
- **Muse Spark 1.3** — decision: picks the next action via tool calling (`press`, `wait`, `report_bug`, `done`).

## How to run
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
echo "<your Meta API key>" > ~/.meta-api-key && chmod 600 ~/.meta-api-key
.venv/bin/python -m src.run
```

## Demo video
_Coming soon._

## Bug reports
See [`bugs/INDEX.md`](bugs/INDEX.md).
