---
name: decision-record
description: Writes a decision record (ADR) capturing the choice, the alternatives, the reasoning, the consequences, and the conditions that would reverse it. Use when the user says "ADR", "결정 기록", "이 선택 기록해두자", "decision record", "write this down", or when a technical choice between conflicting options was just made, a decision is hard to reverse, or an investigation concluded in a long-lived choice.
---

# Decision Record

결정 기록의 가치는 **선택 자체가 아니라 이유와 되돌리는 조건**에 있다. 선택만 적힌 문서는 다음 사람이 무심코 뒤집는다.

## 문서 위치 결정

경로를 하드코딩하지 않는다. 위에서부터 순서대로 해결한다.

1. 사용자가 이번 요청에서 지정한 경로
2. `AGENTS.md` / `CLAUDE.md` 의 문서 규약
3. `docs/README.md` 라우터
4. 저장소 탐지 — `**/adr/**`, `**/decisions/**`, `docs/adr*/**`, `**/*-adr-*.md`. 기존 파일이 있으면 그 **명명 규칙과 번호 체계를 그대로 따른다** (예: `adr/0007-use-uv.md`). **기존 관행이 이 스킬의 기본값과 달라도 기존 관행을 따른다.**
5. 아무것도 없으면 `docs/decisions/<날짜>-<제목>.md` 를 제안하고 **한 번 묻는다.** `docs/` 트리를 통째로 만들지 말고 필요한 파일 하나만 만든다. 문서 파일을 쓰지 않는 프로젝트라면 PR 설명, 커밋 메시지, 기존 설계 문서의 한 섹션에 남기는 대체안을 제시한다.

경로가 정해지면 "이 규약을 `AGENTS.md`에 기록할까요?"를 **제안하고 승인받은 경우에만** 추가한다.

## 작성 전

관련 코드, spec, investigation 증거를 실제로 확인한다. **확인되지 않은 근거를 만들어내지 않는다.** 비교 수치가 없으면 없다고 쓴다.

## 구조

```markdown
# <결정 제목>
Status: proposed | accepted | superseded
Date: YYYY-MM-DD
Decision owners: <담당자 또는 unknown>

## Context
결정이 필요해진 문제, 제약, 결정 동인. 지금 왜 이걸 정해야 하는가.

## Options Considered
각 선택지를 **같은 기준으로** 비교한다: 장점, 단점, 위험, 운영 비용.
채택하지 않은 선택지도 공정하게 쓴다. 결론에 맞춰 대안을 약하게 묘사하지 않는다.

## Decision
채택한 방안과 **적용 범위**. 어디까지 적용되고 어디는 적용되지 않는가.

## Rationale
현재 제약에서 왜 이 선택이 가장 적합한가. 증거와 함께 쓴다.

## Consequences
긍정적 결과 / 부정적 결과 / 후속 작업을 구분한다.
감수하기로 한 trade-off를 명시한다.

## Rejected Approaches and Revisit Triggers
폐기 이유와 **어떤 조건이 생기면 다시 검토할 것인지**.
예: "요청량이 초당 500건을 넘으면 재검토."

## Validation
이 결정이 유효함을 확인할 측정값, 테스트, 운영 신호.

## Related
관련 spec, plan, investigation, architecture 경로.
```

## 필수 조건

다음이 없으면 decision record가 아니다.

- `Rationale` — 왜 이 선택인지
- `Consequences` — 감수하기로 한 trade-off
- `Rejected Approaches and Revisit Triggers` — 되돌리는 조건

## 대체 관계

기존 decision을 대체한다면 **양쪽 모두** 갱신한다.

- 새 문서: `supersedes: <이전 경로>`
- 이전 문서: `Status: superseded`, `superseded_by: <새 경로>`, 그리고 상단에 현재 기준이 아님을 표시

이전 문서의 본문을 지우지 않는다. 당시의 근거가 기록의 목적이다.

## 결정 이후

결정 결과가 현재 architecture 설명을 바꾼다면, 해당 canonical 문서의 **구체적인 갱신 위치**를 제시한다. 바로 고치는 것은 `doc-closeout` 스킬의 승인 흐름을 따른다.

## 참고

조사 끝에 나온 결정이라면 `investigation` 스킬의 증거를 `Related`에 링크한다.
