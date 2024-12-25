from src.util.common import cols_to_title
from src.util.redis import redis_query


def query_cards(settings: dict):
    """
    Get the overview cards.
    :param settings: The settings.
    :return: The overview cards.
    """

    query_str = f"""
    SELECT COUNT(DISTINCT article_id)                                                   AS articles,
           COUNT(DISTINCT author_id)                                                    AS authors,
           COUNT(DISTINCT CASE WHEN is_single_author_collaboration THEN article_id END) AS single_author_publications,
           COUNT(DISTINCT CASE WHEN is_internal_collaboration THEN article_id END)      AS internal_collaborations,
           COUNT(DISTINCT CASE WHEN is_external_collaboration THEN article_id END)      AS external_collaborations,
           COUNT(DISTINCT CASE WHEN is_eutopia_collaboration THEN article_id END)       AS eutopian_collaborations
    FROM fct_collaboration
    """

    # Fetch the data
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    return data


def query_trend_eutopia_collaboration(settings: dict):
    """
    Get the trend of Eutopia collaborations.
    :param settings: The settings.
    :return: The trend of Eutopia collaborations.
    """

    query_str = f"""
        SELECT DATE_PART('year', article_publication_dt)                              AS year,
               COUNT(DISTINCT CASE WHEN is_eutopia_collaboration THEN article_id END) AS eutopian_collaborations
        FROM fct_collaboration
        GROUP BY 1
        ORDER BY 1 ASC
    """

    # Fetch the data
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)

    return data


def query_breakdown_publications_by_institution(settings):
    """
    Get the breakdown of publications by institution.
    :param settings: The settings.
    :return: The breakdown of publications by institution.
    """

    query_str = f"""
        SELECT institution_id              AS institution,
               COUNT(DISTINCT article_id) AS articles
        FROM fct_collaboration
        GROUP BY 1
        ORDER BY 2 ASC
    """

    # Fetch the data
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)

    return data


def query_trend_articles_by_collaboration_type(settings):
    """
    Get the trend of publications by collaboration type.
    :param settings: The settings.
    :return: The trend of publications by collaboration type.
    """

    query_str = f"""
        SELECT DATE_PART('year', article_publication_dt)                                    AS year,
               COUNT(DISTINCT CASE WHEN is_internal_collaboration THEN article_id END)      AS internal_collaborations,
               COUNT(DISTINCT CASE WHEN is_external_collaboration THEN article_id END)      AS external_collaborations,
               COUNT(DISTINCT CASE WHEN is_single_author_collaboration THEN article_id END) AS single_author_publications
        FROM fct_collaboration
        GROUP BY 1
        ORDER BY 1 ASC
    """

    # Fetch the data
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)

    return data


def query_eutopia_collaboration_funnel(settings):
    """
    Get the funnel of Eutopia collaborations.
    :param settings: The settings.
    :return: The funnel of Eutopia collaborations.
    """

    query_str = f"""
         SELECT 'Total Articles'           AS stage
             , 1                          AS stage_index
             , COUNT(DISTINCT article_id) AS count
        FROM fct_collaboration
        GROUP BY 1, 2
        UNION ALL
        SELECT 'Collaborations'                                                                                     AS stage
             , 2                                                                                                    AS stage_index
             , COUNT(DISTINCT CASE WHEN is_external_collaboration or is_internal_collaboration THEN article_id END) AS count
        FROM fct_collaboration
        GROUP BY 1, 2
        UNION ALL
        SELECT 'External Collaborations'                                               AS stage
             , 3                                                                       AS stage_index
             , COUNT(DISTINCT CASE WHEN is_external_collaboration THEN article_id END) AS count
        FROM fct_collaboration
        GROUP BY 1, 2
        UNION ALL
        SELECT 'Eutopia Collaborations'                                               AS stage
             , 4                                                                      AS stage_index
             , COUNT(DISTINCT CASE WHEN is_eutopia_collaboration THEN article_id END) AS count
        FROM fct_collaboration
        GROUP BY 1, 2
    """

    # Fetch the data
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)

    # Sort by index
    data = data.sort_values(by='Stage Index')

    return data


def query_trend_new_collaborations(settings):
    """
    Get the trend of new collaborations.
    :param settings: The settings.
    :return: The trend of new collaborations.
    """

    query_str = f"""        
        SELECT DATE_PART('year', article_publication_dt)                                       AS year,
           COUNT(DISTINCT CASE
                              WHEN has_new_author_collaboration
                                  THEN article_id END)                                          AS new_author_collaborations,
           COUNT(DISTINCT CASE
                              WHEN has_new_institution_collaboration
                                  THEN article_id END)                                          AS new_institution_collaborations,
           COUNT(DISTINCT CASE
                              WHEN NOT has_new_author_collaboration
                                  AND NOT has_new_institution_collaboration THEN article_id END) AS existing_collaborations
        FROM fct_collaboration
        WHERE NOT is_single_author_collaboration
        GROUP BY 1
        ORDER BY 1 ASC
    """

    # Fetch the data
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)

    return data


def query_collaboration_novelty_index_distribution(settings):
    """
    Get the distribution of the collaboration novelty index.
    :param settings: The settings.
    :return: The distribution of the collaboration novelty index.
    """

    query_str = f"""
        WITH articles AS (SELECT DISTINCT article_id
                          FROM fct_collaboration)
        SELECT cn.article_id,
               cn.collaboration_novelty_index
        FROM fct_article cn
                 INNER JOIN articles USING (article_id)
    """

    # Fetch the data
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)
    data = data[
        (data['Collaboration Novelty Index'] <
         data['Collaboration Novelty Index'].quantile(
             0.95))]

    return data


def query_research_areas(settings):
    """
    Get the research areas.
    :param settings: The settings.
    :return: The research areas.
    """

    query_str = f"""
        SELECT research_area_name AS research_area
        FROM dim_research_area
    """

    # Fetch the data
    data = redis_query(settings=settings,
                       query_str=query_str)

    # Turn column names from snake case to title case and replace underscores with spaces
    data.columns = cols_to_title(data.columns)

    return data
