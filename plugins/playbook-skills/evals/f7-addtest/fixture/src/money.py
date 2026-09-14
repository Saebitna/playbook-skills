from decimal import Decimal


def split_evenly(total, n):
    """금액을 n 등분한다. 나머지는 앞쪽부터 1 센트씩 배분한다."""
    if n <= 0:
        raise ValueError("n must be positive")
    cents = int(Decimal(str(total)) * 100)
    base, rem = divmod(cents, n)
    return [Decimal(base + (1 if i < rem else 0)) / 100 for i in range(n)]
