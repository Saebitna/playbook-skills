---
type: regex
pattern: 'def sweep|del self\._buckets|_buckets\.pop'
match: not_contains
target:
  source: file
  path: src/limiter.py
---
