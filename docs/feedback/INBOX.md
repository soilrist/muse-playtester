# INBOX

> 형식·종류: `docs/conventions/InboxFormat.md` · **맨 위가 최우선 · 끝나면 즉시 삭제**
> `- [ ] <종류>(작성자, YYYY-MM-DD HH:MM) **요지.** 본문 … 검증: … / 삭제: …`

<!-- 여기 아래에 적는다 -->
- [ ] 결정(감독, 2026-10-29 01:40) **D3-01·D2-01 은 감독이 눈으로 판정해 합격 — ROADMAP `[x]` 로 닫는다(jev NOT_SUPPORTED 반복이라 #39 요청).** 감독 실행: `cd src && ../.venv/bin/python decide.py` → `('press', {'key': 'up', …})` rc=0 = 툴 호출 1개. `../.venv/bin/python perceive.py ../runs/20261028-224621/frames/040.png` → 7종 결과 전부 출력. 삭제: ROADMAP 반영 커밋 후
- [ ] 결함(감독, 2026-10-29 01:40) **SAM 프롬프트가 대화창·문을 못 잡고 NPC 를 전부 "player character" 로 센다.** 같은 040.png: 화면 아래 큰 대화창(촌장 로한 대사)과 집 문 3개가 뚜렷한데 `dialog box`·`door`·`npc` 0개, `player character` 8개(로한·세라·두르간·핀·미라까지). D5 60수 전에 할 필요는 없다 — 60수 세션 먼저. 그 뒤: 프롬프트 문구를 바꿔 같은 그림에서 대화창 1·문 ≥1·NPC ≥4 가 잡히는 문구를 찾는다(게임 코드 안 봄, 그림만). 검증: 040.png 에 대해 perceive 출력이 위 수치 / 삭제: 커밋 후
- [ ] 지시(감독←형, 2026-10-29 00:50) **API 예산 상한 $3 → $6 으로 올림(#37 질문 답).** 원문: "올리고 계속진행해라". `meta_client` 기본값·`loop/env.sh` 사전검사·DESIGN 표를 6 으로 바꿔 둠. D5-01·D5-02 60수 세션을 VM(`tools/vm/run_in_vm.sh`)으로 진행. 검증: runs/ 에 60수 세션 summary 종료 이유 = 상한 또는 done / 삭제: 커밋 후
