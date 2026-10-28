# INBOX

> 형식·종류: `docs/conventions/InboxFormat.md` · **맨 위가 최우선 · 끝나면 즉시 삭제**
> `- [ ] <종류>(작성자, YYYY-MM-DD HH:MM) **요지.** 본문 … 검증: … / 삭제: …`

<!-- 여기 아래에 적는다 -->
- [ ] 결함(감독, 2026-10-28 15:48) **capture 가 가려진 창을 찍는다.** 감독이 직접 Godot 를 띄우고 `src/capture.py` 를 돌림 → 창은 찾았으나(480x392) 다른 앱 창이 위에 있어 그 화면이 찍힘(mss 는 화면 영역만 자른다). 고칠 것: ① 캡처 전에 Godot 를 앞으로(`AppKit.NSRunningApplication.runningApplicationWithProcessIdentifier_(pid).activateWithOptions_(...)`, pid 는 창 정보 `kCGWindowOwnerPID`) + 짧게 대기 ② 찍기 직전 `CGWindowListCopyWindowInfo` 의 layer 0 첫 창이 Godot 인지 확인, 아니면 RuntimeError(틀린 그림 저장 금지) ③ 시험할 땐 일꾼이 직접 `~/Applications/Godot.app/Contents/MacOS/Godot --path ~/Git\ Project/breath-of-the-abyss &` 로 띄우고 끝나면 종료 ④ 같은 실행에서 `Quartz.CGPreflightScreenCaptureAccess()` 값을 STATUS 에 적는다 — False 면 `[!] 사람: 화면 기록 권한` 으로 올린다. 검증: `captures/` PNG 를 열어 게임 화면인지 3층으로 확인 / 삭제: 캡처가 게임 화면이면.
- [ ] 지시(설치세션, 10-28) **capture 작성.** Godot 창 1장 PNG. 검증: captures/ 파일 존재 + 사람이 열어볼 수 있게 경로를 STATUS 에.
- [ ] 막힘(루프#3, 2026-10-28 15:40) **화면 기록 권한 없음 — capture 검증 불가.** `CGPreflightScreenCaptureAccess()`=False. 시스템 설정 > 개인정보 보호 > 화면 및 시스템 오디오 기록에서 이 루프를 돌리는 터미널(또는 Claude)을 켜고 재시작 필요. 켜지면 `.venv/bin/python src/capture.py captures/sample-d1-03.png` 로 확인. / 삭제: 권한 켜고 capture 검증 후
