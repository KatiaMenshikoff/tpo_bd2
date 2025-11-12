from fastapi import APIRouter, HTTPException
from src.schemas import ClienteIn, ClientePatch
from src.services import customers

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("")
def list_clientes():
    return customers.list_clients()

@router.post("")
def crear_cliente(cliente: ClienteIn):
    try:
        return customers.create_client(cliente.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{id_cliente}")
def actualizar_cliente(id_cliente: int, patch: ClientePatch):
    try:
        body = {k: v for k, v in patch.dict().items() if v is not None}
        return customers.update_client(id_cliente, body)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_cliente}")
def borrar_cliente(id_cliente: int):
    try:
        return customers.delete_client(id_cliente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
