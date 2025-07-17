"""Simple in-memory caching system.

This module provides basic caching functionality using a Python dictionary.
Suitable for single-instance deployments.
"""

cache = {}

def get_cache(key):
    """Retrieve a value from cache.
    
    Args:
        key: Cache key to lookup.
        
    Returns:
        Any | None: Cached value or None if key doesn't exist.
    """
    return cache.get(key)

def set_cache(key, value):
    """Store a value in cache.
    
    Args:
        key: Cache key to store under.
        value: Value to cache.
    """
    cache[key] = value

def invalidate(key):
    """Remove a key from cache.
    
    Args:
        key: Cache key to remove.
    """
    cache.pop(key, None) 