import json
from json import JSONDecodeError

from dash import dcc

from src.util.dash_common.app_config import AppConfig


def parse_filter(filter: list, filter_name: str) -> list | None:
    """
    Parse the filter value from the list of filters.
    :param filters: List of filters.
    :param filter_name: Name of the filter to parse.
    :return: The filter value.
    """
    try:
        values = list()
        for f in filter:
            if f is None:
                continue
            if type(f) != str:
                continue
            # Parse the filter value
            filter_dict = json.loads(f)
            values.append("'" + filter_dict['filter-value'] + "'")
        return values
    except JSONDecodeError:
        return None


def parse_filters(filters: list,
                  filter_ids: list) -> dict:
    """
    Parse the filter values from the list of filters.
    :param filters: List of filters.
    :param filter_ids: List of filter ids.
    :return: The filter values.
    """
    filter_scope = dict()
    for id, value in zip(filter_ids, filters):
        if id['index'] == 'article_publication_dt':
            filter_scope[
                'article_publication_dt'] = f'EXTRACT(YEAR FROM article_publication_dt) BETWEEN {value[0]} AND {value[1]}'
        else:
            filter_name = id['index']
            if type(value) != list:
                value = [value]
            filter_value = parse_filter(filter=value, filter_name=filter_name)
            filter_scope[filter_name] = f'{filter_name} IN ({", ".join(filter_value)})' if filter_value else 'TRUE'

    return filter_scope


def cols_to_title(df_cols: list) -> list:
    """
    Turn column names from snake case to title case and replace underscores with spaces.
    :param df_cols: The column names.
    :return: The column names in title case.
    """
    return [col.replace('_', ' ').title() for col in df_cols]


def get_dropdown_filter(app_config: AppConfig,
                        filter_name: str,
                        page_name: str,
                        query_filter_func: callable,
                        filter_value_name: str = None,
                        select_first_by_default: bool = False,
                        multi: bool = True) -> dcc.Dropdown:
    """
    Get the filter for the page.
    :param multi: Whether the dropdown is multi-select.
    :param app_config: The app_config.
    :param filter_name: The name of the filter.
    :param page_name: The name of the page.
    :param query_filter_func: The function to query the filter data.
    :param select_first_by_default: Whether to select the first entry by default.
    :return: The filter.
    """

    # Fetch filter data using the filter_institutions function
    df = query_filter_func(app_config=app_config)
    filter_name_lower = filter_name.lower().replace(' ', '_')

    if filter_value_name is None:
        filter_value_name = filter_name
    filter_name_value_lower = filter_value_name.lower().replace(' ', '_')
    # Check if df is not empty and create dropdown options
    if not df.empty:
        options = [
            {'label': row[filter_name],
             'value': json.dumps({'filter-name': filter_name_value_lower, 'filter-value': row[filter_value_name]})}
            for index, row in df.iterrows()
        ]
        # Set the first institution as the default value
        default_value = '/' if not select_first_by_default else options[0]['value']
    else:
        # Default options if df is empty
        options = [
            {'label': 'No entries available', 'value': '/'}
        ]
        default_value = '/'

    return dcc.Dropdown(
        id={'type': f'filter-{page_name}', 'index': filter_name_value_lower},
        options=options,
        placeholder=f"Select an entry",
        value=default_value,
        searchable=True,
        multi=multi
    )
