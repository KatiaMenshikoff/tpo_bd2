from fastapi import APIRouter, Query
from src.queries import mongo_q, neo_q

router = APIRouter(prefix="", tags=["Consultas"])

@router.get("/q1")
def q1_clientes_activos_con_sus_polizas_vigentes(limit: int = Query(100, ge=1, le=1000), start: int = Query(0, ge=0)):
    """
    Clientes activos con sus pólizas vigentes
    """
    return mongo_q.q1(limit, start)

@router.get("/q2")
def q2_siniestros_abiertos_con_tipo_monto_y_cliente_afectado(limit: int = Query(100, ge=1, le=1000), start: int = Query(0, ge=0)):
    """
    Siniestros abiertos con tipo, monto y cliente afectado
    """
    return mongo_q.q2(limit, start)

@router.get("/q6")
def q6_polizas_vencidas_con_el_nombre_del_cliente(limit: int = Query(100, ge=1, le=1000), start: int = Query(0, ge=0)):
    """
    Pólizas vencidas con el nombre del cliente
    """
    return mongo_q.q6(limit, start)

@router.get("/q7")
def q7_top_10_clientes_por_cobertura_total():
    """
    Top 10 clientes por cobertura total
    """
    return mongo_q.q7()

@router.get("/q8")
def q8_siniestros_tipo_accidente_del_ultimo_ano():
    """
    Siniestros tipo “Accidente” del último año
    """
    return mongo_q.q8()

@router.get("/q9")
def q9_vista_polizas_activas_ordenadas_por_fecha_inicio(limit: int = Query(100, ge=1, le=1000), start: int = Query(0, ge=0)):
    """
    Vista de pólizas activas ordenadas por fecha de inicio
    """
    return mongo_q.q9(limit, start)

@router.get("/q10")
def q10_polizas_suspendidas_con_estado_del_cliente(limit: int = Query(100, ge=1, le=1000), start: int = Query(0, ge=0)):
    """
    Pólizas suspendidas con estado del cliente
    """
    return mongo_q.q10(limit, start)

#NEO4J QUERIES

@router.get("/q3")
def q3_vehiculos_asegurados_con_su_cliente_y_poliza():
    """
    Vehículos asegurados con su cliente y póliza
    """
    return neo_q.q3()

@router.get("/q4")
def q4_clientes_sin_polizas_activas():
    """
    Clientes sin pólizas activas
    """
    return neo_q.q4()

@router.get("/q5")
def q5_agentes_activos_con_cantidad_de_polizas_asignadas():
    """
    Agentes activos con cantidad de pólizas asignadas
    """
    return neo_q.q5()

@router.get("/q11")
def q11_clientes_con_mas_de_un_vehiculo_asegurado():
    """
    Clientes con más de un vehículo asegurado
    """
    return neo_q.q11()

@router.get("/q12")
def q12_agentes_y_cantidad_de_siniestros_asociados():
    """
    Agentes y cantidad de siniestros asociados
    """
    return neo_q.q12()

