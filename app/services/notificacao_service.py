from datetime import datetime, timedelta
from fastapi import HTTPException
from app.repositories.notificacao_repository import NotificacaoRepository
from app.services.sms_service import SmsService
from app.core.datetime_utils import limites_do_dia_atual_em_utc
from app.core import config

TIPO_CONSUMO_ATIPICO = "CONSUMO_ATIPICO"
TIPO_FLUXO_CONTINUO = "CONTINUOUS_FLOW"
TIPO_REFERENCIA_PENDENTE = "REFERENCIA_PENDENTE"


class NotificacaoService:

    @staticmethod
    def _criar_se_nao_duplicada(device_id: str, user: dict, tipo: str, mensagem: str, desde=None):
        existente = NotificacaoRepository.find_existing(device_id, tipo, desde)
        if existente:
            return None  # já existe notificação desse tipo dentro da janela — não duplica

        notificacao = {
            "deviceId": device_id,
            "userEmail": user["email"],
            "type": tipo,
            "message": mensagem,
            "createdAt": datetime.utcnow(),
            "read": False,
        }
        notificacao_id = NotificacaoRepository.create(notificacao)

        SmsService.send_sms(user.get("cell"), mensagem)

        return notificacao_id

    @staticmethod
    def notificar_consumo_atipico(device_id: str, user: dict, consumo_litros: float, referencia_litros: float):
        mensagem = (
            f"Seu consumo de água hoje ({consumo_litros:.1f} L) ultrapassou "
            f"sua referência diária de {referencia_litros:.1f} L."
        )
        inicio_dia, _ = limites_do_dia_atual_em_utc()
        return NotificacaoService._criar_se_nao_duplicada(
            device_id, user, TIPO_CONSUMO_ATIPICO, mensagem, desde=inicio_dia
        )

    @staticmethod
    def notificar_fluxo_continuo(device_id: str, user: dict, duration_seconds: int):
        minutos = duration_seconds // 60
        mensagem = (
            f"Fluxo de água contínuo detectado por {minutos} minutos. "
            f"Verifique se alguma torneira está aberta ou se pode existir um vazamento."
        )
        cooldown_desde = datetime.utcnow() - timedelta(minutes=config.NOTIFICATION_COOLDOWN_MINUTES)
        return NotificacaoService._criar_se_nao_duplicada(
            device_id, user, TIPO_FLUXO_CONTINUO, mensagem, desde=cooldown_desde
        )

    @staticmethod
    def notificar_referencia_pendente(device_id: str, user: dict):
        mensagem = "Cadastre pelo menos 3 contas de água anteriores para ativarmos o monitoramento de consumo atípico."
        # desde=None → verifica se já existe ALGUMA VEZ, não só num período — só notifica isso uma única vez
        return NotificacaoService._criar_se_nao_duplicada(
            device_id, user, TIPO_REFERENCIA_PENDENTE, mensagem, desde=None
        )

    @staticmethod
    def listar_do_usuario(user_email: str, limit: int = 20):
        docs = NotificacaoRepository.find_by_user(user_email, limit)
        resultado = []
        for doc in docs:
            doc["id"] = str(doc.pop("_id"))
            resultado.append(doc)
        return resultado

    @staticmethod
    def marcar_como_lida(notificacao_id: str, user_email: str):
        modificado = NotificacaoRepository.mark_as_read(notificacao_id, user_email)
        if not modificado:
            raise HTTPException(status_code=404, detail="Notificação não encontrada")
        return {"message": "Notificação marcada como lida"}