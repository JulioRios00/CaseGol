from dash import html, dcc
import dash_bootstrap_components as dbc

login_layout = dbc.Container([
    dcc.Location(id="login-redirect", refresh=True),
    
    dbc.Row([
        dbc.Col([
            html.H1("Login", className="text-center my-4"),
            
            dbc.Card([
                dbc.CardBody([
                    html.Div(id="login-error", className="text-danger mb-3"),
                    
                    dbc.Row([
                        dbc.Label("Nome de Usuário"),
                        dbc.Input(id="login-username", type="text", placeholder="Digite seu nome de usuário", autoFocus=True)
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Label("Senha"),
                        dbc.Input(id="login-password", type="password", placeholder="Digite sua senha")
                    ], className="mb-3"),
                    
                    dbc.Button(
                        "Entrar", 
                        id="login-button", 
                        color="primary", 
                        className="mt-3 w-100",
                        n_clicks=0
                    ),
                    
                    html.Hr(),
                    
                    html.P([
                        "Não tem uma conta? ",
                        dcc.Link("Registrar", href="/register")
                    ], className="text-center")
                ], className="px-4 py-4")
            ], className="shadow")
        ], xs=12, sm=10, md=8, lg=6, xl=4, className="mx-auto")
    ], className="align-items-center min-vh-100")
], fluid=True, className="bg-light")