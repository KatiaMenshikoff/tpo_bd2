#!/usr/bin/env python3
import os, sys, csv
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:example@mongo:27017/?authSource=admin")
MONGO_DB  = os.getenv("MONGO_DB", "aseguradora_tp")
DATA_DIR  = os.path.join(os.path.dirname(__file__),  "data")
FILES = {
    "clientes":   "clientes.csv",
    "agentes":    "agentes.csv",
    "polizas":    "polizas.csv",
    "siniestros": "siniestros.csv",
    "vehiculos":  "vehiculos.csv",
}

def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def cast(coll, docs):
    def to_int(x): 
        try: return int(x) if x not in ("", None) else None
        except: return x
    def to_float(x): 
        try: return float(x) if x not in ("", None) else None
        except: return x
    for d in docs:
        if coll=="clientes":
            d["id_cliente"]=to_int(d.get("id_cliente"))
            if "activo" in d: d["activo"]=str(d["activo"]).lower() in ("1","true","t","yes","y","si","sí")
        elif coll=="agentes":
            d["id_agente"]=to_int(d.get("id_agente"))
            if "activo" in d: d["activo"]=str(d["activo"]).lower() in ("1","true","t","yes","y","si","sí")
        elif coll=="polizas":
            d["id_cliente"]=to_int(d.get("id_cliente"))
            d["id_agente"]=to_int(d.get("id_agente"))
            d["prima_mensual"]=to_float(d.get("prima_mensual"))
            d["cobertura_total"]=to_float(d.get("cobertura_total"))
        elif coll=="siniestros":
            d["id_siniestro"]=to_int(d.get("id_siniestro"))
            d["monto_estimado"]=to_float(d.get("monto_estimado"))
        elif coll=="vehiculos":
            d["id_vehiculo"]=to_int(d.get("id_vehiculo"))
            d["id_cliente"]=to_int(d.get("id_cliente"))
            d["anio"]=to_int(d.get("anio"))
            if "asegurado" in d: d["asegurado"]=str(d["asegurado"]).lower() in ("1","true","t","yes","y","si","sí")
    return docs

def main():
    drop = len(sys.argv)>1 and sys.argv[1]=="--drop"
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    if drop:
        print("Dropping colecciones...")
    total=0
    for coll, fname in FILES.items():
        path = os.path.normpath(os.path.join(DATA_DIR, fname))
        if not os.path.exists(path):
            print(f"WARN: {path} no existe, salto {coll}")
            continue
        docs = cast(coll, load_csv(path))
        if drop: db[coll].drop()
        if docs: db[coll].insert_many(docs)
        print(f"{coll}: {len(docs)} registros insertados")
        total += len(docs)
    print(f"OK total: {total}")

if __name__ == "__main__":
    main()