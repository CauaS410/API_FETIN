from fastapi import APIRouter, Depends, Query
from app.services.consumo_atipico_service import ConsumoAtipicoService
from app.core.dependencies import get_current_user, get_authenticated_device_id

router = APIRouter(prefix="/consumo-atipico", tags=["Consumo Atípico"])


@router.get("/hoje", summary="Consumo de hoje e comparação com a referência diária")
def get_status_hoje(
    device_id: str = Depends(get_authenticated_device_id),
    current_user: dict = Depends(get_current_user),
):
    return ConsumoAtipicoService.get_status_consumo(device_id, current_user["email"])


@router.get("/historico", summary="Consumo diário agregado dos últimos N dias, para gráfico")
def get_historico(
    dias: int = Query(default=14, ge=1, le=90),
    device_id: str = Depends(get_authenticated_device_id),
    current_user: dict = Depends(get_current_user),
):
    return ConsumoAtipicoService.get_historico_diario(device_id, current_user["email"], dias)