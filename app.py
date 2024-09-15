import redis
import grpc
import subprocess
from fastapi import FastAPI
from pydantic import BaseModel
from cache_pb2_grpc import CacheServiceStub
from cache_pb2 import DomainRequest
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

# Configurar clientes Redis (varios para particiones)
redis_clients = [
    redis.Redis(host='127.0.0.1', port=6380, decode_responses=True),
    redis.Redis(host='127.0.0.1', port=6381, decode_responses=True),
    redis.Redis(host='127.0.0.1', port=6382, decode_responses=True)
]

# Obtener el cliente Redis correspondiente basado en el hash de la clave
def get_redis_client(key: str):
    index = hash(key) % len(redis_clients)
    return redis_clients[index]

# Consultar el caché de Redis
def get_from_cache(domain: str):
    client = get_redis_client(domain)
    return client.get(domain)

# Guardar el resultado en el caché de Redis
def save_to_cache(domain: str, ip: str):
    client = get_redis_client(domain)
    client.set(domain, ip)

# Llamada gRPC al servidor para obtener la IP
def get_ip_from_grpc(domain: str):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = CacheServiceStub(channel)
        request = DomainRequest(domain=domain)
        response = stub.ResolveDomain(request)
        return response.ip_address

# Usar `dig` para obtener la IP en caso de que gRPC no esté configurado
def get_ip_using_dig(domain: str):
    try:
        result = subprocess.run(['dig', '+short', domain], stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running dig for {domain}: {e}")
        return None

# Definir el modelo de entrada para la API REST
class DomainQuery(BaseModel):
    domain: str

# Punto de entrada para resolver el dominio
@app.get("/resolve")
def resolve_domain(domain: str):
    # Primero, buscar en la caché de Redis
    ip_address = get_from_cache(domain)

    if ip_address:
        return {"domain": domain, "ip_address": ip_address, "cache_hit": True}

    # Si no está en la caché, obtener la IP a través del servidor gRPC o dig()
    try:
        ip_address = get_ip_from_grpc(domain)
    except Exception:
        ip_address = get_ip_using_dig(domain)

    if ip_address:
        # Guardar en caché la IP resuelta
        save_to_cache(domain, ip_address)
        return {"domain": domain, "ip_address": ip_address, "cache_hit": False}
    else:
        return {"error": "Unable to resolve domain"}, 404

