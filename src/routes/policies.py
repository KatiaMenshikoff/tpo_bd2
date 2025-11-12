from fastapi import APIRouter, HTTPException
from src.schemas import PolizaIn
from src.services import policies

router = APIRouter(prefix="/polizas", tags=["Pólizas"])

@router.post("")
def emitir_poliza(poliza: PolizaIn):
    try:
        return policies.issue_policy(poliza.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
