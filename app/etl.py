import os
from pathlib import Path
import pandas as pd
import pandera as pa
from dotenv import load_dotenv
from sqlalchemy import create_engine
import duckdb


from .schema import ProdutoSchema, ProdutoSchemaKPI


def load_settings():
    """
    Load settings from environment variables.
    """
    load_dotenv(".env")
    settings = {
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'DB_DB': os.getenv('DB_DB')
    }
    return settings

@pa.check_output(ProdutoSchema, lazy=True)
def extract_data_sql(query: str) -> pd.DataFrame:
    """
    Extract data from the database.
    """
    settings = load_settings()
    
    connection_string = f"postgresql://{settings['DB_USER']}:{settings['DB_PASSWORD']}@{settings['DB_HOST']}:{settings['DB_PORT']}/{settings['DB_DB']}"

    engine = create_engine(connection_string)
    with engine.connect() as connection:
        df_crm = pd.read_sql(query, connection)
    # and extract data using the settings loaded from environment variables.
    #print(f"Extracting data from {settings['DB_HOST']}:{settings['DB_PORT']} as {settings['DB_USER']}")
    return df_crm

#@pa.check_input(ProdutoSchema, lazy=True)
#@pa.check_output(ProdutoSchemaKPI, lazy=True)
def transformar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the extracted data.
    """
    # Example transformation: normalize product names and calculate total value in stock
    df['valor_total_estoque'] = df['quantidade'] * df['preco']
    
    # Example of adding a normalized category
    df['categoria_normalizada'] = df['categoria'].str.upper()
    
    # Example of adding a boolean availability column
    df['disponibilidade'] = df['quantidade'] > 0
    
    return df

#@pa.check_input(ProdutoSchemaKPI, lazy=True)
def load_to_duckdb(df: pd.DataFrame, table_name: str, db_file: str = 'meu_duckdb2.db') -> None:

    con = duckdb.connect(database=db_file, read_only=False)

    con.register('df_temp', df)

    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df_temp")

    con.close()

    

if __name__ == "__main__":
    # Example usage
    query = "SELECT * FROM produtos_bronze_email"
    df_crm = extract_data_sql(query=query)
    df_crm_kpi = transformar(df_crm)
    load_to_duckdb(df=df_crm_kpi, table_name='tabela_kpi')
    #schema_crm = pa.infer_schema(df_crm)
    # with open("schema_crm.py", "w", encoding="utf-8") as arquivo:
    #     arquivo.write(schema_crm.to_script())

    print(df_crm)

