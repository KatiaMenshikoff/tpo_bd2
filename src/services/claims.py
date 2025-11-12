from __future__ import annotations
from typing import Dict, Any
from src.db.mongo import db

def create_claim(doc: Dict[str, Any]) -> Dict[str, Any]:
    pol = db().polizas.find_one({"nro_poliza": doc["nro_poliza"]})
    if not pol:
        raise ValueError("Póliza no existe")
    db().siniestros.insert_one(doc)
    return {"ok": True}
