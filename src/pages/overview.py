import dash

from dash import html

import dash_bootstrap_components as dbc

from src.util.config import GLOBAL_CONFIG
from src.util.overview.visual import (
    cards_base_metrics,
    trend_eutopia_collaboration,
    trend_articles_by_collaboration_type,
    breakdown_publications_by_institution,
    eutopia_collaboration_funnel,
    trend_new_collaborations,
    collaboration_novelty_index_distribution
)

# ----------- Main layout ------------
dash.register_page(__name__, path='/')


def overview_content() -> list:
    return [
        dbc.Row(
            dbc.Col(
                html.H4("COLLABORATION OVERVIEW", className="text-left p-2 font-italic"),
                width=12
            )
        ),
        # Some space between the title and the cards
        dbc.Row(children=cards_base_metrics(settings=GLOBAL_CONFIG),
                className="gray-background-custom m-1"),
        dbc.Row(
            children=[
                dbc.Col(
                    trend_articles_by_collaboration_type(settings=GLOBAL_CONFIG),
                    className="mt-4",
                    width=6
                ),
                dbc.Col(
                    breakdown_publications_by_institution(settings=GLOBAL_CONFIG),
                    className="mt-4",
                    width=6
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    trend_eutopia_collaboration(settings=GLOBAL_CONFIG),
                    className="mt-4",
                    width=6
                ),
                dbc.Col(
                    eutopia_collaboration_funnel(settings=GLOBAL_CONFIG),
                    className="mt-4",
                    width=6
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    trend_new_collaborations(settings=GLOBAL_CONFIG),
                    className="mt-4",
                    width=6
                ),
                dbc.Col(
                    collaboration_novelty_index_distribution(settings=GLOBAL_CONFIG),
                    className="mt-4",
                    width=6
                )
            ]
        )
    ]


layout_container_children = [
    dbc.Container(children=overview_content(),
                  className='p-2',
                  id='overview-content',
                  fluid=True),
]

layout = dbc.Container(children=layout_container_children,
                       fluid=True
                       )
