from dash import Input, Output, State, no_update
from flask_login import logout_user

from app.utils.utils import direct_login, direct_register


def register_auth_callbacks(app):
    @app.callback(
        [Output("login-error", "children"), Output("login-redirect", "href")],
        [Input("login-button", "n_clicks")],
        [State("login-username", "value"), State("login-password", "value")],
    )
    
    def login_user_callback(n_clicks, username, password):
        if n_clicks is None or n_clicks == 0:
            return "", no_update

        if not username and not password:
            return "Por favor, insira o nome de usuário e senha", no_update
        elif not username:
            return "Por favor, insira o nome de usuário", no_update
        elif not password:
            return "Por favor, insira a senha", no_update

        try:
            success, error_msg = direct_login(username, password)

            if success:
                return "", "/dashboard"
            else:
                return error_msg, no_update
        except Exception as e:
            return f"Erro ao fazer login: {str(e)}", no_update

    @app.callback(
        [Output("register-error", "children"), Output("register-redirect", "href")],
        [Input("register-button", "n_clicks")],
        [State("register-username", "value"), State("register-password", "value")],
        prevent_initial_call=True,
    )
    def register_user_callback(n_clicks, username, password):
        if n_clicks is None:
            return "", no_update

        if not username and not password:
            return "Por favor, insira o nome de usuário e senha", no_update
        elif not username:
            return "Por favor, insira o nome de usuário", no_update
        elif not password:
            return "Por favor, insira a senha", no_update

        try:
            success, error_msg = direct_register(username, password)

            if success:
                return "", "/dashboard"
            else:
                return error_msg, no_update
        except Exception as e:
            return f"Erro ao registrar: {str(e)}", no_update

    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("logout-button", "n_clicks")],
        prevent_initial_call=True,
    )
    def logout_user_callback(n_clicks):
        if n_clicks:
            logout_user()
            return "/login"
        return no_update
