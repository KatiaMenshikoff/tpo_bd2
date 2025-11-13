from fastapi import APIRouter, Query
from src.queries import mongo_q, neo_q

router = APIRouter(prefix="", tags=["Consultas"])

@router.get("/q1")
def q1(limit: int = Query(100, ge=1, le=1000), start: int = Query(0, ge=0)):  return mongo_q.q1(limit, start)

@router.get("/q2")
def q2(limit: int = Query(100, ge=1, le=1000), start: int = Query(0, ge=0)):  return mongo_q.q2(limit, start)

@router.get("/q6")
def q6(limit: int = Query(100, ge=1, le=1000), start: int = Query(0, ge=0)):  return mongo_q.q6(limit, start)

@router.get("/q7")
def q7():  return mongo_q.q7()

@router.get("/q8")
def q8():  return mongo_q.q8()

@router.get("/q9")
def q9(limit: int = Query(100, ge=1, le=1000), start: int = Query(0, ge=0)):  return mongo_q.q9(limit, start)

@router.get("/q10")
def q10(limit: int = Query(100, ge=1, le=1000), start: int = Query(0, ge=0)):  return mongo_q.q10(limit, start)

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

