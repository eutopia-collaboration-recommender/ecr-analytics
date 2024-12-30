import re
import dash
import dash_bootstrap_components as dbc

from dash import ALL, callback, dcc, html, Input, Output

from src.util.dash_common.filter import filter_author, filter_publication_date
from src.util.dash_author.visual import articles_by_breakdown, author_recommendations, cards_base_metrics, \
    co_author_clustering, \
    published_articles
from src.util.dash_common.app_config import app_config
from src.util.dash_common.common import parse_filters


# -------------------- PAGE LAYOUT HELPERS --------------------
def page_header():
    """
    Get the page header.
    :return: The page header.
    """
    return dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(
                html.H4("AUTHOR COLLABORATION", className="text-left p-2 font-italic"),
                width=8
            ),
            dbc.Col(
                [
                    html.H6("PUBLICATION PERIOD", className="text-left p-2 font-italic"),
                    filter_publication_date(page_name='author')
                ],
                width=2
            ),
            dbc.Col(
                [
                    html.H6("AUTHOR", className="text-left p-2 font-italic"),
                    filter_author(app_config=app_config, page_name='author'),
                ],
                width=2
            )
        ])
    ],
        fluid=True,
        className="mt-4"
    )


# -------------------- CALLBACKS --------------------
@callback(Output('author-page', 'children'),
          Input({'type': 'filter-author', 'index': ALL}, 'value'),
          Input({'type': 'filter-author', 'index': ALL}, 'id'))
def page_author(filters: list, filter_ids: list) -> dbc.Container:
    """
    Get the layout for the dash_author page.
    :param filter_ids: The filter ids
    :param filters: The filters.
    :return: The layout.
    """
    # Get the filter values
    filter_scope = parse_filters(filters=filters, filter_ids=filter_ids)

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

    return dbc.Container(children=[
        # Some space between the title and the cards
        dbc.Row(children=cards_base_metrics(app_config=app_config, filter_scope=filter_scope),
                className="gray-background-custom m-3"),
        dbc.Row(children=[
            dbc.Col(
                [
                    dbc.Row([
                        html.H6("RESEARCH STREAMS CLUSTERING", className="text-left p-2 font-italic"),
                        dbc.Col(children=[
                            html.P("MIN SAMPLES (HDBSCAN)"),
                            dcc.Slider(id='filter-min-samples', min=1, max=5, step=1, value=2)
                        ],
                            width=6
                        ),
                        dbc.Col(children=[
                            html.P("MIN CLUSTER SIZE (HDBSCAN)"),
                            dcc.Slider(id='filter-min-cluster-size', min=2, max=10, step=1, value=3)
                        ],

                            width=6
                        )
                    ]),
                    dbc.Row(children=[], id='research-streams-clustering', className="gray-background-custom m-3")],
                width=5
            ),
            dbc.Col(
                [
                    dbc.Row([
                        html.H6("AUTHOR RESEARCH INTEREST", className="text-left p-2 font-italic"),
                        dbc.Col(children=[
                            html.P("BREAKDOWN"),
                            dcc.Dropdown(id='filter-research-direction-grouping',
                                         options=['By keyword', 'By research area'],
                                         value='By research area')
                        ],
                            width=4
                        ),
                    ]),
                    dbc.Row(children=[], id='author-research-direction', className="gray-background-custom m-3")],
                width=5
            ),
            dbc.Col(children=[
                dbc.Row(html.H6("RECOMMENDED NEW COLLABORATIONS", className="text-left p-2 font-italic")),
                dbc.Row(
                    children=[],  # author_recommendations(app_config=app_config, filter_scope=filter_scope),
                    id='author-recommendations', className="gray-background-custom m-3"),

            ],
                width=2)
        ], className="m-3"),
        dbc.Row(children=[
            html.H6("PUBLISHED ARTICLES", className="text-left p-2 font-italic"),
            published_articles(app_config=app_config, filter_scope=filter_scope)
        ],
            className="gray-background-custom m-3"
        )
    ],
        className='p-4',
        fluid=True
    )


@callback(Output('research-streams-clustering', 'children'),
          Input({'type': 'filter-author', 'index': ALL}, 'value'),
          Input({'type': 'filter-author', 'index': ALL}, 'id'),
          Input('filter-min-samples', 'value'),
          Input('filter-min-cluster-size', 'value'))
def research_streams_clustering(filters: list, filter_ids: list, min_samples: int, min_cluster_size: int):
    # Get the filter values
    filter_scope = parse_filters(filters=filters, filter_ids=filter_ids)

    return co_author_clustering(
        app_config=app_config,
        filter_scope=filter_scope,
        min_samples=min_samples,
        min_cluster_size=min_cluster_size
    )


@callback(Output('author-research-direction', 'children'),
          Input({'type': 'filter-author', 'index': ALL}, 'value'),
          Input({'type': 'filter-author', 'index': ALL}, 'id'),
          Input('filter-research-direction-grouping', 'value'))
def author_research_direction(filters: list, filter_ids: list, grouping: str):
    # Get the filter values
    filter_scope = parse_filters(filters=filters, filter_ids=filter_ids)

    return articles_by_breakdown(
        app_config=app_config,
        filter_scope=filter_scope,
        grouping=grouping,
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
