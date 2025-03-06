import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

dashboard_layout = html.Div(
    [
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Sair", id="logout-button", href="#")),
            ],
            brand="Case Julio Araujo",
            brand_href="#",
            color="primary",
            dark=True,
        ),
        dbc.Container(
            [
                html.Div(style={"height": "30px"}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4("Filtros", className="mb-6"),
                                html.Label("Mercado:"),
                                dcc.Dropdown(
                                    id="market-dropdown",
                                    placeholder="Selecione o mercado",
                                    searchable=True,
                                    clearable=False,
                                    style={"marginBottom": "15px"},
                                ),
                                html.Label("Data Inicial:"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="start-year-dropdown",
                                                placeholder="Ano",
                                                clearable=False,
                                            )
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="start-month-dropdown",
                                                placeholder="Mês",
                                                clearable=False,
                                            )
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Label("Data Final:"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="end-year-dropdown",
                                                placeholder="Ano",
                                                clearable=False,
                                            )
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="end-month-dropdown",
                                                placeholder="Mês",
                                                clearable=False,
                                            )
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Button(
                                    "Aplicar Filtros",
                                    id="filter-button",
                                    color="primary",
                                    className="mt-3 w-10",
                                ),
                            ],
                            md=4,
                            className="d-flex flex-column",
                        ),
                        dbc.Col(
                            [
                                html.H4("RPK ao Longo do Tempo", className="mb-4"),
                                dcc.Graph(id="rpk-graph", style={"height": "60vh"}),
                            ],
                            md=8,
                        ),
                    ],
                    className="align-items-start",
                ),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4("Tabela de Dados"),
                                html.Div(id="data-table-container"),
                            ]
                        )
                    ]
                ),
            ],
            fluid=True,
            className="pt-4",
        ),
    ]
)
