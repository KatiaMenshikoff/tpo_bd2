from fastapi import APIRouter, Query
from src.queries import mongo_q, neo_q

router = APIRouter(prefix="", tags=["Consultas"])

@router.get("/q1")
def q1(limit: int = Query(100, ge=1, le=1000)):  return mongo_q.q1(limit)

@router.get("/q2")
def q2(limit: int = Query(100, ge=1, le=1000)):  return mongo_q.q2(limit)

#NEO4J QUERIES

@router.get("/q3")
def q3():  return neo_q.q3()

@router.get("/q4")
def q4():  return neo_q.q4()

@router.get("/q5")
def q5():  return neo_q.q5()

@router.get("/q11")
def q11(): return neo_q.q11()

@router.get("/q12")
def q12(): return neo_q.q12()