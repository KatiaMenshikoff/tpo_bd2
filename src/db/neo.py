from __future__ import annotations
import logging
from neo4j import GraphDatabase, Driver
from src.config import settings

log = logging.getLogger("db.neo")
_driver: Driver | None = None

def get_driver() -> Driver:
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(settings.NEO4J_URI, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
        log.info("Neo4j driver created")
    return _driver

def run(query: str, **params):
    with get_driver().session() as s:
        return [r.data() for r in s.run(query, **params)]
