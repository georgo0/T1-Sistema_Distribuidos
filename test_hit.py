import sqlite3
import random
import requests
import matplotlib.pyplot as plt

# Archivo de base de datos
db_file = 'domains.db'  # Base de datos con 50 mil filas

# URL de la API REST
api_url = "http://localhost:8000/resolve"

# Número de consultas aleatorias
num_queries = 10000

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

# Contadores para cache hits y misses
cache_hits = 0
cache_misses = 0

# Realizar consultas y contar hits y misses
for domain in sampled_domains:
    try:
        response = requests.get(api_url, params={'domain': domain})
        #print(f'Preguntando por dominio: {domain}')
        result = response.json()
        #print(result)
        # Manejar los casos en que la respuesta no es un dict o tiene un formato inesperado
        if isinstance(result, dict) and 'cache_hit' in result:
            cache_hit = result.get('cache_hit', False)
            if cache_hit:
                cache_hits += 1
            else:
                cache_misses += 1
        #else:
        #    print(f"Unexpected response format for domain {domain}: {result}")
    except requests.exceptions.RequestException as e:
        pass
        #print(f"Request failed for domain {domain}: {e}")

# Imprimir resultados
print(f"Cache hits: {cache_hits}")
print(f"Cache misses: {cache_misses}")

# Graficar resultados
labels = ['Cache Hits', 'Cache Misses']
sizes = [cache_hits, cache_misses]

plt.figure(figsize=(8, 6))
plt.bar(labels, sizes, color=['green', 'red'])
plt.xlabel('Cache Status')
plt.ylabel('Count')
plt.title('Cache Hits vs Cache Misses')
plt.show()


