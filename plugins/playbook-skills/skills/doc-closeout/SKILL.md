---
name: doc-closeout
description: Audits whether documentation still matches the code after a feature, fix, or refactor, proposes changes for approval, then applies only the approved ones. Use when the user says "문서 정리", "문서 close-out", "코드랑 문서 맞는지 확인", "구현 끝났으니 문서", "update the docs", or when a completed change altered public API, configuration, or operational procedures. Audit and mutation are separate phases — Phase A never edits files.
---

# Documentation Close-out

이번 변경과 **직접 관련된** 문서만 점검한다. docs 전체 개편은 이 스킬의 범위가 아니다.

핵심 규율: **audit과 mutation을 분리한다.** Phase A는 어떤 파일도 수정·이동·이름 변경·삭제하지 않는다. 사용자가 명시적으로 Phase B를 승인하기 전까지 제안만 한다.

## 문서 위치 결정

경로를 하드코딩하지 않는다. 위에서부터 순서대로 해결한다.

1. 사용자가 이번 요청에서 지정한 경로
2. `AGENTS.md` / `CLAUDE.md` 의 문서 규약
3. `docs/README.md` 라우터
4. 저장소 탐지 — 변경된 심볼·경로·설정 키·명령 이름으로 저장소 전체를 검색한다 (`README*`, `docs/**`, `**/adr/**`, `**/*.md`). **기존 문서 관행이 이 스킬의 기본값과 달라도 기존 관행을 따른다.**
5. 문서가 거의 없는 프로젝트라면 새 문서 체계를 만들지 말고, 갱신이 필요한 기존 파일(대개 `README.md`)만 다룬다.

## Phase A — Audit only (기본 진입점)

먼저 확인한다.

1. `git status --porcelain` — 출력을 기록해 둔다. 끝에서 다시 비교한다.
2. 이번 요구사항과 완료 조건 — 대화, spec, plan, handoff에서 찾는다. 찾지 못하면 없다고 적고, 코드 변경만으로 audit한다.
3. 변경 범위 — 커밋되지 않은 변경(`git diff HEAD`)과, 현재 브랜치가 기본 브랜치에서 갈라진 뒤의 커밋(`git diff <merge-base>..HEAD`)을 모두 본다. 기본 브랜치 위에서 작업 중이면 커밋되지 않은 변경만 본다. **어떤 범위를 봤는지 보고에 적는다.**
4. 변경된 public API, 설정 키, CLI, 운영 절차를 **목록으로** 뽑는다. 이름이 바뀐 것은 옛 이름과 새 이름을 모두 적는다.
5. 위 목록의 각 항목을 검색어로 삼아 위 4단계 탐지로 관련 문서를 찾는다. 검색어와 결과 파일을 보고에 남긴다.
6. `docs/README.md`와 적용되는 `AGENTS.md` / `CLAUDE.md`

**지금은 문서와 코드를 수정, 이동, 이름 변경, 삭제하지 않는다.**

관련 문서를 다음으로 분류해 표로 보고한다. 승인을 받기 쉽게 **각 행에 번호를 붙인다.**

| 분류 | 의미 | Phase B 처리 |
| --- | --- | --- |
| `Update` | 현재 동작과 문서 설명이 불일치하거나, 문서화해야 할 변경(새 설정 키, 새 옵션 등)이 빠져 있음 | 내용 갱신 |
| `No change` | 검토했으나 계약·운영 방식이 동일 | 없음 |
| `Complete` | active 상태 문서(plan, handoff, investigation)가 할 일을 끝냄 | 영구 지식 승격 후 상태 변경 또는 제거 |
| `Archive` | 보존은 하되 현재 기준이 아님 | 상단에 현재 기준 아님·대체 문서 링크 표시 |
| `Supersede` | 새 canonical 문서가 대체함 | 양쪽 문서에 대체 관계 표시 |
| `Decision needed` | 지속되는 기술 선택인데 decision/ADR이 없음 | 승인되면 `decision-record` 스킬로 작성 |
| `Unresolved` | 코드와 문서 중 어느 쪽이 의도인지 판단 불가 | 없음. 필요한 결정을 보고 |
| `Remove` | 파일 삭제 후보 | **별도 후보 목록에만** 표시. 승인 목록에 파일명이 명시돼야 실행 |

각 항목에 **target file, proposed action, 근거(코드·diff·spec 인용), 갱신하지 않을 때의 위험**을 함께 쓴다.

추가로 확인한다.

- 중요한 기술 선택인데 decision/ADR이 없는 것 → `Decision needed`
- acceptance criteria별 증거의 존재 여부
- plan / handoff / investigation의 상태가 현재와 맞는지
- `docs/README.md` 라우팅과 instruction 파일의 링크 유효성

`No change`에도 반드시 근거를 적는다. 예: "내부 구현만 변경, public contract와 설정은 동일."

문서와 코드가 충돌하지만 의도가 불명확하면 **자동으로 고치지 말고** 충돌과 필요한 결정을 보고한다. 코드가 옳다고 자동으로 단정하지 않는다 — 의도된 변경인지 회귀인지는 acceptance criteria와 decision으로 판정한다.

`Remove`는 실행 목록에 넣지 않고 별도 후보로만 표시한다.

**audit 결과를 보고한 뒤 멈추고 승인을 기다린다.**

## Phase B — 승인된 변경만 적용

사용자가 승인 목록을 준 뒤에만 실행한다. 승인 범위 밖으로 확장하지 않고, **소스 코드는 수정하지 않는다** (docstring·코드 주석 포함 — 코드 안의 설명이 틀렸다면 별도 후보로 보고한다). 새 문서 작성(ADR 포함)도 승인 목록에 있는 경우에만 한다.

승인 해석:

- 행 번호나 파일명으로 준 승인은 그 행만 승인한 것이다.
- "좋아", "다 해줘" 같은 포괄 승인은 `Update`, `Complete`, `Archive`, `Supersede`, `Decision needed` 행 전체에 대한 승인으로 본다. `Remove`와 `Unresolved`는 포함하지 않는다.
- 적용을 시작하기 전에 해석한 승인 범위(행 번호 목록)를 한 줄로 밝힌다.

Phase A와 다른 세션에서 승인을 받았거나 대화에 audit 표가 남아 있지 않다면, Phase A를 다시 수행해 표를 재생성하고 이전 승인과 달라진 행을 표시한 뒤 승인을 다시 받는다. 그사이 코드가 바뀌었을 수 있기 때문이다.

1. `Update` — architecture 문서는 현재 구현을 설명하도록, spec 상태는 acceptance criteria의 실제 증거를 반영하도록 갱신한다.
2. `Decision needed` — 승인된 항목만 `decision-record` 스킬로 작성한다. plan에 묻어두지 않는다.
3. `Complete` — 영구 지식만 canonical 문서에 통합하고 설명을 중복하지 않는다. active handoff는 승격 후 제거하고, 감사 요구가 있을 때만 archive한다.
4. `Archive` / `Supersede` — 현재 기준이 아님과 대체 문서 링크를 남긴다.
5. `Remove` — 승인 목록에 **파일명이 명시된 파일에만** 수행한다. 삭제 전 inbound link와 대체 문서를 확인한다.
6. `docs/README.md`는 마지막에 갱신한다.

예상하지 못한 참조나 충돌을 발견하면 건드리지 말고 보고한다.

완료 후 보고: 실제 변경된 파일, 상태 변경, complete/archive/supersede/remove 내역, 링크 검증 결과, 남은 risk.

## Phase C — 독립 리뷰 (선택)

사용자가 요청하면 수행한다. **파일을 수정하지 않는다.**

code diff와 documentation diff를 함께 읽고 확인한다: architecture와 구현의 일치, spec `completed` 상태의 증거, 누락된 ADR, archive 문서가 현재 기준처럼 노출되는지, README routing, 중복 설명, 삭제로 인한 링크·지식 유실.

finding을 severity 순으로 path·근거와 함께 보고한다. 문제가 없으면 residual risk와 사람이 마지막으로 확인할 항목을 적는다.

## 완료 조건

보고 직전에 해당 Phase의 항목을 하나씩 확인한다. 채우지 못한 항목은 이유와 함께 보고한다.

### Phase A

- [ ] 시작할 때와 보고 직전의 `git status --porcelain` 출력이 같다. 두 출력을 보고에 포함한다.
- [ ] 변경된 public API·설정 키·CLI·운영 절차를 목록으로 적었고, 각각을 검색한 검색어와 결과 파일을 적었다.
- [ ] 목록의 모든 변경 항목이 분류표의 한 행 이상에 나오거나, "문서 언급 없음 — 문서화 불필요" 같은 근거와 함께 표 아래에 적혀 있다.
- [ ] 모든 행에 target file, proposed action, 근거, 갱신하지 않을 때의 위험이 있다. `No change` 행에도 근거가 있다.
- [ ] `Remove` 후보는 실행 목록과 분리돼 있다.
- [ ] 승인을 요청하고 멈췄다.

### Phase B

- [ ] 변경한 파일이 모두 승인 목록에 있다. 소스 코드 파일은 변경하지 않았다.
- [ ] 이름이 바뀌거나 사라진 심볼·설정 키를 문서 전체에서 다시 검색해, archive·superseded 문서와 ADR 본문을 제외하면 남은 참조가 없다.
- [ ] 변경한 문서의 상대 링크와 `docs/README.md` 라우팅이 실제 파일을 가리킨다.
- [ ] `Remove`는 승인 목록에 파일명이 명시된 파일에만 수행했고, 삭제 전 inbound link를 확인했다.

## 참고

docs 전체 점검이나 대형 재구성은 이 스킬이 아니라 해당 audit / migration 절차를 쓴다.
