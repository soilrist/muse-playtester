# INBOX

> 형식·종류: `docs/conventions/InboxFormat.md` · **맨 위가 최우선 · 끝나면 즉시 삭제**
> `- [ ] <종류>(작성자, YYYY-MM-DD HH:MM) **요지.** 본문 … 검증: … / 삭제: …`

<!-- 여기 아래에 적는다 -->
- [ ] 결함(감독, 2026-10-29 17:10) **note 가 60수 3회 내내 0번 — 프롬프트 한 줄(e0bd131 의 (5))로는 안 부른다. D5-03 미충족.** runs/20261029-163724 log.jsonl 에 `"tool": "note"` 0줄인데 same_screen 은 3번(14·40·46수) 났다. 모델은 매 수 툴 1개만 고르니 늘 press 를 고른다. 고칠 곳: (a) decide.py:14 note 설명이 "non-bug player impression" 이라 좁다 — 이상한 점·불편함 전부로 넓힌다. (b) run.py 에서 probe 가 죽은 키를 찾은 바로 다음 수에는 decide 에 `tool_choice` 로 note 를 강제(1회)하거나 힌트에 "이번 수는 note 를 먼저 불러라" 를 넣는다. **예산: 누적 $5.29/$6 — 60수(≈$0.77) 는 못 돌린다.** 검증은 20수 run 1회(≈$0.26)로: log.jsonl 에 note ≥1줄(수 번호·capture 포함). 60수 재실행 금지 / 삭제: 커밋 후
- [ ] 결함(감독, 2026-10-29 17:10) **summary.md 의 리포트 경로가 UNC(`\\Mac\Home\...`) 그대로다.** log.jsonl 은 `_rel` 로 상대 경로가 됐는데 summary.md 리포트 줄은 안 됐다(runs/20261029-163724/summary.md). viewer·다른 기계에서 링크가 깨진다. 같은 `_rel` 를 쓴다. 검증: 기존 summary 하나를 재생성하지 말고 새 20수 run 의 summary.md 에 `\\Mac` 0회 / 삭제: 커밋 후
