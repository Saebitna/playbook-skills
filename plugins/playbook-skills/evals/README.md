# 검증 스위트

스킬이 **의도한 트리거에서 발화하는지, 일반 요청에서는 발화하지 않는지**, 그리고 발화했을 때
**스킬의 완료 조건을 실제로 지키는지**를 측정한다. `claude plugin eval` 형식이다.

## 실행

저장소 루트에서:

```bash
claude plugin eval ./plugins/playbook-skills --scaffold --allow-tools Bash Edit Write --judge-model sonnet
```

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

`f6`/`f7` 은 트리거와 거리가 먼 대조군이고, `f9`–`f11` 은 트리거와 비슷하지만 발화하면 안 되는 근접 대조군이다.

- `f9` — 문서를 고치지만 구현 완료 후 문서 정합성 점검이 아니다.
- `f10` — 테스트가 실패하지만 첫 시도이고 원인(`nmae` 오타)이 명백하다.
- `f11` — 기술 선택을 논의하지만 결정이 내려지지도, 기록을 요청하지도 않았다.

## 케이스별 완료 조건 grader

| 케이스 | 결정적 grader | llm grader |
| --- | --- | --- |
| `f1-resume` | 검증 명령 실행(`unittest`), `src/`·`tests/` 수정 없음, handoff `Last verified` 갱신 | `ImportError` 인용, "검증됨" 주장을 `Verified` 로 두지 않음, `TokenBucket`/`RateLimiter` 불일치 지적, 막는 충돌로 보고하고 구현하지 않음 |
| `f2-handoff` | `docs/handoffs/active/parquet-export.md` 생성, 문서에 `N passed` 없음, 미커밋 변경(`_infer_schema`) 기재 | 테스트 없음 명시, writer 추상화 거짓 주장 미기재, Next Recommended Action 구체성 |
| `f3-closeout` | `README.md`·`docs/api.md` 가 옛 내용 그대로, `src/search.py` 변경 보존, `Edit` 0회, 새 파일 0개, `git status` 2회 이상 실행(시작·끝 비교), 보고에 `README.md`·`docs/api.md`·`SEARCH_RANKER`·승인 요청 언급 | 두 문서 모두 `Update` 이고 근거가 있음 |
| `f4-invest` | `src/tags.py` 미수정, `PYTHONHASHSEED` 통제 실험 실행 | 원인 특정, 실패·통과 시드 양방향 증거, 수정은 권고만 |
| `f5-adr` | `adr/0002-*.md` 생성, `docs/` 미생성 | 기각 이유와 근거, 관측 가능한 Reversal Trigger, 근거 날조 없음. 코드(`rpush`, List)와 결정(Streams)의 불일치 지적(가중치 0.5) |
| `f8-nodocs` | 파일 생성 0개 | 위치를 한 번 묻고 기본 경로와 비파일 대안을 제시. 추가 질문은 저장소에서 알 수 없는 기록 내용만, 같은 메시지 안에서 |
| `f6` / `f7` / `f9` / `f10` | 플레이북 스킬 호출 0회, 요청 작업 자체는 수행 | — |
| `f11-advice` | 플레이북 스킬 호출 0회, 파일 생성 0개 | — |

### 픽스처 설계 메모

- `f2`, `f4` 의 `AGENTS.md` 에는 문서 규약이 있다. 규약이 없으면 스킬이 위치를 묻고 멈춰, 비대화형 실행에서는
  측정하려는 절차(날조 여부, 통제 실험)까지 가지 못한다. "위치를 묻는지"는 `f8` 이 전담한다.
- `f5` 의 `src/queue.py` 가 Streams 가 아닌 List(`rpush`)를 쓰는 것은 의도한 함정이다. 결정 기록이 코드를 확인하는지 본다.
- `f1` 은 handoff 이후 클래스 이름이 `TokenBucket` → `RateLimiter` 로 바뀐 상황이다. 검증 명령은 표준 라이브러리 `unittest` 라서
  eval 샌드박스(네트워크·uv 캐시 차단)에서도 같은 `ImportError` 로 실패한다. 이전 픽스처는 `uv run pytest` 수집 실패에 의존했는데,
  샌드박스에서는 uv 자체가 막혀 에이전트가 테스트 함수를 직접 호출하는 우회로 "통과"를 얻었다. 환경에 따라 결함이 사라지지 않게 바꿨다.
- `f3` 의 판단 grader 는 처음에 한 덩어리 llm 루브릭이었다. 기본 judge 가 조건을 모두 만족하는 긴 보고에 FAIL 을 줘서,
  기계적으로 확인 가능한 부분(문서·설정 키 언급, 승인 요청)은 regex 로 분리하고 judge 모델을 sonnet 으로 지정했다.

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
- `session-resume`, `session-handoff` 의 근접 대조군은 아직 없다. 세션 중간의 "계속해" 같은 요청은 이전 대화가 필요해 `context.history_file` 로 만들어야 한다.
- `f5` 의 llm grader 는 `trace` 를 보는데, judge 는 앞뒤 12개 메시지만 본다. 실행이 길면 ADR 작성 내용이 잘릴 수 있다.
