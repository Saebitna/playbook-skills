# Handoff 문서 구조

아래 구조를 그대로 사용한다. 해당 없는 섹션은 삭제하지 말고 "없음"과 이유를 쓴다.

```markdown
# <Workstream 이름>
Status: active | blocked
Last verified: YYYY-MM-DD
```

## 섹션별 지침

### Goal and Acceptance Criteria

최종적으로 무엇이 달라져야 하는가를 사용자 관점으로 쓴다. 완료 조건은 각각 검증 가능한 문장으로 쓰고, 조건마다 현재 상태를 아래 표시로 붙인다. 파일 목록이나 활동 목록이 아니다.

### Current Status

지금 어디까지 왔는가. 한두 문단. 진행률 숫자보다 "무엇이 동작하고 무엇이 아직 아닌가"가 중요하다. `blocked`라면 무엇이 막고 있으며 누가·무엇이 풀 수 있는지 쓴다.

커밋 상태를 한 줄로 쓴다. 예: "`api/billing.py`의 `refund_partial`은 미커밋 — 이 브랜치의 working tree에만 있다."


### Relevant Documents

spec, plan, investigation, decision, architecture의 **경로만** 링크한다. 내용을 복사하지 않는다. 각 링크에 왜 관련 있는지 한 줄을 붙인다.

### Completed Work

끝난 작업을 결과 중심으로 쓴다. 각 항목에 확인 가능한 증거(파일, 테스트, 커밋)를 붙인다.

### Key Decisions

채택한 선택과 **그 이유**를 함께 쓴다. 이유 없는 결정은 다음 세션이 무심코 뒤집는다. 장기적으로 유효한 결정은 별도 decision/ADR로 승격을 **제안**하고(승인 후 `decision-record` 스킬로 작성), 작성되면 여기에는 링크만 남긴다.

### Rejected Approaches / Do Not Redo

시도했다가 버린 접근, **폐기 이유**, 그리고 **어떤 조건이면 다시 검토할 만한지**를 쓴다. 이 섹션이 다음 세션의 시간을 가장 많이 아낀다.

### Files Changed

각 파일의 경로, **변경 목적**, 커밋 여부를 쓴다. diff를 복사하지 않는다.

### Tests and Evidence

실행한 **명령 원문**과 **정확한 결과**를 쓴다.

```text
uv run pytest tests/test_adapter.py  →  18 passed, 2 skipped
uv run ruff check src/              →  clean
```

실행하지 않은 검증은 여기 쓰지 말고 아래 `Known Issues and Unverified Assumptions`에 `Unverified`로 표시한다.

### Known Issues and Unverified Assumptions

확인된 사실과 가정을 구분한다. 각 항목에 표시를 붙인다. 이 정의는 `session-resume` 스킬과 같다.

- `Verified` — 이번 세션에 정식 수단으로 확인함. 동작에 관한 주장은 문서·`AGENTS.md`가 정한 명령의 실행 결과가 증거다. `파일:줄`은 존재·부재 같은 구조에 관한 주장에만 증거로 쓴다.
- `Unverified` — 이번 세션에 정식 수단으로 확인하지 못함. 이유를 함께 적는다: 확인 수단이 저장소 밖에 있음 / 정식 명령이 실행되지 않음 / 확인할 명령이 없음 / 이번 세션에 실행하지 않음 / 추론함.
- `Outdated` — 현재 코드·테스트·문서와 다름. 무엇과 다른지 적는다.

### Remaining Tasks

남은 작업을 우선순위와 의존성과 함께 쓴다. 다른 workstream에 속하는 일은 여기 섞지 말고 분리한다.

### Next Recommended Action

가장 우선순위 높은 **하나의** 행동을 구체적으로 쓴다. 반드시 포함할 것:

- 열어야 할 첫 파일과 심볼
- 수행할 변경
- 그 직후 실행할 검증 명령

### Next Session Prompt

다음 세션에 그대로 붙여 넣을 수 있는 3~5줄짜리 재개 프롬프트. 이 handoff 경로와 목표, 첫 행동을 담는다.

## 금지 사항

- 시간순 대화 요약
- 실행하지 않은 테스트를 통과로 기록
- 다른 handoff 내용 복사 (경로로 링크할 것)
- 완료된 workstream의 handoff를 `completed` 상태로 장기 보관
