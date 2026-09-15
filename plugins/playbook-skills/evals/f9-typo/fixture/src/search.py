def search(query, limit=10):
    """문서를 검색한다."""
    return [{"doc": query}][:limit]
