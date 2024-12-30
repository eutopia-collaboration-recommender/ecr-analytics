import pandas as pd

from src.util.dash_common.app_config import AppConfig
from src.util.dash_common.common import cols_to_title
from src.util.redis import redis_query


def query_research_areas(app_config: AppConfig) -> pd.DataFrame:
    """
    Get the research areas.
    :param app_config: The app_config.
    :return: The research areas.
    """

    query_str = f"""
        SELECT research_area_name AS research_area,
               research_area_code AS research_area_code
        FROM dim_research_area
    """

    # Fetch the data
    data = redis_query(app_config=app_config,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)

    return data


def query_institutions(app_config: AppConfig) -> pd.DataFrame:
    """
    Get the filters for the dash_overview page.
    :param app_config: The app_config.
    :return: The filters.
    """

    query_str = f"""
        SELECT institution_id
        FROM dim_eutopia_institution
    """

    # Fetch the data
    data = redis_query(app_config=app_config,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)

    return data


def query_authors(app_config: AppConfig) -> pd.DataFrame:
    """
    Get the authors used for filtering.
    :param app_config: The app_config including BigQuery client, Redis client and config file.
    :return: The authors used for filtering.
    """
    query_str = f"""
        SELECT CONCAT(a.author_name, ' (', a.author_id, ')') AS author,
               COUNT(DISTINCT article_id)                    AS article_count,
               a.author_id
        FROM fct_collaboration c
                 INNER JOIN dim_author a
                            ON c.author_id = a.author_id
        GROUP BY author, a.author_id
        HAVING COUNT(DISTINCT article_id) > 10
        ORDER BY article_count DESC
    """

    # Fetch the data
    data = redis_query(app_config=app_config,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data
