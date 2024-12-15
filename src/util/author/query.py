import pandas as pd

from src.util.common import cols_to_title
from src.util.redis import redis_query


def filter_authors(settings: dict) -> pd.DataFrame:
    """
    Get the authors used for filtering.
    :param settings: The settings including BigQuery client, Redis client and config file.
    :return: The authors used for filtering.
    """
    query_str = f"""
    SELECT CONCAT(a.author_full_name, ' - ', a.author_orcid_id, ' (', a.author_sid, ')') AS author,
           COUNT(DISTINCT article_sid)                                                   AS article_count
    FROM fct_collaboration c
             INNER JOIN dim_author a
                        ON c.author_sid = a.author_sid
    WHERE c.institution_sid = 'UNI_LJ'
    GROUP BY author
    HAVING COUNT(DISTINCT article_sid) > 10
    ORDER BY article_count DESC
    """

    # Fetch the data
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data


def query_cards(settings: dict,
                author_sid: str) -> pd.DataFrame:
    """
    Get the overview cards.
    :param settings: The settings.
    :return: The overview cards.
    """
    query_str = f"""
    WITH df_publications AS (SELECT COUNT(DISTINCT article_sid)                                               AS articles,
                                    COUNT(DISTINCT CASE WHEN is_sole_author_publication THEN article_sid END) AS single_author_publications,
                                    COUNT(DISTINCT CASE WHEN is_internal_collaboration THEN article_sid END)  AS internal_collaborations,
                                    COUNT(DISTINCT CASE WHEN is_external_collaboration THEN article_sid END)  AS external_collaborations,
                                    COUNT(DISTINCT CASE WHEN is_eutopian_collaboration THEN article_sid END)  AS eutopian_collaborations
                             FROM fct_collaboration
                             WHERE DATE_PART('year', article_publication_dt::DATE) >= 2000
                               AND institution_sid IS NOT NULL
                               AND institution_sid <> 'n/a'
                               AND is_eutopian_publication
                               AND is_article_relevant
                               AND author_sid = '{author_sid}'),
         df_collaborators AS (SELECT COUNT(DISTINCT c2.author_sid) AS collaborators
                              FROM fct_collaboration c1
                                       INNER JOIN fct_collaboration c2
                                                  ON c1.article_sid = c2.article_sid
                              WHERE c1.author_sid = '{author_sid}'
                                AND c1.author_sid <> c2.author_sid)
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
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data


def query_published_articles(settings: dict,
                             author_sid: str) -> pd.DataFrame:
    """
    Get the published articles.
    :param settings: The settings.
    :return: The published articles.
    """
    query_str = f"""
    SELECT a.article_doi,
           a.article_title,
           f.normalized_article_citation_count               as normalized_citations,
           f.collaboration_novelty_index,
           DATE_PART('year', a.article_publication_dt::DATE) as publication_year
    FROM fct_collaboration c
             INNER JOIN dim_article a
                        ON c.article_sid = a.article_sid
             INNER JOIN fct_article f
                        ON c.article_sid = f.article_sid
    WHERE author_sid = '{author_sid}'
    ORDER BY a.article_publication_dt DESC
    """

    # Fetch the data
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data
