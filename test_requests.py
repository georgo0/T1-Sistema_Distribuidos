import sqlite3
import random
import requests
import matplotlib.pyplot as plt
from collections import Counter

# Archivo de base de datos
db_file = '3rd_lev_domains.db'  # Base de datos con 50 mil filas

# URL de la API REST
api_url = "http://localhost:8000/resolve"

# Número de consultas aleatorias
num_queries = 100000

# Leer dataset desde la base de datos
with sqlite3.connect(db_file) as conn:
    cursor = conn.cursor()
    cursor.execute('''SELECT domain FROM valid_domains''')
    domains = [row[0] for row in cursor.fetchall()]

# Verifica que hay suficientes dominios
if len(domains) == 0:
    raise ValueError(f"El archivo {db_file} está vacío. No hay dominios para consultar.")

# Seleccionar aleatoriamente 10,000 dominios con repetición
sampled_domains = random.choices(domains, k=num_queries)

# Contar las frecuencias de cada dominio consultado
domain_frequencies = Counter(sampled_domains)

# Obtener la frecuencia de cada dominio
frequencies = list(domain_frequencies.values())

# Graficar la distribución de frecuencias
plt.figure(figsize=(10, 6))
plt.hist(frequencies, bins=30, color='blue', edgecolor='black')
plt.xlabel('Cantidad de consultas por dominio')
plt.ylabel('Frecuencia de consultas')
plt.title('Distribución de frecuencias de consultas a dominios')
plt.grid(True)
plt.show()