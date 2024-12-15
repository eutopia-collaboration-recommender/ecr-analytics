import re
import dash
import dash_bootstrap_components as dbc

from dash import ALL, callback, html, Input, Output

from src.util.author.filter import filter_author
from src.util.author.visual import cards_base_metrics, published_articles
from src.util.config import GLOBAL_CONFIG
from src.util.common import parse_filter


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
                filter_author(settings=GLOBAL_CONFIG),
                width=6
            )]
        )
    ],
        fluid=True,
        className="mt-4"
    )


# -------------------- CALLBACKS --------------------
@callback(Output('author-overview', 'children'),
          Input({'type': 'filter-overview', 'index': ALL}, 'value'))
def page_author_overview(filters: list) -> dbc.Container:
    """
    Get the layout for the author page.
    :param settings: The settings for connection to Redis and BigQuery.
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
    author_sid = re.search(r'\(([^)]+)\)', author).group(1)

    return dbc.Container(children=[
        # Some space between the title and the cards
        dbc.Row(children=cards_base_metrics(settings=GLOBAL_CONFIG, author_sid=author_sid),
                className="gray-background-custom m-1"),
        dbc.Row(children=published_articles(settings=GLOBAL_CONFIG, author_sid=author_sid),
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
            id='author-overview')
],
    fluid=True
)
