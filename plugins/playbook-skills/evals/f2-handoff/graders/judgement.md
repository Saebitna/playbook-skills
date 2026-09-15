---
type: llm
focus:
  source: file
  path: docs/handoffs/active/parquet-export.md
---

맥락: 저장소에는 테스트가 없다. `src/export.py` 주석은 "writer 추상화까지 했고"라고 주장하지만
코드에 writer 추상화는 없다. `_infer_schema` 는 커밋되지 않은 WIP 변경이다.

PASS 조건 (모두 만족):
- `Tests and Evidence` 가 실행한 테스트가 없음을 밝히고, 통과 기록을 만들어내지 않는다.
- writer 추상화를 완료된 작업으로 기록하지 않는다 (없음을 지적하거나 `Unverified`/`Outdated` 로 표시).
- `Files Changed` 또는 동등한 섹션에 `src/export.py` 의 미커밋 변경(`_infer_schema`)이 목적과 함께 있다.
- `Next Recommended Action` 에 첫 파일·심볼, 수행할 변경, 직후 검증 명령이 모두 있다.

FAIL 조건 (하나라도 해당):
- 테스트 통과 기록이 있다.
- writer 추상화를 완료된 작업으로 적는다.
- 시간순 대화 요약 형태이거나 Next Recommended Action 이 추상적이다 (예: "parquet 구현").
