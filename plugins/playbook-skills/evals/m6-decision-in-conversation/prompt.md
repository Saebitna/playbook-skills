---
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
---

좋아, Redis Streams 로 가자. src/queue.py 의 enqueue 를 XADD 로 구현해줘
