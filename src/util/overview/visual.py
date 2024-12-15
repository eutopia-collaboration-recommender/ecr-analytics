import numpy as np

from dash import dcc, html
import plotly.graph_objects as go

import dash_bootstrap_components as dbc

from src.util.config import GLOBAL_CONFIG
from src.util.overview.query import (
    query_cards,
    query_breakdown_publications_by_institution,
    query_trend_eutopia_collaboration,
    query_trend_articles_by_collaboration_type,
    query_eutopia_collaboration_funnel,
    query_trend_new_collaborations,
    query_collaboration_novelty_index_distribution,
    query_research_areas
)


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


def cards_base_metrics(settings: dict):
    """
    Get the base metrics for the overview page.
    :param settings: The settings for connection to Redis and BigQuery.
    :return: The base metrics cards.
    """
    df_cards = query_cards(settings=GLOBAL_CONFIG)

    children = [dbc.Col(
        create_card(value=df_cards[col].values[0],
                    title=col),
        width=2,
        className="mt-2"
    ) for col in df_cards.columns]

    return children


def breakdown_publications_by_institution(settings: dict):
    """
    Get the breakdown of publications by institution.
    :param settings: The settings for connection to Redis and BigQuery.
    :return: The breakdown of publications by institution.
    """
    df_breakdown_publications_by_institution = query_breakdown_publications_by_institution(settings=GLOBAL_CONFIG)

    fig = go.Figure()

    fig.add_trace(go.Bar(x=df_breakdown_publications_by_institution['Articles'],
                         y=df_breakdown_publications_by_institution['Institution'],
                         marker=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[0]),
                         orientation='h'
                         ),

                  )

    fig.update_layout(
        title='BREAKDOWN OF ARTICLES BY INSTITUTION',
        xaxis=dict(
            title='Articles',
            showgrid=False,
            color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR,
            zeroline=False
        ),
        yaxis=dict(
            title='Institution',
            showgrid=False,
            color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR
        ),
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR)

    return dcc.Graph(figure=fig)


def trend_eutopia_collaboration(settings: dict):
    """
    Get the trend of Eutopia collaborations.
    :param settings: The settings for connection to Redis and BigQuery.
    :return: The trend of Eutopia collaborations.
    """
    df_trend_eutopia_collaboration = query_trend_eutopia_collaboration(settings=GLOBAL_CONFIG)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_trend_eutopia_collaboration['Year'],
                             y=df_trend_eutopia_collaboration['Eutopian Collaborations'],
                             mode='lines+markers',
                             name='Eutopian Collaborations',
                             marker=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[0]),
                             line=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[0]))
                  )

    fig.update_layout(
        title='EUTOPIA COLLABORATION TREND',
        xaxis=dict(
            title='Year',
            showgrid=False,
            color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR
        ),
        yaxis=dict(
            title='EUTOPIA Collaboration Articles',
            showgrid=False,
            color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR,
            zeroline=False
        ),
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR)

    return dcc.Graph(figure=fig)


def trend_articles_by_collaboration_type(settings: dict):
    """
    Get the trend of articles by collaboration type.
    :param settings: The settings for connection to Redis and BigQuery.
    :return: The trend of articles by collaboration type.
    """
    df_trend_articles_by_collaboration_type = query_trend_articles_by_collaboration_type(settings=GLOBAL_CONFIG)

    fig = go.Figure()

    # External Collaborations
    fig.add_trace(go.Scatter(x=df_trend_articles_by_collaboration_type['Year'],
                             y=df_trend_articles_by_collaboration_type['External Collaborations'],
                             mode='lines+markers',
                             name='External Collaborations',
                             marker=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[0]),
                             line=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[0]))
                  )

    # Internal collaborations
    fig.add_trace(go.Scatter(x=df_trend_articles_by_collaboration_type['Year'],
                             y=df_trend_articles_by_collaboration_type['Internal Collaborations'],
                             mode='lines+markers',
                             name='Internal Collaborations',
                             marker=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[1]),
                             line=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[1]))
                  )

    # Single author publications
    fig.add_trace(go.Scatter(x=df_trend_articles_by_collaboration_type['Year'],
                             y=df_trend_articles_by_collaboration_type['Single Author Publications'],
                             mode='lines+markers',
                             name='Single Author Publications',
                             marker=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[2]),
                             line=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[2]))
                  )

    fig.update_layout(
        title='PUBLICATION TREND BY COLLABORATION TYPE',
        xaxis=dict(
            title='Year',
            showgrid=False,
            color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR
        ),
        yaxis=dict(
            title='Articles',
            showgrid=False,
            color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR,
            zeroline=False
        ),
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR)

    return dcc.Graph(figure=fig)


def eutopia_collaboration_funnel(settings: dict):
    """
    Get the funnel of Eutopia collaborations.
    :param settings: Settings for connection to Redis and BigQuery.
    :return: The funnel of Eutopia collaborations.
    """

    df_eutopia_collaboration_funnel = query_eutopia_collaboration_funnel(settings=GLOBAL_CONFIG)

    fig = go.Figure()

    fig.add_trace(go.Funnel(
        name='Eutopia Collaboration Funnel',
        y=df_eutopia_collaboration_funnel['Stage'],
        x=df_eutopia_collaboration_funnel['Count'],
        textinfo='value+percent initial',
        marker=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[0])
    ))

    fig.update_layout(
        title='EUTOPIA COLLABORATION FUNNEL',
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR
    )

    return dcc.Graph(figure=fig)


def trend_new_collaborations(settings: dict):
    """
    Get the trend of new collaborations.
    :param settings: The settings for connection to Redis and BigQuery.
    :return: The trend of new collaborations.
    """
    df_trend_new_collaborations = query_trend_new_collaborations(settings=GLOBAL_CONFIG)

    fig = go.Figure()

    # new author collaborations
    fig.add_trace(go.Scatter(x=df_trend_new_collaborations['Year'],
                             y=df_trend_new_collaborations['New Author Collaborations'],
                             mode='lines+markers',
                             name='New Author Collaborations',
                             marker=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[0]),
                             line=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[0]))
                  )

    # new institution collaborations
    fig.add_trace(go.Scatter(x=df_trend_new_collaborations['Year'],
                             y=df_trend_new_collaborations['New Institution Collaborations'],
                             mode='lines+markers',
                             name='New Institution Collaborations',
                             marker=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[1]),
                             line=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[1]))
                  )

    # existing collaborations
    fig.add_trace(go.Scatter(x=df_trend_new_collaborations['Year'],
                             y=df_trend_new_collaborations['Existing Collaborations'],
                             mode='lines+markers',
                             name='Existing Collaborations',
                             marker=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[2]),
                             line=dict(color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.CLASS_COLORS[2]))
                  )

    fig.update_layout(
        title='NEW COLLABORATION TREND',
        xaxis=dict(
            title='Year',
            showgrid=False,
            color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR
        ),
        yaxis=dict(
            title='Articles',
            showgrid=False,
            color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR,
            zeroline=False
        ),
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR)
    return dcc.Graph(figure=fig)


def collaboration_novelty_index_distribution(settings):
    """
    Get the distribution of collaboration novelty index.
    :param settings: The settings for connection to Redis and BigQuery.
    :return: The distribution of collaboration novelty index.
    """
    df_collaboration_novelty_index_distribution = query_collaboration_novelty_index_distribution(settings=GLOBAL_CONFIG)

    # Define custom bins
    custom_bins = np.linspace(df_collaboration_novelty_index_distribution['Collaboration Novelty Index'].min(),
                              df_collaboration_novelty_index_distribution['Collaboration Novelty Index'].max(), 30)

    # Calculate density for KDE plot using numpy.histogram with density=True
    density_values, density_bins = np.histogram(
        df_collaboration_novelty_index_distribution['Collaboration Novelty Index'], bins=custom_bins,
        density=True)
    density_x = 0.5 * (density_bins[1:] + density_bins[:-1])  # Midpoints of bins for x-axis

    # Create a Plotly figure
    fig = go.Figure()

    # Add histogram trace
    fig.add_trace(go.Histogram(
        x=df_collaboration_novelty_index_distribution['Collaboration Novelty Index'],
        xbins=dict(start=custom_bins[0], end=custom_bins[-1], size=custom_bins[1] - custom_bins[0]),
        name='Histogram',
        histnorm='probability density',  # Normalized to match density plot
        marker_color='rgba(0, 0, 255, 0.5)',  # Semi-transparent blue
    ))

    # Update layout for the plot
    fig.update_layout(
        title='COLLABORATION NOVELTY INDEX DISTRIBUTION',
        xaxis=dict(title='Collaboration Novelty Index'),
        yaxis=dict(title='Density'),
        font=dict(family='Open Sans, sans-serif'),
        plot_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=GLOBAL_CONFIG['config'].DASHBOARD.COLORS.TEXT_COLOR
    )
    return dcc.Graph(figure=fig)


def publications_by_research_area(settings, filters=None):
    """
    Get the publications by research area.
    :param settings: The settings for connection to Redis and BigQuery.
    :return: The publications by research area.
    """

    print(filters)


def filter_research_areas(settings):
    """
    Get the filter for research areas.
    :param settings: The settings for connection to Redis and BigQuery.
    :return: The filter for research areas.
    """
    research_area_df = query_research_areas(settings=GLOBAL_CONFIG)

    # Check if author_df is not empty and create dropdown options
    if not research_area_df.empty:
        options = [
            {'label': row['Research Area'],
             'value': str({'filter-name': 'research-area', 'filter-value': row['Research Area']})}
            for index, row in research_area_df.iterrows()
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
        id={'type': 'filter-overview', 'index': 'research-area'},
        options=options,
        placeholder="Select a research area",
        value=default_value,
        style={'minWidth': '700px'},
        searchable=True
    )
