# STATUS — 바퀴 기록

> 루프의 기억. **최근 것이 위.** 1200줄 넘으면 감독이 `loop/ctl.sh tidy` 로 오래된 것부터 `docs/archive/STATUS-YYYY-MM-DD.md` 로 옮긴다.
> 한 바퀴 = 아래 형식 한 덩어리. 검사는 층마다 **통과 / 실패 / 못 함** 중 하나로 (못 한 걸 통과라 쓰지 않는다).
> **"지금 상태" 는 일지가 아니라 현황판** — 15줄 이내, 덧붙이지 말고 바뀐 줄만 고쳐 쓴다 (25줄을 넘으면 루프 커밋이 거절된다). 한 일은 아래 바퀴 기록에. 감독이 직접 한 일도 `## #감독 · 날짜 · 요지` 덩어리로 아래에.

## 지금 상태 (루프가 매 바퀴 고쳐 씀, 감독이 바로잡을 수 있음)
- 마일스톤: D6-02 README 부분(run.py 대기), D1 골격 3/3 완료, D2-01 perceive·D3-01 decide 코드 완료(2층 jev 미확인), D3-02 act 완료(키 입력 후 화면 바뀜 확인), D4-01 judge·D4-02 report·D6-04 notes·D6-01 viewer·D6-03 영상 대본 완료, D3-03 run.py 10수 재실측 대기(#22 은 log 없음 불합격 → log.jsonl 코드 #23), D5-03 note→playtest_notes 연결 코드 완료(실측 못 함)
- 브랜치: develop
- 다음 조각: INBOX 결함 3번(decide 프롬프트: 안내문 읽기·삭제 확인창 esc) → D3-03 새 실측 10수 → D4-03, D2-02 SAM 10장
- 막힌 것: 없음 — 키 주입 #7 해소
- 사람만 할 수 있는 것(`[!] 사람:`): D7 데모 영상 촬영·제출 / 접근성 권한(키 입력 첫 실행 때)
- 사람 답 기다리는 것: 🔴 0개 / 🟡 가정 0개 / 안 채운 숫자 0개
- 비용: 상한 $3 안 (`logs/api_usage.csv` 42줄, 10수 Spark 10회·SAM 20장)
- 감독이 눈으로 봐야 할 것(일꾼이 `못 함 — 감독` 으로 넘긴 칸): 없음

---

## #23 · 2026-10-28 · D3-03 log.jsonl + D4-01 same_screen 오탐 보정
- 계획: D3-03·D4-01 · INBOX 결함 1·2번(맨 위부터, 3번은 바퀴당 조각 2개 제한으로 다음 바퀴) · src/run.py, src/judge.py, bugs/ · 근거 DESIGN §4.8·§6.4
- 한 것: run.py 가 수마다 `runs/<시각>/log.jsonl` 에 수·t·Scene 요약·툴 이름과 인자·캡처 경로·judge 결과를 쓰고 summary.md 에서 링크. judge `same_screen` 은 구간당 1개만, 이동 키에 화면이 한 번도 반응 안 한 세션이면 안 쏜다. 처음 정한 "SAM 에 player 없음" 기준은 쓸 수 없었다 — 저장 frames 10장 전부 `player character` 1개로 잡혔다(타이틀 일러스트 인물, 001.png 직접 열어 확인). 그래서 응답 기준으로 바꾸고 DESIGN §6.4 에 적었다. `bugs/0001~0008` 삭제(git rm) + INDEX 정리. judge selftest 가 이미 깨져 있어(없는 `public-after-import.png` 를 엶) `priv-b0.png` 로 고쳤다
- 커밋: af6def0 feat(run), a20cf5e fix(judge)
- 검사: 1층 통과(`python3 -m py_compile src/run.py src/judge.py` → `compiled`) / 2층 통과(`judge selftest ok`, `run selftest ok` — log.jsonl 3줄·캡처 경로 실재 검증 포함, jev 둘 다 SUPPORTED. 저장 frames 001~010 을 SAM 재인식해 mtime·키(w d s a space e w d s a)로 judge 에 재생 → `findings: []`) / 3층 해당 없음(화면 없음)
- 플레이어 눈: 해당 없음(도구)
- 점검한 규칙: 3(자기 파일만 add), 11, 15(게임 안 띄움, SAM 10장만 호출 ≈$0.05 x2 재생, 세이브 안 건드림), 5(규칙 문서 안 고침)
- 못 한 것: 새 run 의 log.jsonl 10줄 실측은 안 했다(게임 실행 필요, decide 보정 후 한 번에). `bugs/000N-*` 빈 폴더 8개가 디스크에 남음(`rm` 거부됨; 추적 안 되는 빈 폴더라 git 에는 없음)
- INBOX 처리: 결함 2번(오탐 8개) 삭제. 결함 1번(log)은 새 실측 10줄 확인 때까지 유지. 결함 3번 남음
- 다음: decide 프롬프트 보정(결함 3) → D3-03 새 실측으로 log.jsonl 10줄과 타이틀 탈출 확인

## #22 · 2026-10-28 · D3-02 합격 + D3-03 실제 10수
- 계획: D3-02·D3-03 · INBOX 답(감독) 1번 · 코드 변경 없음, 실행·확인 · 근거 DESIGN §4.5·§4.8
- 한 것: 게임을 띄워 `act.press("down",150)` 전후 캡처 비교 → 해시 달라짐, `captures/tmp/d302-0.png`(커서 새 게임)→`d302-1.png`(커서 이어하기) 직접 열어 확인. 이어 `PT_MAX_ACTIONS=10 .venv/bin/python src/run.py` → `session end: action limit (10 steps)`, frames 10장, 세이브 폴더 `diff -r` 백업과 일치(복원됨)
- 발견: Spark 가 타이틀에서 w·d·s 만 눌러 메뉴를 못 벗어남(Enter 안 누름). 10수째 `runs/20261028-194618/frames/010.png` 에 "슬롯1(Lv16) 기록을 지운다. 한 번 더 누르면 진행" 경고가 떴다(세이브 삭제 확인창 — 복원돼 무사). judge `same_screen` 8건(bugs/0001~0008)은 메뉴에서 이동키 후 화면이 안 바뀐 것 → 오탐 성격
- 커밋: 이 STATUS 커밋에 ROADMAP·INBOX·bugs 리포트 포함
- 검사: 1층 해당 없음(코드 변경 없음) / 2층 통과(세션 실행 `session end: action limit (10 steps) -> .../runs/20261028-194618`, frames 10장) / 3층 통과(본 그림: captures/tmp/d302-0.png, d302-1.png, runs/20261028-194618/frames/010.png)
- 플레이어 눈: 해당 없음(도구)
- 점검한 규칙: 15(백업 후 실행, 복원 diff 확인, 키는 pynput), 11, 3. 실행은 시스템 python3 이 아닌 `.venv` 로 해야 한다(requests)
- INBOX 처리: 답 삭제
- 다음: judge same_screen 이 메뉴·타이틀에서 오탐하지 않게 보정, decide 가 Enter 로 타이틀을 벗어나게(프롬프트) — 그 뒤 게임플레이 SAM 10장

## #21 · 2026-10-28 · D3-03 대상 교체 + 세이브 보호
- 계획: D3-03 · INBOX 지시 1·2번(맨 위) · src/run.py · 근거 DESIGN §6
- 한 것: GAME 을 zerostudyrpg-snapshot 으로, SAVE_DIR 백업(backup_saves)·복원(restore_saves)을 main 의 try/finally 로 감쌌다. 게임 종료 후 wait 추가
- 커밋: 05771fb feat(run)
- 검사: 1층 통과(`python3 -m py_compile src/run.py` 오류 없음) / 2층 통과(`run selftest ok`, jev SUPPORTED, 가짜 폴더 백업→변경→복원→`diff -r` 일치) / 3층 해당 없음(화면 없음). `grep -rn breath-of-the-abyss src/` 0줄
- 점검한 규칙: 3(자기 파일만 add), 15(백업 없이 게임 안 띄움, 게임 미실행), 11. 실제 세이브 폴더로는 실행하지 않았다
- INBOX 처리: 지시 2개 삭제. 답(키 주입 재현 안 됨, D3-02 재개)은 D3-02 합격 확인 때 삭제
- 다음: D3-02 2층 확인(`act.py down 150`) → D3-03 실제 10수

## #20 · 2026-10-28 · 막힘 기록 · 루프 정지
- 계획: 없음 · INBOX 에 루프 몫·`→루프` 줄 없음, ROADMAP `[ ]` 12개 전부 키 주입(#7)·게임플레이 장면(#8)을 기다림 → ④-2-4 막힘 기록
- 한 것: 막힌 조각을 의존 순으로 세워 기록하고 loop/STOP 을 만든다. 코드는 건드리지 않았다
- 막힘: 사람 답 필요 1개 (1순위: 키 주입 확인 — D3-02 2층 → D3-03·D2-02·D4-03·D5-01~03 이 기다림, 마일스톤 D2·D3·D4·D5 네 개). 감독이 사람 터미널에서 `python src/act.py down 150` 후 메뉴 커서 이동을 확인해 달라고 요청하고 다시 켠다
- 검사: 해당 없음(문서만)
- 점검한 규칙: 11(돌리지 않은 것을 통과라 쓰지 않음), 15(API 호출 없음), ④-2-4. `captures/public-after-import.png` 는 내 파일이 아니라 건드리지 않음
- 다음: 키 주입 해소 뒤 `python src/run.py` 로 10수 실측

## #19 · 2026-10-28 · D6-02 README 현행화
- 계획: D6-02 · INBOX 루프 몫 없음, 남은 `[ ]` 는 전부 키 주입 #7 에 막혀 오프라인으로 할 수 있는 README 부분만 · README.md · 근거 ROADMAP D6-02
- 한 것: README 의 "run.py 아직 없음" 문구를 현재 상태(자체검사 통과, 실제 60수는 미검증)로 고치고 실행 줄 주석을 바로잡았다
- 커밋: docs(readme) 한 개 + docs(status) 한 개
- 검사: 1층 해당 없음(문서만) / 2층 못 함 — 새 사람이 3줄로 실행되는지는 실제 세션을 못 돌려 확인 못 함 / 3층 해당 없음
- 플레이어 눈: 해당 없음
- 점검한 규칙: 11(돌리지 않은 것을 통과라 쓰지 않음), 14(D6-02 는 ROADMAP 에 있음), 15(API 호출 없음)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. `captures/public-after-import.png` 는 내 파일이 아니라 건드리지 않음
- INBOX 처리: 루프 몫 없음
- 다음: 키 주입 확인 뒤 `python src/run.py` 로 10수·60수 실측

## #18 · 2026-10-28 · D5-03 note 연결
- 계획: D5-03 · 남은 `[ ]` 중 키 주입 #7 에 안 막힌 코드 부분 · src/run.py · 근거 DESIGN §4.4·§4.10 (decide.py 에는 note 툴이 이미 있었고 run.py 가 무시하고 있었다)
- 한 것: run.py 가 `note` 를 수 번호·캡처 경로와 함께 모으고, 세션 끝에 notes.summarize → write_notes 로 `runs/<시각>/playtest_notes.md` 를 쓴다. 노트가 없으면 Spark 를 부르지 않는다. 정리 실패는 종료 이유 뒤에 덧붙이고 세션 기록은 남긴다
- 커밋: feat(run) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `compile_exit=0` / 2층 못 함 — 자체검사 `run selftest ok`, `notes selftest ok`(jev SUPPORTED)는 가짜 입력으로 note→playtest_notes.md 연결만 본 것이고, 합격 기준인 실제 60수 세션에서 note 가 로그에 남는지는 돌리지 않았다(키 주입 #7) / 3층 해당 없음
- 플레이어 눈: 해당 없음
- 점검한 규칙: 11(실제 출력만 인용, 실제 세션은 못 함), 14(D5-03 은 ROADMAP 에 있는 조각), 15(API 호출 안 함, 키 없음). 시스템 python3 에는 requests 가 없어 `.venv/bin/python` 으로 돌렸다
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. `captures/public-after-import.png` 는 내 파일이 아니라 건드리지 않음
- INBOX 처리: 루프 몫 없음
- 다음: 키 주입 확인 뒤 `python src/run.py` 로 10수·60수 실측(D3-03·D5-01·D5-03 2층). 그 전엔 오프라인으로 할 `[ ]` 가 없다

## #17 · 2026-10-28 · D3-03 run.py
- 계획: D3-03 · ROADMAP 첫 `[ ]` 중 코드로 쓸 수 있는 조각(D2-02·D3-02 2층·D4-03 은 키 주입 #7 에 막힘) · src/run.py · 근거 DESIGN §3.2·§4.8
- 한 것: `run_session(ports, ...)` — 수마다 capture→perceive→decide→act→judge, 종료 이유 5종(done·행동/Spark/SAM 상한·예외)을 summary.md 에, judge/Spark `report_bug` 는 bugs/ 리포트로. 실제 모듈은 `default_ports()` 로, 자체검사는 가짜 입력으로. SAM 은 judge 가 쓰는 2종(player character·health bar)만 물어 60수 x 2장 = 상한 120 에 맞춤
- 커밋: feat(run) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `py_compile src/run.py exit=0` (jev SUPPORTED) / 2층 못 함 — 자체검사 `run selftest ok`(jev SUPPORTED)는 가짜 입력으로 종료 조건·리포트·예외 기록만 본 것이고, 합격 기준인 실제 키 입력 10수는 돌리지 않았다(키 주입 #7) / 3층 해당 없음
- 플레이어 눈: 해당 없음
- 점검한 규칙: 11(실제 출력만 인용, 못 한 2층은 못 함), 14(조각 밖 안 건드림), 15(게임 폴더는 실행만, 키 값 없음, API 호출 안 함)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. `captures/public-after-import.png` 는 내 파일이 아니라 건드리지 않음
- INBOX 처리: 루프 몫 없음
- 다음: 키 주입 확인 뒤 `python src/run.py` 로 10수 실측(D3-03 2층). 그 전엔 오프라인으로 할 `[ ]` 가 없다

## #16 · 2026-10-28 · D6-03 영상 대본
- 계획: D6-03 · ROADMAP 의 첫 `[ ]` 중 오프라인으로 되는 조각(D2~D5 는 키 주입 #7·#8 에 막힘) · docs/specs/demo-script.md · 근거 DESIGN §0·§7
- 한 것: 180초 8장면 표(시간·화면·영어 내레이션·재료 준비 조각). 아직 없는 재료(run.py·끼임 재현)는 표에 명시, 비용 숫자는 실측으로 바꾸라고 적음
- 커밋: docs(demo) 한 개 + docs(status) 한 개
- 검사: 1층 해당 없음(문서) / 2층 `python3 tools/check_conventions.py` 결과: 통과 (오류 0 / 경고 0 / 미정 숫자 0) / 3층 해당 없음
- 점검한 규칙: 11(출력 그대로 인용), 14(조각 밖 안 건드림), 15(키 값 안 적음)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음
- INBOX 처리: 루프 몫 없음
- 다음: D3-03 run.py (키 주입 #7 확인 필요)

## #15 · 2026-10-28 · D6-02 README (부분)
- 계획: D6-02 · ROADMAP 의 첫 `[ ]` 중 오프라인으로 되는 조각(D2~D5 는 키 주입 #7·#8 에 막힘) · README.md · 근거 DESIGN §0
- 한 것: How to run 을 실제 있는 것에 맞췄다 — 키 설정·권한·viewer 여는 법·Status 절 추가. `src.run` 은 아직 없어서(D3-03 전) "not merged yet" 로 솔직히 표시. 그래서 합격 "새 사람이 실행 가능" 은 run.py 가 생길 때까지 `[ ]` 로 둔다
- 커밋: docs(readme) 한 개 + docs(status) 한 개
- 검사: 1층 해당 없음(문서) / 2층 통과 — `viewer_build selftest ok`, `report selftest ok`, `notes selftest ok` / 3층 해당 없음. `check_conventions.py` 결과: 통과 (오류 0 / 경고 0 / 미정 숫자 0)
- 점검한 규칙: 11(출력 그대로 인용), 14(조각 밖 코드 안 건드림), 15(키 값 안 적음)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음
- INBOX 처리: 루프 몫 없음
- 다음: D6-03 영상 대본, 그 뒤 D3-03 run.py. run.py 가 생기면 README 첫 줄 표시를 지우고 D6-02 `[x]`

## #14 · 2026-10-28 · D6-01 viewer
- 계획: D6-01 · ROADMAP 의 `[ ]` 중 D2~D5 는 키 주입(#7·#8) 에 막혀 오프라인으로 되는 첫 조각 · src/viewer_build.py + viewer/index.html · 근거 DESIGN §4.9
- 한 것: 정적 페이지는 폴더 목록을 못 읽으므로 `viewer_build.py build` 가 `bugs/INDEX.md` 표와 `runs/*/summary.md` 를 HTML 한 장에 박는다(최근 세션이 위, 소감 파일이 있으면 링크, 모든 글자는 html.escape). 리포트·세션 링크는 `../bugs/…`·`../runs/…` 상대경로
- 커밋: feat(viewer) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `py_compile src/viewer_build.py exit=0` (jev SUPPORTED, p=0.87) / 2층 통과 — 버그 1줄(제목에 `<in>`)·세션 2개로 빌드해 표·정렬·이스케이프·소감 링크를 확인하는 자체검사 `viewer_build selftest ok` (jev SUPPORTED, p=0.94) / 3층 headless Chrome 으로 `captures/tmp/viewer-empty.png` 를 열어 봄: 제목·"Bug reports (0)"·"Sessions (0)" 빈 상태 문구가 보인다. 리포트가 있는 화면은 못 찍음(실제 리포트 없음, 자체검사로 대신). `check_conventions.py` 결과: 통과 (오류 0 / 경고 0 / 미정 숫자 0)
- 플레이어 눈: 처음 보는 심사자가 열면 제목·두 목록이 바로 보인다. 다만 리포트 링크는 저장소 루트에서 열어야 이어지고, `frames/` 는 깃 제외라 이미지는 로컬에서만 보인다
- 점검한 규칙: 11(출력 그대로 인용), 12(렌더 결과·화면으로 확인), 15(src/ 안, 모델 호출 없음)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음
- INBOX 처리: 루프 몫 없음
- 다음: 남은 오프라인 조각 D6-02 README 마무리 → D6-03 영상 대본. D6-01 은 리포트가 생기면 `viewer_build.py build` 를 다시 돌려 갱신한다. 참고: #12·#13 은 STATUS 에 기록이 없다

## #11 · 2026-10-28 · D6-04 playtest_notes
- 계획: D6-04 · ROADMAP 의 `[ ]` 중 D2~D5 는 키 주입(#7·#8) 때문에 막혀 오프라인으로 되는 첫 조각 · src/notes.py (새 파일, report.py 와 역할이 달라 분리) · 근거 DESIGN §4.10

- 한 것: `notes.py` — `keep_grounded` 가 수 번호≥1 + 실제 있는 캡처 파일 + 장르 비교·제안이 있는 것만 남기고 3개로 자른다. `write_notes` 가 `playtest_notes.md` 를 쓴다(남긴 수·버린 수 반환). `summarize` 는 Spark 1회로 note+수 기록을 JSON 개선점으로 받는다(코드만, 실호출 안 함)
- 커밋: feat(notes) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `py_compile src/notes.py exit=0` (jev SUPPORTED, p=0.88) / 2층 통과 — 근거 없는 4건(수 0·없는 파일·장르 빈칸)을 버리고 3건만 남기는 자체검사 `notes selftest ok` (jev SUPPORTED, p=0.89). `summarize` 의 Spark 실호출은 못 함 / 3층 해당 없음(제품 내부 도구). `check_conventions.py` 결과: 통과 (오류 0 / 경고 0 / 미정 숫자 0)
- 플레이어 눈: 해당 없음
- 점검한 규칙: 11(출력 그대로 인용), 12(파일 존재 여부로 근거 판정), 15(이번 바퀴 모델 호출 없음, src/ 안)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음
- INBOX 처리: 루프 몫 없음
- 다음: D5-03·D2~D4 는 키 주입(#7·#8) 해소가 필요. 오프라인으로 되는 건 D6-01 viewer/ 정적 HTML

## #10 · 2026-10-28 · D4-02 report
- 계획: D4-02 · ROADMAP 첫 `[ ]` D2-01·D2-02·D3-0x 는 키 주입/게임플레이 장면 필요로 건너뜀 → 저장된 입력으로 되는 D4-02 · src/report.py · 근거 DESIGN §4.7
- 한 것: `write_report(Bug)` 가 `bugs/<4자리>-<slug>/report.md` + `frames/` 복사 + `bugs/INDEX.md` 한 줄을 쓴다. 필수 칸(제목·심각도·재현 순서·기대·실제·근거 프레임·판단 근거)이 비거나 심각도가 low/medium/high 가 아니면 ValueError. 번호는 기존 폴더 최댓값+1
- 커밋: feat(report) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `py_compile src/report.py exit=0` (jev SUPPORTED, p=0.93) / 2층 통과 — 임시 폴더에 리포트 2건·잘못된 입력 2건 자체검사 `report selftest ok` (jev SUPPORTED, p=0.9) / 3층 해당 없음(제품 내부 도구). `check_conventions.py` 결과: 통과 (오류 0 / 경고 0 / 미정 숫자 0)
- 플레이어 눈: 해당 없음
- 점검한 규칙: 11(출력 그대로 인용), 12(파일 존재·내용으로 확인), 15(모델 호출 없음, src/ 안)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. 플레이 소감(§4.10 playtest_notes.md)은 D5~D6 몫이라 이번엔 안 만듦
- INBOX 처리: 루프 몫 없음
- 다음: D4-03 은 run.py 필요 — D3-03 키 주입 문제(#7·#8) 해소 전이면 계획 바퀴/사람 확인 필요

## #9 · 2026-10-28 · D4-01 judge
- 계획: D4-01 · ROADMAP 첫 `[ ]` 인 D2-01·D2-02 는 키 주입 불가로 게임플레이 장면이 없어 건너뜀(#8 다음 항목) · src/judge.py · 근거 DESIGN §4.6·§6.4
- 한 것: `Judge.check(Step)` 이 4규칙을 본다 — 검은 화면(밝기 ≤8, 2수 연속) / 같은 화면(이동 키를 눌렀는데 10초 넘게 같음) / HP바 소실 / 플레이어 소실(직전 수엔 있었고 지금 0개). 인식 실패·scene 없음은 「모름」으로 보고 소실로 치지 않는다
- 커밋: feat(judge) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `py_compile judge exit=0` (jev SUPPORTED, p=0.79) / 2층 통과 — 저장된 캡처(`captures/sample-d1-03.png`, `public-after-import.png`)와 합성 검은 그림으로 규칙 8건 자체검사 `judge selftest ok` (jev SUPPORTED, p=0.88) / 3층 해당 없음(제품 내부 도구). `check_conventions.py` 결과: 통과 (오류 0 / 경고 0 / 미정 숫자 0)
- 플레이어 눈: 해당 없음
- 점검한 규칙: 11(출력 그대로 인용), 12(문자열이 아니라 그림 픽셀로 판정), 15(모델 호출 없음, 게임 폴더 수정 없음)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. `SAME_DIFF=1.0`(그림 평균 차이)은 코드 상수 — 실제 게임플레이 캡처로 D4 에서 재조정 필요
- INBOX 처리: 루프 몫 없음
- 다음: D4-02 report.py

## #8 · 2026-10-28 · D2-01 perceive
- 계획: D2-01 · ROADMAP 첫 `[ ]` (INBOX 루프 몫 없음) · src/perceive.py + src/meta_client.py(`call_sam`) · 근거 DESIGN §4.3, 문서 dev.meta.ai/docs/media-segmentation·sam/reading-segmentation·sam/segmenting 을 WebFetch 로 읽음
- 한 것: `call_sam`(sam-3.1, `input_image` data URL, `stream:false`, `include_confidence`) 추가. `perceive.py` 는 7종을 한 번에 한 종류씩 SAM 에 보내 `<|box;x1..y2;c|>` 토큰만 파싱해 `Scene`(종류별 `Box` 목록·오류·`summary()`)을 만든다. 종류 하나가 실패해도 나머지 계속(Spark 폴백은 D2-02 결과를 본 뒤 정함)
- 커밋: feat(perceive) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `py_compile perceive+meta_client exit=0` (jev SUPPORTED, p=0.72) / 2층 못 함 — `captures/public-after-import.png`(메뉴 화면)에 7종 모두 실행해 출력은 나왔으나 전부 `[]`(`detected: nothing`). 메뉴에 해당 물체가 없어 맞는 결과로 보이지만 jev 가 "7종 출력"·"박스 파싱" 인용을 둘 다 NOT_SUPPORTED 로 판정해 통과라고 쓰지 않는다. 대신 파이프라인 확인: 같은 그림에 `moon` 을 물으니 박스 (338,94)-(429,185) 신뢰도 0.93 이 왔고 그림을 열어 보니 달 위치와 일치. 파서 자체검사(`perceive selftest ok`, jev SUPPORTED p=0.91) / 3층 해당 없음(제품 내부 도구)
- 플레이어 눈: 해당 없음
- 점검한 규칙: 11(jev NOT_SUPPORTED 를 통과로 안 씀), 12(문자열이 아니라 그림 위치로 박스 확인), 15(키는 파일에서만 읽고 출력 안 함, 게임 폴더 수정 없음, SAM 8회 $0.02 로 상한 안)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. `captures/public-after-import.png` 는 내 파일이 아니라 건드리지 않았다(읽기만)
- INBOX 처리: 루프 몫 없음
- 다음: D2-02 는 게임플레이 장면 10장이 필요한데 지금은 키가 Godot 에 안 닿아(#7) 메뉴 화면만 찍힌다. 감독이 키 주입 되는 환경을 확인해 주기 전에는 D4-01 judge(저장된 캡처로 자체검사) 를 먼저 한다. ROADMAP D2-01 은 2층 jev 미확인이라 `[ ]` 로 두고 주석만 달았다

## #7 · 2026-10-28 · D3-02 act 2층 재확인
- 계획: D3-02 2층 · 지난 바퀴 「다음」 · 코드 변경 없음 · 근거 DESIGN §4.5
- 한 것: Godot 를 띄워 메뉴 화면에서 키 입력 전후 캡처 비교. 맨 앞 창이 Godot 인 것(`front Godot`, 입력 후에도 유지)과 AXIsProcessTrusted True 는 확인. 그런데 pynput `down` 1회·2회(300ms 누름), 창 클릭 후 `down`, Quartz `CGEventPost`(keycode 125) 로 직접 쏜 것까지 네 가지 모두 캡처 그림(`a0`~`a4`, 지움)에서 메뉴 커서가 「새 게임」에 그대로였다. 즉 pynput 문제가 아니라 이 실행 환경(Claude 셸)에서 보낸 키 이벤트가 Godot 에 안 닿는다
- 커밋: docs(status) 한 개
- 검사: 1층 해당 없음(코드 변경 없음) / 2층 못 함 — 커서가 안 움직여 「키 입력 후 캡처가 바뀜」을 통과로 못 씀 / 3층 해당 없음
- 플레이어 눈: 해당 없음
- 점검한 규칙: 11(못 한 검사를 통과로 안 씀), 12(그림 내용으로 판정), 15(게임 폴더 수정 없음, 조작은 키 입력만)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. 원인 후보: 샌드박스가 입력 주입을 막음 또는 Godot 가 키 창이 아님. 샌드박스 해제는 내 권한 밖이라 시도하지 않았다
- INBOX 처리: 루프 몫 없음
- 다음: D2-01 perceive 로 넘어간다. D3-03 run 10수 전에 키 주입이 되는 환경(감독이 사람 터미널에서 `python src/act.py down 150` 후 커서 이동 확인)이 필요하다

## #6 · 2026-10-28 · D3-02 act
- 계획: D3-02 · ROADMAP 첫 `[ ]` (INBOX 루프 몫 없음) · src/act.py · 근거 DESIGN §4.5
- 한 것: `press(key, hold_ms)`·`wait(ms)`·키 이름 변환. 키 누르기 전 게임 창을 앞으로 올리고(최대 3회 재시도) 못 올리면 RuntimeError
- 커밋: feat(act) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `py_compile src/act.py exit=0` (jev SUPPORTED) / 2층 못 함 — 「키 입력 후 캡처가 바뀜」은 해시가 `changed` 였으나 jev NOT_SUPPORTED, 게다가 `captures/act-before.png`·`act-after.png` 를 열어 보니 바뀐 건 배경 입자뿐이고 메뉴 커서는 둘 다 「새 게임」이라 키가 안 들어간 가짜 통과였다. 다시 시험하니 `focus_game` 통과 1초 뒤 맨 앞 창이 Claude 로 되돌아가 캡처가 거절됨(3회 중 3회 반복) / 3층 해당 없음(제품 내부 도구)
- 플레이어 눈: 해당 없음
- 점검한 규칙: 11(해시 변화를 통과로 안 씀), 12(문자열 아닌 그림 내용으로 판정), 15(키 입력은 pynput, 게임 폴더 수정 없음)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. AXIsProcessTrusted 는 True. 검사 그림은 지웠다
- INBOX 처리: 루프 몫 없음
- 다음: D3-02 2층 재확인 — Claude 앱이 앞을 되가져가지 않는 상태(사람이 터미널만 쓰는 때)에서 메뉴 영역 픽셀 비교(커서 이동)로. 실패가 계속되면 `bring_to_front` 를 osascript 방식으로 보강

## #5 · 2026-10-28 · D1-03 capture 가려진 창 결함
- 계획: D1-03 · INBOX 결함 1번(맨 위) · src/capture.py · 근거 DESIGN §4.2
- 한 것: 캡처 전에 `NSRunningApplication.activateWithOptions_` 로 Godot 를 앞으로 + 0.6초 대기, 찍기 직전 layer 0 맨 앞 창 소유자가 Godot 가 아니면 RuntimeError(그림 저장 안 함). 시험은 Godot 를 직접 띄우고 끝나면 종료. 같은 실행 `Quartz.CGPreflightScreenCaptureAccess()` 출력 `True` (권한 있음, `[!] 사람` 불필요)
- 커밋: feat(capture) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `.venv/bin/python -m py_compile src/capture.py exit=0` (jev SUPPORTED) / 2층 못 함 — `saved captures/sample-d1-03.png 480x392` 출력, `exit=0` 이나 jev evidence 가 NOT_SUPPORTED 라 통과로 쓰지 않는다 / 3층 통과 — `captures/sample-d1-03.png` 를 열어 봄: 「심연의 숨결 (DEBUG)」 타이틀 메뉴(새 게임·이어하기·클리어 기록·종료)가 보이고 다른 앱 창은 없음
- 플레이어 눈: 해당 없음(제품 내부 도구)
- 점검한 규칙: 15(게임 폴더 수정 없음, 키 값 없음), 11(jev 불인정 2층을 통과로 안 씀), 13(캡처 파일은 고정 경로, 이번 실행 후 열어 봄)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. 부수: mss.mss 가 deprecated 경고(mss.MSS 권장) — 동작엔 영향 없어 유지
- INBOX 처리: 결함·capture 지시·화면 기록 막힘 3줄 삭제(삭제 조건 충족)
- 다음: D3-02 act.py

## #4 · 2026-10-28 · D3-01 decide
- 계획: D3-01 · D1-03 이 권한으로 막혀 캡처 불필요한 조각으로 넘어감 · src/decide.py, meta_client 에 tools 인자 · 근거 DESIGN §4.4
- 한 것: 공식 문서 tool-calling 을 WebFetch(함수 툴 `{type,name,description,parameters}`, `tool_choice` 는 `auto` 만, 응답 `function_call` 항목의 `arguments` 는 JSON 문자열). `call_text(tools=)`·`function_calls()` 추가, `decide.py` 에 툴 5종과 `decide()` 구현
- 커밋: feat(decide) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `.venv/bin/python -m py_compile src/decide.py src/meta_client.py exit=0` (jev SUPPORTED) / 2층 못 함 — `cd src && ../.venv/bin/python decide.py` 가 `('press', {'hold_ms': 500, 'key': 'w'})` `exit=0` 을 냈으나 jev evidence 가 3번 NOT_SUPPORTED 라 통과로 쓰지 않는다 / 3층 해당 없음
- 점검한 규칙: 11(jev 불인정을 통과로 안 씀), 15(키 출력 없음, 호출 1회 $0.003)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. INBOX.md 에 남의 수정이 있어 건드리지 않음
- 다음: 감독이 D3-01 2층을 위 출력으로 판정 / 권한 켜지면 D1-03

## #3 · 2026-10-28 · D1-03 capture
- 계획: D1-03 · INBOX 지시 capture · src/capture.py · 근거 DESIGN §4.2
- 한 것: `src/capture.py` 작성(Quartz 창 탐색 소유자 Godot + mss 영역 캡처, 폭 1280 이하 PNG). Godot 를 `--path` 로 직접 띄워 시도 → `Quartz.CGPreflightScreenCaptureAccess()` 출력 `False`, 창 제목이 전부 `None` 이고 `find_game_window` 가 None → RuntimeError. 이 터미널에 화면 기록 권한이 없다. 띄운 Godot 는 종료함. 부수 관찰: 게임 `.godot/imported` 가 없어 폰트 로드 오류와 `title.gd:11` 스크립트 오류 로그가 났다(게임 수정 금지라 손대지 않음, 결함 후보)
- 커밋: feat(capture) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `.venv/bin/python -m py_compile src/capture.py` `exit=0` / 2층 못 함 — `.venv/bin/python src/capture.py captures/sample-d1-03.png` 가 `RuntimeError: 게임 창을 찾지 못했다` `exit=1` (권한 없음) / 3층 못 함(캡처 PNG 없음 — 감독 아님, 사람 권한 필요)
- 점검한 규칙: 15(게임 폴더 수정 없음·키 값 없음), 11(못 한 2층을 통과라 쓰지 않음)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. 막힘 1건(사람이 시스템 설정 > 개인정보 > 화면 기록에서 터미널/Claude 허용)
- INBOX 처리: capture 지시는 2층 미검증이라 삭제하지 않고 남김. 막힘 줄 추가
- 다음: 권한이 켜지면 capture 2층·3층 확인 후 D1-03 `[x]`

## #2 · 2026-10-28 · D1-02 meta_client
- 계획: D1-02 · INBOX 지시 1번 · src/meta_client.py, DESIGN §6.3 단가 · 근거 DESIGN §4.1
- 한 것: 공식 문서 4개 WebFetch(quickstart·models·media-segmentation·pricing-rate-limits). 엔드포인트 `POST https://api.meta.ai/v1/responses`, Bearer 키, `{"model","input"}`, usage.input/output_tokens. `call_text`·`output_text` 와 누적 예산 가드, csv 기록 구현. SAM 호출은 스트리밍(SSE) 형식이라 D2 에서 구현. §6.3 단가 기입(Spark 1.25/4.25 per 1M, SAM 2.50 per 1k 이미지)
- 커밋: feat(meta) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `.venv/bin/python -m py_compile src/meta_client.py` 출력 `compiled` / 2층 통과 — `.venv/bin/python src/meta_client.py` 출력 `pong`, `exit=0`; csv `2026-10-28T15:24:12,muse-spark-1.3,text,15,277,0,0.001196,1` (jev evidence SUPPORTED) / 3층 해당 없음(보이는 조각 아님)
- 점검한 규칙: 15(키 값 출력·커밋 없음, 호출은 상한 안), 12(status 필드·csv 로 판단)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음. 세션별 호출 수 상한(PT_MAX_*)은 run.py 에서 센다(client 는 누적 예산만)
- INBOX 처리: meta_client 지시 삭제
- 다음: INBOX capture (D1-03)

## #1 · 2026-10-28 · D1-01 requirements + .venv
- 계획: D1-01 · INBOX 지시 중 meta_client 가 requests 에 의존해 venv 먼저 · requirements.txt, .venv(깃 제외)
- 한 것: requirements.txt(mss, pyobjc-framework-Quartz, pynput, requests, pillow) 작성, `python3 -m venv .venv`(Python 3.15.0), 설치. `src/` 는 아직 비어 있어 만들지 않음
- 커밋: build(deps) 한 개 + docs(status) 한 개
- 검사: 1층 통과 — `.venv/bin/python -c "import mss, Quartz, pynput, requests, PIL; print('ok')"` 출력 `ok`, `exit=0` (jev evidence SUPPORTED) / 2층 못 함(대상 코드 없음) / 3층 해당 없음(보이는 조각 아님)
- 점검한 규칙: 15(저장소 밖 수정 없음, 키 없음), 8(.venv 는 .gitignore 에 있음)
- 가정한 것(🟡): 없음 / 물은 것(🔴): 없음
- INBOX 처리: requirements.txt + .venv 지시 삭제
- 다음: INBOX meta_client (D1-02, WebFetch 필요)
