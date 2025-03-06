import os

from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app
from flask_login import login_required, login_user, logout_user, current_user

from app import db
from app.models.models import Flight, User
from app.utils.utils import hash_password, process_and_load_flight_data
import pandas as pd

from datetime import datetime
import json
from flask_login import current_user

main = Blueprint("main", __name__)


"""
    Mesmo comportamento em relação ao arquivo de models.
    Devido a pequena quantidade de rotas,
    mantive todas elas em um mesmo arquivo.

    Same behavior as the models file. Due the small number of routes,
    I kept them all in the same file.
"""


@main.before_app_first_request
def setup_database():
    db.create_all()

    if Flight.query.count() == 0:
        csv_path = os.path.join(main.root_path, "../data/Dados_Estatisticos.csv")
        if os.path.exists(csv_path):
            process_and_load_flight_data(csv_path)


"""
    Rotas de autenticação
    Authentication routes
"""
@main.route("/api/register", methods=["POST"])
def api_register():
    username = request.form["username"]
    password = request.form["password"]

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists. Please choose another one."}), 400

    new_user = User(username=username, password=hash_password(password))

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201


@main.route("/api/login", methods=["POST"])
def api_login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(
        username=username, password=hash_password(password)
    ).first()

    if user is None:
        return jsonify({"error": "Invalid username and/or password"}), 401

    login_user(user)

    return jsonify({"message": "Login successful", "user_id": user.id}), 200


@main.route("/api/logout")
@login_required
def api_logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


"""
    Rotas da aplicação
    Application routes
"""
@main.route("/")
@login_required
def dashboard():
    year_min = db.session.query(db.func.min(Flight.ano)).scalar()
    year_max = db.session.query(db.func.max(Flight.ano)).scalar()

    markets = [
        market[0]
        for market in Flight.query.with_entities(Flight.mercado).distinct().all()
    ]

    return (
        jsonify({"year_min": year_min, "year_max": year_max, "markets": markets}),
        200,
    )


@main.route("/filter", methods=["POST"])
@login_required
def filter():
    market = request.form.get("market")
    start_year = int(request.form.get("start_year"))
    start_month = int(request.form.get("start_month"))
    end_year = int(request.form.get("end_year"))
    end_month = int(request.form.get("end_month"))

    flights = (
        Flight.query.filter(
            Flight.mercado == market,
            Flight.ano >= start_year,
            Flight.mes >= start_month,
            Flight.ano <= end_year,
            Flight.mes <= end_month,
        )
        .order_by(Flight.ano, Flight.mes)
        .all()
    )

    labels = [f"{flight.ano}-{flight.mes}" for flight in flights]
    rpk_values = [flight.rpk for flight in flights]

    flight_data = []
    for flight in flights:
        flight_data.append(
            {
                "id": flight.id,
                "ano": flight.ano,
                "mes": flight.mes,
                "mercado": flight.mercado,
                "rpk": flight.rpk,
            }
        )

    response_data = {
        "flights": flight_data,
        "labels": labels,
        "rpk_values": rpk_values,
        "market": market,
    }
    return jsonify(response_data), 200


@main.route("/api/dashboard-data")
@login_required
def api_dashboard_data():
    year_min = db.session.query(db.func.min(Flight.ano)).scalar()
    year_max = db.session.query(db.func.max(Flight.ano)).scalar()

    markets = [
        market[0]
        for market in Flight.query.with_entities(Flight.mercado).distinct().all()
    ]
    
    return jsonify({
        "year_min": year_min,
        "year_max": year_max,
        "markets": markets
    }), 200


@main.route("/api/filter", methods=["POST"])
@login_required
def api_filter():
    """
    Função para filtrar os dados de voo com base nos filtros selecionados
    Function to filter flight data based on selected filters
    """
    try:
        for key, value in request.form.items():
            print(f"  {key}: {value}")
        
        market = request.form.get("market")
        start_year = int(request.form.get("start_year"))
        start_month = int(request.form.get("start_month"))	
        end_year = int(request.form.get("end_year"))
        end_month = int(request.form.get("end_month"))

        query = Flight.query.filter(Flight.mercado == market)
        
        date_condition = (
            ((Flight.ano > start_year) | ((Flight.ano == start_year) & (Flight.mes >= start_month))) &
            ((Flight.ano < end_year) | ((Flight.ano == end_year) & (Flight.mes <= end_month)))
        )
        
        query = query.filter(date_condition)
        
        flights = query.order_by(Flight.ano, Flight.mes).all()
        
        labels = [f"{flight.ano}-{flight.mes:02d}" for flight in flights]
        rpk_values = [float(flight.rpk) if flight.rpk is not None else 0.0 for flight in flights]

        flight_data = []
        for flight in flights:
            flight_data.append({
                "id": flight.id,
                "ano": flight.ano,
                "mes": flight.mes,
                "mercado": flight.mercado,
                "rpk": float(flight.rpk) if flight.rpk is not None else 0.0
            })

        response_data = {
            "flights": flight_data,
            "labels": labels,
            "rpk_values": rpk_values,
            "market": market
        }
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/markets")
def api_markets():
    """
    Obtém todos os mercados disponíveis no banco de dados
    Get all available markets in the database
    """
    try:
        markets = [
            market[0]
            for market in Flight.query.with_entities(Flight.mercado).distinct().all()
        ]
        
        for i, market in enumerate(markets[:10]):
            print(f"  {i+1}. {market}")
        
        if len(markets) > 10:
            print(f"  ... and {len(markets) - 10} more")
            
        return jsonify({
            "status": "success",
            "count": len(markets),
            "markets": markets
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def direct_login(username, password):
    """
    Função para logar um usuário diretamente a partir de callbacks do Dash
    Function to log in a user directly from Dash callbacks
    """
    from flask_login import current_user
    
    user = User.query.filter_by(
        username=username, password=hash_password(password)
    ).first()
    
    if user is None:
        return False, "Nome de usuário ou senha inválidos"
    
    login_user(user)
    
    return True, None


def direct_register(username, password):
    """
    Função para registrar um usuário diretamente a partir de callbacks do Dash
    Function to register a user directly from Dash callbacks
    """
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return False, "Nome de usuário já existe"
    
    new_user = User(username=username, password=hash_password(password))
    db.session.add(new_user)
    
    try:
        db.session.commit()
        login_user(new_user)
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, f"Erro ao registrar: {str(e)}"


def process_and_load_flight_data(csv_path):
    """
    Processa os dados do CSV da ANAC e carrega no banco de dados.
    Filtros:
    - EMPRESA = "GLO" (GOL)
    - GRUPO_DE_VOO = "REGULAR"
    - NATUREZA = "DOMÉSTICA"

    Cria MERCADO ordenando alfabeticamente ORIGEM + DESTINO
    
    Process and load flight data from ANAC CSV file into the database.
    Filters:
    - EMPRESA = "GLO" (GOL)
    - GRUPO_DE_VOO = "REGULAR"
    - NATUREZA = "DOMÉSTICA"
    
    Creates MARKET by sorting alphabetically ORIGIN + DESTINATION
    """
	
    df = pd.read_csv(csv_path, sep=';', encoding='latin1')
    
    df = df[
        (df['EMPRESA'] == 'GLO') & 
        (df['GRUPO DE VOO'] == 'REGULAR') & 
        (df['NATUREZA'] == 'DOMÉSTICA')
    ]
    
    def create_market(row):
        airports = sorted([row['ORIGEM'], row['DESTINO']])
        return ''.join(airports)
    
    df['MERCADO'] = df.apply(create_market, axis=1)
    
    grouped = df.groupby(['ANO', 'MÊS', 'MERCADO'])['RPK'].sum().reset_index()
    
    for _, row in grouped.iterrows():
        flight = Flight(
            ano=int(row['ANO']),
            mes=int(row['MÊS']),
            mercado=row['MERCADO'],
            rpk=float(row['RPK'])
        )
        db.session.add(flight)
    
    db.session.commit()