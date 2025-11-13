from __future__ import annotations
from src.db.neo import run

def q3():
    q = (
        "MATCH (v:Vehiculo {asegurado:true})-[:DE]->(c:Cliente)-[:TIENE]->(p:Poliza {estado:'Activa'})\n"
        "RETURN v.id AS id_vehiculo, v.marca AS marca, v.modelo AS modelo, c.id AS id_cliente, c.nombre AS nombre, c.apellido AS apellido, p.nro AS nro_poliza"
    )
    return run(q)

def q4():
    q = (
        "MATCH (c:Cliente {activo:true})\n"
        "WHERE NOT (c)-[:TIENE]->(:Poliza {estado:'Activa'})\n"
        "RETURN c.id AS id_cliente, c.nombre AS nombre, c.apellido AS apellido"
    )
    return run(q)

def q5():
    q = (
        "MATCH (a:Agente {activo:true})-[:ASIGNADO_A]->(p:Poliza)\n"
        "RETURN a.id AS id_agente, a.nombre AS nombre, COUNT(p) AS polizas\n"
        "ORDER BY polizas DESC"
    )
    return run(q)

def q11():
    q = (
        "MATCH (c:Cliente)<-[:DE]-(v:Vehiculo {asegurado:true})\n"
        "WITH c, COUNT(v) AS n\n"
        "WHERE n > 1\n"
        "RETURN c.id AS id_cliente, n"
    )
    return run(q)

def q12():
    q = (
        "MATCH (a:Agente)-[:ASIGNADO_A]->(:Poliza)-[:TIENE_SINIESTRO]->(s:Siniestro)\n"
        "RETURN a.id AS id_agente, COUNT(s) AS siniestros\n"
        "ORDER BY siniestros DESC"
    )
    return run(q)
