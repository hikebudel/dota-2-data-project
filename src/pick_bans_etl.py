import os
from dotenv import load_dotenv
import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Carrega as variáveis do arquivo .env
load_dotenv()

def fetch_picks_bans():
    # Query simples para extrair todos os dados da tabela picks_bans
    query = "SELECT * FROM picks_bans"
    encoded_query = requests.utils.quote(query)
    url = f"https://api.opendota.com/api/explorer?sql={encoded_query}"
    response = requests.get(url)
    if response.status_code == 200:
        # Retorna apenas os registros (rows) do JSON
        return response.json()['rows']
    else:
        raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")

def process_picks_bans(data):
    # Converte os dados brutos em um DataFrame sem alterações adicionais
    df = pd.DataFrame(data)
    return df

def create_picks_bans_table(conn):
    # Cria a tabela picks_bans no schema dota_dw com as colunas necessárias.
    # Aqui usamos match_id e ord como chave composta para evitar duplicação.
    query = """
    CREATE TABLE IF NOT EXISTS dota_dw.picks_bans (
        match_id BIGINT,
        is_pick BOOLEAN,
        hero_id INTEGER,
        team INTEGER,
        ord INTEGER,
        PRIMARY KEY (match_id, ord)
    );
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()

def insert_picks_bans(df, conn):
    # Converte o DataFrame para uma lista de tuplas, semelhante ao ETL dos heroes
    tuples = list(df[['match_id', 'is_pick', 'hero_id', 'team', 'ord']].itertuples(index=False, name=None))
    
    query = """
    INSERT INTO dota_dw.picks_bans (match_id, is_pick, hero_id, team, ord)
    VALUES %s
    ON CONFLICT (match_id, ord) DO UPDATE SET
       is_pick = EXCLUDED.is_pick,
       hero_id = EXCLUDED.hero_id,
       team = EXCLUDED.team;
    """
    
    with conn.cursor() as cursor:
        execute_values(cursor, query, tuples)
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
        data = fetch_picks_bans()
        df = process_picks_bans(data)
        print("Visualização dos dados tratados:")
        print(df.head())
        create_picks_bans_table(conn)
        insert_picks_bans(df, conn)
        print("Dados de picks_bans inseridos com sucesso!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
