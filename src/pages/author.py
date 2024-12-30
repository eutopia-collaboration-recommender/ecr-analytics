import re
import dash
import dash_bootstrap_components as dbc

from dash import ALL, callback, html, Input, Output

from src.util.dash_common.filter import filter_author
from src.util.dash_author.visual import cards_base_metrics, published_articles
from src.util.dash_common.app_config import app_config
from src.util.dash_common.common import parse_filter


# -------------------- PAGE LAYOUT HELPERS --------------------
def page_header():
    """
    Get the page header.
    :return: The page header.
    """
    return dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(
                html.H4("AUTHOR COLLABORATION OVERVIEW", className="text-left p-2 font-italic"),
                width=6
            ),
            dbc.Col(
                filter_author(app_config=app_config, page_name='author'),
                width=6
            )]
        )
    ],
        fluid=True,
        className="mt-4"
    )


# -------------------- CALLBACKS --------------------
@callback(Output('author-page', 'children'),
          Input({'type': 'filter-author', 'index': ALL}, 'value'))
def page_author(filters: list) -> dbc.Container:
    """
    Get the layout for the dash_author page.
    :param app_config: The app_config for connection to Redis and BigQuery.
    :param filters: The filters.
    :return: The layout.
    """

    if filters is None or len(filters) == 0:
        return dbc.Container(children=[
            dbc.Row(
                dbc.Col(
                    # Greyed text in the center of the page that no author is selected
                    html.H4("No author is currently selected. Select an author.",
                            className="text-center p-2 font-italic"),
                    width=12
                )
            )
        ],
            fluid=True,
            className="mt-4"
        )

    author = parse_filter(filters, filter_name='author')
    author_id = re.search(r'\(([^)]+)\)', author).group(1)

    return dbc.Container(children=[
        # Some space between the title and the cards
        dbc.Row(children=cards_base_metrics(app_config=app_config, author_id=author_id),
                className="gray-background-custom m-1"),
        dbc.Row(children=published_articles(app_config=app_config, author_id=author_id),
                className="gray-background-custom m-1"
                )
    ],
        className='p-4',
        fluid=True
    )


# -------------------- DASH PAGE --------------------
dash.register_page(__name__, path_name='/author')

layout = dbc.Container(children=[
    page_header(),
    # Some space between the title and the cards
    dbc.Row(children=[],
            id='author-page')
],
    fluid=True
)
