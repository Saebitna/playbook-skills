import unittest

from src.limiter import TokenBucket


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


class TokenBucketTest(unittest.TestCase):
    def test_rate_limit(self):
        clock = FakeClock()
        b = TokenBucket(rate=10, burst=1, clock=clock)
        self.assertTrue(b.allow("ip1"))
        self.assertFalse(b.allow("ip1"))
        clock.now = 0.05  # 10/s 면 0.05초로는 토큰이 차지 않는다
        self.assertFalse(b.allow("ip1"))
        clock.now = 0.15  # 0.1초가 더 지나면 토큰 1개
        self.assertTrue(b.allow("ip1"))
