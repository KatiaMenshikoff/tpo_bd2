from __future__ import annotations
from datetime import datetime, timedelta
from src.db.mongo import db

def q1(limit: int = 100, start: int = 0):
    pipeline = [
        {"$match": {"activo": {"$in": [True, "True", "true", "TRUE", 1]}}},
        {"$lookup": {
            "from": "polizas",
            "let": {"cid": "$id_cliente"},
            "pipeline": [
                {"$match": {
                    "$expr": {
                        "$and": [
                            {"$eq": [
                                {"$toInt": "$id_cliente"},
                                {"$toInt": "$$cid"}
                            ]},
                            {"$regexMatch": {
                                "input": "$estado",
                                "regex": "^activa$",
                                "options": "i"
                            }}
                        ]
                    }
                }}
            ],
            "as": "polizas_vigentes"
        }},
        {"$addFields": {"cant_polizas_vigentes": {"$size": "$polizas_vigentes"}}},
        {"$match": {"cant_polizas_vigentes": {"$gt": 0}}},
        {"$project": {
            "_id": 0,
            "id_cliente": 1, "nombre": 1, "apellido": 1,
            "cant_polizas_vigentes": 1,
            "polizas_vigentes.nro_poliza": 1,
            "polizas_vigentes.tipo": 1
        }},
        {"$sort": {"id_cliente": 1}},
        {"$skip": start},
        {"$limit": limit}
    ]
    return list(db().clientes.aggregate(pipeline))

def q2(limit: int = 100, start: int = 0):
    pipeline = [
        {"$match": {"estado": "Abierto"}},
        {"$lookup": {"from":"polizas","localField":"nro_poliza","foreignField":"nro_poliza","as":"pol"}},
        {"$unwind": "$pol"},
        {"$lookup": {"from":"clientes","localField":"pol.id_cliente","foreignField":"id_cliente","as":"cli"}},
        {"$unwind": "$cli"},
        {"$project":{"_id":0,"id_siniestro":1,"tipo":1,"monto_estimado":1,
                     "cliente":{"id":"$cli.id_cliente","nombre":"$cli.nombre","apellido":"$cli.apellido"}}},
        {"$skip": start},
        {"$limit": limit}
    ]
    return list(db().siniestros.aggregate(pipeline))

def q6(limit: int = 100, start: int = 0):
    pipeline = [
        {"$match": {"estado": "Vencida"}},
        {"$lookup": {"from":"clientes","localField":"id_cliente","foreignField":"id_cliente","as":"cli"}},
        {"$unwind": "$cli"},
        {"$project":{"_id":0,"nro_poliza":1,"estado":1,
                     "cliente":{"id":"$cli.id_cliente","nombre":"$cli.nombre","apellido":"$cli.apellido"}}},
        {"$skip": start},
        {"$limit": limit}
    ]
    return list(db().polizas.aggregate(pipeline))

def q7():
    pipeline = [
        {"$match": {"estado": "Activa"}},
        {"$group": {"_id":"$id_cliente","cobertura_total":{"$sum":{"$toDouble":"$cobertura_total"}}}},
        {"$sort": {"cobertura_total": -1}},
        {"$limit": 10},
        {"$lookup":{"from":"clientes","localField":"_id","foreignField":"id_cliente","as":"cli"}},
        {"$unwind":"$cli"},
        {"$project":{"_id":0,"id_cliente":"$cli.id_cliente","cliente":"$cli.nombre","apellido":"$cli.apellido","cobertura_total":1}}
    ]
    return list(db().polizas.aggregate(pipeline))

def q8():
    hace_un_anio = datetime.now() - timedelta(days=365)
    pipeline = [
        {"$match": {"tipo": "Accidente"}},
        {"$addFields": {"fecha_dt":{"$dateFromString":{"dateString":"$fecha","format":"%d/%m/%Y"}}}},
        {"$match": {"fecha_dt": {"$gte": hace_un_anio}}},
        {"$project": {"_id":0, "id_siniestro":1, "fecha":"$fecha_dt", "nro_poliza":1, "monto_estimado":1}}
    ]
    return list(db().siniestros.aggregate(pipeline))

def q9(limit: int = 100, start: int = 0):
    pipeline = [
        {"$match":{"estado":"Activa"}},
        {"$addFields":{"fi":{"$dateFromString":{"dateString":"$fecha_inicio","format":"%d/%m/%Y"}}}},
        {"$sort":{"fi":1}},
        {"$project":{"_id":0,"nro_poliza":1,"fecha_inicio":"$fi"}},
        {"$skip": start},
        {"$limit": limit}
    ]
    return list(db().polizas.aggregate(pipeline))

def q10(limit: int = 100, start: int = 0):
    pipeline = [
        {"$match":{"estado":"Suspendida"}},
        {"$lookup":{"from":"clientes","localField":"id_cliente","foreignField":"id_cliente","as":"cli"}},
        {"$unwind":"$cli"},
        {"$project":{"_id":0,"nro_poliza":1,"estado_poliza":"$estado","cliente_activo":"$cli.activo"}},
        {"$skip": start},
        {"$limit": limit}
    ]
    return list(db().polizas.aggregate(pipeline))