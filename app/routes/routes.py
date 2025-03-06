from flask import Blueprint, flash, request, jsonify

from flask_login import login_user, logout_user, login_required, current_user

from app import db

from app.models.models import User, Flight

from app.utils.utils import hash_password, process_and_load_flight_data

import os


# Create a Blueprint
main = Blueprint('main', __name__)


"""
    Mesmo comportamento em relação ao arquivo de models. Devido a pequena quantidade de rotas,
    mantive todas elas em um mesmo arquivo.
   
    Same behavior as the models file. Due the small number of routes,
    I kept them all in the same file.
"""
@main.before_app_first_request
def setup_database():
    db.create_all()
   
    if Flight.query.count() == 0:
        csv_path = os.path.join(main.root_path, '../data/Dados_Estatisticos.csv')
        if os.path.exists(csv_path):
            process_and_load_flight_data(csv_path)


"""
    Rotas de autenticação
    Authentication routes
"""
@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return jsonify({"message": "Register page"}), 200
    elif request.method == "POST":
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
   

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return jsonify({"message": "Login page"}), 200
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username, password=hash_password(password)
        ).first()

        if user is None:
            return jsonify({"error": "Invalid username and/or password"}), 401

        login_user(user)

        return jsonify({"message": "Login successful", "user_id": user.id}), 200
   

@main.route("/logout")
@login_required
def logout():
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

    markets = [market[0] for market in Flight.query.with_entities(Flight.mercado).distinct().all()]
    
    return jsonify({
        "year_min": year_min,
        "year_max": year_max,
        "markets": markets
    }), 200


@main.route("/filter", methods=["POST"])
@login_required
def filter():
    market = request.form.get("market")
    start_year = int(request.form.get("start_year"))
    start_month = int(request.form.get("start_month"))
    end_year = int(request.form.get("end_year"))
    end_month = int(request.form.get("end_month"))

    flights = Flight.query.filter(
        Flight.mercado == market,
        Flight.ano >= start_year,
        Flight.mes >= start_month,
        Flight.ano <= end_year,
        Flight.mes <= end_month,
    ).order_by(Flight.ano, Flight.mes).all()

    labels = [f"{flight.ano}-{flight.mes}" for flight in flights]
    rpk_values = [flight.rpk for flight in flights]

    # Convert flight objects to serializable dictionaries
    flight_data = []
    for flight in flights:
        flight_data.append({
            "id": flight.id,
            "ano": flight.ano,
            "mes": flight.mes,
            "mercado": flight.mercado,
            "rpk": flight.rpk
        })

    response_data = {
        "flights": flight_data,
        "labels": labels,
        "rpk_values": rpk_values,
        "market": market
    }
    return jsonify(response_data), 200
    
@main.route("/admin/load-data")
def admin_load_data():
    db.create_all()
    
    count_before = Flight.query.count()
    
    csv_path = "/home/clint/learning/testes/gol/data/Dados_Estatisticos.csv"
    
    if not os.path.exists(csv_path):
        return jsonify({
            "error": "CSV file not found",
            "path_checked": csv_path
        }), 404
    
    try:
        process_and_load_flight_data(csv_path)
        count_after = Flight.query.count()
        
        return jsonify({
            "success": True,
            "message": "Data loaded successfully",
            "records_before": count_before,
            "records_after": count_after,
            "csv_path": csv_path
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Failed to load data",
            "exception": str(e)
        }), 500

@main.route("/filter-test", methods=["POST"])
@login_required
def filter_test():
    # A simplified version to test if the basic functionality works
    return jsonify({"test": "success"}), 200
