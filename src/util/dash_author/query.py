import pandas as pd

from src.util.dash_common.app_config import AppConfig
from src.util.dash_common.common import cols_to_title
from src.util.redis import redis_query


def query_cards(app_config: AppConfig,
                filter_scope: dict) -> pd.DataFrame:
    """
    Get the dash_overview cards.
    :param filter_scope: The filter scope.
    :param app_config: The app_config.
    :return: The dash_overview cards.
    """
    query_str = f"""
        WITH filtered_data AS (
            SELECT *
            FROM fct_collaboration
            WHERE {filter_scope['author_id']}
                AND {filter_scope['article_publication_dt']}), 
        df_publications AS (SELECT COUNT(DISTINCT article_id)                                                   AS articles,
                                        COUNT(DISTINCT CASE
                                                           WHEN is_single_author_collaboration
                                                               THEN article_id END)                                  AS single_author_publications,
                                        COUNT(DISTINCT CASE WHEN is_internal_collaboration THEN article_id END)      AS internal_collaborations,
                                        COUNT(DISTINCT CASE WHEN is_external_collaboration THEN article_id END)      AS external_collaborations,
                                        COUNT(DISTINCT CASE WHEN is_eutopia_collaboration THEN article_id END)       AS eutopian_collaborations
                                 FROM filtered_data),
             df_collaborators AS (SELECT COUNT(DISTINCT c2.author_id) AS collaborators
                                  FROM filtered_data c1
                                           INNER JOIN fct_collaboration c2
                                                      ON c1.article_id = c2.article_id
                                  WHERE c1.author_id <> c2.author_id)
        SELECT collaborators,
               articles,
               single_author_publications,
               internal_collaborations,
               external_collaborations,
               eutopian_collaborations
        FROM df_publications
                 CROSS JOIN df_collaborators
    """

    # Fetch the data
    data = redis_query(app_config=app_config,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data


def query_published_articles(app_config: AppConfig,
                             filter_scope: dict) -> pd.DataFrame:
    """
    Get the published articles.
    :param filter_scope: The filter scope.
    :param app_config: The app_config.
    :return: The published articles.
    """
    query_str = f"""
        WITH filtered_data AS (
            SELECT *
            FROM fct_collaboration
            WHERE {filter_scope['author_id']}
                AND {filter_scope['article_publication_dt']})
        SELECT DISTINCT a.article_doi,
                        a.article_title,
                        f.article_citation_count                    as citations,
                        f.collaboration_novelty_index,
                        DATE_PART('year', a.article_publication_dt) as publication_year
        FROM filtered_data c
                 INNER JOIN dim_article a
                            ON c.article_id = a.article_id
                 INNER JOIN fct_article f
                            ON c.article_id = f.article_id
        ORDER BY DATE_PART('year', a.article_publication_dt) DESC
    """

    # Fetch the data
    data = redis_query(app_config=app_config,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data


def query_co_author_embeddings(app_config: AppConfig,
                               filter_scope: dict) -> pd.DataFrame:
    """
    Get the co_author_embeddings.
    :param filter_scope: The filter scope.
    :param app_config: The app_config.
    :return: The published articles.
    """
    query_str = f"""
        WITH filtered_data AS (SELECT *
                               FROM fct_collaboration
                               WHERE {filter_scope['author_id']}
                                    AND {filter_scope['article_publication_dt']}),
             co_authors AS (SELECT DISTINCT c2.author_id
                            FROM filtered_data c1
                                     INNER JOIN fct_collaboration c2
                                                ON c1.article_id = c2.article_id
                                                    AND c1.author_id <> c2.author_id)
        SELECT c.author_id,
               a.author_name,
               e.embedding_tensor_data::float8[] AS embedding_tensor_data
        FROM co_authors c
                 INNER JOIN dim_author a
                            ON a.author_id = c.author_id
                 INNER JOIN author_embedding e
                            ON a.author_id = e.author_id
    """

    # Fetch the data
    data = redis_query(app_config=app_config,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data


def query_articles_by_research_area(app_config: AppConfig,
                                    filter_scope: dict,
                                    k: int) -> pd.DataFrame:
    """
    Get the articles by research area
    :param filter_scope: The filter scope.
    :param app_config: The app_config.
    :return: Articles by research area
    """
    query_str = f"""
        WITH filtered_data AS (SELECT *
                               FROM fct_collaboration
                               WHERE {filter_scope['author_id']}
                                    AND {filter_scope['article_publication_dt']})
        SELECT r.research_area_name         AS research_area,
               COUNT(DISTINCT f.article_id) AS articles
        FROM filtered_data f
                 INNER JOIN dim_research_area r
                            ON r.research_area_code = f.research_area_code
        GROUP BY r.research_area_name
        ORDER BY articles DESC
        LIMIT {k}
    """

    # Fetch the data
    data = redis_query(app_config=app_config,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data


def query_articles_by_keyword(app_config: AppConfig,
                              filter_scope: dict,
                              k: int) -> pd.DataFrame:
    """
    Get the articles by research area
    :param filter_scope: The filter scope.
    :param app_config: The app_config.
    :return: Articles by research area
    """
    query_str = f"""
        WITH filtered_data AS (SELECT *
                               FROM fct_collaboration
                               WHERE {filter_scope['author_id']}
                                    AND {filter_scope['article_publication_dt']})
        SELECT k.article_keyword            AS keyword,
               COUNT(DISTINCT f.article_id) AS articles
        FROM filtered_data f
                 INNER JOIN fct_article_keyword k
                            ON k.article_id = f.article_id
        GROUP BY k.article_keyword
        ORDER BY articles DESC
        LIMIT {k}
    """

    # Fetch the data
    data = redis_query(app_config=app_config,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data
