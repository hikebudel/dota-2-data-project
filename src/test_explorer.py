import requests
import urllib.parse
import pandas as pd

def test_explorer_query():
    query = "SELECT * FROM player_matches"
    
    encoded_query = urllib.parse.quote(query)
    
    url = f"https://api.opendota.com/api/explorer?sql={encoded_query}"
    
    print("URL:", url)

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data['rowCount'])
    else:
        print(f"Erro {response.status_code}: {response.text}")
    

if __name__ == "__main__":
    test_explorer_query()