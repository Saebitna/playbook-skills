from src.limiter import TokenBucket


def test_rate_limit():
    b = TokenBucket(rate=10, burst=1)
    assert b.allow("ip1") is True
    assert b.allow("ip1") is False
