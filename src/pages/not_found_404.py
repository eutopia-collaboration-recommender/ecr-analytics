import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/404')

layout = dbc.Container(children=[
    dbc.Row(
        dbc.Col(
            html.H1("404 - Page not found", className="text-center"),
            width=12
        )
    )
],
    fluid=True,
    className="mt-4")
