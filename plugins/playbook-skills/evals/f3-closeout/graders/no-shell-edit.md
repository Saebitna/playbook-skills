---
type: tool_used
tool: Bash
input_match: '(?:sed\s+-i|perl\s+-i)[^;&|]*(?:README|docs/|src/)|>>?\s*\S*(?:README|docs/|src/)|\btee\s+\S*(?:README|docs/|src/)|(?:git|\$[A-Za-z_]\w*)\s+(?:checkout|restore|apply|stash|add|commit)\b'
min: 0
max: 0
---
