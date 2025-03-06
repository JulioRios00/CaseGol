import json

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import requests
from dash import Input, Output, State, dash_table, dcc, html, no_update
from flask import request
from flask_login import current_user


def register_dashboard_callbacks(app):
    @app.callback(
        [
            Output("market-dropdown", "options"),
            Output("start-year-dropdown", "options"),
            Output("end-year-dropdown", "options"),
            Output("start-month-dropdown", "options"),
            Output("end-month-dropdown", "options"),
            Output("market-dropdown", "value"),
        ],
        [Input("url", "pathname")],
    )
    def initialize_filters(pathname):
        if pathname != "/dashboard":
            return [], [], [], [], [], None

        if not current_user.is_authenticated:
            years = [{"label": str(year), "value": year} for year in range(2000, 2024)]
            months = [{"label": str(month), "value": month} for month in range(1, 13)]
            return (
                [{"label": "Login Required", "value": "error"}],
                years,
                years,
                months,
                months,
                None,
            )

        try:
            base_url = request.host_url.rstrip("/")

            response = requests.get(
                f"{base_url}/api/dashboard-data", cookies=request.cookies
            )

            if response.status_code == 200:
                data = response.json()

                markets_list = data.get("markets", [])
                if markets_list:
                    for i, market in enumerate(markets_list[:5]):
                        print(f"  {i+1}. {market}")

                    markets = [
                        {"label": market, "value": market} for market in markets_list
                    ]

                    markets.sort(key=lambda x: x["label"])

                    initial_market = markets_list[0] if markets_list else None

                else:
                    print("AVISO: Nenhum mercado encontrado no banco de dados!")
                    markets = [{"label": "Nenhum mercado disponível", "value": "none"}]
                    initial_market = None

                year_min = data.get("year_min", 2000)
                year_max = data.get("year_max", 2023)
                years = [
                    {"label": str(year), "value": year}
                    for year in range(year_min, year_max + 1)
                ]

                months = [
                    {"label": "Janeiro", "value": 1},
                    {"label": "Fevereiro", "value": 2},
                    {"label": "Março", "value": 3},
                    {"label": "Abril", "value": 4},
                    {"label": "Maio", "value": 5},
                    {"label": "Junho", "value": 6},
                    {"label": "Julho", "value": 7},
                    {"label": "Agosto", "value": 8},
                    {"label": "Setembro", "value": 9},
                    {"label": "Outubro", "value": 10},
                    {"label": "Novembro", "value": 11},
                    {"label": "Dezembro", "value": 12},
                ]

                return markets, years, years, months, months, initial_market
            else:
                years = [
                    {"label": str(year), "value": year} for year in range(2000, 2024)
                ]
                months = [
                    {"label": str(month), "value": month} for month in range(1, 13)
                ]
                return (
                    [{"label": "Error loading markets", "value": "error"}],
                    years,
                    years,
                    months,
                    months,
                    None,
                )
        except Exception as e:
            print(f"Error in initialize_filters: {str(e)}")
            years = [{"label": str(year), "value": year} for year in range(2000, 2024)]
            months = [{"label": str(month), "value": month} for month in range(1, 13)]
            return (
                [{"label": "Error loading markets", "value": "error"}],
                years,
                years,
                months,
                months,
                None,
            )

    @app.callback(
        [Output("rpk-graph", "figure"), Output("data-table-container", "children")],
        [Input("filter-button", "n_clicks")],
        [
            State("market-dropdown", "value"),
            State("start-year-dropdown", "value"),
            State("start-month-dropdown", "value"),
            State("end-year-dropdown", "value"),
            State("end-month-dropdown", "value"),
        ],
    )
    def update_dashboard(
        n_clicks, market, start_year, start_month, end_year, end_month
    ):
        if n_clicks is None or not all(
            [market, start_year, start_month, end_year, end_month]
        ):
            print("Filtros incompletos, retornando gráfico vazio")
            return px.line(title=""), html.Div(
                [
                    html.H4(
                        "Por Favor, Selecione Todos os Filtros", className="text-info"
                    ),
                    html.P("Para visualizar os dados de voo, selecione:"),
                    html.Ul(
                        [
                            html.Li("Um mercado no menu suspenso"),
                            html.Li("Ano e mês inicial"),
                            html.Li("Ano e mês final"),
                        ]
                    ),
                    html.P("Em seguida, clique no botão 'Aplicar Filtros'."),
                ]
            )

        if market in ["none", "error"]:
            print(f"Mercado inválido selecionado: {market}")
            return px.line(title="Seleção de Mercado Inválida"), html.Div(
                [
                    html.H4("Seleção de Mercado Inválida", className="text-warning"),
                    html.P("Por favor, selecione um mercado válido no menu suspenso."),
                    html.P(
                        "Se nenhum mercado válido estiver disponível, o banco de dados pode não conter dados de voo."
                    ),
                ]
            )

        try:
            base_url = request.host_url.rstrip("/")
            api_url = f"{base_url}/api/filter"

            response = requests.post(
                api_url,
                data={
                    "market": market,
                    "start_year": start_year,
                    "start_month": start_month,
                    "end_year": end_year,
                    "end_month": end_month,
                },
                cookies=request.cookies,
            )

            if response.status_code == 200:
                try:
                    data = response.json()

                    if (
                        not data.get("labels")
                        or not data.get("rpk_values")
                        or len(data.get("labels", [])) == 0
                    ):
                        print("Nenhum dado encontrado para os filtros selecionados")
                        no_data_fig = px.line(
                            title=f"Sem dados para o mercado {market}"
                        )
                        no_data_fig.update_layout(
                            xaxis_title="Data",
                            yaxis_title="RPK",
                            annotations=[
                                {
                                    "text": "Nenhum dado disponível para os filtros selecionados",
                                    "showarrow": False,
                                    "font": {"size": 16},
                                    "xref": "paper",
                                    "yref": "paper",
                                    "x": 0.5,
                                    "y": 0.5,
                                }
                            ],
                        )
                        return no_data_fig, html.Div(
                            [
                                html.H4(
                                    "Nenhum Dado Encontrado", className="text-warning"
                                ),
                                html.P(
                                    f"Nenhum dado de voo encontrado para o mercado '{market}' no intervalo de datas selecionado."
                                ),
                                html.P(
                                    f"Intervalo de datas: {start_year}/{start_month} - {end_year}/{end_month}"
                                ),
                                html.P(
                                    "Tente selecionar um mercado diferente ou intervalo de datas."
                                ),
                            ]
                        )

                    fig = px.line(
                        x=data.get("labels", []),
                        y=data.get("rpk_values", []),
                        title=f"RPK para o mercado {market}",
                        labels={"x": "Data", "y": "RPK"},
                    )

                    fig.update_layout(
                        xaxis_title="Data (Ano-Mês)",
                        yaxis_title="RPK",
                        template="plotly_white",
                        hovermode="x unified",
                    )

                    table = dash_table.DataTable(
                        data=data.get("flights", []),
                        columns=[
                            {"name": "Ano", "id": "ano"},
                            {"name": "Mês", "id": "mes"},
                            {"name": "Mercado", "id": "mercado"},
                            {
                                "name": "RPK",
                                "id": "rpk",
                                "type": "numeric",
                                "format": {"specifier": ",.2f"},
                            },
                        ],
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left", "padding": "10px"},
                        style_header={
                            "backgroundColor": "lightgrey",
                            "fontWeight": "bold",
                        },
                        sort_action="native",
                        filter_action="native",
                        page_size=10,
                    )

                    return fig, table

                except json.JSONDecodeError as je:
                    error_fig = px.line(title="Error parsing response")
                    error_message = html.Div(
                        [
                            html.H4(
                                "Error parsing API response", className="text-danger"
                            ),
                            html.P(f"Error: {str(je)}"),
                            html.P("The API response could not be parsed as JSON."),
                        ]
                    )
                    return error_fig, error_message
            elif response.status_code == 401:
                print("Erro de autenticação - usuário não está logado")
                return px.line(title="Autenticação Necessária"), html.Div(
                    [
                        html.H4("Autenticação Necessária", className="text-danger"),
                        html.P("Por favor, faça login para visualizar estes dados."),
                        dcc.Location(
                            pathname="/login",
                            id="redirect-to-login-from-dash",
                            refresh=True,
                        ),
                    ]
                )
            else:
                print(f"API error: {response.status_code}")
                error_fig = px.line(title="Error loading data")
                error_message = html.Div(
                    [
                        html.H4("Error loading data", className="text-danger"),
                        html.P(f"Status code: {response.status_code}"),
                        html.P(f"Response: {response.text[:100]}..."),
                        html.P("Please try again or contact support."),
                    ]
                )
                return error_fig, error_message
        except Exception as e:
            error_fig = px.line(title="Error processing data")
            error_message = html.Div(
                [
                    html.H4("Error processing data", className="text-danger"),
                    html.P(f"Error: {str(e)}"),
                    html.P("Please try again or contact support."),
                ]
            )
            return error_fig, error_message
