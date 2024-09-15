# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y el código fuente
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente de la API REST, gRPC y otros scripts
COPY . /app/

# Expone los puertos necesarios para la API REST y gRPC
EXPOSE 5000
EXPOSE 50051

# Comando para ejecutar ambos servicios
CMD ["sh", "-c", "python3 grpc_server.py & python3 app.py & traffic_generator.py"]




