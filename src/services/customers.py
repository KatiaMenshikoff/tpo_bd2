from __future__ import annotations
from typing import Any, Dict, List
from src.db.mongo import db

def list_clients() -> List[Dict[str, Any]]:
    return list(db().clientes.find({}, {"_id": 0}))

def create_client(doc: Dict[str, Any]) -> Dict[str, Any]:
    db().clientes.insert_one(doc)
    return {"ok": True}

def update_client(id_cliente: int, patch: Dict[str, Any]) -> Dict[str, Any]:
    db().clientes.update_one({"id_cliente": id_cliente}, {"$set": patch})
    return {"ok": True}

def delete_client(id_cliente: int) -> Dict[str, Any]:
    db().clientes.delete_one({"id_cliente": id_cliente})
    return {"ok": True}
