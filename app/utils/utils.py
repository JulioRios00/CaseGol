import hashlib
import os

import pandas as pd
from flask_login import login_user

from app import db
from app.models.models import Flight, User


def hash_password(password):
    hash_obj = hashlib.sha256(password.encode("utf-8"))
    return hash_obj.hexdigest()


def direct_login(username, password):
    """
    Função para logar um usuário diretamente a partir de callbacks do Dash
    Function to log in a user directly from Dash callbacks
    """
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


def process_and_load_flight_data(csv_path, chunk_size=100000):
    """
    Faz o processamento dos dados de voo da ANAC e insere os dados processados no banco de dados.
    Adicionei alguns logs para facilitar a depuração de erros
    Process the flight data from ANAC and insert the processed data into the database.
    I added some logs to facilitate debugging errors
    
    Args:
        csv_path: Path to the CSV file
        chunk_size: Number of rows to process in each chunk (default: 100,000)
    """

    if not os.path.exists(csv_path):
        print(f"ERROR: CSV file not found at {csv_path}")
        return False

    try:
        print("Analisando a estrutura do arquivo CSV...")
        with open(csv_path, 'r', encoding='utf-8') as f:
            first_few_lines = [next(f) for _ in range(5)]
            print("Primeiras linhas do arquivo:")
            for i, line in enumerate(first_few_lines):
                print(f"Linha {i+1}: {line.strip()}")
        
        print("Lendo as primeiras linhas do CSV para debug (pulando linha de metadados)...")
        df_sample = pd.read_csv(
            csv_path,
            delimiter=";",
            quotechar='"',
            skipinitialspace=True,
            skiprows=1,
            nrows=5,
            encoding="utf-8",
        )
        print(f"Colunas disponíveis: {df_sample.columns.tolist()}")
        
        required_cols = [
            "EMPRESA_SIGLA",
            "GRUPO_DE_VOO",
            "NATUREZA",
            "AEROPORTO_DE_ORIGEM_SIGLA",
            "AEROPORTO_DE_DESTINO_SIGLA",
            "ANO",
            "MES",
            "RPK",
        ]

        missing_cols = [col for col in required_cols if col not in df_sample.columns]
        if missing_cols:
            print(f"ERROR: Missing required columns: {missing_cols}")
            return False
            
        print(f"Processando CSV em chunks de {chunk_size} linhas...")
        
        chunks = pd.read_csv(
            csv_path,
            delimiter=";",
            quotechar='"',
            skipinitialspace=True,
            skiprows=1,
            low_memory=False,
            encoding="utf-8",
            chunksize=chunk_size
        )
        
        total_chunks = 0
        total_records = 0
        
        for chunk_num, df_chunk in enumerate(chunks, 1):
            df_filtered = df_chunk[
                (df_chunk["EMPRESA_SIGLA"] == "GLO")
                & (df_chunk["GRUPO_DE_VOO"] == "REGULAR")
                & (df_chunk["NATUREZA"] == "DOMÉSTICA")
            ].copy()
            
            if len(df_filtered) == 0:
                print(f"Chunk {chunk_num} has no matching records, skipping...")
                continue
                
            df_filtered.loc[:, "MERCADO"] = df_filtered.apply(
                lambda row: "".join(
                    sorted(
                        [
                            row["AEROPORTO_DE_ORIGEM_SIGLA"],
                            row["AEROPORTO_DE_DESTINO_SIGLA"],
                        ]
                    )
                ),
                axis=1,
            )
            
            df_final = (
                df_filtered.groupby(["ANO", "MES", "MERCADO"])["RPK"].sum().reset_index()
            )
            
            for _, row in df_final.iterrows():
                flight = Flight(
                    ano=row["ANO"], mes=row["MES"], mercado=row["MERCADO"], rpk=row["RPK"]
                )
                db.session.add(flight)
                total_records += 1
                
            db.session.commit()
            total_chunks += 1
            print(f"Processed chunk {chunk_num} with {len(df_final)} records")
            
        print(f"Processing complete. Processed {total_chunks} chunks with {total_records} total records.")
        return True

    except Exception as e:
        print(f"Error populating database: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return False
