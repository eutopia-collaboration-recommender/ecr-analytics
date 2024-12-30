import numpy as np

from dash import dcc, html
import plotly.graph_objects as go

import dash_bootstrap_components as dbc

from src.util.dash_common.app_config import AppConfig
from src.util.dash_overview.query import (
    query_cards,
    query_breakdown_publications_by_institution,
    query_trend_eutopia_collaboration,
    query_trend_articles_by_collaboration_type,
    query_eutopia_collaboration_funnel,
    query_trend_new_collaborations,
    query_collaboration_novelty_index_distribution
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


def cards_base_metrics(app_config: AppConfig,
                       filter_scope: dict) -> list:
    """
    Get the base metrics for the dash_overview page.
    :param app_config: The app_config for connection to Redis and BigQuery.
    :return: The base metrics cards.
    """
    df_cards = query_cards(app_config=app_config, filter_scope=filter_scope)

    children = [dbc.Col(
        create_card(value=df_cards[col].values[0],
                    title=col),
        width=2,
        className="mt-2"
    ) for col in df_cards.columns]

    return children


def breakdown_publications_by_institution(app_config: AppConfig,
                                          filter_scope: dict) -> dcc.Graph:
    """
    Get the breakdown of publications by institution.
    :param app_config: The app_config for connection to Redis and BigQuery.
    :return: The breakdown of publications by institution.
    """
    df_breakdown_publications_by_institution = query_breakdown_publications_by_institution(app_config=app_config,
                                                                                           filter_scope=filter_scope)

    fig = go.Figure()

    fig.add_trace(go.Bar(x=df_breakdown_publications_by_institution['Articles'],
                         y=df_breakdown_publications_by_institution['Institution'],
                         marker=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[0]),
                         orientation='h'
                         ),

                  )

    fig.update_layout(
        title='BREAKDOWN OF ARTICLES BY INSTITUTION',
        xaxis=dict(
            title='Articles',
            showgrid=False,
            color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR,
            zeroline=False
        ),
        yaxis=dict(
            title='Institution',
            showgrid=False,
            color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR
        ),
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR)

    return dcc.Graph(figure=fig)


def trend_eutopia_collaboration(app_config: AppConfig,
                                filter_scope: dict) -> dcc.Graph:
    """
    Get the trend of Eutopia collaborations.
    :param app_config: The app_config for connection to Redis and BigQuery.
    :return: The trend of Eutopia collaborations.
    """
    df_trend_eutopia_collaboration = query_trend_eutopia_collaboration(app_config=app_config, filter_scope=filter_scope)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_trend_eutopia_collaboration['Year'],
                             y=df_trend_eutopia_collaboration['Eutopian Collaborations'],
                             mode='lines+markers',
                             name='Eutopian Collaborations',
                             marker=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[0]),
                             line=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[0]))
                  )

    fig.update_layout(
        title='EUTOPIA COLLABORATION TREND',
        xaxis=dict(
            title='Year',
            showgrid=False,
            color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR
        ),
        yaxis=dict(
            title='EUTOPIA Collaboration Articles',
            showgrid=False,
            color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR,
            zeroline=False
        ),
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR)

    return dcc.Graph(figure=fig)


def trend_articles_by_collaboration_type(app_config: AppConfig,
                                         filter_scope: dict) -> dcc.Graph:
    """
    Get the trend of articles by collaboration type.
    :param app_config: The app_config for connection to Redis and BigQuery.
    :return: The trend of articles by collaboration type.
    """
    df_trend_articles_by_collaboration_type = query_trend_articles_by_collaboration_type(app_config=app_config,
                                                                                         filter_scope=filter_scope)

    fig = go.Figure()

    # External Collaborations
    fig.add_trace(go.Scatter(x=df_trend_articles_by_collaboration_type['Year'],
                             y=df_trend_articles_by_collaboration_type['External Collaborations'],
                             mode='lines+markers',
                             name='External Collaborations',
                             marker=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[0]),
                             line=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[0]))
                  )

    # Internal collaborations
    fig.add_trace(go.Scatter(x=df_trend_articles_by_collaboration_type['Year'],
                             y=df_trend_articles_by_collaboration_type['Internal Collaborations'],
                             mode='lines+markers',
                             name='Internal Collaborations',
                             marker=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[1]),
                             line=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[1]))
                  )

    # Single dash_author publications
    fig.add_trace(go.Scatter(x=df_trend_articles_by_collaboration_type['Year'],
                             y=df_trend_articles_by_collaboration_type['Single Author Publications'],
                             mode='lines+markers',
                             name='Single Author Publications',
                             marker=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[2]),
                             line=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[2]))
                  )

    fig.update_layout(
        title='PUBLICATION TREND BY COLLABORATION TYPE',
        xaxis=dict(
            title='Year',
            showgrid=False,
            color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR
        ),
        yaxis=dict(
            title='Articles',
            showgrid=False,
            color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR,
            zeroline=False
        ),
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR)

    return dcc.Graph(figure=fig)


def eutopia_collaboration_funnel(app_config: AppConfig,
                                 filter_scope: dict) -> dcc.Graph:
    """
    Get the funnel of Eutopia collaborations.
    :param app_config: app_config for connection to Redis and BigQuery.
    :return: The funnel of Eutopia collaborations.
    """

    df_eutopia_collaboration_funnel = query_eutopia_collaboration_funnel(app_config=app_config,
                                                                         filter_scope=filter_scope)

    fig = go.Figure()

    fig.add_trace(go.Funnel(
        name='Eutopia Collaboration Funnel',
        y=df_eutopia_collaboration_funnel['Stage'],
        x=df_eutopia_collaboration_funnel['Count'],
        textinfo='value+percent initial',
        marker=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[0])
    ))

    fig.update_layout(
        title='EUTOPIA COLLABORATION FUNNEL',
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR
    )

    return dcc.Graph(figure=fig)


def trend_new_collaborations(app_config: AppConfig,
                             filter_scope: dict) -> dcc.Graph:
    """
    Get the trend of new collaborations.
    :param app_config: The app_config for connection to Redis and BigQuery.
    :return: The trend of new collaborations.
    """
    df_trend_new_collaborations = query_trend_new_collaborations(app_config=app_config, filter_scope=filter_scope)

    fig = go.Figure()

    # new dash_author collaborations
    fig.add_trace(go.Scatter(x=df_trend_new_collaborations['Year'],
                             y=df_trend_new_collaborations['New Author Collaborations'],
                             mode='lines+markers',
                             name='New Author Collaborations',
                             marker=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[0]),
                             line=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[0]))
                  )

    # new institution collaborations
    fig.add_trace(go.Scatter(x=df_trend_new_collaborations['Year'],
                             y=df_trend_new_collaborations['New Institution Collaborations'],
                             mode='lines+markers',
                             name='New Institution Collaborations',
                             marker=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[1]),
                             line=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[1]))
                  )

    # existing collaborations
    fig.add_trace(go.Scatter(x=df_trend_new_collaborations['Year'],
                             y=df_trend_new_collaborations['Existing Collaborations'],
                             mode='lines+markers',
                             name='Existing Collaborations',
                             marker=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[2]),
                             line=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[2]))
                  )

    fig.update_layout(
        title='NEW COLLABORATION TREND',
        xaxis=dict(
            title='Year',
            showgrid=False,
            color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR
        ),
        yaxis=dict(
            title='Articles',
            showgrid=False,
            color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR,
            zeroline=False
        ),
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR)
    return dcc.Graph(figure=fig)


def collaboration_novelty_index_distribution(app_config: AppConfig,
                                             filter_scope: dict) -> dcc.Graph:
    """
    Get the distribution of collaboration novelty index.
    :param app_config: The app_config for connection to Redis and BigQuery.
    :return: The distribution of collaboration novelty index.
    """
    df_collaboration_novelty_index_distribution = query_collaboration_novelty_index_distribution(app_config=app_config,
                                                                                                 filter_scope=filter_scope)

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
        plot_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR
    )
    return dcc.Graph(figure=fig)
