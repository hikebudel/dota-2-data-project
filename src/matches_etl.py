import os
from dotenv import load_dotenv
import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Carrega as variáveis do arquivo .env
load_dotenv()

def fetch_matches():
    # Query em uma única linha, sem filtragem e sem a coluna picks_bans
    query = ("SELECT match_id, radiant_win, start_time, duration, first_blood_time, "
             "lobby_type, human_players, game_mode, radiant_score, dire_score FROM matches")
    encoded_query = requests.utils.quote(query)
    url = f"https://api.opendota.com/api/explorer?sql={encoded_query}"
    
    # Define um timeout (em segundos) para aguardar a resposta da API
    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        # Retorna apenas os registros sob a chave 'rows'
        return response.json()['rows']
    else:
        raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")

def process_matches(data):
    df = pd.DataFrame(data)
    return df

def create_matches_table(conn):
    # Cria ou substitui a tabela matches no schema dota_dw sem a coluna picks_bans
    query = """
    DROP TABLE IF EXISTS dota_dw.matches;
    CREATE TABLE IF NOT EXISTS dota_dw.matches (
        match_id BIGINT PRIMARY KEY, 
        radiant_win BOOLEAN,
        start_time BIGINT,
        duration INTEGER,
        first_blood_time FLOAT,
        lobby_type FLOAT,
        human_players FLOAT,
        game_mode FLOAT,
        radiant_score FLOAT,
        dire_score FLOAT
    );
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
    conn.commit()

def insert_matches(df, conn):
    # Converte o DataFrame para uma lista de tuplas, usando apenas as colunas desejadas
    tuples = list(df[['match_id', 'radiant_win', 'start_time', 'duration', 'first_blood_time', 
                       'lobby_type', 'human_players', 'game_mode', 'radiant_score', 'dire_score']]
                  .itertuples(index=False, name=None))
    
    query = """
    INSERT INTO dota_dw.matches (match_id, radiant_win, start_time, duration, first_blood_time, 
                                   lobby_type, human_players, game_mode, radiant_score, dire_score)
    VALUES %s
    ON CONFLICT (match_id) DO UPDATE SET
      radiant_win = EXCLUDED.radiant_win,
      start_time = EXCLUDED.start_time,
      duration = EXCLUDED.duration,
      first_blood_time = EXCLUDED.first_blood_time,
      lobby_type = EXCLUDED.lobby_type,
      human_players = EXCLUDED.human_players,
      game_mode = EXCLUDED.game_mode,
      radiant_score = EXCLUDED.radiant_score,
      dire_score = EXCLUDED.dire_score;
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
        data = fetch_matches()
        df_matches = process_matches(data)
        print("Visualização dos dados tratados:")
        print(df_matches.head())
        create_matches_table(conn)
        insert_matches(df_matches, conn)
        print("Dados de matches inseridos com sucesso!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
