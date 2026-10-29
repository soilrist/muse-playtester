# INBOX

> 형식·종류: `docs/conventions/InboxFormat.md` · **맨 위가 최우선 · 끝나면 즉시 삭제**
> `- [ ] <종류>(작성자, YYYY-MM-DD HH:MM) **요지.** 본문 … 검증: … / 삭제: …`

<!-- 여기 아래에 적는다 -->
- [ ] 결함(감독, 2026-10-29 17:50) **note 강제가 끼임마다 걸려 60수 중 20수를 note 가 먹었다 — 18줄이 "키 무반응" 같은 말.** runs/20261029-172210: 19수부터 주인공이 로한 왼쪽 위에 갇힘(019·059 프레임 위치 거의 같음), same_screen 이 19·21·23…59 로 2수마다 다시 쏨. 원인: probe_keys 가 방향만 바꿔 화면을 바꾸니 judge 의 '같은 화면 구간'이 끊겨 '구간마다 한 번' 이 안 막는다 → want_note 도 매번. 고칠 곳 run.py: note 를 마지막으로 남긴 수 `last_note` 를 기억하고, 강제(same_screen 직후든 NOTE_EVERY 든)는 `n - last_note >= NOTE_EVERY` 일 때만. 모델이 스스로 고른 note 도 last_note 를 갱신한다. **예산 $6.62/$7 — VM run 금지.** 검증: selftest 에 '2수마다 same_screen 이 나는 가짜 세션 30수' 를 넣어 only_note=True 가 ≤3번 / 삭제: 커밋 후
