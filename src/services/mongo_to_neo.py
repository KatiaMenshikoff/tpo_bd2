from __future__ import annotations
from typing import Any, Dict
from src.db.mongo import db
from src.db.neo import get_driver

CREATE_CLIENT = "MERGE (c:Cliente {id: $id}) SET c += $props"
CREATE_AGENT  = "MERGE (a:Agente {id: $id}) SET a += $props"
CREATE_POLICY = "MERGE (p:Poliza {nro: $nro}) SET p += $props"
CREATE_CLAIM  = "MERGE (s:Siniestro {id: $id}) SET s += $props"
CREATE_VEHICLE= "MERGE (v:Vehiculo {id: $id}) SET v += $props"

REL_CLIENT_POLICY = "MATCH (c:Cliente {id: $id_cliente}), (p:Poliza {nro: $nro_poliza}) MERGE (c)-[:TIENE]->(p)"
REL_AGENT_POLICY  = "MATCH (a:Agente {id: $id_agente}), (p:Poliza {nro: $nro_poliza}) MERGE (a)-[:ASIGNADO_A]->(p)"
REL_POLICY_CLAIM  = "MATCH (p:Poliza {nro: $nro_poliza}), (s:Siniestro {id: $id_siniestro}) MERGE (p)-[:TIENE_SINIESTRO]->(s)"
REL_VEHICLE_CLIENT= "MATCH (v:Vehiculo {id: $id_vehiculo}), (c:Cliente {id: $id_cliente}) MERGE (v)-[:DE]->(c)"

def run_tx(query: str, **params):
    """Ejecuta una transacción en Neo4j."""
    with get_driver().session() as s:
        s.run(query, **params)

def sync_mongo_to_neo() -> Dict[str, Any]:
    """
    Sincroniza datos desde MongoDB a Neo4j.
    Crea nodos para clientes, agentes, polizas, siniestros y vehiculos,
    y establece las relaciones entre ellos.
    Retorna un diccionario con el resultado de la sincronización.
    """
    results = {
        "nodos": {},
        "relaciones": {},
    }
    total_nodos = 0
    total_relaciones = 0
    warnings = []

    try:
        # Nodos - Clientes
        clientes_count = 0
        for doc in db().clientes.find({}):
            try:
                run_tx(CREATE_CLIENT, id=int(doc["id_cliente"]), props={
                    "nombre": doc.get("nombre"),
                    "apellido": doc.get("apellido"),
                    "dni": doc.get("dni"),
                    "email": doc.get("email"),
                    "telefono": doc.get("telefono"),
                    "direccion": doc.get("direccion"),
                    "ciudad": doc.get("ciudad"),
                    "provincia": doc.get("provincia"),
                    "activo": str(doc.get("activo")).lower() in ("true", "1", "yes", "si", "sí")
                })
                clientes_count += 1
            except Exception as e:
                warnings.append(f"Error creando cliente {doc.get('id_cliente')}: {str(e)}")
        results["nodos"]["clientes"] = clientes_count
        total_nodos += clientes_count

        # Nodos - Agentes
        agentes_count = 0
        for doc in db().agentes.find({}):
            try:
                run_tx(CREATE_AGENT, id=int(doc["id_agente"]), props={
                    "nombre": doc.get("nombre"),
                    "apellido": doc.get("apellido"),
                    "matricula": doc.get("matricula"),
                    "telefono": doc.get("telefono"),
                    "email": doc.get("email"),
                    "zona": doc.get("zona"),
                    "activo": str(doc.get("activo")).lower() in ("true", "1", "yes", "si", "sí")
                })
                agentes_count += 1
            except Exception as e:
                warnings.append(f"Error creando agente {doc.get('id_agente')}: {str(e)}")
        results["nodos"]["agentes"] = agentes_count
        total_nodos += agentes_count

        # Nodos - Polizas
        polizas_count = 0
        for doc in db().polizas.find({}):
            try:
                run_tx(CREATE_POLICY, nro=doc["nro_poliza"], props={
                    "tipo": doc.get("tipo"),
                    "fecha_inicio": doc.get("fecha_inicio"),
                    "fecha_fin": doc.get("fecha_fin"),
                    "prima_mensual": float(doc["prima_mensual"]) if doc.get("prima_mensual") not in ("", None) else None,
                    "cobertura_total": float(doc["cobertura_total"]) if doc.get("cobertura_total") not in ("", None) else None,
                    "estado": doc.get("estado")
                })
                polizas_count += 1
            except Exception as e:
                warnings.append(f"Error creando poliza {doc.get('nro_poliza')}: {str(e)}")
        results["nodos"]["polizas"] = polizas_count
        total_nodos += polizas_count

        # Nodos - Siniestros
        siniestros_count = 0
        for doc in db().siniestros.find({}):
            try:
                run_tx(CREATE_CLAIM, id=int(doc["id_siniestro"]), props={
                    "nro_poliza": doc.get("nro_poliza"),
                    "fecha": doc.get("fecha"),
                    "tipo": doc.get("tipo"),
                    "monto_estimado": float(doc["monto_estimado"]) if doc.get("monto_estimado") not in ("", None) else None,
                    "descripcion": doc.get("descripcion"),
                    "estado": doc.get("estado")
                })
                siniestros_count += 1
            except Exception as e:
                warnings.append(f"Error creando siniestro {doc.get('id_siniestro')}: {str(e)}")
        results["nodos"]["siniestros"] = siniestros_count
        total_nodos += siniestros_count

        # Nodos - Vehiculos
        vehiculos_count = 0
        for doc in db().vehiculos.find({}):
            try:
                run_tx(CREATE_VEHICLE, id=int(doc["id_vehiculo"]), props={
                    "id_cliente": int(doc["id_cliente"]) if doc.get("id_cliente") not in ("", None) else None,
                    "marca": doc.get("marca"),
                    "modelo": doc.get("modelo"),
                    "anio": int(doc["anio"]) if doc.get("anio") not in ("", None) else None,
                    "patente": doc.get("patente"),
                    "nro_chasis": doc.get("nro_chasis"),
                    "asegurado": str(doc.get("asegurado")).lower() in ("true", "1", "yes", "si", "sí")
                })
                vehiculos_count += 1
            except Exception as e:
                warnings.append(f"Error creando vehiculo {doc.get('id_vehiculo')}: {str(e)}")
        results["nodos"]["vehiculos"] = vehiculos_count
        total_nodos += vehiculos_count

        # Relaciones - Cliente -> Poliza
        rel_cliente_poliza = 0
        for p in db().polizas.find({}):
            if p.get("id_cliente") not in ("", None):
                try:
                    run_tx(REL_CLIENT_POLICY, id_cliente=int(p["id_cliente"]), nro_poliza=p["nro_poliza"])
                    rel_cliente_poliza += 1
                except Exception as e:
                    warnings.append(f"Error creando relación Cliente-Poliza para poliza {p.get('nro_poliza')}: {str(e)}")
        results["relaciones"]["cliente_poliza"] = rel_cliente_poliza
        total_relaciones += rel_cliente_poliza

        # Relaciones - Agente -> Poliza
        rel_agente_poliza = 0
        for p in db().polizas.find({}):
            if p.get("id_agente") not in ("", None):
                try:
                    run_tx(REL_AGENT_POLICY, id_agente=int(p["id_agente"]), nro_poliza=p["nro_poliza"])
                    rel_agente_poliza += 1
                except Exception as e:
                    warnings.append(f"Error creando relación Agente-Poliza para poliza {p.get('nro_poliza')}: {str(e)}")
        results["relaciones"]["agente_poliza"] = rel_agente_poliza
        total_relaciones += rel_agente_poliza

        # Relaciones - Poliza -> Siniestro
        rel_poliza_siniestro = 0
        for s in db().siniestros.find({}):
            try:
                run_tx(REL_POLICY_CLAIM, id_siniestro=int(s["id_siniestro"]), nro_poliza=s["nro_poliza"])
                rel_poliza_siniestro += 1
            except Exception as e:
                warnings.append(f"Error creando relación Poliza-Siniestro para siniestro {s.get('id_siniestro')}: {str(e)}")
        results["relaciones"]["poliza_siniestro"] = rel_poliza_siniestro
        total_relaciones += rel_poliza_siniestro

        # Relaciones - Vehiculo -> Cliente
        rel_vehiculo_cliente = 0
        for v in db().vehiculos.find({}):
            if v.get("id_cliente") not in ("", None):
                try:
                    run_tx(REL_VEHICLE_CLIENT, id_vehiculo=int(v["id_vehiculo"]), id_cliente=int(v["id_cliente"]))
                    rel_vehiculo_cliente += 1
                except Exception as e:
                    warnings.append(f"Error creando relación Vehiculo-Cliente para vehiculo {v.get('id_vehiculo')}: {str(e)}")
        results["relaciones"]["vehiculo_cliente"] = rel_vehiculo_cliente
        total_relaciones += rel_vehiculo_cliente

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "nodos": results["nodos"],
            "relaciones": results["relaciones"],
            "warnings": warnings if warnings else None,
        }

    return {
        "ok": True,
        "total_nodos": total_nodos,
        "total_relaciones": total_relaciones,
        "nodos": results["nodos"],
        "relaciones": results["relaciones"],
        "warnings": warnings if warnings else None,
    }
