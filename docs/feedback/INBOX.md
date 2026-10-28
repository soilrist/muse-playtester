# INBOX

> 형식·종류: `docs/conventions/InboxFormat.md` · **맨 위가 최우선 · 끝나면 즉시 삭제**
> `- [ ] <종류>(작성자, YYYY-MM-DD HH:MM) **요지.** 본문 … 검증: … / 삭제: …`

<!-- 여기 아래에 적는다 -->
- [ ] 지시(감독←형, 2026-10-28 19:34) **테스트 대상을 비공개판 고정 복사본으로.** 형 원문: "비공개판으로 바꿔라. 캐처·리포트가 공개 저장소에 올라가도 괜찮다." `src/run.py` 의 `GAME` 을 `Path.home() / "Git Project/zerostudyrpg-snapshot"` 으로 (`07a3d58c` 고정, `.godot/` import 캐시 감독이 이미 만듦). 문서(CLAUDE.md·DESIGN·PROMPT·README)는 감독이 고쳤다. 검증: `grep -rn breath-of-the-abyss src/` 0줄 / 삭제: 커밋 후
- [ ] 지시(감독, 2026-10-28 19:34) **세이브 보호 — 게임 띄우기 전 백업, 끝나면 복원.** 비공개판과 사람 게임이 같은 세이브 폴더 `~/Library/Application Support/Godot/app_userdata/심연의 숨결/` 를 쓴다(Lv56 슬롯 등 사람 세이브). run.py 세션 시작 때 이 폴더를 `backups/userdata-<시각>/` 로 통째 복사하고, 끝날 때 **예외·Ctrl-C 가 나도**(`try/finally`) 원래대로 되돌린다. 감독 백업 `backups/userdata-20261028-193115/` 은 지우지 말 것(`backups/` 는 gitignore). 검증: 가짜 폴더로 백업→파일 변경→복원 후 `diff -r` 일치하는 자체검사 / 삭제: 커밋 후
- [ ] 답(감독, 2026-10-28 19:34) **키 주입 #7 재현 안 됨 — D3-02·D3-03 재개.** 감독이 같은 분리 실행 조건에서 비공개판 타이틀에 `act.py down 150` → 커서 새 게임→이어하기 이동 확인(`captures/priv-b0.png`→`priv-b1.png`). 그때 막힌 건 import 캐시 없는 공개판이었던 탓일 수 있다. 위 두 지시 뒤 D3-02 합격 확인, 이어 D3-03 실제 10수. 검증: `runs/` 에 10수 로그 + 캡처 10장 / 삭제: D3-02 커밋 후
