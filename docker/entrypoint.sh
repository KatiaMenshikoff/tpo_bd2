#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] Esperando a Mongo y Neo4j..."

# wait for Mongo
python - <<'PY'
import os, time
from pymongo import MongoClient, errors
uri = os.getenv("MONGO_URI", "mongodb://root:example@mongo:27017/?authSource=admin")
deadline = time.time()+120
while True:
    try:
        MongoClient(uri).admin.command("ping")
        print("[entrypoint] Mongo OK")
        break
    except errors.PyMongoError as e:
        if time.time() > deadline:
            raise
        time.sleep(2)
PY

# wait for Neo4j
python - <<'PY'
import os, time
from neo4j import GraphDatabase
uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
user = os.getenv("NEO4J_USER", "neo4j")
pwd  = os.getenv("NEO4J_PASSWORD", "neo4jpassword")
deadline = time.time()+120
while True:
    try:
        with GraphDatabase.driver(uri, auth=(user,pwd)) as d:
            with d.session() as s:
                s.run("RETURN 1").consume()
        print("[entrypoint] Neo4j OK")
        break
    except Exception as e:
        if time.time() > deadline:
            raise
        time.sleep(2)
PY

# Crear índices en Mongo y constraints en Neo4j (vía Python)
echo "[entrypoint] Creando índices/constraints..."
python src/create_indexes.py
python src/neo4j_setup.py

# Sync Mongo -> Neo4j
echo "[entrypoint] Sincronizando Mongo -> Neo4j..."
python src/sync/mongo_to_neo.py || true

# Iniciar API FastAPI (Uvicorn)
echo "[entrypoint] Iniciando API en :8000 ..."
exec uvicorn src.api:app --host 0.0.0.0 --port 8000

# Mantener el contenedor vivo si no hay API
tail -f /dev/null