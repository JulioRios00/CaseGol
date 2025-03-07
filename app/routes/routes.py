import os

from flask import Blueprint, jsonify, request, redirect
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import TimeoutError
from flask import current_app
import time

from app import db
from app.models.models import Flight, User
from app.utils.utils import hash_password, process_and_load_flight_data, direct_login, direct_register

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
            process_and_load_flight_data(csv_path, chunk_size=50000)


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
        return (
            jsonify({"error": "Username already exists. Please choose another one."}),
            400,
        )

    new_user = User(username=username, password=hash_password(password))

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return (
        jsonify({"message": "User registered successfully", "user_id": new_user.id}),
        201,
    )


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
def root():
    """
    Root route handler - redirects to appropriate page based on authentication
    """
    if current_user.is_authenticated:
        return redirect("/dashboard")
    return redirect("/login")


@main.route("/api/filter", methods=["POST"])
@login_required
def api_filter():
    """
    Função para filtrar os dados de voo com base nos filtros selecionados
    Function to filter flight data based on selected filters
    """
    try:
        market = request.form.get("market")
        start_year = int(request.form.get("start_year"))
        start_month = int(request.form.get("start_month"))
        end_year = int(request.form.get("end_year"))
        end_month = int(request.form.get("end_month"))
        
        start_time = time.time()
        timeout = 25 

        query = db.session.query(
            Flight.id, Flight.ano, Flight.mes, Flight.mercado, Flight.rpk
        ).filter(Flight.mercado == market)

        date_condition = (
            (Flight.ano > start_year)
            | ((Flight.ano == start_year) & (Flight.mes >= start_month))
        ) & (
            (Flight.ano < end_year)
            | ((Flight.ano == end_year) & (Flight.mes <= end_month))
        )

        query = query.filter(date_condition)
        
        flights = query.order_by(Flight.ano, Flight.mes).limit(1000).all()
        
        if time.time() - start_time > timeout:
            return jsonify({"error": "Query timeout. Please try with a smaller date range."}), 408

        labels = []
        rpk_values = []
        flight_data = []
        
        for flight in flights:
            if time.time() - start_time > timeout:
                break
                
            labels.append(f"{flight.ano}-{flight.mes:02d}")
            rpk_value = float(flight.rpk) if flight.rpk is not None else 0.0
            rpk_values.append(rpk_value)
            
            flight_data.append({
                "id": flight.id,
                "ano": flight.ano,
                "mes": flight.mes,
                "mercado": flight.mercado,
                "rpk": rpk_value,
            })

        response_data = {
            "flights": flight_data,
            "labels": labels,
            "rpk_values": rpk_values,
            "market": market,
        }
        return jsonify(response_data), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@main.route("/api/dashboard-data")
@login_required
def api_dashboard_data():
    import time
    start_time = time.time()
    timeout = 25  
    
    try:

        year_data = db.session.query(
            db.func.min(Flight.ano).label('min_year'),
            db.func.max(Flight.ano).label('max_year')
        ).first()
        
        year_min = year_data.min_year if year_data else 2000
        year_max = year_data.max_year if year_data else 2023
        

        if time.time() - start_time > timeout:

            return jsonify({
                "year_min": 2000,
                "year_max": 2023,
                "markets": []
            }), 200
        
        markets = [
            market[0]
            for market in db.session.query(Flight.mercado).distinct().limit(200).all()
        ]
        
        return (
            jsonify({"year_min": year_min, "year_max": year_max, "markets": markets}),
            200,
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "year_min": 2000,
            "year_max": 2023,
            "markets": [],
            "error": str(e)
        }), 200

@main.route("/api/dashboard-data/markets", methods=["GET"])
@login_required
def api_dashboard_markets():
    """
    Obtém todos os mercados disponíveis no banco de dados
    Get all available markets in the database
    """
    import time
    start_time = time.time()
    timeout = 25  
    
    try:

        markets = [
            market[0]
            for market in db.session.query(Flight.mercado).distinct().limit(200).all()
        ]
        
        if time.time() - start_time > timeout:
            return jsonify({
                "status": "partial", 
                "message": "Query timed out, returning partial results",
                "count": 0, 
                "markets": []
            }), 200
            
        markets.sort()

        return (
            jsonify({"status": "success", "count": len(markets), "markets": markets}),
            200,
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e), "markets": []}), 200


@main.route("/api/auth-status")
def auth_status():
    """Debug endpoint to check authentication status"""
    if current_user.is_authenticated:
        return (
            jsonify(
                {
                    "authenticated": True,
                    "user_id": current_user.id,
                    "username": current_user.username,
                }
            ),
            200,
        )
    else:
        return jsonify({"authenticated": False}), 200
