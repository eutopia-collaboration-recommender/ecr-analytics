import json


def parse_filter(filters: list, filter_name: str) -> str:
    """
    Parse the filter value from the list of filters.
    :param filters: List of filters.
    :param filter_name: Name of the filter to parse.
    :return: The filter value.
    """
    filter_value = None
    for filter_str in filters:
        filter_dict = json.loads(filter_str)
        if filter_dict['filter-name'] == filter_name:
            filter_value = filter_dict['filter-value']
            break

    if filter_value is None:
        filter_value = 'none'

    return filter_value


def cols_to_title(df_cols: list) -> list:
    """
    Turn column names from snake case to title case and replace underscores with spaces.
    :param df_cols: The column names.
    :return: The column names in title case.
    """
    return [col.replace('_', ' ').title() for col in df_cols]
