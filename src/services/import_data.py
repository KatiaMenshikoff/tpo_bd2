from __future__ import annotations
from typing import Any, Dict, List
import os, csv
from src.db.mongo import db

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FILES = {
    "clientes": "clientes.csv",
    "agentes": "agentes.csv",
    "polizas": "polizas.csv",
    "siniestros": "siniestros.csv",
    "vehiculos": "vehiculos.csv",
}

def load_csv(path: str) -> List[Dict[str, Any]]:
    """Carga un archivo CSV y retorna una lista de diccionarios."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def cast(coll: str, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convierte los tipos de datos según la colección."""
    def to_int(x):
        try:
            return int(x) if x not in ("", None) else None
        except:
            return x

    def to_float(x):
        try:
            return float(x) if x not in ("", None) else None
        except:
            return x

    for d in docs:
        if coll == "clientes":
            d["id_cliente"] = to_int(d.get("id_cliente"))
            if "activo" in d:
                d["activo"] = str(d["activo"]).lower() in ("1", "true", "t", "yes", "y", "si", "sí")
        elif coll == "agentes":
            d["id_agente"] = to_int(d.get("id_agente"))
            if "activo" in d:
                d["activo"] = str(d["activo"]).lower() in ("1", "true", "t", "yes", "y", "si", "sí")
        elif coll == "polizas":
            d["id_cliente"] = to_int(d.get("id_cliente"))
            d["id_agente"] = to_int(d.get("id_agente"))
            d["prima_mensual"] = to_float(d.get("prima_mensual"))
            d["cobertura_total"] = to_float(d.get("cobertura_total"))
        elif coll == "siniestros":
            d["id_siniestro"] = to_int(d.get("id_siniestro"))
            d["monto_estimado"] = to_float(d.get("monto_estimado"))
        elif coll == "vehiculos":
            d["id_vehiculo"] = to_int(d.get("id_vehiculo"))
            d["id_cliente"] = to_int(d.get("id_cliente"))
            d["anio"] = to_int(d.get("anio"))
            if "asegurado" in d:
                d["asegurado"] = str(d["asegurado"]).lower() in ("1", "true", "t", "yes", "y", "si", "sí")
    return docs

def import_data() -> Dict[str, Any]:
    """
    Importa datos desde archivos CSV a MongoDB usando upsert.
    Retorna un diccionario con el resultado de la importación.
    """
    # Campos únicos para cada colección (usados como filtro en upsert)
    UNIQUE_FIELDS = {
        "clientes": "id_cliente",
        "agentes": "id_agente",
        "polizas": "nro_poliza",
        "siniestros": "id_siniestro",
        "vehiculos": "id_vehiculo",
    }

    results = {}
    total = 0
    warnings = []

    for coll, fname in FILES.items():
        path = os.path.normpath(os.path.join(DATA_DIR, fname))
        if not os.path.exists(path):
            warnings.append(f"{path} no existe, salto {coll}")
            results[coll] = {"procesados": 0, "error": "archivo no encontrado"}
            continue

        try:
            docs = cast(coll, load_csv(path))
            if docs:
                unique_field = UNIQUE_FIELDS[coll]
                for doc in docs:
                    filter_dict = {unique_field: doc[unique_field]}
                    db()[coll].update_one(filter_dict, {"$set": doc}, upsert=True)
            results[coll] = {"procesados": len(docs)}
            total += len(docs)
        except Exception as e:
            results[coll] = {"procesados": 0, "error": str(e)}
            warnings.append(f"Error en {coll}: {str(e)}")

    return {
        "ok": True,
        "total": total,
        "resultados": results,
        "warnings": warnings if warnings else None,
    }
