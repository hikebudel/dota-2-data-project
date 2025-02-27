import os
from dotenv import load_dotenv
import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Carrega as variáveis do arquivo .env
load_dotenv()

def fetch_heroes():
    url = "https://api.opendota.com/api/heroes"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao buscar heroes: {response.status_code}")

def process_heroes(data):
    df = pd.DataFrame(data)
    df['roles'] = df['roles'].apply(lambda roles: ", ".join(roles) if isinstance(roles, list) else roles)
    return df

def insert_heroes(df, conn):
    tuples = list(df[['id', 'name', 'localized_name', 'primary_attr', 'attack_type', 'roles', 'legs']].itertuples(index=False, name=None))
    
    query = """
    INSERT INTO dota_dw.heroes (id, name, localized_name, primary_attr, attack_type, roles, legs)
    VALUES %s
    ON CONFLICT (id) DO UPDATE SET 
        name = EXCLUDED.name,
        localized_name = EXCLUDED.localized_name,
        primary_attr = EXCLUDED.primary_attr,
        attack_type = EXCLUDED.attack_type,
        roles = EXCLUDED.roles,
        legs = EXCLUDED.legs;
    """
    
    with conn.cursor() as cursor:
        execute_values(cursor, query, tuples)
    conn.commit()

def create_heroes_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS dota_dw.heroes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        localized_name TEXT,
        primary_attr TEXT,
        attack_type TEXT,
        roles TEXT,
        legs INTEGER
    );
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()

def main():
    # Recupera as credenciais a partir das variáveis de ambiente
    dbname = os.getenv("DB_NAME")
    dbuser = os.getenv("DB_USER")
    dbpassword = os.getenv("DB_PASSWORD")
    dbhost = os.getenv("DB_HOST")
    dbport = os.getenv("DB_PORT")
    
    # Conexão com o PostgreSQL
    conn = psycopg2.connect(
        dbname=dbname,
        user=dbuser,
        password=dbpassword,
        host=dbhost,
        port=dbport
    )
    
    try:
        heroes_data = fetch_heroes()
        df_heroes = process_heroes(heroes_data)
        print("Dados tratados:")
        print(df_heroes.head())
        create_heroes_table(conn)
        insert_heroes(df_heroes, conn)
        print("Dados de heroes inseridos com sucesso!")
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
