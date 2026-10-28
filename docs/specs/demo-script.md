# 3분 데모 영상 대본 (D6-03)

> 근거: DESIGN §0(점수: 임팩트 30 · 메타 모델 25 · 기술 20 · 데모 25), §7(박스 오버레이 + 판단 문장 + 리포트). 총 180초.
> 내레이션은 심사용이라 영어. 촬영·편집은 사람(ROADMAP D7). **화면 재료는 아직 없는 것이 있다** — 맨 오른쪽 칸이 "재료"가 준비되는 조각.

## 장면표

| # | 시간 | 길이 | 화면 | 내레이션 (영어) | 재료 |
|---|---|---|---|---|---|
| 1 | 0:00–0:15 | 15초 | 게임 창 「심연의 숨결」 + 제목 "PlayTester" | "Every indie dev ships bugs they never found, because nobody played the game long enough. PlayTester plays it for you." | 게임 실행만 (지금 가능) |
| 2 | 0:15–0:35 | 20초 | 화면 분할: 왼쪽 게임, 오른쪽 터미널에서 `python3 -m src.run` 시작 | "It sees only the screen — no game code, no hooks. It presses real keys." | D3-03 run.py |
| 3 | 0:35–1:05 | 30초 | 캡처 위에 SAM 3.1 박스 오버레이 (player, door, npc …) | "SAM 3.1 segments what is on screen: player, walls, doors, characters." | D2-01 perceive (코드 있음), D2-02 |
| 4 | 1:05–1:40 | 35초 | Spark 의 툴 호출(`move`·`interact` …)과 판단 문장이 자막으로 흐르고 캐릭터가 실제로 움직임 | "Muse Spark reads the scene and picks one tool call per step: move, interact, wait, note. Every decision is logged with its reason." | D3-01 decide (코드 있음), D3-03 |
| 5 | 1:40–2:10 | 30초 | 캐릭터가 벽에 끼어 10초 정지 → judge 가 "stuck" 표시 | "When the screen stops changing while it keeps pressing a direction, the judge flags a stuck." | D4-01 judge (완료), D4-03 |
| 6 | 2:10–2:35 | 25초 | `bugs/0001-*/report.md` 를 열어 재현 순서·캡처 보여줌 | "It writes a report a human can reproduce: steps, screenshots, severity." | D4-02 report (완료), D4-03 |
| 7 | 2:35–2:50 | 15초 | `viewer/index.html` 열기 — 세션·리포트 목록, 플레이 소감 `playtest_notes.md` | "A static viewer lists every run, bug, and the agent's playtest notes — each backed by a scene." | D6-01 viewer, D6-04 notes (완료) |
| 8 | 2:50–3:00 | 10초 | 60수 summary.md(종료 이유·비용) + 저장소 주소 | "60 actions, under three dollars. Open source." | D5-01 |

합계 15+20+30+35+30+25+15+10 = 180초.

## 촬영 전 확인 (사람 몫)
- 2~6장은 D3-03(run.py)이 끝나야 찍을 수 있다. 키 주입이 아직 막혀 있다(STATUS #7·#8).
- 비용 숫자는 8장 직전에 `runs/<시각>/summary.md` 에서 실제 값을 읽어 바꾼다 — 위 "under three dollars" 는 상한($3)이지 실측이 아니다.
- 5장 끼임은 D4-03 에서 일부러 만든 재현이어야 한다. 우연히 안 걸리면 이 장면은 빼고 4장을 늘린다.
- 영상에 API 키·홈 경로가 비치지 않게 터미널을 정리한다.
