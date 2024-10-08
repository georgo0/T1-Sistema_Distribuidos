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

# Seleccionar aleatoriamente 100,000 dominios con repetición
sampled_domains = random.choices(domains, k=num_queries)

# Contar las frecuencias de cada dominio consultado
domain_frequencies = Counter(sampled_domains)

# Ordenar los dominios por frecuencia en orden descendente
sorted_domain_frequencies = domain_frequencies.most_common()

# Separar dominios y frecuencias
frequencies_sorted = [freq for _, freq in sorted_domain_frequencies]

# Graficar la cantidad de consultas de cada dominio como una curva
plt.figure(figsize=(10, 6))
plt.plot(frequencies_sorted, color='blue', marker='o')  # Graficar curva
plt.xlabel('Dominios consultados')
plt.ylabel('Frecuencia')
plt.title('Cantidad de consultas por dominio')
plt.grid(True)
plt.show()
