---
type: llm
focus: trace
---

맥락: NOTES.md 는 Postgres SKIP LOCKED / Redis Streams / SQS 를 비교하고 Redis Streams 를 골랐다.
기존 `adr/0001-use-uv.md` 가 있으므로 `adr/0002-...` 로 이어써야 한다.

에이전트가 작성한 `adr/0002-*.md` 의 내용을 기준으로 판정한다.

PASS 조건 (모두 만족):
- Postgres SKIP LOCKED 와 SQS 를 기각한 이유가 NOTES.md 의 근거(처리량 약 2k/s 대비 피크 5k/s, 로컬 개발 불편)와 함께 있다.
- 채택안(Redis Streams)을 뒤집거나 재검토할 조건이 관측 가능한 수치나 사건으로 하나 이상 있다.
- NOTES.md 에 없는 수치나 근거를 지어내지 않는다.

FAIL 조건 (하나라도 해당):
- 채택안을 뒤집는 조건이 없거나 "필요하면 재검토" 같은 관측 불가능한 문장뿐이다.
- 기각한 대안이나 기각 이유가 빠졌다.
