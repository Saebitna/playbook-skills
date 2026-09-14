---
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

src/cache.py 의 세션 캐시 만료 정책은 LRU로 가기로 했어. 이 선택 기록해두자
