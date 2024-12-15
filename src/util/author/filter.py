import json

import dash_bootstrap_components as dbc

from dash import dcc

from src.util.author.query import filter_authors


def filter_author(settings: dict) -> dcc.Dropdown:
    """
    Get the filters for the author page.
    :param settings: The settings.
    :return: The filters.
    """

    # Fetch author data using the filter_authors function
    author_df = filter_authors(settings=settings)

    # Check if author_df is not empty and create dropdown options
    if not author_df.empty:
        options = [
            {'label': row['Author'], 'value': json.dumps({'filter-name': 'author', 'filter-value': row['Author']})}
            for index, row in author_df.iterrows()
        ]
        # Set the first author as the default value
        default_value = options[0]['value']
    else:
        # Default options if author_df is empty
        options = [
            {'label': 'No authors available', 'value': 'none'}
        ]
        default_value = 'none'

    return dcc.Dropdown(
        id={'type': 'filter-overview', 'index': 'author'},
        options=options,
        placeholder="Select an author",
        value=default_value,
        searchable=True
    )
