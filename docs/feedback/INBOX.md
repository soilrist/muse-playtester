# INBOX

> 형식·종류: `docs/conventions/InboxFormat.md` · **맨 위가 최우선 · 끝나면 즉시 삭제**
> `- [ ] <종류>(작성자, YYYY-MM-DD HH:MM) **요지.** 본문 … 검증: … / 삭제: …`

<!-- 여기 아래에 적는다 -->
- [ ] 지시(감독←형, 2026-10-29 17:25) **예산 상한 $7 승인 — 60수 세션 1회를 VM 에서 돌려 D5-03 을 원래 기준(60수)으로 확인한다.** 상한은 loop/env.sh·meta_client.py 둘 다 7 로 감독이 바꿨다. 실행은 `PT_BUDGET_USD=7 tools/vm/run_in_vm.sh` — **명령에 6 을 적지 말 것**(PT_* 는 VM 으로 그대로 실려 가서 6 이면 $6 에서 끊긴다). 누적 $5.80 + 60수 ≈ $0.77 = 약 $6.57. 60수는 이 1회만, 끝나면 새 run 금지. 검증: summary 종료 이유 action limit·60수, log.jsonl 에 note ≥6줄(10·20·…·60수, step·capture 포함), 리포트가 생기면 summary.md 에 `\\Mac` 0회 / 삭제: STATUS 반영 커밋 후
