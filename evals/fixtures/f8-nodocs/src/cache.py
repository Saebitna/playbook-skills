# 세션 캐시. 만료 정책을 LRU 로 바꿨다.
from collections import OrderedDict

_store = OrderedDict()
MAX = 1000


def put(k, v):
    if k in _store:
        _store.move_to_end(k)
    _store[k] = v
    if len(_store) > MAX:
        _store.popitem(last=False)
