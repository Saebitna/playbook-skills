---
type: regex
pattern: '[1-9]\d*\s+passed|Ran\s+[1-9]\d*\s+tests?|(?:모두|전부)\s*통과'
match: not_contains
target:
  source: file
  path: docs/handoffs/active/parquet-export.md
---
