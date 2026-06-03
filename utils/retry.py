import time
import random
from functools import wraps
from typing import Callable, Any


def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exceptions: tuple = (Exception,),
):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exc = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt == max_retries - 1:
                        break
                    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 0.5), max_delay)
                    time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator


def is_rate_limit_error(e: Exception) -> bool:
    msg = str(e).lower()
    return any(k in msg for k in ("rate limit", "quota", "429", "resource_exhausted", "too many requests"))


def is_model_fallback_error(e: Exception) -> bool:
    msg = str(e).lower()
    return any(k in msg for k in ("rate limit", "quota", "429", "resource_exhausted", "too many requests", "404", "not found", "not supported"))


def safe_call(func: Callable, *args, fallback: Any = None, **kwargs) -> Any:
    try:
        return func(*args, **kwargs)
    except Exception:
        return fallback

