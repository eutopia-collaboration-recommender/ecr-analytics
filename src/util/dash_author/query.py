import pandas as pd

from src.util.dash_common.app_config import AppConfig
from src.util.dash_common.common import cols_to_title
from src.util.redis import redis_query


def query_cards(app_config: AppConfig,
                author_id: str) -> pd.DataFrame:
    """
    Get the dash_overview cards.
    :param app_config: The app_config.
    :return: The dash_overview cards.
    """
    query_str = f"""
        WITH df_publications AS (SELECT COUNT(DISTINCT article_id)                                                   AS articles,
                                        COUNT(DISTINCT CASE
                                                           WHEN is_single_author_collaboration
                                                               THEN article_id END)                                  AS single_author_publications,
                                        COUNT(DISTINCT CASE WHEN is_internal_collaboration THEN article_id END)      AS internal_collaborations,
                                        COUNT(DISTINCT CASE WHEN is_external_collaboration THEN article_id END)      AS external_collaborations,
                                        COUNT(DISTINCT CASE WHEN is_eutopia_collaboration THEN article_id END)       AS eutopian_collaborations
                                 FROM fct_collaboration
                                 WHERE author_id = '{author_id}'),
             df_collaborators AS (SELECT COUNT(DISTINCT c2.author_id) AS collaborators
                                  FROM fct_collaboration c1
                                           INNER JOIN fct_collaboration c2
                                                      ON c1.article_id = c2.article_id
                                  WHERE c1.author_id = '{author_id}'
                                    AND c1.author_id <> c2.author_id)
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
                             author_id: str) -> pd.DataFrame:
    """
    Get the published articles.
    :param app_config: The app_config.
    :return: The published articles.
    """
    query_str = f"""
        SELECT a.article_doi,
               a.article_title,
               f.article_citation_normalized_count         as normalized_citations,
               f.collaboration_novelty_index,
               DATE_PART('year', a.article_publication_dt) as publication_year
        FROM fct_collaboration c
                 INNER JOIN dim_article a
                            ON c.article_id = a.article_id
                 INNER JOIN fct_article f
                            ON c.article_id = f.article_id
        WHERE author_id = '{author_id}' 
        ORDER BY a.article_publication_dt DESC
    """

    # Fetch the data
    data = redis_query(app_config=app_config,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data
