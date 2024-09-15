import sqlite3
import random
import requests

# Archivo de base de datos
db_file = 'domains.db'  # Base de datos con 50 mil filas

# Número de consultas aleatorias
num_queries = 10

# Leer dataset desde la base de datos
with sqlite3.connect(db_file) as conn:
    cursor = conn.cursor()
    cursor.execute('''SELECT domain FROM domain''')
    domains = [row[0] for row in cursor.fetchall()]

# Verifica que hay suficientes dominios
if len(domains) == 0:
    raise ValueError(f"El archivo {db_file} está vacío. No hay dominios para consultar.")

# Seleccionar aleatoriamente 75,000 dominios con repetición
sampled_domains = random.choices(domains, k=num_queries)

# URL de la API REST
api_url = "http://localhost:8000/resolve"  # Ajusta el puerto si es necesario

# Enviar consultas a la API REST
for domain in sampled_domains:
    try:
        requests.get(api_url, params={'domain': domain})
    except requests.exceptions.RequestException:
        pass

# Imprimir mensaje final
print(f"Se han generado {num_queries} consultas.")







