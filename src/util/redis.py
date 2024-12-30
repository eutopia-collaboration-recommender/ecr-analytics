import json

import pandas as pd
import redis

from src.util.dash_common.app_config import AppConfig
from src.util.postgres import query


def redis_query(app_config: AppConfig,
                query_str: str) -> pd.DataFrame:
    """
    Fetch the data from Postgres and cache the result.
    :param app_config: The app_config.
    :param query_str: The query.
    :return: The data.
    """
    # Check if the query result is already in the cache
    cache_key: str = f"postgres_cache:{query_str}"
    results: pd.DataFrame | None = None
    try:
        cached_result: str = app_config.redis_client.get(cache_key)

        if cached_result:
            if app_config.verbose:
                app_config.logger.debug(f"Cache hit for query: {query_str}")
            # Return cached result if available
            return pd.DataFrame(json.loads(cached_result))

        else:
            if app_config.verbose:
                app_config.logger.debug(f"Cache miss for query: {query_str}")
            # Otherwise, query Postgres
            results = query(
                conn=app_config.pg_connection,
                query_str=query_str
            )

            # Cache the result for future use
            app_config.redis_client.set(cache_key, json.dumps(results.to_dict('records')), ex=3600)  # Cache for 1 hour
    except redis.ConnectionError as e:
        if app_config.verbose:
            app_config.logger.debug(f"Redis connection error: {e}")
            # Otherwise, query Postgres
            results = query(
                conn=app_config.pg_connection,
                query_str=query_str
            )
    return results
