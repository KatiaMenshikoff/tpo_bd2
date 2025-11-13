from fastapi import APIRouter, HTTPException
from src.schemas import SiniestroIn
from src.services import claims

router = APIRouter(prefix="/siniestros", tags=["Siniestros"])

@router.post("")
def alta_siniestro(siniestro: SiniestroIn):
    """
    Crea un nuevo siniestro.
    """
    try:
        return claims.create_claim(siniestro.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
