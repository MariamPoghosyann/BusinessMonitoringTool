import functools
import json
import hashlib
from django.core.cache import cache

def cache_func(func):
    """
    Decorator that automatically generates a cache key based on
    the function name and arguments, and caches the result in Redis.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a unique cache key
        key_base = f"{func.__name__}:{args}:{kwargs}"
        cache_key = f"{hashlib.md5(key_base.encode()).hexdigest()}"

        cached_data = cache.get(cache_key)
        if cached_data:
            print("aaaaaaaa")
            return cached_data

        # Otherwise, compute result and cache it
        data = func(*args, **kwargs)
        cache.set(cache_key, data)
        return data
    return wrapper

