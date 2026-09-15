---
type: tool_used
tool: Bash
input_match: '(?:sed\s+-i|perl\s+-i)[^;&|]*(?:src|tests)/|>>?\s*\S*(?:src|tests)/|\btee\s+\S*(?:src|tests)/|(?:git|\$[A-Za-z_]\w*)\s+(?:checkout|restore|apply|stash)\b'
min: 0
max: 0
---
