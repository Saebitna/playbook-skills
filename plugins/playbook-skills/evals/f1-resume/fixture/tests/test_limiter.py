import unittest

from src.limiter import TokenBucket


class RateLimitTest(unittest.TestCase):
    def test_rate_limit(self):
        b = TokenBucket(rate=10, burst=1)
        self.assertIs(b.allow("ip1"), True)
        self.assertIs(b.allow("ip1"), False)
