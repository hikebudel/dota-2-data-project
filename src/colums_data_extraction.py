import requests
import pandas as pd

"""
    Faz a requisição ao endpoint /api/schema do OpenDota
    e retorna o conteúdo em formato JSON.
    """
url = "https://api.opendota.com/api/schema?"
response = requests.get(url)
if response.status_code == 200:
    ex = response.json()
else:
    print(f"Erro ao obter schema. Status code: {response.status_code}")
    ex = []

tables = {}
for table_info in ex:
    table_name = table_info.get("table_name")
    column_name = table_info.get("column_name")
    if table_name not in tables:
        tables[table_name] = []
    
    if column_name not in tables[table_name]:
        tables[table_name].append(column_name)

df = pd.DataFrame({
    "table_name": tables.keys(),
    "columns": [", ".join(cols) for cols in tables.values()]  
})

df.to_csv("teste.csv", index=False, encoding="utf-8")

