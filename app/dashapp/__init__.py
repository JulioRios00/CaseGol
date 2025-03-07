import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, dcc, html
from flask import session
from flask_login import current_user

from .callbacks.auth_callbacks import register_auth_callbacks
from .callbacks.dashboard_callbacks import register_dashboard_callbacks
from .layouts.dashboard import dashboard_layout
from .layouts.login import login_layout
from .layouts.register import register_layout


def init_dashboard(server):
    """
    Cria um aplicativo Dash com layout multi-página
    Create a Dash app with multi-page layout
    """
    dash_app = Dash(
        __name__,
        server=server,
        url_base_pathname="/dash/",
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    dash_app.layout = html.Div(
        [dcc.Location(id="url", refresh=True), html.Div(id="page-content")]
    )

    register_auth_callbacks(dash_app)
    register_dashboard_callbacks(dash_app)

    @dash_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def display_page(pathname):
        if pathname == "/dash/" or pathname == "/dash/dashboard":
            if current_user.is_authenticated:
                return dashboard_layout
            else:
                return dcc.Location(pathname="/dash/login", id="redirect-to-login")

        elif pathname == "/dash/login":
            if current_user.is_authenticated:
                return dcc.Location(pathname="/dash/dashboard", id="redirect-to-dashboard")
            return login_layout
        elif pathname == "/dash/register":
            if current_user.is_authenticated:
                return dcc.Location(pathname="/dash/dashboard", id="redirect-to-dashboard")
            return register_layout
        else:
            return "404 - Page not found"

    return dash_app
