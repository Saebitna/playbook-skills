---
name: investigation
description: Runs a hypothesis-driven investigation with controlled experiments and a written evidence log, instead of guess-and-patch debugging. Use when the same failure keeps recurring, a fix attempt has already failed once, the cause is unclear, a bug is intermittent or performance-related, or the user says "원인을 모르겠어", "계속 실패해", "조사해줘", "investigate", "why does this keep happening".
---

# Investigation

원인이 불명확한 문제를 **추측 기반 수정 반복** 대신 가설과 통제된 실험으로 좁힌다. 같은 수정을 두 번 실패했다면 구현을 계속하지 말고 이 절차로 전환한다.

## 기록 위치 결정

경로를 하드코딩하지 않는다. 위에서부터 순서대로 해결한다.

1. 사용자가 이번 요청에서 지정한 경로
2. `AGENTS.md` / `CLAUDE.md` 의 문서 규약
3. `docs/README.md` 라우터
4. 저장소 탐지 — `**/investigation*`, `docs/investigations/**`, `**/debug*.md`, 기존 조사 노트. **기존 관행이 이 스킬의 기본값과 달라도 기존 관행을 따른다.**
5. 아무것도 없으면 `docs/investigations/active/<problem>.md` 를 제안하고 **한 번 묻는다.** `docs/` 트리를 통째로 만들지 말고 필요한 파일 하나만 만든다. 조사가 짧게 끝날 것 같거나 사용자가 파일을 원하지 않으면 같은 구조를 대화 안에서 유지한다.

경로가 정해지면 "이 규약을 `AGENTS.md`에 기록할까요?"를 **제안하고 승인받은 경우에만** 추가한다.

## 시작

1. 관련 코드, 로그, 테스트, 저장소 규칙을 먼저 읽는다.
2. **재현 가능한지** 판단한다. 재현이 안 되면 그것 자체가 첫 번째 조사 대상이다.
3. `Baseline`을 고정한다 — 환경, 데이터, 입력, 현재 측정값, **재현 명령**. 실험 전에 기준값이 없으면 결과를 해석할 수 없다.

코드를 곧바로 크게 수정하지 않는다.

## 실험 루프

실험마다 아래를 기록한다. 구조와 예시는 `references/investigation-structure.md`를 읽고 따른다.

```text
Observation → Hypothesis → Experiment → Expected Result → Actual Result → Interpretation → Next
```

규율:

- **한 번에 한 변수만 바꾼다.** 두 개를 동시에 바꾸면 어느 쪽이 원인인지 알 수 없다.
- 가설은 서로 **구분 가능**해야 한다. 같은 실험으로 둘 다 지지되면 가설을 다시 나눈다.
- 실험 **전에** 예상 결과를 쓴다. 나중에 쓰면 사후 합리화가 된다.
- 재현 명령, 입력, 환경, 로그 원문을 보존한다.
- 해석은 `Supported` / `Rejected` / `Inconclusive` 중 하나로 명시한다. `Inconclusive`를 `Supported`로 반올림하지 않는다.
- **상관관계를 원인으로 단정하지 않는다.**
- 임시 진단용 변경(로그 추가, 코드 주석 처리)은 제품 수정과 분리하고, 조사가 끝나면 되돌린다.
- 기존 사용자 변경은 보존한다.
- 다음 실험은 **정보 가치가 가장 큰 것**을 고른다. 가능하면 후보를 절반으로 가르는 실험.

아직 답하지 못한 질문은 `Open Questions`, 연결된 ADR은 `Related Decisions`에 둔다.

## 중단 조건

시작할 때 중단 조건을 정한다. 사용자가 정하지 않았다면 제안한다. 예: "3회 실험 안에 원인이 좁혀지지 않으면 현재까지의 증거와 남은 가설을 보고하고 멈춘다."

조사가 원래 문제와 무관한 영역으로 번지면 별도 workstream으로 분리한다.

## 종료

원인이 확인되면 정리한다.

- **근본 원인**과 그것을 지지하는 증거
- **배제된 원인**과 배제 근거
- 수정 권고 (최소 범위)
- 재발을 잡을 **회귀 테스트**
- 남은 불확실성

중요한 기술 선택이 필요해지면 `decision-record` 스킬로 승격한다. 현재 architecture 설명이 바뀌면 갱신 후보 위치를 제시한다. 조사가 끝나면 문서 상태를 `resolved`로 바꾸거나 archive한다 — 파일 삭제·이동은 승인 없이 하지 않는다.

