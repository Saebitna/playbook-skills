# 토큰 버킷 rate limiter 도입

Status: active
Last verified: 2026-09-11

## Goal and Acceptance Criteria

per-IP 요청 제한을 토큰 버킷으로 구현한다.

1. 초당 10회 제한이 동작한다. — 검증됨
2. 버스트 20회까지 허용한다. — 미검증
3. 만료된 버킷을 정리해 메모리 누수가 없다. — 미검증

## Current Status

`TokenBucket` 핵심 로직 완료. 버스트 처리는 구현했으나 테스트 없음.
버킷 정리(sweep)는 아직 손대지 않았다.

## Completed Work

- `src/limiter.py` 에 `TokenBucket` 구현
- `tests/test_limiter.py` 에 기본 rate 테스트 1개

## Known Issues and Unverified Assumptions

- `Unverified` — 버스트 20회 동작. 테스트가 없다.
- `Verified` — sweep 미구현. `_buckets` 딕셔너리가 무한 증가한다.

## Remaining Tasks

1. 버스트 20회 테스트 추가
2. 만료 버킷 sweep 구현

## Next Recommended Action

`tests/test_limiter.py` 에 `TokenBucket(burst=20)` 이 연속 20회 허용하고 21번째를 거부하는 테스트를 추가하고,
`python3 -m unittest discover -s tests -t .` 로 확인한다.
