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

1. 이번 요구사항과 완료 조건
2. `git diff` (base branch 대비 또는 working tree)
3. 변경된 public API, 설정, CLI, 운영 절차
4. 위 4단계로 찾은 관련 문서
5. `docs/README.md`와 적용되는 `AGENTS.md` / `CLAUDE.md`

**지금은 문서와 코드를 수정, 이동, 이름 변경, 삭제하지 않는다.**

관련 문서를 다음으로 분류해 표로 보고한다.

| 분류 | 의미 |
| --- | --- |
| `Update` | 현재 동작과 문서 설명이 불일치 |
| `No change` | 검토했으나 계약·운영 방식이 동일 |
| `Complete / Remove / Archive` | active 상태를 끝내야 함 |
| `Supersede` | 새 canonical 문서가 대체함 |
| `Unresolved` | 코드와 문서 중 어느 쪽이 의도인지 판단 불가 |

각 항목에 **target file, proposed action, 근거(코드·diff·spec 인용), 갱신하지 않을 때의 위험**을 함께 쓴다.

추가로 확인한다.

- 중요한 기술 선택인데 decision/ADR이 없는 것 (`decision-record` 스킬로 연결)
- acceptance criteria별 증거의 존재 여부
- plan / handoff / investigation의 상태가 현재와 맞는지
- `docs/README.md` 라우팅과 instruction 파일의 링크 유효성

`No change`에도 반드시 근거를 적는다. 예: "내부 구현만 변경, public contract와 설정은 동일."

문서와 코드가 충돌하지만 의도가 불명확하면 **자동으로 고치지 말고** 충돌과 필요한 결정을 보고한다. 코드가 옳다고 자동으로 단정하지 않는다 — 의도된 변경인지 회귀인지는 acceptance criteria와 decision으로 판정한다.

`DELETE`는 실행 목록에 넣지 않고 별도 후보로만 표시한다.

**audit 결과를 보고한 뒤 멈추고 승인을 기다린다.**

## Phase B — 승인된 변경만 적용

사용자가 승인 목록을 준 뒤에만 실행한다. 승인 범위 밖으로 확장하지 않고, **소스 코드는 수정하지 않는다.**

1. architecture 문서는 현재 구현을 설명하도록 갱신한다.
2. 지속되는 결정은 plan에 묻어두지 않고 ADR로 승격한다.
3. spec 상태는 acceptance criteria의 실제 증거를 반영한다.
4. 영구 지식만 canonical 문서에 통합하고 설명을 중복하지 않는다. 다른 문서는 링크한다.
5. archive / superseded 문서에는 현재 기준이 아님과 대체 문서 링크를 남긴다.
6. active handoff는 영구 지식을 승격한 뒤 제거하고, 감사 요구가 있을 때만 archive한다.
7. `DELETE`는 승인 목록에 **명시된 파일에만** 수행한다. 삭제 전 inbound link와 대체 문서를 확인한다.
8. `docs/README.md`는 마지막에 갱신한다.

예상하지 못한 참조나 충돌을 발견하면 건드리지 말고 보고한다.

완료 후 보고: 실제 변경된 파일, 상태 변경, remove/archive/delete 내역, 링크 검증 결과, 남은 risk.

## Phase C — 독립 리뷰 (선택)

사용자가 요청하면 수행한다. **파일을 수정하지 않는다.**

code diff와 documentation diff를 함께 읽고 확인한다: architecture와 구현의 일치, spec `completed` 상태의 증거, 누락된 ADR, archive 문서가 현재 기준처럼 노출되는지, README routing, 중복 설명, 삭제로 인한 링크·지식 유실.

finding을 severity 순으로 path·근거와 함께 보고한다. 문제가 없으면 residual risk와 사람이 마지막으로 확인할 항목을 적는다.

## 참고

docs 전체 점검이나 대형 재구성은 이 스킬이 아니라 해당 audit / migration 절차를 쓴다.
