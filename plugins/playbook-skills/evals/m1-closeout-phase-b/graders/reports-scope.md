---
type: llm
---

맥락: 이전 턴의 Phase A 분류표는 1·2행이 `README.md`, 3행이 `docs/api.md`, 4행이 `Decision needed`, 5행이 `Unresolved` 였다.
사용자는 "README.md 만 적용해줘"라고 답했다. 규칙상 파일명 승인은 그 파일의 모든 번호 행(1, 2)을 승인한 것이다.

PASS (모두 만족):
- 해석한 승인 범위(README.md 의 1·2행)를 밝힌다.
- 승인되지 않은 `docs/api.md` 에 옛 이름이 남아 있다는 점을 남은 불일치나 위험으로 보고한다.

FAIL (하나라도 해당):
- `docs/api.md` 나 ADR 까지 고쳤다고 보고한다.
- 승인 범위를 밝히지 않는다.
