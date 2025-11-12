#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from neo4j import GraphDatabase

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "aseguradora_tp")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

CREATE_CLIENT = "MERGE (c:Cliente {id: $id}) SET c += $props"
CREATE_AGENT  = "MERGE (a:Agente {id: $id}) SET a += $props"
CREATE_POLICY = "MERGE (p:Poliza {nro: $nro}) SET p += $props"
CREATE_CLAIM  = "MERGE (s:Siniestro {id: $id}) SET s += $props"
CREATE_VEHICLE= "MERGE (v:Vehiculo {id: $id}) SET v += $props"

REL_CLIENT_POLICY = "MATCH (c:Cliente {id: $id_cliente}), (p:Poliza {nro: $nro_poliza}) MERGE (c)-[:TIENE]->(p)"
REL_AGENT_POLICY  = "MATCH (a:Agente {id: $id_agente}), (p:Poliza {nro: $nro_poliza}) MERGE (a)-[:ASIGNADO_A]->(p)"
REL_POLICY_CLAIM  = "MATCH (p:Poliza {nro: $nro_poliza}), (s:Siniestro {id: $id_siniestro}) MERGE (p)-[:TIENE_SINIESTRO]->(s)"
REL_VEHICLE_CLIENT= "MATCH (v:Vehiculo {id: $id_vehiculo}), (c:Cliente {id: $id_cliente}) MERGE (v)-[:DE]->(c)"

def run_tx(query, **params):
    with driver.session() as s:
        s.run(query, **params)

# Nodos
for doc in db.clientes.find({}):
    run_tx(CREATE_CLIENT, id=int(doc["id_cliente"]), props={
        "nombre":doc.get("nombre"),"apellido":doc.get("apellido"),
        "dni":doc.get("dni"),"email":doc.get("email"),"telefono":doc.get("telefono"),
        "direccion":doc.get("direccion"),"ciudad":doc.get("ciudad"),"provincia":doc.get("provincia"),
        "activo": str(doc.get("activo")).lower() in ("true","1","yes","si","sí")
    })

for doc in db.agentes.find({}):
    run_tx(CREATE_AGENT, id=int(doc["id_agente"]), props={
        "nombre":doc.get("nombre"),"apellido":doc.get("apellido"),
        "matricula":doc.get("matricula"),"telefono":doc.get("telefono"),
        "email":doc.get("email"),"zona":doc.get("zona"),
        "activo": str(doc.get("activo")).lower() in ("true","1","yes","si","sí")
    })

for doc in db.polizas.find({}):
    run_tx(CREATE_POLICY, nro=doc["nro_poliza"], props={
        "tipo":doc.get("tipo"),"fecha_inicio":doc.get("fecha_inicio"),"fecha_fin":doc.get("fecha_fin"),
        "prima_mensual": float(doc["prima_mensual"]) if doc.get("prima_mensual") not in ("",None) else None,
        "cobertura_total": float(doc["cobertura_total"]) if doc.get("cobertura_total") not in ("",None) else None,
        "estado":doc.get("estado")
    })

for doc in db.siniestros.find({}):
    run_tx(CREATE_CLAIM, id=int(doc["id_siniestro"]), props={
        "nro_poliza":doc.get("nro_poliza"),"fecha":doc.get("fecha"),"tipo":doc.get("tipo"),
        "monto_estimado": float(doc["monto_estimado"]) if doc.get("monto_estimado") not in ("",None) else None,
        "descripcion":doc.get("descripcion"),"estado":doc.get("estado")
    })

for doc in db.vehiculos.find({}):
    run_tx(CREATE_VEHICLE, id=int(doc["id_vehiculo"]), props={
        "id_cliente": int(doc["id_cliente"]) if doc.get("id_cliente") not in ("",None) else None,
        "marca":doc.get("marca"),"modelo":doc.get("modelo"),
        "anio": int(doc["anio"]) if doc.get("anio") not in ("",None) else None,
        "patente":doc.get("patente"),"nro_chasis":doc.get("nro_chasis"),
        "asegurado": str(doc.get("asegurado")).lower() in ("true","1","yes","si","sí")
    })

# Relaciones
for p in db.polizas.find({}):
    if p.get("id_cliente") not in ("",None):
        run_tx(REL_CLIENT_POLICY, id_cliente=int(p["id_cliente"]), nro_poliza=p["nro_poliza"])
    if p.get("id_agente") not in ("",None):
        run_tx(REL_AGENT_POLICY, id_agente=int(p["id_agente"]), nro_poliza=p["nro_poliza"])

for s in db.siniestros.find({}):
    run_tx(REL_POLICY_CLAIM, id_siniestro=int(s["id_siniestro"]), nro_poliza=s["nro_poliza"])

for v in db.vehiculos.find({}):
    if v.get("id_cliente") not in ("",None):
        run_tx(REL_VEHICLE_CLIENT, id_vehiculo=int(v["id_vehiculo"]), id_cliente=int(v["id_cliente"]))

print("Sync Mongo → Neo4j OK")