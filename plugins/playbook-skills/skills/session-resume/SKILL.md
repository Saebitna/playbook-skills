---
name: session-resume
description: Recovers and verifies workstream state from a handoff document before resuming multi-session work. Use when the user says "이어서 작업", "이어서 해줘", "재개", "resume", "pick up where we left off", hands off from another agent or session, points at a handoff/status document, or restarts after a context compaction. Verifies handoff claims against the actual repository instead of trusting them.
---

# Session Resume

Handoff나 상태 문서를 **사실로 가정하지 않고 저장소와 대조해 검증**한 뒤, 막는 충돌이 없으면 바로 다음 행동을 수행한다.

## 상태 문서 위치 결정

경로를 하드코딩하지 않는다. 위에서부터 순서대로 해결한다.

1. 사용자가 이번 요청에서 지정한 경로
2. `AGENTS.md` / `CLAUDE.md` 의 문서 규약
3. `docs/README.md` 라우터
4. 저장소 탐지 — `**/handoff*`, `**/HANDOFF*`, `docs/handoffs/**`, `**/status*.md`, `.claude/plans/**` 를 찾는다. **기존 관행이 이 스킬의 기본값과 달라도 기존 관행을 따른다.**
5. 아무것도 없으면 사용자에게 재개할 대상을 묻는다. 상태 문서가 아예 없는 경우 `git log`, `git diff`, 최근 변경 파일로 상태를 복구하고 그 사실을 보고한다.

관련 없는 다른 workstream의 handoff와 archive 문서는 읽지 않는다. dependency나 역사적 근거 확인이 꼭 필요할 때만 대상 경로와 이유를 밝히고 읽는다.

## 절차

1. 적용되는 `AGENTS.md` / `CLAUDE.md` 를 읽는다.
2. `docs/README.md`(있으면)로 문서 배치를 파악한다.
3. 대상 handoff / 상태 문서를 읽는다.
4. 그 문서가 **참조하는** spec, plan, decision, investigation만 읽는다.
5. 저장소 현재 상태를 확인한다 — branch, `git status`, `git diff`, 변경 파일.
6. 문서가 언급한 코드와 테스트를 실제로 읽는다.
7. 문서의 주장과 저장소 증거를 대조한다.

## 대조 규율

문서의 모든 주장을 다음 셋 중 하나로 분류한다.

- `Verified` — 저장소 증거로 확인됨
- `Unverified` — 확인할 수단이 없음 (예: 실행 로그가 남지 않은 테스트 결과)
- `Outdated` — 현재 코드·테스트와 다름

테스트를 직접 실행하지 않았다면 통과했다고 추정하지 않는다. 불일치는 다음 표로 보고한다.

| 항목 | handoff/문서의 주장 | 현재 저장소 증거 | 판단과 조치 |
| --- | --- | --- | --- |

## 재개 판단

- 진행을 **막는** 충돌이 없으면 → Next Recommended Action이 아직 유효한지 확인하고 **바로 수행한다.** 안전한 저장소 내부 작업과 비파괴적 검증은 승인을 기다리지 않는다.
- Next Recommended Action이 유효하지 않으면 → 가장 안전하고 구체적인 다음 행동으로 갱신한 뒤 수행한다.
- 막는 충돌이 있으면 → 큰 구현을 시작하지 않고 충돌과 필요한 결정을 보고한다.

기존 사용자 변경(dirty worktree)은 어떤 경우에도 덮어쓰거나 되돌리지 않는다.

## 최종 보고

- 복구한 목표와 완료 조건
- 발견한 충돌 (위 표)
- 이번 세션에서 수행한 작업
- 실행한 검증과 정확한 결과 / 실행하지 못한 검증과 이유
- 다음 행동

## 참고

세션을 끝낼 때는 `session-handoff` 스킬을 쓴다.
