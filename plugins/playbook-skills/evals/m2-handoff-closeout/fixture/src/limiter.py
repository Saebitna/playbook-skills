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

    def sweep(self, max_idle):
        """max_idle 초 넘게 요청이 없던 버킷을 지운다."""
        now = self._clock()
        for key in [k for k, (_, last) in self._buckets.items() if now - last > max_idle]:
            del self._buckets[key]
