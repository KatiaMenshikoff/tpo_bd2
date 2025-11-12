#!/usr/bin/env python3
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4jpassword")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

CONSTRAINTS = [
    "CREATE CONSTRAINT cliente_id IF NOT EXISTS FOR (c:Cliente) REQUIRE c.id IS UNIQUE",
    "CREATE CONSTRAINT poliza_nro IF NOT EXISTS FOR (p:Poliza) REQUIRE p.nro IS UNIQUE",
    "CREATE CONSTRAINT siniestro_id IF NOT EXISTS FOR (s:Siniestro) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT vehiculo_id IF NOT EXISTS FOR (v:Vehiculo) REQUIRE v.id IS UNIQUE",
    "CREATE CONSTRAINT agente_id IF NOT EXISTS FOR (a:Agente) REQUIRE a.id IS UNIQUE",
]

if __name__ == "__main__":
    with driver.session() as s:
        for q in CONSTRAINTS:
            s.run(q)
    print("Neo4j constraints OK")