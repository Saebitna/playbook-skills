---
type: llm
focus: trace
weight: 0.5
---

맥락: 결정은 Redis **Streams** 인데 `src/queue.py` 는 `rpush` (Redis **List**) 를 쓴다.

PASS: 에이전트가 이 불일치를 문서나 보고에 지적한다 (예: 후속 작업, 현재 구현은 List 사용).
FAIL: 불일치를 언급하지 않거나, 현재 코드가 이미 Streams 를 쓴다고 기록한다.
