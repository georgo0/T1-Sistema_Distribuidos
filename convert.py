import pandas as pd
import sqlite3

# Lee solo las primeras 50,000 filas del archivo CSV
csv_file = '3rd_lev_domains.csv'
df = pd.read_csv(csv_file, header=None, names=['domain'], nrows=40000)

# Conecta a la base de datos SQLite (se creará si no existe)
db_file = 'domains.db'
conn = sqlite3.connect(db_file)

# Verificar si la tabla ya existe, si no, crearla
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS domain (domain TEXT)")

# Guarda el DataFrame en la base de datos SQLite
df.to_sql('domain', conn, if_exists='replace', index=False)

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print(f"La base de datos '{db_file}' se ha creado correctamente con la tabla 'domain'.")

