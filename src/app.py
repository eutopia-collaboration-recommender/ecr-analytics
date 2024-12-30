import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# -------------------- DASH APP --------------------
app = Dash(__name__,
           use_pages=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        dbc.Container(children=[
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src='/assets/eutopia.png', height="80px")),
                ], align="center"),
                href="/",
                style={"textDecoration": "none"}
            ),
            dbc.Collapse(
                dbc.Nav(
                    children=[
                        dbc.NavItem(
                            dbc.NavLink(f"{page['name']}", href=page["relative_path"],
                                        id=f"navlink-{page['name']}", className='h5', active="exact")
                        )
                        for page in dash.page_registry.values()
                        if page["path"] != "/404"

                    ], className="ml-auto", navbar=True),
                id="navbar-collapse",
                navbar=True
            ),
            dbc.Row(
                children=[],
                justify="end",
                align="center",
                className="ml-auto",
                id='navbar-filters'
            ),
        ],
            fluid=True),
        className='navbar-expand-lg navbar-custom',
        color="light",
        dark=False
    ),
    dash.page_container,
    # Footer
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.P("© 2024 EUTOPIA. All rights reserved.", className="text-center mt-4")
            ], width=12)
        ])
    ],
        fluid=True,
        className="footer-custom")
])

# -------------------- MAIN FUNCTION --------------------
if __name__ == '__main__':
    app.run(debug=True)
