# find_docs 를 search 로 개편

Status: active
Last verified: 2026-09-10

## Goal and Acceptance Criteria

1. `find_docs` 를 `search(query, limit, ranker)` 로 바꾼다. — `Unverified`(이번 세션에 실행하지 않음)
2. 랭커를 `SEARCH_RANKER` 로 고를 수 있다. — `Unverified`(이번 세션에 실행하지 않음)

## Current Status

`src/search.py` 에 구현 중. 문서는 아직 옛 이름을 설명한다.

## Next Recommended Action

`src/search.py` 의 `search` 구현을 마치고 README 와 `docs/api.md` 를 갱신한다.
