from typing import Optional
from pydantic import BaseModel, Field

class ClienteIn(BaseModel):
    id_cliente: int
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    activo: bool = Field(default=True)

class ClientePatch(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    activo: Optional[bool] = None
