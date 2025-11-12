from fastapi import APIRouter, Query
from src.queries import mongo_q, neo_q

router = APIRouter(prefix="", tags=["Consultas"])

@router.get("/q1")
def q1(limit: int = Query(100, ge=1, le=1000)):  return mongo_q.q1(limit)

