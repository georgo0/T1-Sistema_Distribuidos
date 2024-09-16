# Tarea 1 - Sistema Distribuidos
En este repositorio se encuentran todos los códigos implementados para  levantar el sistema de cache solicitado en la tarea 

Integrantes:
* Cristobal Barra
* Jorge Gallegos
  

## Stack de tecnologías usado

[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=flat)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=flat)](https://www.python.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white&style=flat)](https://redis.io/)

## Instrucciones de uso

En la terminal utilizar los siguientes comandos:

```bash
 git clone https://github.com/georgo0/T1-Sistema_Distribuidos
```
Desde la carpeta T1_Sistema_Distribuidos, levantar los contenedores y arrancar la API
```bash
docker compose up -d
```
```bash
uvicorn app:app --reload
```
Ejemplos de uso:
```bash
 python traffic_generator.py
```
```bash
 python test_requests.py
```
