import dash_table
from dash import html

import dash_bootstrap_components as dbc

from src.util.dash_author.query import (
    query_cards,
    query_published_articles
)
from src.util.dash_common.app_config import AppConfig


def create_card(value: float,
                title: str) -> dbc.Card:
    """
    Create a card with a value and a title.
    :param value:  Numeric value.
    :param title: Metric title.
    :return: The card.
    """
    return dbc.Card(
        dbc.CardBody([
            html.H3(f"{value:,}", className="card-text text-center"),
            html.P(title, className="card-title text-center")
        ]),
        className="card-custom"
    )


def cards_base_metrics(app_config: AppConfig,
                       author_id: str) -> list:
    """
    Get the base metrics for the dash_overview page.
    :param app_config: The app_config for connection to Redis and BigQuery.
    :param author_id: The author SID.
    :return: The base metrics cards.
    """
    df_cards = query_cards(app_config=app_config,
                           author_id=author_id)

    children = [dbc.Col(
        create_card(value=df_cards[col].values[0],
                    title=col),
        width=2,
        className="mt-2"
    ) for col in df_cards.columns]

    return children


def published_articles(app_config: AppConfig,
                       author_id: str):
    """
    Get the published articles table.
    :param app_config:
    :param author_id:
    :return:
    """

    published_articles_df = query_published_articles(app_config=app_config,
                                                     author_id=author_id)

    # Visualize a table visualization of articles grouped by PUBLICATION_YEAR
    published_articles_df['Article Title'] = published_articles_df.apply(
        lambda row: f"[{row['Article Title']}](https://doi.org/{row['Article Doi']})", axis=1
    )
    # Format collaboration novelty index to 2 decimal places
    published_articles_df['Collaboration Novelty Index'] = published_articles_df['Collaboration Novelty Index'].apply(
        lambda x: round(x, 2))
    published_articles_df['Normalized Citations'] = published_articles_df['Normalized Citations'].apply(
        lambda x: round(x, 5))
    # Remove DOI column
    published_articles_df.drop(columns=['Article Doi'], inplace=True)

    # Create the Dash DataTable with the updated data
    return dash_table.DataTable(
        data=published_articles_df.to_dict('records'),
        columns=[
            {"name": "Publication Year", "id": "Publication Year"},
            {"name": "Article Title", "id": "Article Title", "presentation": "markdown"},
            {"name": "Normalized Citations", "id": "Normalized Citations"},
            {"name": "Collaboration Novelty Index", "id": "Collaboration Novelty Index"},
        ],
        style_table={
            'width': '100%',  # Ensure the table width is 100% of its container
            'overflowX': 'auto'  # Allow horizontal scrolling if needed
        },
        style_cell={
            'minWidth': '150px',
            'maxWidth': '80%',
            'fontFamily': 'Open Sans, sans-serif',
            'whiteSpace': 'normal',
            'backgroundColor': app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,  # Set cell background color
            'border': '1px solid white',
            'padding': '5px 5px 5px 5px',
        },
        style_header={
            'backgroundColor': app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
            'fontWeight': 'bold',
            'border': '1px solid white',
            'padding': '5px 5px 5px 5px',
            'textAlign': 'left'
        },
        style_data_conditional=[
            {
                'if': {'column_id': 'Article Title'},
                'textDecoration': 'none',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'whiteSpace': 'nowrap',
                'maxWidth': '800px',
            },
        ],
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in published_articles_df.to_dict('records')
        ],
        tooltip_duration=None,  # Keeps the tooltip visible as long as the user hovers
        page_action='native',  # Enable pagination
        page_size=10  # Number of rows per page
    )
