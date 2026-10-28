# PlayTester — 설계서

> **이 문서가 제품의 "진짜 답".** 루프는 여기 적힌 것만 만든다. 안 적힌 건 🟡 `확인`(작은 것) 또는 🔴 `질문`(방향).
> 루프는 통째로 읽지 않고 `grep "## 4.2"` 처럼 **절 번호로 범위만** 읽는다 → 절 번호를 바꾸지 말 것.
> 키트 템플릿은 게임용이다. 이 저장소의 제품은 **게임이 아니라 Python 에이전트**라서 §5(콘텐츠)·§7(아트) 는 짧다.

- 버전: 0.1 · 최종 수정: 2026-10-28

---

## 0. 해커톤 규칙 (먼저 읽는다)
- 출품: **Meta Global AI Developer Hackathon · Indie Developer 트랙**
- 제출 마감: **2026-11-05 11:00 KST** · 제출물: 공개 저장소 + 3분 데모 영상
1. **기간 중 새로 만든 것만 보여준다.** `loop/`·`docs/`·`tools/` 는 공개 템플릿(soilrist/loop-starter-kit)이고, 제품 코드는 전부 `src/` 에 있으며 전부 2026-10-28 이후 커밋이다. → `src/` 밖에 제품 코드를 두지 않는다.
2. **메타 모델 필수.** SAM 3.1(인식) + Muse Spark `muse-spark-1.3`(판단·툴 호출).
3. **금지:** 단순 이미지 분석기, 기본 RAG, 의료/영양/교육 챗봇. → PlayTester 는 "보고 → 판단하고 → 손으로 누르고 → 기록하는" **에이전트**다. 이미지 분석만 하고 끝나면 규칙 위반.
4. **점수:** 임팩트 30 / 메타 모델 창의적 활용 25 / 기술 완성도 20 / 데모 25. 보너스 "Best Agentic Use-Case".

## 1. 한눈에
- **한 줄 소개:** 게임을 직접 플레이하면서 버그를 찾아 리포트를 쓰는 AI 에이전트.
- **형태:** macOS 명령줄 도구 (`python -m src.run`). Python 3.11+, `.venv`, `requirements.txt`.
- **테스트 대상 게임:** `~/Git Project/breath-of-the-abyss` — 「심연의 숨결」 공개판(github.com/soilrist/breath-of-the-abyss, `e0c2e3a` 고정 — 대상이 바뀌면 재현이 깨지므로 `git pull` 은 사람 지시 때만). 사람이 비공개 작업본에서 계속 개발 중인 미완성 게임이다 (Godot 4.7, 2D 픽셀 탑다운 RPG, 내부 해상도 320×240, 창 960×720). **읽기·실행만, 수정 금지.** PlayTester 는 게임 코드를 모른다고 가정하고 **화면만 보고** 플레이한다.
- **사용자:** 인디 개발자 — QA 인력 없이 밤새 자기 게임을 돌려 보고 아침에 버그 리포트를 받는다.

## 2. 핵심 가치 (필러)
1. **사람처럼 논다** — 화면 픽셀과 키보드만 쓴다. 게임 내부 함수 호출 금지.
2. **재현 가능한 리포트** — 사람이 읽고 그대로 따라 하면 같은 버그가 난다(입력 순서 + 프레임).
3. **싸고 안전하게 무인으로** — 호출 상한·예산 상한에서 스스로 멈춘다.

## 3. 핵심 루프
### 3.1 한 수 (perceive → decide → act → judge)
캡처(`capture`) → SAM 으로 화면 요소 찾기(`perceive`) → Spark 가 다음 행동 하나 고르기(`decide`) → 키 입력(`act`) → 규칙 기반 이상 감지(`judge`) → 이상이면 리포트(`report`)
### 3.2 한 세션
`run.py` 가 게임을 띄우고 3.1 을 최대 `PT_MAX_ACTIONS` 수 반복 → `done` 툴 호출·상한·예산 초과 중 하나로 종료 → `runs/<시각>/summary.md`
### 3.3 밤새
일꾼 루프가 아니라 사람이 `run.py` 를 여러 번 돌린다(D5 합격 기준: 60수 세션 3회 무인 완주).

## 4. 시스템 (src/ 파일 하나당 역할 하나)
### 4.1 `meta_client.py` — 메타 API
- 키는 `~/.meta-api-key` 또는 환경변수 `META_API_KEY` 에서만 읽는다. **키 값을 로그·출력·커밋에 남기지 않는다.**
- 엔드포인트·요청 형식은 **공식 문서를 WebFetch 로 읽고 쓴다. 추측 금지.** 문서: https://dev.meta.ai/docs/quickstart · https://dev.meta.ai/docs/models · https://dev.meta.ai/docs/media-segmentation
- 호출마다 `logs/api_usage.csv` 에 한 줄: `ts,model,kind,input_tokens,output_tokens,images,cost_usd,ok` (헤더 1줄 포함). 비용 단가는 §6.3.
- 호출 전에 §6.1 상한과 §6.2 예산을 확인하고, 넘으면 예외로 멈춘다.
### 4.2 `capture.py` — 스크린샷
- Quartz(pyobjc) 로 게임 창(소유자 Godot / 제목 「심연의 숨결」)을 찾고 mss 로 그 영역을 캡처. PNG, 폭 1280 이하로 축소.
### 4.3 `perceive.py` — 인식
- SAM 3.1 에 텍스트 프롬프트로 요청, **한 요청에 한 종류**: "player character", "enemy", "health bar", "door", "chest", "npc", "dialog box".
- 결과는 `Scene` 데이터클래스(종류별 박스 목록 + 캡처 경로).
- SAM 이 실패하거나 0개면 Muse Spark 이미지 입력으로 폴백.
### 4.4 `decide.py` — 판단
- `muse-spark-1.3` 툴 호출로 다음 행동 **하나**를 받는다.
- 툴: `press(key, hold_ms)`, `wait(ms)`, `report_bug(title, severity, why)`, `done(reason)`.
- 입력: Scene + 최근 5수 + 목표.
### 4.5 `act.py` — 입력
- pynput 으로 키 입력. 게임 창을 앞으로 가져온 뒤 입력한다. **게임 내부 함수 호출 금지.**
### 4.6 `judge.py` — 이상 감지 (규칙 기반, 모델 호출 없음)
- 같은 화면 N초 지속(§6.4) · HP바 소실 · 플레이어 박스 소실 · 검은 화면.
### 4.7 `report.py` — 리포트
- `bugs/<번호 4자리>-<slug>/report.md` + `frames/`(깃 제외) + `bugs/INDEX.md`(한 줄씩).
- report.md 필수 칸: 제목 · 심각도 · 재현 순서(입력 목록) · 기대/실제 · 근거 프레임 경로 · 판단 근거(judge 규칙 또는 Spark `why`).
### 4.8 `run.py` — 세션
- `~/Applications/Godot.app/Contents/MacOS/Godot --path ~/Git\ Project/breath-of-the-abyss` 로 게임 실행(PATH 에 `godot` 없음) → 3.1 루프 → 종료 조건 → 게임 종료 → `runs/<시각>/summary.md`.
### 4.9 `viewer/` — 정적 HTML (D6)
- `runs/`·`bugs/` 를 읽어 보여주는 정적 페이지. 서버 없음.

## 5. 산출물 목록
| 경로 | 깃 | 내용 |
|---|---|---|
| `logs/api_usage.csv` | 제외 | API 호출 한 줄씩 (§4.1 형식) |
| `captures/` | 포함(샘플만) | D1·D2 확인용 캡처 |
| `runs/<시각>/` | 제외 | 세션 로그·캡처·summary.md |
| `bugs/<번호>-<slug>/report.md` | **포함** | 버그 리포트 (데모·심사용) |
| `bugs/*/frames/` | 제외 | 근거 프레임 |
| `bugs/INDEX.md` | **포함** | 리포트 목록 |

## 6. 숫자 (비용·안전 가드)
> 같은 값을 `loop/env.sh` 의 `PT_*` 와 `src/` 양쪽에 둔다. `src/` 는 환경변수가 있으면 그걸, 없으면 이 표의 기본값을 쓴다.
### 6.1 호출 상한 (세션당)
| 이름 | 값 | 환경변수 | 근거 |
|---|---|---|---|
| 행동 수 | 60 | `PT_MAX_ACTIONS` | 설치 지시(10-28). 3분 데모에 담기는 길이 |
| SAM 이미지 | 120 | `PT_MAX_SAM_CALLS` | 설치 지시. 60수 × 수당 평균 2장 |
| Spark 호출 | 80 | `PT_MAX_SPARK_CALLS` | 설치 지시. 60수 + 폴백·리포트 여유 20 |
### 6.2 예산
| 이름 | 값 | 환경변수 | 근거 |
|---|---|---|---|
| 누적 비용 상한 | 3 | `PT_BUDGET_USD` | 설치 지시. `logs/api_usage.csv` 의 `cost_usd` 합이 넘으면 크레딧 반영 확인 전까지 중단 (감독이 올린다) |
### 6.3 단가
| 이름 | 값 | 단위 | 근거 |
|---|---|---|---|
| Spark 1.3 입력 / 출력 | 1.25 / 4.25 | USD per 1M tokens | https://dev.meta.ai/docs/pricing-rate-limits (Standard mode) |
| SAM 3.1 | 2.50 | USD per 1,000 images | 같은 페이지 |
### 6.4 judge 규칙
| 이름 | 값 | 단위 | 근거 |
|---|---|---|---|
| 같은 화면 지속 | 10 | 초 | 탑다운 RPG 에서 이동 키를 누르는데 10초 동안 화면이 같으면 끼임으로 본다 (D4 에 실제로 재 조정) |
| 검은 화면 | 평균 밝기 8 이하 | 0~255 | 페이드 전환(1초 미만)은 제외하려고 2수 연속일 때만 |

## 7. 화면·데모 방향
- 리포트·README·viewer 는 **영어**(심사용). 내부 문서(docs/)는 한국어.
- 데모 영상 3분: 게임 화면 + 에이전트가 본 박스 오버레이 + 판단 문장 + 생성된 리포트.

## 8. 출력 형식
### 8.1 `runs/<시각>/summary.md`
수 수 · 종료 이유 · SAM/Spark 호출 수 · 비용 · 발견한 버그 링크.
### 8.2 `bugs/INDEX.md`
`| 번호 | 제목 | 심각도 | 세션 |` 표 한 줄씩.

## 9. 기술 결정
- Python 3.11+ · `.venv` · 의존성: mss, pyobjc-framework-Quartz, pynput, requests, pillow
- macOS 전용 (Quartz 창 탐색). 접근성·화면 기록 권한이 필요하다 — 없으면 사람이 시스템 설정에서 켠다(`[!] 사람:`).
- Godot: `~/Applications/Godot.app/Contents/MacOS/Godot` 4.7.2
- 자세한 이유는 `docs/decisions/`

## 10. 범위 밖 (안 만드는 것)
- 게임 코드 읽기·수정·내부 함수 호출 (화면만 본다)
- 「심연의 숨결」 외 다른 게임 지원 (데모 뒤)
- 윈도우·리눅스 지원
- 서버·DB·로그인 (viewer 는 정적 HTML)

## 11. 열린 질문
- 없음
