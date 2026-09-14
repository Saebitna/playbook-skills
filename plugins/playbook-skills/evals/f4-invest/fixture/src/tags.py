def primary_tag(tags):
    """가장 우선순위 높은 태그를 반환한다."""
    candidates = {t for t in tags if t.startswith("pri:")}
    if not candidates:
        return None
    return next(iter(candidates))
