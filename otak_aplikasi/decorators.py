from functools import wraps
from django.core.cache import cache


def cache_view(cache_key_prefix, timeout=900, include_params=None):
    """
    Decorator untuk cache view dengan parameter dinamis
    
    Args:
        cache_key_prefix: Prefix untuk cache key
        timeout: Waktu cache dalam detik (default 15 menit)
        include_params: List parameter GET yang akan dimasukkan ke cache key
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Build cache key
            cache_key_parts = [cache_key_prefix]
            
            if include_params:
                for param in include_params:
                    value = request.GET.get(param, '')
                    cache_key_parts.append(f"{param}_{value}")
            
            cache_key = '_'.join(cache_key_parts)
            
            # Try to get from cache
            cached_data = cache.get(cache_key)
            if cached_data:
                return cached_data
            
            # Execute view and cache result
            response = view_func(request, *args, **kwargs)
            cache.set(cache_key, response, timeout)
            
            return response
        return wrapper
    return decorator
