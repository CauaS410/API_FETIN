from fastapi import APIRouter, Depends, Query
from app.services.consumo_atipico_service import ConsumoAtipicoService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/consumo-atipico", tags=["Consumo Atípico"])


@router.get("/hoje", summary="Consumo de hoje e comparação com a referência diária")
def get_status_hoje(current_user: dict = Depends(get_current_user)):
    return ConsumoAtipicoService.get_status_consumo(current_user["email"])


@router.get("/historico", summary="Consumo diário agregado dos últimos N dias, para gráfico")
def get_historico(dias: int = Query(default=14, ge=1, le=90), current_user: dict = Depends(get_current_user)):
    return ConsumoAtipicoService.get_historico_diario(current_user["email"], dias)