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
4. 저장소 탐지 — `**/handoff*`, `**/HANDOFF*`, `docs/handoffs/**`, `**/status*.md`, `.claude/plans/**` 를 찾는다. **기존 관행이 이 스킬의 기본값과 달라도 기존 관행을 따른다.** active 후보가 둘 이상이면 각 제목과 `Last verified`만 나열하고 무엇을 재개할지 **한 번 묻는다.**
5. 아무것도 없으면 `git log`, `git diff`, 최근 변경 파일로 재개 후보를 복구해 제시하고, 무엇을 재개할지 **한 번 묻는다.** 후보가 하나뿐이고 명확하면 묻지 않고 그 후보로 진행하되, 상태 문서 없이 복구했다는 사실을 보고한다.

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

- `Verified` — 이번 세션에 정식 수단으로 확인함. 동작에 관한 주장은 문서·`AGENTS.md`가 정한 명령의 실행 결과가 증거다. `파일:줄`은 존재·부재 같은 구조에 관한 주장에만 증거로 쓴다.
- `Unverified` — 이번 세션에 정식 수단으로 확인하지 못함. 이유를 함께 적는다: 확인 수단이 저장소 밖에 있음 / 정식 명령이 실행되지 않음 / 확인할 명령이 없음 / 이번 세션에 실행하지 않음 / 추론함.
- `Outdated` — 현재 코드·테스트·문서와 다름. 무엇과 다른지 적는다.

**검증은 실행한다.** 문서가 성공했다고 주장하는 테스트·빌드·린트 중 저장소 안에서 비파괴적으로 실행할 수 있는 것은 직접 실행한다. 실행할 수 있는데 실행하지 않은 채 `Unverified`(이번 세션에 실행하지 않음)로 두지 않는다. 실행이 오래 걸리거나 부작용이 있으면 정식 명령의 **인자만 좁혀**(단일 테스트 파일 등) 실행하고, 그것도 불가하면 이유를 적는다.

**검증은 문서·`AGENTS.md`가 정한 명령으로 한다.** 그 명령이 실행되지 않아 다른 방식(테스트 함수 직접 호출, 다른 러너, 경로 조작 등)으로 우회했다면 그 결과는 보조 증거일 뿐 `Verified`의 근거가 아니다. 우회는 정식 명령이 잡는 결함(수집 실패, 설정 누락)을 가릴 수 있기 때문이다. 그런 항목은 `Unverified`(정식 명령이 실행되지 않음)로 두고 실패 원문을 함께 적는다.

문서 안에 적힌 `Verified` 같은 표시는 **작성자의 주장**일 뿐 증거가 아니다. 그 주장도 다른 주장과 똑같이 대조한다.

불일치는 다음 표로 보고한다.

| 항목 | handoff/문서의 주장 | 현재 저장소 증거 | 판단과 조치 |
| --- | --- | --- | --- |

## 재개 판단

다음 중 하나라도 해당하면 **막는 충돌**이다.

- Next Recommended Action이 고치라는 파일·심볼이 존재하지 않거나 문서 설명과 다르다.
- 그 행동 직후 실행할 검증 명령이 현재 저장소에서 실행 불가다 (수집 실패, 의존성 누락, 명령 자체가 없음). 원인이 저장소가 아니라 실행 환경(샌드박스, 네트워크, 권한)이어도 마찬가지다 — 우회 실행으로 대신하지 않고 보고한다.
- 커밋되지 않은 기존 변경이 그 행동이 수정할 파일과 겹친다. 단, handoff의 `Files Changed`·`Current Status`에 미커밋으로 기록돼 있고 현재 diff가 그 설명과 일치하는 변경은 이전 세션의 작업이므로 충돌이 아니다.
- 문서의 목표·완료 조건이 코드나 다른 canonical 문서와 모순되어 무엇이 의도인지 판단할 수 없다.

판단은 이 순서로 한다. **막는 충돌 판정이 항상 먼저다.**

1. 막는 충돌이 있으면 → 구현을 시작하지 않는다. Next Recommended Action을 다른 행동으로 바꿔 진행하지도 않는다. 충돌을 해소하는 데 필요한 결정과 선택지를 **제안만** 하고 멈춘다.
2. 막는 충돌이 없고 Next Recommended Action이 유효하면 → **바로 수행한다.** 안전한 저장소 내부 작업과 비파괴적 검증은 승인을 기다리지 않는다.
3. 막는 충돌이 없지만 Next Recommended Action이 이미 완료됐으면 → 가장 안전하고 구체적인 다음 행동으로 바꾸고, **바꾼 행동에도 막는 충돌 기준을 다시 적용한 뒤** 수행한다. 바꾼 이유를 보고에 쓴다.

상태 문서 없이 git 이력으로 복구한 경우 Next Recommended Action이 없다. 복구한 후보와 제안하는 첫 행동을 보고하고, 수행하지 않고 멈춘다.

기존 사용자 변경(dirty worktree)은 어떤 경우에도 덮어쓰거나 되돌리지 않는다.

## 상태 문서 갱신

대조가 끝나면 대상 handoff / 상태 문서에 결과를 반영한다. 다음 세션이 같은 검증을 되풀이하거나 틀린 주장을 다시 믿지 않게 하기 위해서다.

- `Outdated`로 판정한 주장은 현재 증거로 고치거나 `Outdated` 표시와 근거를 붙인다. 원래 주장을 조용히 지우지 않는다.
- 이번 세션에 실행한 검증은 `Tests and Evidence`에 명령 원문과 결과로 갱신한다.
- Next Recommended Action을 바꿨다면 문서에도 반영한다.
- 위 갱신을 했다면 `Last verified`를 오늘 날짜(`date`로 확인)로 바꾼다.

막는 충돌로 멈췄다면 `Status: blocked`로 바꾸고 `Current Status`에 무엇이 막는지 쓴다. 문서에 `Tests and Evidence` 섹션이 없으면 추가한다.

갱신은 **handoff 형식 문서**(`session-handoff` 스킬의 구조를 따르는 문서)에 한해 승인을 기다리지 않는다. `.claude/plans/**`나 사용자가 직접 관리하는 상태 문서는 반영할 내용을 제안만 한다. 문서가 참조하는 spec, decision, architecture 같은 다른 문서는 고치지 않고 불일치만 보고한다.

## 멈추는 지점

사용자가 범위를 따로 지정하지 않았다면 **Next Recommended Action 하나와 그 직후 검증까지** 수행하고 보고한 뒤 멈춘다. Remaining Tasks를 연달아 진행하지 않는다. 사용자가 "끝까지", "남은 작업 전부"처럼 범위를 넓힌 경우에만 이어서 진행한다.

## 완료 조건

최종 보고 직전에 아래를 하나씩 확인한다. 채우지 못한 항목은 빼지 말고 이유와 함께 보고한다.

- [ ] 대상 상태 문서의 경로와, 그 경로를 어떤 해석 단계로 찾았는지 적었다.
- [ ] 문서의 사실 주장(완료 조건별 상태, Current Status, Completed Work, Files Changed, Tests and Evidence, Known Issues)을 `Verified` / `Unverified` / `Outdated` 중 하나로 분류했다. 목표와 Next Recommended Action은 분류 대신 유효한지 판정했다.
- [ ] `Verified`마다 이번 세션의 증거가 붙어 있다. 동작 주장의 증거는 정식 명령의 실행 결과이고, 문서 자신의 표시를 증거로 쓰지 않았다.
- [ ] `Unverified`마다 이유가 붙어 있다.
- [ ] 저장소 안에서 실행 가능한 검증은 실행했고, 명령 원문과 결과를 적었다.
- [ ] 막는 충돌 여부를 위 기준으로 판정했고, 판정 근거를 적었다.
- [ ] 막는 충돌이 없었다면 다음 행동을 수행하고 그 검증 결과를 적었다. 있었다면 어떤 행동도 대신 수행하지 않았다.
- [ ] 대조 결과를 상태 문서에 반영했다(handoff 형식이 아니면 제안만 했다). 갱신했다면 `Last verified`를 오늘 날짜로 바꿨다. 상태 문서가 없었다면 그 사실을 적었다.
- [ ] 작업 시작 전 dirty 상태였던 파일의 기존 변경이 그대로 남아 있다.

## 최종 보고

- 복구한 목표와 완료 조건
- 발견한 충돌 (위 표)과 막는 충돌 판정
- 이번 세션에서 수행한 작업
- 실행한 검증과 정확한 결과 / 실행하지 못한 검증과 이유
- 다음 행동

## 참고

세션을 끝낼 때는 `session-handoff` 스킬을 쓴다.
