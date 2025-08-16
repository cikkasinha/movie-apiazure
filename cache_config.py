from flask_caching import Cache

# Using 'simple' in-memory cache for demonstration.
cache = Cache(config={'CACHE_TYPE': 'simple'})
