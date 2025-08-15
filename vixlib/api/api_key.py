import time
from typing import Dict, Deque
from collections import defaultdict, deque


_api_usage: Dict[str, Deque[float]] = defaultdict(deque)

def get_api_key(keys: list):
    now: time = time.time()

    _key: str = None
    _count: float = float("inf")

    for key in keys:
        if not key:
            continue

        while _api_usage[key] and now - _api_usage[key][0] > 60:
            _api_usage[key].popleft()

        count = len(_api_usage[key])

        if count < _count:
            _key = key
            _count = count

    if not _key:
        raise RuntimeError("No valid API keys available")

    _api_usage[_key].append(now)
    return _key