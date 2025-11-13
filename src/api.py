#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from src.logging_conf import configure_logging
from src.routes import clients_router, policies_router, claims_router, queries_router, import_data_router
from src.db.mongo import db

configure_logging()
app = FastAPI(
    title="API Aseguradoras",
    description="Backoffice (Mongo SoR + Neo4j) – Consultas q1–q12 y Servicios s13–s15",
    version="1.0.0",
)

app.include_router(clients_router)
app.include_router(policies_router)
app.include_router(claims_router)
app.include_router(queries_router)
app.include_router(import_data_router)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
