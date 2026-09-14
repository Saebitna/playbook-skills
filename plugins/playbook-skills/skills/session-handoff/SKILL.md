---
name: session-handoff
description: Writes or updates a workstream handoff document so the next session or agent can resume from the repository without the prior conversation, and closes it out when the workstream finishes. Use when the user says "인계", "핸드오프", "다음 세션용으로 정리", "오늘 여기까지", "handoff", "wrap up for next time", when work will not finish in this session, or when a finished workstream's handoff needs to be promoted and removed.
---

# Session Handoff

Handoff는 **대화 요약이 아니라 저장소에서 작업을 재개하기 위한 상태 문서**다. 두 가지 모드가 있다.

- **작성/갱신** — 진행 중인 workstream의 현재 상태를 기록한다.
- **종료** — workstream이 끝났으면 장기 지식을 승격하고 handoff를 제거한다.

기본은 작성/갱신 모드다. 종료 모드는 사용자가 workstream 완료를 명시하거나 종료 정리를 요청했을 때만 들어간다. 작성 중에 모든 완료 조건이 충족된 것으로 보이면, 작성/갱신 모드로 기록을 마친 뒤 종료 모드 전환을 **제안만** 한다.

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
6. 코드 주석, TODO, 커밋 메시지에 적힌 진행 주장 — 옮겨 적기 전에 코드로 확인한다
7. 커밋 상태 — 작업 중인 변경이 커밋·push되지 않았다면, 다른 clone이나 worktree에서는 재개할 수 없다

## 작성 규율

- 시간순 transcript를 쓰지 않는다. "무엇이 현재 유효한가 / 무엇을 다시 하지 말아야 하는가 / 다음에 어떤 파일에서 무엇을 할 것인가"에 답한다.
- 실행하지 않은 테스트를 통과했다고 쓰지 않는다.
- 저장소와 충돌하는 과거 정보는 `Outdated`, 확인할 수 없는 정보는 `Unverified`로 표시한다.
- 참조 문서는 경로만 링크하고 내용을 복사하지 않는다.
- 커밋되지 않은 변경이 있거나 handoff 문서 자체가 커밋되지 않았다면 그 사실을 `Current Status`에 쓰고, 보고에서 커밋을 **제안한다.** 직접 커밋하지 않는다.
- Next Recommended Action은 **첫 파일·심볼, 수행할 변경, 직후 검증**까지 구체적으로 쓴다. "adapter 구현"은 나쁘고, "`src/.../adapter.py`의 기존 interface를 기준으로 `predict_batch`를 구현하고 `uv run pytest tests/test_adapter.py` 실행"은 좋다.

문서 구조와 섹션별 지침은 `references/handoff-structure.md`를 읽고 그대로 따른다.

## 종료 모드

workstream이 완료됐다면 active handoff를 completed 상태로 장기 보관하지 않는다.

1. 남은 작업이 정말 없는지 검증한다. `Goal and Acceptance Criteria`의 **완료 조건마다** 이번 세션의 증거(실행한 명령과 결과, `파일:줄`, 커밋)를 대응시킨다. 증거가 없는 조건이 하나라도 있으면 종료 모드를 중단하고 작성/갱신 모드로 돌아간다.
2. 남은 정보를 수명에 따라 분류하고, **대상 경로와 변경안을 표로 제시한 뒤 승인을 기다린다.** 기존 canonical 문서 수정, 새 ADR 작성, handoff 제거는 모두 승인 후에만 한다 (`doc-closeout` 스킬의 Phase A → B 흐름과 같다).

   | 정보 | 처리 |
   | --- | --- |
   | 최종 시스템 동작 | architecture 문서 갱신 |
   | 지속되는 기술 선택 | decision/ADR로 승격 (`decision-record` 스킬) |
   | 재사용 가능한 조사 결과 | research 또는 runbook으로 승격 |
   | 완료된 작업 상태와 일회성 TODO | 제거 |

3. 승인된 승격을 적용한 뒤 active handoff를 **제거한다.** 과거 상태는 Git history로 복구할 수 있다.
4. 감사·규제·회고 요구가 있을 때만 archive를 제안하고, 문서 상단에 현재 기준이 아님과 대체 문서 링크를 남긴다.

파일 삭제·이동은 사용자 승인 없이 수행하지 않는다.

## 완료 조건

보고 직전에 해당 모드의 항목을 하나씩 확인한다. 채우지 못한 항목은 이유와 함께 보고한다.

### 작성/갱신 모드

- [ ] `references/handoff-structure.md`의 모든 섹션이 있다. 해당 없는 섹션은 "없음"과 이유가 적혀 있다.
- [ ] `Last verified`가 오늘 날짜다 (`date`로 확인한 값).
- [ ] 완료 조건이 각각 검증 가능한 문장이다.
- [ ] `Completed Work`의 모든 항목에 확인 가능한 증거(파일, 테스트, 커밋)가 붙어 있다.
- [ ] `Tests and Evidence`에는 **이번 세션에 실제로 실행한** 명령과 그 출력만 있다. 실행하지 않은 검증은 `Known Issues`에 `Unverified`로 있다.
- [ ] `git status`에 나오는 모든 변경 파일이 `Files Changed`에 목적과 함께 있다.
- [ ] 문서에 적은 모든 경로가 실제로 존재한다.
- [ ] `Next Recommended Action`에 첫 파일·심볼, 수행할 변경, 직후 검증 명령이 모두 있다.
- [ ] 코드 주석·커밋 메시지·기존 문서의 진행 주장을 옮겨 적었다면, 코드로 확인했거나 `Unverified`로 표시했다.
- [ ] 커밋되지 않은 변경이 있다면 `Current Status`에 적었고, 보고에서 커밋을 제안했다.

### 종료 모드

- [ ] 완료 조건마다 증거가 대응된 표를 보고에 포함했다.
- [ ] 승격 대상과 변경안을 제시하고 승인을 받은 뒤에만 기존 문서를 수정하거나 새 문서를 만들었다.
- [ ] 승격한 각 정보의 대상 경로를 적었다.
- [ ] handoff 제거·archive는 사용자 승인을 받은 뒤에만 수행했다.

## 참고

다음 세션 재개는 `session-resume` 스킬을 쓴다.
