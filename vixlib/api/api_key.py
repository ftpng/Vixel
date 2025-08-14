import time
from typing import Dict, Deque
from collections import defaultdict, deque


_api_usage: Dict[str, Deque[float]] = defaultdict(deque)

def get_api_key(keys: list):
    """
    Select an API key with the lowest usage in the last 60 seconds.

    This function keeps track of API key usage timestamps in `_api_usage` and ensures
    that the key with the fewest calls in the past minute is returned.
    It updates the usage record for the selected key before returning it.

    :param keys: A list of API keys (strings) to choose from.
                 Keys that are None or empty are ignored.
    :return: The API key string with the lowest recent usage.
    :raises RuntimeError: If no valid API keys are available.
    """
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