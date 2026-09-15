# playbook-skills

장기 workstream을 여러 세션에 걸쳐 수행할 때 반복되는 다섯 가지 절차를
Claude Code 스킬로 제공하는 플러그인이다.

절차 자체는 문서로도 존재할 수 있지만, 문서는 사람이 기억해서 찾아 읽어야 한다.
스킬은 에이전트가 상황을 감지해 스스로 호출한다. 이 저장소는 후자를 담당한다.

## 설치

```bash
claude plugin marketplace add Saebitna/playbook-skills
claude plugin install playbook-skills --scope project
```

`--scope project` 는 현재 프로젝트에만 적용한다. 모든 프로젝트에서 쓰려면
`--scope user` 를 쓴다. 로컬 체크아웃에서 바로 쓰려면:

```bash
claude plugin marketplace add ./경로/playbook-skills
```

## 스킬

| 스킬 | 언제 발화하나 | 무엇을 강제하나 |
| --- | --- | --- |
| `session-resume` | "이전 작업 이어서 해줘", 핸드오프 문서를 가리킬 때 | 문서의 주장을 저장소 증거와 대조해 `Verified` / `Unverified` / `Outdated` 로 분류한 뒤 재개 |
| `session-handoff` | "오늘 여기까지", "다음 세션용으로 정리" | 다음 세션이 대화 기록 없이 저장소만으로 재개할 수 있는 상태 문서 작성. workstream 종료 시 영구 지식 승격 후 제거 |
| `doc-closeout` | "구현 끝났으니 문서 정리" | audit 과 mutation 분리. Phase A 는 **어떤 파일도 수정하지 않고** 분류표만 내고 멈춘다 |
| `investigation` | "계속 실패해", "원인을 모르겠어" | 추측 후 패치 대신 가설 → 통제 실험 → 증거 로그. 한 번에 한 변수만 바꾼다 |
| `decision-record` | "이 선택 기록해두자", "ADR" | 선택·대안·근거·결과, 그리고 **되돌리는 조건**까지 기록 |

다섯 개는 서로를 이름으로 참조한다(`investigation` → `decision-record`,
`session-resume` ↔ `session-handoff` 등). 각 스킬의 절차는 단독으로 동작하지만, 다른 스킬로
넘기는 연계는 함께 설치했을 때만 동작한다. 그래서 플러그인은 다섯 개를 한 단위로 배포한다.

## 설계 원칙

### 스킬은 자족적이다

각 `SKILL.md` 는 외부 문서를 읽어야 동작하는 구조가 아니다. 절차 전체가 파일 안에 있다.
플레이북 문서가 없는 프로젝트, 문서가 아예 없는 프로젝트에서도 그대로 동작한다.

### 문서의 "역할"만 강제하고 "위치"는 프로젝트가 정한다

경로를 하드코딩하지 않는다. 다섯 스킬 모두 1~4단계는 같은 해석 순서를 쓰고, 5단계(아무것도 없을 때)의 처리만 스킬별로 다르다.

1. 사용자가 이번 요청에서 지정한 경로
2. `AGENTS.md` / `CLAUDE.md` 의 문서 규약
3. `docs/README.md` 라우터
4. 저장소 탐지 — **기존 관행이 이 스킬의 기본값과 달라도 기존 관행을 따른다**
5. 아무것도 없으면 사용자에게 묻는다

4단계가 핵심이다. `adr/0001-*.md` 만 있는 저장소에서는 `adr/0002-...` 로 이어쓰고,
`docs/decisions/` 를 강요하지 않는다. 문서가 하나도 없는 저장소에서는 트리를 임의로
만들지 않고 위치를 한 번 묻는다.

### 경로 해석 블록은 의도적으로 복제한다

같은 경로 해석 블록이 다섯 `SKILL.md` 에 중복돼 있다. `_shared/` 로 분리하거나 별도
스킬을 호출하게 만들지 않았다. **스킬 디렉터리 하나만 복사해도 그 스킬의 절차가 완전히 동작하는 것**이
DRY 보다 중요하다고 판단했다. 이식성이 이 프로젝트의 목적이기 때문이다.

이 결정을 뒤집으려면: 스킬 수가 늘어 중복 유지 비용이 실제로 문제가 되고,
동시에 단독 복사 사용 사례가 사라졌을 때.

### 사용자 파일을 임의로 고치지 않는다

다섯 스킬이 같은 승인 규칙을 쓴다.

| 대상 | 승인 |
| --- | --- |
| 사용자가 이번 요청으로 부른 스킬의 산출물 — handoff, 조사 기록, decision record | 경로가 정해지면 바로 작성 |
| 다른 스킬의 흐름 안에서 파생해 만드는 문서 — handoff 종료 모드의 승격 ADR, doc-closeout 의 `Decision needed`, investigation 끝의 ADR | 제안 → 승인 → 작성 |
| 기존 canonical 문서 수정 — architecture, README, spec, 이전 ADR | 변경안 제시 → 승인 → 적용 (`doc-closeout` 의 Phase A → B) |
| 제품 코드 수정 | 사용자가 요청한 작업 범위 안에서만 (investigation 은 수정 요청이 있을 때만) |
| 임시 진단 변경 — 로그, 디버그 플래그 | 바로 하되, 끝내기 전에 되돌린다 |
| 파일 삭제·이동·archive, `AGENTS.md` 규약 추가, 커밋 | 항상 승인 후. 사용자가 이번 요청에서 명시적으로 요구한 것("커밋까지 해줘")은 승인으로 본다 |

승인 게이트 앞에서 멈추는 것은 기능의 일부다.

### 완료는 체크리스트로 판정한다

각 `SKILL.md` 끝에 `## 완료 조건` 체크리스트가 있다. 에이전트는 보고 직전에 항목을 하나씩
확인하고, 채우지 못한 항목은 빼지 않고 이유와 함께 보고한다. `evals/` 의 grader 는 그중
파일 상태와 도구 호출로 확인할 수 있는 조건을 바깥에서 다시 판정한다.

## 검증

트리거 발화·오발화와 스킬별 완료 조건을 측정하는 `claude plugin eval` 스위트가
[`plugins/playbook-skills/evals/`](plugins/playbook-skills/evals/) 에 있다.
스킬의 `description` 이나 본문을 수정했다면 재실행한다.

```bash
scripts/eval.sh
```

케이스, grader, 판정 원칙은 [`evals/README.md`](plugins/playbook-skills/evals/README.md) 를 본다.
핵심은 **워크스트림 맥락이 없는 에이전트에게 트리거 문구만 주고**, 발화는 트랜스크립트의 `Skill`
호출로, 완료 조건은 실행 후 파일 상태와 명시적 PASS/FAIL 기준으로 판정한다는 것이다.

## 출처

이 스킬들은 `agent-project-playbook` 문서 규약에서 추출했다. 문서 버전의 절차는
그 저장소에 canonical 로 남아 있고, 이 플러그인은 그중 트리거가 뚜렷하고 반복되는
다섯 가지를 자동화한 것이다.
