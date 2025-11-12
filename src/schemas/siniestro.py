from typing import Optional
from pydantic import BaseModel, Field

class SiniestroIn(BaseModel):
    id_siniestro: int
    nro_poliza: str
    fecha: str = Field(..., description="dd/mm/yyyy")
    tipo: str
    descripcion: Optional[str] = None
    monto_estimado: Optional[float] = None
    estado: str = Field(default="Abierto")
