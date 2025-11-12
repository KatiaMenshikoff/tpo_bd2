#!/usr/bin/env python3
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@mongo:27017/?authSource=admin")
MONGO_DB  = os.getenv("MONGO_DB", "aseguradora_tp")
db = MongoClient(MONGO_URI)[MONGO_DB]

def ensure_indexes():
    # CLIENTES
    db.clientes.create_index([("id_cliente", 1)], unique=True, sparse=True)
    db.clientes.create_index([("dni", 1)], unique=True, sparse=True)
    db.clientes.create_index([("email", 1)], unique=True, sparse=True)
    db.clientes.create_index([("activo", 1)])
    # AGENTES
    db.agentes.create_index([("id_agente", 1)], unique=True)
    db.agentes.create_index([("activo", 1)])
    # POLIZAS
    db.polizas.create_index([("nro_poliza", 1)], unique=True)
    db.polizas.create_index([("id_cliente", 1), ("estado", 1)])
    db.polizas.create_index([("estado", 1), ("fecha_inicio", 1)])
    db.polizas.create_index([("id_agente", 1)])
    # SINIESTROS
    db.siniestros.create_index([("id_siniestro", 1)], unique=True)
    db.siniestros.create_index([("tipo", 1), ("fecha", 1)])
    db.siniestros.create_index([("estado", 1)])
    db.siniestros.create_index([("nro_poliza", 1)])
    # VEHICULOS
    db.vehiculos.create_index([("id_vehiculo", 1)], unique=True)
    db.vehiculos.create_index([("id_cliente", 1), ("asegurado", 1)])

if __name__ == "__main__":
    ensure_indexes()
    print("MongoDB índices OK")