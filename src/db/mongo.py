from __future__ import annotations
import logging
from pymongo import MongoClient
from src.config import settings

log = logging.getLogger("db.mongo")
_client: MongoClient | None = None

def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI)
        log.info("Mongo client created")
    return _client

def db():
    return get_client()[settings.MONGO_DB]
