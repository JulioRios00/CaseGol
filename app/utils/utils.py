import hashlib
import os
import traceback

import pandas as pd

from app import db
from app.models.models import Flight


def hash_password(password):
    hash_obj = hashlib.sha256(password.encode("utf-8"))
    return hash_obj.hexdigest()


def process_and_load_flight_data(csv_path):
    """
    Faz o processamento dos dados de voo da ANAC e inserir os dados processados no banco de dados.
    Adicionei alguns logs para facilitar a depuração de erros
    Process the flight data from ANAC and insert the processed data into the database.
    I added some logs to facilitate debugging errors
    """

    if not os.path.exists(csv_path):
        print(f"ERROR: CSV file not found at {csv_path}")
        return

    try:
        df = pd.read_csv(
            csv_path,
            delimiter=";",
            quotechar='"',
            skipinitialspace=True,
            skiprows=1,
            low_memory=False,
            encoding="utf-8",
        )

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

        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            print(f"ERROR: Missing required columns: {missing_cols}")
            return False

        df_filtered = df[
            (df["EMPRESA_SIGLA"] == "GLO")
            & (df["GRUPO_DE_VOO"] == "REGULAR")
            & (df["NATUREZA"] == "DOMÉSTICA")
        ].copy()
        print(f"Filtered data shape: {df_filtered.shape}")

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
        print(f"Final grouped data shape: {df_final.shape}")

        for _, row in df_final.iterrows():
            flight = Flight(
                ano=row["ANO"], mes=row["MES"], mercado=row["MERCADO"], rpk=row["RPK"]
            )
            db.session.add(flight)

        db.session.commit()
        print("Database populated successfully!")
        print(f"Successfully loaded {Flight.query.count()} records from CSV")
        return True

    except Exception as e:
        print(f"Error populating database: {e}")
        traceback.print_exc()
        db.session.rollback()
        return False
