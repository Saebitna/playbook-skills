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
5. 아무것도 없으면 `docs/decisions/<날짜>-<제목>.md` 를 제안하고 **한 번 묻는다.** 아래 `작성 전`의 확인 질문이 있으면 같은 메시지에 함께 묻는다. `docs/` 트리를 통째로 만들지 말고 필요한 파일 하나만 만든다. 문서 파일을 쓰지 않는 프로젝트라면 PR 설명, 커밋 메시지, 기존 설계 문서의 한 섹션에 남기는 대체안을 제시한다. 대체안을 고르면 같은 구조의 초안 본문만 제시하고, 커밋·PR 작성은 하지 않는다.

경로를 4·5단계로 정했다면 "이 규약을 `AGENTS.md`에 기록할까요?"를 **제안하고 승인받은 경우에만** 추가한다.

## 작성 전

관련 코드, spec, investigation 증거를 실제로 확인한다. **확인되지 않은 근거를 만들어내지 않는다.** 비교 수치가 없으면 없다고 쓴다. 결정 내용과 현재 코드가 다르면(예: 결정은 gRPC인데 코드는 아직 REST 클라이언트) 그 차이를 `Consequences`의 후속 작업이나 보고에 적는다.

같은 주제의 기존 decision이 있는지 확인한다. 있으면 아래 `대체 관계`를 따른다.

필수 조건 중 저장소와 대화에서 확인할 수 없는 내용(기각한 대안, 선택 이유, 되돌리는 조건 등)이 있으면 작성 전에 **한 번** 묻는다. 저장소에서 확인할 수 있는 것은 묻지 않는다. **질문했다면 답을 받기 전에는 파일을 만들지 않는다.** 답을 받은 뒤에도 비어 있는 필수 항목은 지어내지 않고 `미확인 — 확인 필요`로 쓰고, 보고에서 그 목록을 다시 요청한다. 필수 항목에 `미확인`이 남아 있으면 `Status`는 `proposed`다.

메타데이터는 다음 규칙으로 정한다.

- `Status` — 사용자나 근거 문서가 결정이 확정됐다고 명시하면("가기로 했어", "골랐다" 등) `accepted`, 아니면 `proposed`. 판단할 수 없으면 `proposed`로 쓰고 보고에서 확인을 요청한다.
- `Date` — 결정일이 근거로 확인되면 결정일, 아니면 오늘 날짜(`date`로 확인)를 `Date: YYYY-MM-DD (기록일)` 형식으로 쓴다. 날짜를 추정하지 않는다.
- `Decision owners` — 근거에 이름이 없으면 `unknown`.

## 구조

**기존 decision 파일이 있으면 그 파일의 섹션 구조와 메타데이터 형식(`Status:` 줄, frontmatter 등)을 따른다.** 아래 구조는 기존 관행이 없을 때의 기본값이다. 기존 섹션은 그 이름과 순서대로 두고, 기존 구조에 없는 필수 조건 섹션과 선택지 비교(`Options Considered`)는 새 문서 끝에 덧붙인다. 메타데이터는 기존 형식으로 쓰고, 기존 형식에 없는 필드(`Decision owners` 등)는 같은 형식의 줄로 추가한다. 기존 파일을 새 구조로 고치지 않는다.

```markdown
# <결정 제목>
Status: proposed | accepted | superseded
Date: YYYY-MM-DD
Decision owners: <담당자 또는 unknown>
Supersedes: <이전 decision 경로 — 대체할 때만>

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

## Reversal Triggers
**채택한 방안을** 뒤집거나 재검토해야 하는 조건. 관측 가능한 수치나 사건으로 쓴다.
수치는 근거(측정값, 문서, 사용자 발언)가 있을 때만 쓴다. 근거가 없으면 사건 조건으로 쓰거나 `제안값(미확정)`으로 표시한다.
예: "벤더가 지원 종료를 공지하면 재검토." / "(제안값, 미확정) p95 지연이 300ms를 넘으면 재검토."

## Rejected Approaches
기각한 각 선택지의 폐기 이유와, 어떤 조건이 생기면 **그 선택지를** 다시 볼 만한지.
예: "GraphQL — 팀에 운영 경험이 없어 탈락. 경험 있는 담당자가 합류하면 재검토."

## Validation
이 결정이 유효함을 확인할 측정값, 테스트, 운영 신호.

## Related
관련 spec, plan, investigation, architecture 경로.
```

## 필수 조건

다음 항목은 비워 둘 수 없다. 근거가 없으면 지어내지 말고 `미확인 — 확인 필요`로 채우고 `Status`를 `proposed`로 둔다.

- `Rationale` — 왜 이 선택인지
- `Consequences` — 감수하기로 한 trade-off
- `Reversal Triggers` — 채택안을 되돌리는 조건
- `Rejected Approaches` — 기각한 대안과 폐기 이유

## 대체 관계

기존 decision을 대체한다면 **양쪽 모두** 갱신한다. 이전 문서 수정은 기존 canonical 문서를 고치는 일이므로, 변경 내용을 제시하고 승인받은 뒤 적용한다.

- 새 문서: `Supersedes: <이전 경로>` — 새 문서는 바로 작성한다.
- 이전 문서: `Status: superseded`, `Superseded by: <새 경로>`, 그리고 상단에 현재 기준이 아님을 표시 — 승인 후 적용한다. 승인 전이면 새 문서의 보고에 "이전 문서 갱신 승인 대기"로 적는다.

이전 문서의 본문을 지우지 않는다. 당시의 근거가 기록의 목적이다.

## 결정 이후

결정 결과가 현재 architecture 설명을 바꾼다면, 해당 canonical 문서의 **구체적인 갱신 위치**를 제시한다. 바로 고치는 것은 `doc-closeout` 스킬의 승인 흐름을 따른다.

## 완료 조건

보고 직전에 아래 항목을 하나씩 확인한다. 채우지 못한 항목은 빼지 말고 이유와 함께 보고한다.

- [ ] 파일 경로와, 그 경로를 어떤 해석 단계로 정했는지 적었다. 대체안(PR 설명 등)을 골랐다면 "해당 없음 — 초안 본문 제시"로 적었다. 기존 decision 파일이 있다면 그 명명 규칙과 다음 번호를 따랐다.
- [ ] 필수 조건 네 항목이 모두 채워져 있다. `미확인`인 항목이 있다면 `Status`가 `proposed`이고 보고에서 그 목록을 요청했다.
- [ ] 확인 질문을 했다면 답을 받기 전에 파일을 만들지 않았다.
- [ ] 근거 없는 수치를 쓰지 않았다. 제안한 수치에는 `제안값(미확정)` 표시가 있다.
- [ ] 채택안 외 선택지가 하나 이상 같은 기준으로 비교돼 있다. 대안이 정말 없었다면 그 사실과 이유가 있다.
- [ ] `Status`, `Date`, `Decision owners`가 위 메타데이터 규칙을 따른다. 근거 없는 날짜나 담당자를 쓰지 않았다.
- [ ] `Reversal Triggers`에 채택안을 뒤집는 조건이 하나 이상 있고, 각 조건이 관측 가능한 수치나 사건이다. "필요하면 재검토" 같은 문장은 조건이 아니다.
- [ ] `Rationale`의 각 근거에 출처(파일, 문서, 측정값)가 있거나, 출처가 없다고 명시돼 있다.
- [ ] 기존 decision이 있다면 기존 섹션을 그 이름·순서대로 두고, 부족한 필수 섹션과 비교만 덧붙였다.
- [ ] 기존 decision을 대체했다면 새 문서에 `Supersedes:`가 있고, 이전 문서는 승인 후 갱신했거나 "승인 대기"로 보고했다.
- [ ] architecture 문서를 직접 고치지 않았고, 갱신이 필요하면 위치만 제시했다.

## 참고

조사 끝에 나온 결정이라면 `investigation` 스킬의 증거를 `Related`에 링크한다.
