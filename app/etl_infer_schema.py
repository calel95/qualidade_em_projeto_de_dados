import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
import pandera as pa
from schema import SchemaCRM




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

@pa.check_output(SchemaCRM)
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
    print(f"Extracting data from {settings['DB_HOST']}:{settings['DB_PORT']} as {settings['DB_USER']}")
    return df_crm

if __name__ == "__main__":
    # Example usage
    query = "SELECT * FROM public.vendas"
    df_crm = extract_data_sql(query)
    schema_crm = pa.infer_schema(df_crm)
    with open("schema_crm.json", "w", encoding="utf-8") as f:
        f.write(schema_crm.to_script())

    with open("schema_crm.py", "w", encoding="utf-8") as arquivo:
        arquivo.write(schema_crm.to_script())

    print(schema_crm)