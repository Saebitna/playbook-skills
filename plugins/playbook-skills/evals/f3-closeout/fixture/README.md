# Search API

## 사용법

```python
from src.search import find_docs

results = find_docs("query", limit=10)
```

## 설정

| 키 | 기본값 | 설명 |
| --- | --- | --- |
| `SEARCH_INDEX_PATH` | `./index` | 인덱스 위치 |
