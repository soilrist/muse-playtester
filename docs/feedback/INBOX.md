# INBOX

> 형식·종류: `docs/conventions/InboxFormat.md` · **맨 위가 최우선 · 끝나면 즉시 삭제**
> `- [ ] <종류>(작성자, YYYY-MM-DD HH:MM) **요지.** 본문 … 검증: … / 삭제: …`

<!-- 여기 아래에 적는다 -->
- [ ] 결함(감독, 2026-10-29 16:15) **D5-02 3회째 전에 SAM 결함(아래 01:40 항목)을 먼저 고친다 — 2회째 run 이 이것 때문에 20수를 구석에서 버렸다.** runs/20261029-155401: probe 힌트는 효과 있음(`right` 24→1회, same_screen 리포트 1건으로 합쳐짐 — 감독 확인). 그런데 40~60수가 전부 `a`·`w` 이고 045·060 프레임에서 주인공이 맵 왼쪽 위 구석(집 왼편)에 붙어 있다. why 는 "촌장 로한이 왼쪽에 있다, 왼쪽으로" — 실제 로한은 주인공의 오른쪽 아래. scene 이 `8 player character` 라 decide 가 누가 주인공인지 모른다. 고칠 것 2개: ① SAM 프롬프트(01:40 항목 그대로) ② same_screen 이 같은 키로 두 번 이상 나면 "'a' pressed here twice, screen unchanged — blocked (wall/map edge) here; go the other way" 힌트를 붙인다(probe 의 '바뀜'은 짧게 눌러 방향만 바뀐 것일 수 있다). 검증: 040.png 에 perceive → player character 1~2, npc ≥4 / 자체검사 assert 1개(같은 키 same_screen 2번 → 힌트 문구) / 삭제: 커밋 후
- [ ] 결함(감독, 2026-10-29 16:15) **note 툴이 60수 2회에서 한 번도 안 쓰였다 — D5-03 미충족.** 두 run 모두 log.jsonl 에 `"tool": "note"` 0줄. decide 프롬프트에 "이상하거나 불편한 점(예: 화살표 키 무반응, 보스 출현 팝업이 갑자기 뜸 — 045.png)을 보면 note 로 남겨라" 를 넣는다. 검증: 3회째 60수 run 에서 note ≥1줄(수 번호·capture 포함) / 삭제: 커밋 후
- [ ] 결정(감독, 2026-10-29 01:40) **D3-01·D2-01 은 감독이 눈으로 판정해 합격 — ROADMAP `[x]` 로 닫는다(jev NOT_SUPPORTED 반복이라 #39 요청).** 감독 실행: `cd src && ../.venv/bin/python decide.py` → `('press', {'key': 'up', …})` rc=0 = 툴 호출 1개. `../.venv/bin/python perceive.py ../runs/20261028-224621/frames/040.png` → 7종 결과 전부 출력. 삭제: ROADMAP 반영 커밋 후
- [ ] 결정(감독, 2026-10-29 02:20) **D5-01 합격 — 감독이 runs/20261029-013454 를 직접 열어 확인.** summary 종료 이유 = action limit, log.jsonl 60줄, frames 60장 전부 960×720 게임 창(사용자 화면 없음), 033·060 은 마을 화면. ROADMAP D5-01 `[x]`. 단 D5-02 나머지 2회는 아래 결함 2건을 고친 **뒤에** 돌린다(예산: 누적 $3.49/$6, 60수 1회 ≈ $0.77 → 남은 돈으로 3회 남짓). 삭제: ROADMAP 반영 커밋 후
- [ ] 결함(감독, 2026-10-29 01:40) **SAM 프롬프트가 대화창·문을 못 잡고 NPC 를 전부 "player character" 로 센다.** 같은 040.png: 화면 아래 큰 대화창(촌장 로한 대사)과 집 문 3개가 뚜렷한데 `dialog box`·`door`·`npc` 0개, `player character` 8개(로한·세라·두르간·핀·미라까지). D5 60수 전에 할 필요는 없다 — 60수 세션 먼저. 그 뒤: 프롬프트 문구를 바꿔 같은 그림에서 대화창 1·문 ≥1·NPC ≥4 가 잡히는 문구를 찾는다(게임 코드 안 봄, 그림만). 검증: 040.png 에 대해 perceive 출력이 위 수치 / 삭제: 커밋 후
