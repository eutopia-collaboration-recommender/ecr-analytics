import dash

from dash import ALL, callback, html, Input, Output

import dash_bootstrap_components as dbc

from src.util.dash_common.app_config import app_config
from src.util.dash_common.common import parse_filters
from src.util.dash_common.filter import (
    filter_publication_date,
    filter_research_area,
    filter_institution
)
from src.util.dash_overview.visual import (
    cards_base_metrics,
    trend_eutopia_collaboration,
    trend_articles_by_collaboration_type,
    breakdown_publications_by_institution,
    eutopia_collaboration_funnel,
    trend_new_collaborations,
    collaboration_novelty_index_distribution
)


# -------------------- PAGE LAYOUT HELPERS --------------------
def page_header():
    """
    Get the page header.
    :return: The page header.
    """
    return dbc.Container(children=[
        dbc.Row(children=[
            dbc.Col(
                html.H4("COLLABORATION OVERVIEW", className="text-left p-2 font-italic"),
                width=6
            ),
            dbc.Col(
                [
                    html.H6("PUBLICATION PERIOD", className="text-left p-2 font-italic"),
                    filter_publication_date(page_name='overview')
                ],
                width=2
            ),
            dbc.Col(
                children=[
                    html.H6("INSTITUTION", className="text-left p-2 font-italic"),
                    filter_institution(app_config=app_config, page_name='overview')
                ],
                width=2
            ),
            dbc.Col(
                children=[
                    html.H6("RESEARCH AREA", className="text-left p-2 font-italic"),
                    filter_research_area(app_config=app_config, page_name='overview')
                ],
                width=2
            )]
        )
    ],
        fluid=True,
        className="mt-4 m-1"
    )


# -------------------- CALLBACKS --------------------
@callback(Output('overview-page', 'children'),
          Input({'type': 'filter-overview', 'index': ALL}, 'value'),
          Input({'type': 'filter-overview', 'index': ALL}, 'id'))
def page_overview(filters: list, filter_ids: int) -> list:
    # Get the filter values
    filter_scope = parse_filters(filters=filters, filter_ids=filter_ids)
    return [
        # Some space between the title and the cards
        dbc.Row(children=cards_base_metrics(app_config=app_config, filter_scope=filter_scope),
                className="gray-background-custom m-1"),
        dbc.Row(
            children=[
                dbc.Col(children=[
                    dbc.Row(trend_articles_by_collaboration_type(app_config=app_config, filter_scope=filter_scope),
                            className="mt-4 m-1")
                ], width=6
                ),
                dbc.Col(children=[
                    dbc.Row(breakdown_publications_by_institution(app_config=app_config, filter_scope=filter_scope),
                            className="mt-4 m-1")
                ], width=6
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(children=[
                    dbc.Row(trend_eutopia_collaboration(app_config=app_config, filter_scope=filter_scope),
                            className="mt-4 m-1")
                ], width=6
                ),
                dbc.Col(children=[
                    dbc.Row(eutopia_collaboration_funnel(app_config=app_config, filter_scope=filter_scope),
                            className="mt-4 m-1")
                ], width=6
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(children=[
                    dbc.Row(trend_new_collaborations(app_config=app_config, filter_scope=filter_scope),
                            className="mt-4 m-1")
                ], width=6
                ),
                dbc.Col(children=[
                    dbc.Row(collaboration_novelty_index_distribution(app_config=app_config, filter_scope=filter_scope),
                            className="mt-4 m-1")
                ], width=6
                )
            ]
        )
    ]


# ----------- Main layout ------------
dash.register_page(__name__, path='/')

layout = dbc.Container(children=[
    page_header(),
    # Some space between the title and the cards
    dbc.Row(children=[],
            id='overview-page')
],
    fluid=True
)
