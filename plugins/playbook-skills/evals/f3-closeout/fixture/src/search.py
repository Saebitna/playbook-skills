import os

INDEX_PATH = os.environ.get("SEARCH_INDEX_PATH", "./index")


def find_docs(query, limit=10):
    """질의에 맞는 문서를 반환한다."""
    return [{"doc": query}][:limit]
