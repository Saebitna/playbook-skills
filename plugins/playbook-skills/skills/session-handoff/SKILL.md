---
name: session-handoff
description: Writes or updates a workstream handoff document so the next session or agent can resume from the repository without the prior conversation, and closes it out when the workstream finishes. Use when the user says "인계", "핸드오프", "다음 세션용으로 정리", "오늘 여기까지", "handoff", "wrap up for next time", when work will not finish in this session, or when a finished workstream's handoff needs to be promoted and removed.
---

# Session Handoff

Handoff는 **대화 요약이 아니라 저장소에서 작업을 재개하기 위한 상태 문서**다. 두 가지 모드가 있다.

- **작성/갱신** — 진행 중인 workstream의 현재 상태를 기록한다.
- **종료** — workstream이 끝났으면 장기 지식을 승격하고 handoff를 제거한다.

## 문서 위치 결정

경로를 하드코딩하지 않는다. 위에서부터 순서대로 해결한다.

1. 사용자가 이번 요청에서 지정한 경로
2. `AGENTS.md` / `CLAUDE.md` 의 문서 규약
3. `docs/README.md` 라우터
4. 저장소 탐지 — `**/handoff*`, `docs/handoffs/**`, `**/status*.md` 를 찾는다. **기존 관행이 이 스킬의 기본값과 달라도 기존 관행을 따른다.**
5. 아무것도 없으면 `docs/handoffs/active/<workstream>.md` 를 제안하고 **한 번 묻는다.** `docs/` 트리를 통째로 만들지 말고 필요한 파일 하나만 만든다. 문서 파일을 쓰지 않는 프로젝트라면 PR 설명이나 커밋 메시지에 남기는 대체안을 제시한다.

경로가 정해지면 "이 규약을 `AGENTS.md`에 3~5줄로 기록할까요?"를 **제안하고 승인받은 경우에만** 추가한다. 자동으로 고치지 않는다. 기록해 두면 다음 세션부터 2단계에서 해결되어 다시 묻지 않는다.

workstream마다 active handoff는 하나만 둔다. 서로 다른 목표의 TODO를 한 문서에 섞지 않는다.

## 작성 전 확인

1. 현재 요구사항과 완료 조건
2. `git status`, `git diff`, 변경 파일
3. 적용되는 `AGENTS.md` / `CLAUDE.md`
4. 관련 spec, plan, decision, investigation 경로
5. 이번 세션에 **실제로 실행한** 명령과 그 결과

## 작성 규율

- 시간순 transcript를 쓰지 않는다. "무엇이 현재 유효한가 / 무엇을 다시 하지 말아야 하는가 / 다음에 어떤 파일에서 무엇을 할 것인가"에 답한다.
- 실행하지 않은 테스트를 통과했다고 쓰지 않는다.
- 저장소와 충돌하는 과거 정보는 `Outdated`, 확인할 수 없는 정보는 `Unverified`로 표시한다.
- 참조 문서는 경로만 링크하고 내용을 복사하지 않는다.
- Next Recommended Action은 **첫 파일·심볼, 수행할 변경, 직후 검증**까지 구체적으로 쓴다. "adapter 구현"은 나쁘고, "`src/.../adapter.py`의 기존 interface를 기준으로 `predict_batch`를 구현하고 `uv run pytest tests/test_adapter.py` 실행"은 좋다.

문서 구조와 섹션별 지침은 `references/handoff-structure.md`를 읽고 그대로 따른다.

## 종료 모드

workstream이 완료됐다면 active handoff를 completed 상태로 장기 보관하지 않는다.

1. 남은 작업이 정말 없는지 검증한다.
2. 남은 정보를 수명에 따라 승격한다.

   | 정보 | 처리 |
   | --- | --- |
   | 최종 시스템 동작 | architecture 문서 갱신 |
   | 지속되는 기술 선택 | decision/ADR로 승격 (`decision-record` 스킬) |
   | 재사용 가능한 조사 결과 | research 또는 runbook으로 승격 |
   | 완료된 작업 상태와 일회성 TODO | 제거 |

3. 승격이 끝나면 active handoff를 **제거한다.** 과거 상태는 Git history로 복구할 수 있다.
4. 감사·규제·회고 요구가 있을 때만 archive를 제안하고, 문서 상단에 현재 기준이 아님과 대체 문서 링크를 남긴다.

파일 삭제·이동은 사용자 승인 없이 수행하지 않는다.

## 참고

다음 세션 재개는 `session-resume` 스킬을 쓴다.
