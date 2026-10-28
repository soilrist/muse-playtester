# STATUS — 바퀴 기록

> 루프의 기억. **최근 것이 위.** 1200줄 넘으면 감독이 `loop/ctl.sh tidy` 로 오래된 것부터 `docs/archive/STATUS-YYYY-MM-DD.md` 로 옮긴다.
> 한 바퀴 = 아래 형식 한 덩어리. 검사는 층마다 **통과 / 실패 / 못 함** 중 하나로 (못 한 걸 통과라 쓰지 않는다).
> **"지금 상태" 는 일지가 아니라 현황판** — 15줄 이내, 덧붙이지 말고 바뀐 줄만 고쳐 쓴다 (25줄을 넘으면 루프 커밋이 거절된다). 한 일은 아래 바퀴 기록에. 감독이 직접 한 일도 `## #감독 · 날짜 · 요지` 덩어리로 아래에.

## 지금 상태 (루프가 매 바퀴 고쳐 씀, 감독이 바로잡을 수 있음)
- 마일스톤: D1 골격 — 2/3 조각 (설치 세션이 저장소·문서만 세움, `src/` 비어 있음)
- 브랜치: develop
- 다음 조각: INBOX 지시 capture (D1-03)
- 막힌 것: 없음
- 사람만 할 수 있는 것(`[!] 사람:`): D7 데모 영상 촬영·제출 / 화면 기록·접근성 권한(캡처·키 입력 첫 실행 때)
- 사람 답 기다리는 것: 🔴 0개 / 🟡 가정 0개 / 안 채운 숫자 0개
- 비용: $0.0012 / 상한 $3 (`logs/api_usage.csv` 1줄)
- 감독이 눈으로 봐야 할 것(일꾼이 `못 함 — 감독` 으로 넘긴 칸): 없음

---

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
