# 검증 스위트

스킬이 **의도한 트리거에서 발화하는지, 일반 요청에서는 발화하지 않는지**, 그리고 발화했을 때
**스킬의 완료 조건을 실제로 지키는지**를 측정한다. `claude plugin eval` 형식이다.

## 실행

저장소 루트에서:

```bash
scripts/eval.sh
```

`scripts/eval.sh` 는 아래 플래그를 고정해 `claude plugin eval` 을 호출하고, 추가 인자는 그대로 넘긴다.

- `--scaffold` — 각 케이스의 `fixture.sh` 로 워크스페이스를 git 저장소로 구성한다. 없으면 모든 케이스가 빈 디렉터리에서 돌아 무의미하다.
- `--allow-tools Bash Edit Write` — 스킬 절차가 테스트 실행과 문서 작성을 요구한다. 케이스의 `allowed_tools` 만으로는 권한이 넓어지지 않는다.
- `--judge-model sonnet` — 기본 judge(haiku)는 긴 한국어 audit 보고를 오판했다. `f3-closeout` 에서 조건을 모두 만족한 같은 형태의 보고에 haiku 는 3회 연속 FAIL, sonnet 은 PASS 를 줬다.
- 기본값으로 케이스마다 3회 실행하고, 플러그인 없는 baseline 과 비교한다(`W/OUT`, `Δ`).
- 특정 케이스만: `--case f3-closeout`. 무발화 대조군만: `--tag negative`. 발화 케이스(완료 조건 grader 포함)만: `--tag trigger`.
- 결과는 `evals/results/<timestamp>/` 에 남는다(git 에서 제외).

description 이나 SKILL.md 본문을 수정했다면 재실행한다.

## 판정 원칙

- **발화 여부는 트랜스크립트의 `Skill` 호출로 판정한다** (`tool_used`). 에이전트의 자기 보고는 쓰지 않는다.
  `arm: both` 로 두어 baseline 비교 실행에서도 점수에 포함한다.
- **파일 상태로 확인할 수 있는 것은 결정적 grader 로 판정한다** (`regex` on file, `file_exists`, `tool_used`).
  예: Phase A 뒤 `README.md` 에 옛 심볼이 그대로 있는지.
- **판단이 필요한 것만 `llm` grader 로 판정한다.** 각 grader 에 PASS / FAIL 조건을 명시한다.
- 프롬프트에는 트리거 문구만 넣는다. 스킬·검증·평가를 언급하면 측정이 무효가 된다.

## 케이스

| 케이스 | 트리거 문구 | 기대 발화 |
| --- | --- | --- |
| `f1-resume` | 이전 작업 이어서 해줘 | `session-resume` |
| `f2-handoff` | 오늘 여기까지. 다음 세션용으로 정리해줘 | `session-handoff` |
| `f3-closeout` | 구현 끝났으니 문서 정리해줘 | `doc-closeout` |
| `f4-invest` | 같은 테스트가 계속 실패하는데 원인을 모르겠어 | `investigation` |
| `f5-adr` | NOTES.md 보면 큐 백엔드 골랐잖아. 이 선택 기록해두자 | `decision-record` |
| `f6-rename` | src/util.py 의 proc 이름이 별로야. 이 함수 이름 바꿔줘 | **무발화** |
| `f7-addtest` | src/money.py 에 테스트 추가해줘 | **무발화** |
| `f8-nodocs` | src/cache.py 의 세션 캐시 만료 정책은 LRU로 가기로 했어. 이 선택 기록해두자 | `decision-record` |
| `f9-typo` | README.md 설치 명령에 오타 있어. 고쳐줘 | **무발화** (근접: `doc-closeout`) |
| `f10-obvious-error` | tests/test_greet.py 가 실패해. 고쳐줘 | **무발화** (근접: `investigation`) |
| `f11-advice` | 작업 큐로 Postgres SKIP LOCKED 랑 Redis Streams 중 뭐가 나을까? 짧게 비교만 해줘 | **무발화** (근접: `decision-record`) |
| `f12-research` | 작업 큐 후보로 Redis Streams 랑 Kafka 차이 조사해줘. 간단히 정리만 | **무발화** (근접: `investigation`) |
| `f13-add-docs` | README.md 에 설치 섹션 추가해줘. 설치 명령은 pip install search-api 야 | **무발화** (근접: `doc-closeout`) |
| `f14-handoff-commit` | 오늘 여기까지. 다음 세션용으로 정리하고 커밋까지 해줘 | `session-handoff` + 커밋 |
| `f15-ambiguous-wrapup` | 작업 끝났으니 정리해줘 | 발화 여부는 판정하지 않음 — 모호함을 드러내고 파일을 바꾸지 않는지 (`ambiguous` 태그) |

`f6`/`f7` 은 트리거와 거리가 먼 대조군이고, `f9`–`f11` 은 트리거와 비슷하지만 발화하면 안 되는 근접 대조군이다.

- `f9` — 문서를 고치지만 구현 완료 후 문서 정합성 점검이 아니다.
- `f10` — 테스트가 실패하지만 첫 시도이고 원인(`nmae` 오타)이 명백하다.
- `f11` — 기술 선택을 논의하지만 결정이 내려지지도, 기록을 요청하지도 않았다.
- `f12` — "조사해줘"지만 결함 조사가 아니라 일반 리서치다.
- `f13` — 구현 직후 문서 작업이지만 사용자가 수정 내용을 이미 정했다.
- `f14` — `f2` 픽스처에서 커밋을 명시적으로 요청한다. 명시적 요청이면 커밋한다는 규칙을 본다.
- `f15` — handoff 와 문서 불일치가 함께 있는 저장소에서 모호한 마무리 요청. 처음에는 "둘 중 하나가 발화"를 기대했으나, 실제로는 3회 모두 스킬을 부르지 않고 두 해석(문서 정리 / handoff 종료)을 제시해 물었다. 그쪽이 더 나은 동작이라 판정을 "모호함을 드러내고 파일을 바꾸지 않음"으로 바꿨다.

## 케이스별 완료 조건 grader

| 케이스 | 결정적 grader | llm grader |
| --- | --- | --- |
| `f1-resume` | 검증 명령(`-m unittest discover`) 실행, `src/limiter.py`·`tests/test_limiter.py` 내용 그대로, Bash 로 `src/`·`tests/` 편집 0회, handoff `Status: blocked` 전환·옛 `Last verified` 줄 제거 | `ImportError` 인용, "검증됨" 주장을 `Verified` 로 두지 않음, `TokenBucket`/`RateLimiter` 불일치 지적, 막는 충돌로 보고하고 구현하지 않음 |
| `f2-handoff` | `docs/handoffs/active/parquet-export.md` 생성, 통과 기록 날조 없음(`N passed`, `Ran N tests`, "모두 통과"), 미커밋 변경(`_infer_schema`) 기재 | 테스트 없음 명시, writer 추상화 거짓 주장 미기재, Next Recommended Action 구체성 |
| `f3-closeout` | `README.md`·`docs/api.md` 가 옛 내용 그대로, `src/search.py` 변경 보존, `Edit`·`Write` 0회, Bash 편집·git 변경 0회, 새 `.md` 0개, `git status` 2회 이상, 보고에 `README.md`·`docs/api.md`·`SEARCH_RANKER`·승인 요청 언급 | 두 문서 모두 `Update` 이고 근거가 있음 |
| `f4-invest` | `src/tags.py` 미수정, `PYTHONHASHSEED=` 통제 실험 실행, `docs/investigations/active/primary-tag-flaky.md` 에 `Baseline`·`Expected Result`·`Status: resolved`·`권고만` | 원인 특정, 실패·통과 시드 양방향 증거, 수정은 권고만 |
| `f5-adr` | `adr/0002-*.md` 생성, `docs/` 미생성 | 기각 이유와 근거, 관측 가능한 Reversal Trigger, 근거 날조 없음. 코드(`rpush`, List)와 결정(Streams)의 불일치 지적(가중치 0.5) |
| `f8-nodocs` | 새 `.md` 0개 | 위치를 한 번 묻고 기본 경로와 비파일 대안을 제시. 추가 질문은 저장소에서 알 수 없는 기록 내용만, 같은 메시지 안에서 |
| `f6` / `f7` / `f9` / `f10` | 플레이북 스킬 호출 0회, 요청 작업 자체는 수행 | — |
| `f11-advice` / `f12-research` | 플레이북 스킬 호출 0회, 새 `.md` 0개 | — |
| `f13-add-docs` | 플레이북 스킬 호출 0회, `README.md` 에 설치 명령 추가 | — |
| `f14-handoff-commit` | `session-handoff` 발화, handoff 파일 생성, `git commit` 실행 | — |
| `f15-ambiguous-wrapup` | `README.md` 옛 내용 그대로, handoff 파일 유지, `Edit` 0회 | 두 해석을 제시해 묻거나, 파일을 바꾸지 않는 단계에서 승인을 요청 |

### 픽스처 설계 메모

- `f2`, `f4` 의 `AGENTS.md` 에는 문서 규약이 있다. 규약이 없으면 스킬이 위치를 묻고 멈춰, 비대화형 실행에서는
  측정하려는 절차(날조 여부, 통제 실험)까지 가지 못한다. "위치를 묻는지"는 `f8` 이 전담한다.
- `f5` 의 `src/queue.py` 가 Streams 가 아닌 List(`rpush`)를 쓰는 것은 의도한 함정이다. 결정 기록이 코드를 확인하는지 본다.
- `f4` 도 `f1` 과 같은 이유로 표준 라이브러리 `unittest` 를 쓴다. 해시 시드에 따라 `AssertionError` 가 간헐적으로 난다.
- "새 파일 없음" grader 는 `**/*.md` 만 본다. 에이전트가 Python 을 실행하면 `__pycache__` 가 생겨 `**/*` 로는 오판한다.
- shell 명령을 실행하는 grader 타입은 없다. 수정 금지는 보호할 파일의 **내용 regex** 로 판정하고, Bash 편집 패턴(`sed -i`, 리다이렉트, `git checkout` 등) `max: 0` 은 보조로 둔다.
- `f1` 은 handoff 이후 클래스 이름이 `TokenBucket` → `RateLimiter` 로 바뀐 상황이다. 검증 명령은 표준 라이브러리 `unittest` 라서
  eval 샌드박스(네트워크·uv 캐시 차단)에서도 같은 `ImportError` 로 실패한다. 이전 픽스처는 `uv run pytest` 수집 실패에 의존했는데,
  샌드박스에서는 uv 자체가 막혀 에이전트가 테스트 함수를 직접 호출하는 우회로 "통과"를 얻었다. 환경에 따라 결함이 사라지지 않게 바꿨다.
- `f3` 의 판단 grader 는 처음에 한 덩어리 llm 루브릭이었다. 기본 judge 가 조건을 모두 만족하는 긴 보고에 FAIL 을 줘서,
  기계적으로 확인 가능한 부분(문서·설정 키 언급, 승인 요청)은 regex 로 분리하고 judge 모델을 sonnet 으로 지정했다.

## 최근 전체 실행 (2026-09-14, 0.2.0)

`scripts/eval.sh` 기본 설정(케이스당 3회, 플러그인 없는 baseline 비교), 비용 $29.

| 구분 | 케이스 | 플러그인 있음 | baseline |
| --- | --- | --- | --- |
| 발화 + 완료 조건 | f1–f5, f8, f14 | 7개 모두 3회 전부 1.00, 해당 스킬 21/21 발화 | 0.22–0.67 |
| 무발화 대조군 | f6, f7, f9–f13 | 7개 모두 3회 전부 1.00, 오발화 0/21 | 1.00 |
| 모호 | f15 | 스킬 미발화, 두 해석을 제시해 질문 (grader 교체 후 1회 실행 1.00) | — |

description 을 바꾸면 이 표를 다시 채운다.

## 구조

```text
evals/
├── _lib/scaffold.sh       # fixture/ 복사 → git init/commit → patch.diff 적용
└── <case>/
    ├── case.yaml          # name, tags, scaffold_script
    ├── prompt.md          # 트리거 문구와 실행 설정
    ├── fixture.sh         # _lib/scaffold.sh 호출
    ├── fixture/           # 워크스페이스에 복사할 파일
    ├── patch.diff         # (선택) 커밋 뒤 적용할 미커밋 변경
    └── graders/*.md
```

픽스처를 손으로 살펴보려면 빈 디렉터리에서 `bash <케이스>/fixture.sh` 를 실행한다.

## `/skill-doctor` 로 대체할 수 없다

`/skill-doctor` 는 로드된 스킬의 **호출 횟수와 컨텍스트 비용**을 보여주는 프루닝 도구다. description 품질이나
트리거 정확도는 판단하지 않는다. 새로 만든 스킬의 "0회 호출" 은 미사용이 아니라 미검증이므로, 그 리포트의
"disable 또는 remove" 권고를 검증 전에 따르면 안 된다.

## 알려진 한계

- 검증한 것은 위 정형 문구뿐이다. 변형("문서 좀 손봐줘", "이거 왜 자꾸 터지지")은 측정하지 않았다.
- 두 스킬의 트리거가 동시에 성립하는 경우(조사 후 결정 기록 등)의 우선순위는 측정하지 않았다.
- `session-resume` 의 "같은 대화 안의 이어서 해줘", `decision-record` 의 "대화 중 합의" 근접 대조군은 아직 없다. 세션 중간의 "계속해" 같은 요청은 이전 대화가 필요해 `context.history_file` 로 만들어야 한다.
- 보고에 diff 해시가 있는지는 판정하지 않는다. eval 샌드박스에서 `git` 이 xcrun 캐시 문제로 실행되지 않는 경우가 있어, 에이전트가 `.git` 을 직접 읽어 비교하고 그 사실을 보고한 사례가 있다. 결과가 스킬이 아니라 환경에 좌우된다.
- `f5` 의 llm grader 는 `trace` 를 보는데, judge 는 앞뒤 12개 메시지만 본다. 실행이 길면 ADR 작성 내용이 잘릴 수 있다.
