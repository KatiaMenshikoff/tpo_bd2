from fastapi import APIRouter, HTTPException
from src.services import import_data as import_data_service
from src.services import mongo_to_neo as sync_service

router = APIRouter(prefix="/import", tags=["Importación"])

@router.post("/data")
def importar_datos():
    """
    Importa datos desde archivos CSV a MongoDB. Usa upsert para actualizar existentes e insertar nuevos.
    Luego sincroniza los datos desde MongoDB a Neo4j.
    Los archivos CSV a importar deben estar en el directorio src/data/ del proyecto.
    Si este directorio no existe, por favor crearlo y colocar los archivos CSV dentro de él.
    Se puede importar datos para clientes, agentes, polizas, siniestros y vehiculos.
    Los archivos CSV deben tener los siguientes campos para cada colección:
    - clientes: id_cliente, nombre, apellido, dni, email, telefono, direccion, ciudad, provincia, activo
    - agentes: id_agente, nombre, apellido, matricula, telefono, email, zona, activo
    - polizas: nro_poliza, id_cliente, id_agente, prima_mensual, cobertura_total
    - siniestros: id_siniestro, tipo, fecha, estado, nro_poliza
    - vehiculos: id_vehiculo, id_cliente, anio, asegurado

    Retorna un diccionario con el resultado de la importación y sincronización.
    """
    try:
        result_mongo = import_data_service.import_data()
        result_neo = sync_service.sync_mongo_to_neo()
        if not result_mongo.get("ok", False) or not result_neo.get("ok", False):
            raise HTTPException(status_code=500, detail="Error en importación o sincronización")
        return {
            "mongo_import": result_mongo,
            "neo_sync": result_neo,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en importación o sincronización: {str(e)}")

@router.post("/sync")
def sincronizar_mongo_a_neo():
    """
    Sincroniza datos desde MongoDB a Neo4j.
    Crea nodos para clientes, agentes, polizas, siniestros y vehiculos,
    y establece las relaciones entre ellos en Neo4j.
    """
    try:
        result = sync_service.sync_mongo_to_neo()
        if not result.get("ok", False):
            raise HTTPException(status_code=500, detail=result.get("error", "Error desconocido en sincronización"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en sincronización: {str(e)}")

