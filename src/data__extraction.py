# src/extract_data.py

import requests
import os
import time

# Exemplo de função para extrair dados de partidas recentes
def fetch_recent_matches(limit=100):
    """
    Faz uma requisição para a OpenDota API e retorna
    os dados das partidas recentes (até 'limit').
    """
    url = f"https://api.opendota.com/api/proMatches?limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter dados. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    # Exemplo de uso
    matches = fetch_recent_matches(limit=10)
    if matches:
        print("Exemplo de dados de partidas recentes:")
        for match in matches[:3]:  # Mostra só 3 partidas como exemplo
            print(match)