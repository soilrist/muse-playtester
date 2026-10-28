# STATUS — 바퀴 기록

> 루프의 기억. **최근 것이 위.** 1200줄 넘으면 감독이 `loop/ctl.sh tidy` 로 오래된 것부터 `docs/archive/STATUS-YYYY-MM-DD.md` 로 옮긴다.
> 한 바퀴 = 아래 형식 한 덩어리. 검사는 층마다 **통과 / 실패 / 못 함** 중 하나로 (못 한 걸 통과라 쓰지 않는다).
> **"지금 상태" 는 일지가 아니라 현황판** — 15줄 이내, 덧붙이지 말고 바뀐 줄만 고쳐 쓴다 (25줄을 넘으면 루프 커밋이 거절된다). 한 일은 아래 바퀴 기록에. 감독이 직접 한 일도 `## #감독 · 날짜 · 요지` 덩어리로 아래에.

## 지금 상태 (루프가 매 바퀴 고쳐 씀, 감독이 바로잡을 수 있음)
- 마일스톤: D1 골격 — 2/3 조각, D3-01 decide 코드 완료(2층 jev 미확인)
- 브랜치: develop
- 다음 조각: D1-03 capture 2층 검증(권한 켜진 뒤). 권한 없이 가능한 것: D3-02 act.py, D4-01 judge(저장 캡처 필요해 어려움)
- 막힌 것: 화면 기록 권한 없음 → capture 실제 캡처 못 함 (INBOX 막힘)
- 사람만 할 수 있는 것(`[!] 사람:`): D7 데모 영상 촬영·제출 / 화면 기록·접근성 권한(캡처·키 입력 첫 실행 때)
- 사람 답 기다리는 것: 🔴 0개 / 🟡 가정 0개 / 안 채운 숫자 0개
- 비용: $0.0012 / 상한 $3 (`logs/api_usage.csv` 1줄)
- 감독이 눈으로 봐야 할 것(일꾼이 `못 함 — 감독` 으로 넘긴 칸): 없음

---

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
