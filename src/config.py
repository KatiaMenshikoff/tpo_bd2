from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    # Mongo
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://root:example@mongo:27017/?authSource=admin")
    MONGO_DB: str = os.getenv("MONGO_DB", "aseguradora_tp")
    # Neo4j
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "test")
    SYNC_IMMEDIATE_TO_NEO: bool = os.getenv("SYNC_IMMEDIATE_TO_NEO", "0").lower() in ("1","true","yes")

settings = Settings()
