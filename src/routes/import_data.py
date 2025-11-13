from fastapi import APIRouter, HTTPException
from src.services import import_data as import_data_service

router = APIRouter(prefix="/import", tags=["Importación"])

@router.post("/data")
def importar_datos():
    """
    Importa datos desde archivos CSV a MongoDB.
    Usa upsert para actualizar existentes e insertar nuevos.
    """
    try:
        result = import_data_service.import_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en importación: {str(e)}")

