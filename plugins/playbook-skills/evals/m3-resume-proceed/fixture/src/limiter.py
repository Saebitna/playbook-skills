import time


class TokenBucket:
    def __init__(self, rate=10, burst=20, clock=time.monotonic):
        self.rate = rate
        self.burst = burst
        self._clock = clock
        self._buckets = {}

    def allow(self, key):
        now = self._clock()
        tokens, last = self._buckets.get(key, (self.burst, now))
        tokens = min(self.burst, tokens + (now - last) * self.rate)
        if tokens < 1:
            self._buckets[key] = (tokens, now)
            return False
        self._buckets[key] = (tokens - 1, now)
        return True
