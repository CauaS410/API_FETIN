from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ContaAguaCreateSchema(BaseModel):
    consumoM3: float = Field(gt=0, description="Consumo informado na conta de água, em metros cúbicos")
    mesReferencia: Optional[str] = Field(default=None, description="Mês/ano de referência da conta (ex: 2026-08), apenas informativo")


class ContaAguaResponseSchema(BaseModel):
    id: str
    consumoM3: float
    mesReferencia: Optional[str] = None
    createdAt: datetime