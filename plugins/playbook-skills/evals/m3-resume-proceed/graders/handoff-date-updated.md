---
type: regex
pattern: '^Last verified: 2026-09-12\s*$'
flags: m
match: not_contains
target:
  source: file
  path: docs/handoffs/active/rate-limiter.md
---
