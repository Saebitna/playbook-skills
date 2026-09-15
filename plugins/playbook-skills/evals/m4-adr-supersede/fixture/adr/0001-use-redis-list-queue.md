# 0001. 작업 큐로 Redis List 사용

Status: accepted
Date: 2026-06-10

## Context

비동기 작업 큐가 필요했다. Redis 는 이미 캐시로 운영 중이다.

## Decision

`RPUSH` / `BLPOP` 기반 Redis List 를 작업 큐로 쓴다.

## Consequences

- 인프라 추가 없음
- ack 와 재처리가 없어 워커가 죽으면 작업이 사라진다
