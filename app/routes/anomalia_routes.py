from fastapi import APIRouter, HTTPException, status
from app.schemas.anomalia.anomalia_schema import AnomaliaCreateSchema
from app.services.anomalia_service import AnomaliaService
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/anomalias", tags=["Anomalias"])


@router.post("", status_code=status.HTTP_201_CREATED, summary="Registrar anomalia detectada pelo ESP32 (ex: fluxo contínuo)")
def create_anomalia(anomalia: AnomaliaCreateSchema):
    dono = UserRepository.find_by_device_id(anomalia.deviceId)
    if not dono:
        raise HTTPException(status_code=403, detail="deviceId não está vinculado a nenhum usuário cadastrado")

    return AnomaliaService.registrar_anomalia(anomalia, dono)