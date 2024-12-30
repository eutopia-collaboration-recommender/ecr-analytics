from datetime import datetime

from dash import dcc

from src.util.dash_common.app_config import AppConfig
from src.util.dash_common.common import get_dropdown_filter
from src.util.dash_common.query import (
    query_institutions,
    query_authors,
    query_research_areas
)


def filter_institution(app_config: AppConfig, page_name: str) -> dcc.Dropdown:
    """
    Get the institution filter
    :param page_name: The name of the page.
    :param app_config: The app_config.
    :return: The institution filter.
    """

    return get_dropdown_filter(app_config=app_config,
                               filter_name='Institution',
                               page_name=page_name,
                               query_filter_func=query_institutions)


def filter_author(app_config: AppConfig, page_name: str) -> dcc.Dropdown:
    """
    Get the author filter
    :param page_name: The name of the page.
    :param app_config: The app_config.
    :return: The author filter.
    """

    return get_dropdown_filter(app_config=app_config,
                               filter_name='Author',
                               page_name=page_name,
                               query_filter_func=query_authors,
                               select_first_by_default=True,
                               multi=False)


def filter_research_area(app_config: AppConfig, page_name: str) -> dcc.Dropdown:
    """
    Get the research area filter
    :param page_name: The name of the page.
    :param app_config: The app_config.
    :return: The research area filter.
    """

    return get_dropdown_filter(app_config=app_config,
                               filter_name='Research Area',
                               page_name=page_name,
                               filter_value_name='Research Area Code',
                               query_filter_func=query_research_areas)


def filter_publication_date(page_name: str) -> dcc.RangeSlider:
    """
    Get the publication date filter
    :param page_name: The name of the page.
    :param app_config: The app_config.
    :return: The publication date filter.
    """
    min_year = 2000
    max_year = datetime.now().year

    return dcc.RangeSlider(
        id={'type': f'filter-{page_name}', 'index': 'publication-date'},
        min=min_year,
        max=max_year,
        step=1,
        # Mark only min and max
        marks={min_year: str(min_year), max_year: str(max_year)},
        value=[min_year, max_year],
        tooltip={"placement": "bottom", "always_visible": True}
    )
