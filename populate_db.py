import pandas as pd
from sqlalchemy import create_engine
import os
import requests
from io import BytesIO
from dotenv import load_dotenv
import traceback
from app.utils.utils import process_and_load_flight_data
import argparse

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://ue2vq6vfrikq1a:p1973b361910c931982a079e3016e495e9c9c03d24d39488ac5850c09e05f06ed@c3nv2ev86aje4j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dfuev85km9t3nd')

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

def populate_database(chunk_size=100000):
    """
    Popula o banco de dados com dados de voos
    
    Args:
        chunk_size: Number of rows to process in each chunk (default: 100,000)
    """
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
            success = process_and_load_flight_data(CSV_PATH, chunk_size=chunk_size)
            
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
    parser = argparse.ArgumentParser(description='Populate the database with flight data.')
    parser.add_argument('--chunk-size', type=int, default=100000, 
                        help='Number of rows to process in each chunk (default: 100,000)')
    
    args = parser.parse_args()
    populate_database(chunk_size=args.chunk_size)
