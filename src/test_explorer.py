import requests
import urllib.parse
import pandas as pd

def test_explorer_query():
    # Query SQL simples: retorna 1 linhas da tabela matches
    query = "SELECT * FROM heroes"
    
    # Codifica a query para percent-encoding
    encoded_query = urllib.parse.quote(query)
    
    # Monta a URL com o parâmetro 'sql'
    url = f"https://api.opendota.com/api/explorer?sql={encoded_query}"
    
    print("URL gerada:", url)
    
    # Faz a requisição GET
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Erro {response.status_code}: {response.text}")
    

if __name__ == "__main__":
    test_explorer_query()