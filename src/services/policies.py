from __future__ import annotations
from typing import Dict, Any
from src.db.mongo import db

def _is_true(x) -> bool:
    return str(x).lower() in ("1","true","t","yes","y","si","sí")

def issue_policy(doc: Dict[str, Any]) -> Dict[str, Any]:
    cli = db().clientes.find_one({"id_cliente": doc["id_cliente"]})
    if not cli or not _is_true(cli.get("activo", True)):
        raise ValueError("Cliente inexistente o inactivo")
    ag = db().agentes.find_one({"id_agente": doc["id_agente"]})
    if not ag or not _is_true(ag.get("activo", True)):
        raise ValueError("Agente inexistente o inactivo")
    if db().polizas.find_one({"nro_poliza": doc["nro_poliza"]}):
        raise ValueError("nro_poliza ya existe")
    db().polizas.insert_one(doc)
    return {"ok": True}
