import hdbscan
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import requests

from dash import dash_table, dcc, html
from sklearn.manifold import TSNE

from src.util.dash_author.query import (
    query_articles_by_keyword, query_articles_by_research_area, query_cards,
    query_co_author_embeddings, query_published_articles
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
                       filter_scope: dict) -> list:
    """
    Get the base metrics for the dash_overview page.
    :param app_config: The app_config for connection to Redis and BigQuery.
    :param filter_scope: The filter scope
    :return: The base metrics cards.
    """
    df_cards = query_cards(app_config=app_config,
                           filter_scope=filter_scope)

    children = [dbc.Col(
        create_card(value=df_cards[col].values[0],
                    title=col),
        width=2,
        className="mt-2"
    ) for col in df_cards.columns]

    return children


def published_articles(app_config: AppConfig,
                       filter_scope: dict):
    """
    Get the published articles table.
    :param app_config:
    :param filter_scope: The filter scope
    :return:
    """

    published_articles_df = query_published_articles(app_config=app_config,
                                                     filter_scope=filter_scope)

    # Visualize a table visualization of articles grouped by PUBLICATION_YEAR
    published_articles_df['Article Title'] = published_articles_df.apply(
        lambda row: f"[{row['Article Title']}](https://doi.org/{row['Article Doi']})", axis=1
    )
    # Format collaboration novelty index to 2 decimal places
    published_articles_df['Collaboration Novelty Index'] = published_articles_df['Collaboration Novelty Index'].apply(
        lambda x: round(x, 2))
    published_articles_df['Citations'] = published_articles_df['Citations'].apply(
        lambda x: round(x, 5))
    # Remove DOI column
    published_articles_df.drop(columns=['Article Doi'], inplace=True)

    # Create the Dash DataTable with the updated data
    return dash_table.DataTable(
        data=published_articles_df.to_dict('records'),
        columns=[
            {"name": "Publication Year", "id": "Publication Year"},
            {"name": "Article Title", "id": "Article Title", "presentation": "markdown"},
            {"name": "Citations", "id": "Citations"},
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
            'padding': '5px 5px 5px 5px',
            'border': 'none',
            'borderLeft': '1px solid lightgray',  # Add inner left border between columns
            'borderRight': '1px solid lightgray'  # Add inner right border between columns
        },
        style_header={
            'backgroundColor': app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
            'fontWeight': 'bold',
            'padding': '5px 5px 5px 5px',
            'textAlign': 'left',
            'borderBottom': '1px solid lightgray'  # Add a bottom border for the header
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
        page_size=10,  # Number of rows per page
        sort_action="native",
        filter_action="native"
    )


def co_author_clustering(app_config: AppConfig,
                         filter_scope: dict,
                         min_samples: int,
                         min_cluster_size: int) -> dcc.Graph:
    """
    Cluster co-authors using HDBSCAN and visualize the clusters using t-SNE
    :param app_config:
    :param filter_scope: The filter scope
    :return:
    """

    # Query the co-author embedding data
    co_author_embedding_df = query_co_author_embeddings(app_config=app_config, filter_scope=filter_scope)

    # Convert the embedding column into a single NumPy array.
    X = np.array(co_author_embedding_df['Embedding Tensor Data'].tolist())

    # HDBSCAN clustering
    hdb = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        gen_min_span_tree=True
    )
    labels = hdb.fit_predict(X)

    # Assign cluster labels back to the DataFrame
    co_author_embedding_df['cluster'] = labels
    co_author_embedding_df['cluster'] = co_author_embedding_df['cluster'].astype(str)  # Convert to string

    # t-SNE dimensionality reduction (2D)
    tsne = TSNE(
        n_components=2,
        random_state=42,
        perplexity=30,
        max_iter=1000,
        learning_rate='auto'
    )
    tsne_result = tsne.fit_transform(X)

    # Store TSNE components in the DataFrame
    co_author_embedding_df['t-SNE x'] = tsne_result[:, 0]
    co_author_embedding_df['t-SNE y'] = tsne_result[:, 1]

    # Create an interactive Plotly scatter plot
    fig = px.scatter(
        co_author_embedding_df,
        x='t-SNE x',
        y='t-SNE y',
        color='cluster',
        hover_data=['Author Id', 'Author Name'],
        # color_continuous_scale=px.colors.qualitative.Prism,
    )
    fig.update_layout(
        font=dict(
            family='Open Sans, sans-serif'
        ),
        plot_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        paper_bgcolor=app_config.config.DASHBOARD.COLORS.BACKGROUND_COLOR,
        font_color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR)

    return dcc.Graph(figure=fig)


def articles_by_breakdown(app_config: AppConfig,
                          filter_scope: dict,
                          grouping: str) -> dcc.Graph:
    """
    Cluster co-authors using HDBSCAN and visualize the clusters using t-SNE
    :param app_config:
    :param filter_scope: The filter scope
    :return:
    """
    top_k = 10
    if grouping == 'By keyword':
        df = query_articles_by_keyword(app_config=app_config, filter_scope=filter_scope, k=top_k)
        breakdown_col = 'Keyword'
    else:
        df = query_articles_by_research_area(app_config=app_config, filter_scope=filter_scope, k=top_k)
        breakdown_col = 'Research Area'

    # Sort by Articles
    df = df.sort_values(by='Articles', ascending=True)
    fig = go.Figure()

    fig.add_trace(go.Bar(x=df['Articles'],
                         y=df[breakdown_col],
                         marker=dict(color=app_config.config.DASHBOARD.COLORS.CLASS_COLORS[0]),
                         orientation='h'
                         ),

                  )

    fig.update_layout(
        title=f'ARTICLES BY TOP {top_k} {breakdown_col.upper()}S',
        xaxis=dict(
            title='Articles',
            showgrid=False,
            color=app_config.config.DASHBOARD.COLORS.TEXT_COLOR,
            zeroline=False
        ),
        yaxis=dict(
            title=breakdown_col,
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


def author_recommendations(app_config: AppConfig,
                           filter_scope: dict) -> dcc.Graph:
    """
    Cluster co-authors using HDBSCAN and visualize the clusters using t-SNE
    :param app_config:
    :param filter_scope: The filter scope
    :return:
    """
    author_id = filter_scope['author_id']
    # Get author id in between "author_id in ('" and "')"
    author_id = author_id.split("'")[1]
    # Request recommendations from the recommendation engine
    request_url = 'http://0.0.0.0:8080/predict/'
    data = dict(
        author_id=author_id
    )
    response = requests.post(request_url, json=data)

    print(response.json())

    return None