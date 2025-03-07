import pandas as pd
from sqlalchemy import create_engine
import os
import requests
from io import BytesIO
from dotenv import load_dotenv
import traceback
from app.utils.utils import process_and_load_flight_data

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/golcase')

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

CSV_URL = "https://sistemas.anac.gov.br/dadosabertos/Voos%20e%20opera%C3%A7%C3%B5es%20a%C3%A9reas/Dados%20Estat%C3%ADsticos%20do%20Transporte%20A%C3%A9reo/Dados_Estatisticos.csv"
CSV_PATH = "/app/data/Dados_Estatisticos.csv"

def download_csv():
    """Baixa o CSV da ANAC"""
    print(f"Baixando dados da ANAC de: {CSV_URL}")
    
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    
    try:
        response = requests.get(CSV_URL, stream=True)
        response.raise_for_status()
        
        with open(CSV_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Download concluído: {CSV_PATH}")
        return True
    except Exception as e:
        print(f"Erro ao baixar CSV: {str(e)}")
        traceback.print_exc()
        return False

def populate_database():
    """Popula o banco de dados com dados de voos"""
    try:
        from app import create_app, db
        from app.models.models import Flight

        app = create_app()
        with app.app_context():
            if Flight.query.count() > 0:
                print("Banco de dados já possui dados. Pulando importação.")
                return True
            
            if not os.path.exists(CSV_PATH):
                if not download_csv():
                    return False
            
            print(f"Processando CSV: {CSV_PATH}")
            success = process_and_load_flight_data(CSV_PATH)
            
            if success:
                print("Banco de dados populado com sucesso!")
            else:
                print("Falha ao popular o banco de dados.")
            
            return success
    except Exception as e:
        print(f"Erro ao popular banco de dados: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    populate_database()
