import json

import pandas as pd
import redis

from src.util.postgres import query


def redis_query(settings: dict,
                query_str: str) -> pd.DataFrame:
    """
    Fetch the data from Postgres and cache the result.
    :param settings: The settings.
    :param query_str: The query.
    :return: The data.
    """
    # Check if the query result is already in the cache
    cache_key: str = f"postgres_cache:{query_str}"
    results: pd.DataFrame | None = None
    try:
        cached_result: str = settings['redis_client'].get(cache_key)

        if cached_result:
            if settings['config'].DASHBOARD.VERBOSE:
                print(f"Cache hit for query: {query_str}")
            # Return cached result if available
            return pd.DataFrame(json.loads(cached_result))

        else:
            if settings['config'].DASHBOARD.VERBOSE:
                print(f"Cache miss for query: {query_str}")
            # Otherwise, query Postgres
            results = query(
                conn=settings['pg_connection'],
                query=query_str
            )

            # Cache the result for future use
            settings['redis_client'].set(cache_key, json.dumps(results.to_dict('records')), ex=3600)  # Cache for 1 hour
    except redis.ConnectionError as e:
        if settings['config'].DASHBOARD.VERBOSE:
            print(f"Redis connection error: {e}")
            # Otherwise, query Postgres
            results = query(
                conn=settings['pg_connection'],
                query=query_str
            )
    return results
