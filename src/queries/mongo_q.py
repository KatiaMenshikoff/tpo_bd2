from __future__ import annotations
from datetime import datetime, timedelta
from src.db.mongo import db

def q1(limit: int = 100):
    pipeline = [
        {"$match": {"activo": {"$in": [True, "True", "true"]}}},
        {"$lookup": {
            "from": "polizas",
            "let": {"cid": "$id_cliente"},
            "pipeline": [
                {"$match": {"$expr": {"$and": [
                    {"$eq": ["$id_cliente", "$$cid"]},
                    {"$eq": ["$estado", "Activa"]}
                ]}}}
            ],
            "as": "polizas_vigentes"
        }},
        {"$project": {"_id": 0, "id_cliente":1, "nombre":1, "apellido":1, "polizas_vigentes":1}},
        {"$limit": limit}
    ]
    return list(db().clientes.aggregate(pipeline))
