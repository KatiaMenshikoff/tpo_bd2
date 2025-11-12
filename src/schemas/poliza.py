from typing import Optional
from pydantic import BaseModel, Field

class PolizaIn(BaseModel):
    nro_poliza: str
    id_cliente: int
    id_agente: int
    tipo: Optional[str] = None
    fecha_inicio: Optional[str] = Field(None, description="dd/mm/yyyy")
    fecha_fin: Optional[str]   = Field(None, description="dd/mm/yyyy")
    prima_mensual: Optional[float] = None
    cobertura_total: Optional[float] = None
    estado: str = Field(default="Activa")
