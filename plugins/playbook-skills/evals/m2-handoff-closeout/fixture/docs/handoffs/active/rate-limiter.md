# 토큰 버킷 rate limiter 도입

Status: active
Last verified: 2026-09-12

## Goal and Acceptance Criteria

per-IP 요청 제한을 토큰 버킷으로 구현한다.

1. 초당 10회 제한이 동작한다. — `Verified` (`tests/test_limiter.py::test_rate_limit`)
2. 버스트 20회까지 허용한다. — `Verified` (`test_burst_allows_20`)
3. 만료된 버킷을 정리해 메모리 누수가 없다. — `Verified` (`test_sweep_removes_idle_buckets`)

## Current Status

세 조건 모두 구현과 테스트 완료. 모든 변경은 커밋됨.

## Key Decisions

- 시계를 주입(`clock`)해 테스트에서 시간을 제어한다. 이유: `time.sleep` 기반 테스트가 느리고 불안정했다.
- sweep 은 호출자가 주기적으로 부른다. 이유: 백그라운드 스레드를 두지 않아 프로세스 모델에 의존하지 않는다.

## Rejected Approaches / Do Not Redo

- 요청마다 sweep: 요청 경로 지연이 커져 폐기. 요청량이 초당 100건 미만인 서비스라면 재검토할 만하다.

## Tests and Evidence

```text
python3 -m unittest discover -s tests -t .  →  Ran 3 tests, OK
```

## Remaining Tasks

없음.

## Next Recommended Action

workstream 종료 정리.
