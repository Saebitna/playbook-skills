# 0001. 패키지 매니저로 uv 사용

Status: accepted
Date: 2026-07-02

## Context

pip + venv 조합은 lock 재현성이 약했다.

## Decision

`uv` 를 표준 패키지 매니저로 쓴다.

## Consequences

- 설치 속도 개선, `uv.lock` 으로 재현성 확보
- 팀원이 uv 를 설치해야 한다
