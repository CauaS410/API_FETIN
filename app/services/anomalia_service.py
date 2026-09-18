from datetime import datetime
from app.repositories.anomalia_repository import AnomaliaRepository
from app.repositories.user_repository import UserRepository
from app.schemas.anomalia.anomalia_schema import AnomaliaCreateSchema
from app.services.notificacao_service import NotificacaoService


class AnomaliaService:

    @staticmethod
    def registrar_anomalia(anomalia: AnomaliaCreateSchema, dono: dict):
        anomalia_dict = anomalia.model_dump()
        anomalia_dict["timestamp"] = datetime.utcnow()
        AnomaliaRepository.create(anomalia_dict)

        try:
            NotificacaoService.notificar_fluxo_continuo(anomalia.deviceId, dono, anomalia.durationSeconds)
        except Exception as exc:
            print(f"Falha ao notificar fluxo contínuo: {exc}")

        return {"message": "Anomalia registrada com sucesso"}