# INBOX

> 형식·종류: `docs/conventions/InboxFormat.md` · **맨 위가 최우선 · 끝나면 즉시 삭제**
> `- [ ] <종류>(작성자, YYYY-MM-DD HH:MM) **요지.** 본문 … 검증: … / 삭제: …`

<!-- 여기 아래에 적는다 -->
- [ ] 지시(설치세션, 10-28) **capture 작성.** Godot 창 1장 PNG. 검증: captures/ 파일 존재 + 사람이 열어볼 수 있게 경로를 STATUS 에.
- [ ] 막힘(루프#3, 2026-10-28 15:40) **화면 기록 권한 없음 — capture 검증 불가.** `CGPreflightScreenCaptureAccess()`=False. 시스템 설정 > 개인정보 보호 > 화면 및 시스템 오디오 기록에서 이 루프를 돌리는 터미널(또는 Claude)을 켜고 재시작 필요. 켜지면 `.venv/bin/python src/capture.py captures/sample-d1-03.png` 로 확인. / 삭제: 권한 켜고 capture 검증 후
