# 토큰 버킷 rate limiter 도입

Status: active
Last verified: 2026-09-12

## Goal and Acceptance Criteria

per-IP 요청 제한을 토큰 버킷으로 구현한다.

1. 초당 10회 제한이 동작한다. — `Verified` (`test_rate_limit`)
2. 버스트 20회까지 허용한다. — `Unverified` (테스트 없음)
3. 만료된 버킷을 정리해 메모리 누수가 없다. — `Unverified` (미구현)

## Current Status

`TokenBucket` 핵심 로직과 시계 주입 완료. 버스트는 구현돼 있으나 테스트가 없다. sweep 은 아직 없다. 모든 변경은 커밋됨.

## Files Changed

- `src/limiter.py` — `TokenBucket`, 시계 주입 (커밋됨)
- `tests/test_limiter.py` — `FakeClock`, `test_rate_limit` (커밋됨)

## Tests and Evidence

```text
python3 -m unittest discover -s tests -t .  →  Ran 1 test, OK
```

## Remaining Tasks

1. 버스트 20회 테스트 추가
2. 만료 버킷 sweep 구현 (1 이후)

## Next Recommended Action

`tests/test_limiter.py` 의 `TokenBucketTest` 에 `FakeClock` 을 쓰는 `test_burst_allows_20` 을 추가한다:
`TokenBucket(rate=10, burst=20)` 이 같은 키로 21번 호출하면 정확히 20번 허용하는지 확인.
직후 `python3 -m unittest discover -s tests -t .` 실행.
