from dash import html, dcc
import dash_bootstrap_components as dbc

register_layout = dbc.Container([
    dcc.Location(id="register-redirect", refresh=True),
    
    dbc.Row([
        dbc.Col([
            html.H1("Cadastro", className="text-center my-4"),
            
            dbc.Card([
                dbc.CardBody([
                    html.Div(id="register-error", className="text-danger mb-3"),
                    
                    dbc.Row([
                        dbc.Label("Nome de Usuário"),
                        dbc.Input(id="register-username", type="text", placeholder="Escolha um nome de usuário", autoFocus=True)
                    ], className="mb-3"),
                    
                    dbc.Row([
                        dbc.Label("Senha"),
                        dbc.Input(id="register-password", type="password", placeholder="Escolha uma senha")
                    ], className="mb-3"),
                    
                    dbc.Button(
                        "Cadastrar", 
                        id="register-button", 
                        color="success", 
                        className="mt-3 w-100",
                        n_clicks=0
                    ),
                    
                    html.Hr(),
                    
                    html.P([
                        "Já tem uma conta? ",
                        dcc.Link("Fazer Login", href="/login")
                    ], className="text-center")
                ], className="px-4 py-4")
            ], className="shadow")
        ], xs=12, sm=10, md=8, lg=6, xl=4, className="mx-auto")
    ], className="align-items-center min-vh-100")
], fluid=True, className="bg-light")