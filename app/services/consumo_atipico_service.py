from datetime import datetime, timedelta
from fastapi import HTTPException
from app.repositories.medicao_repository import MedicaoRepository
from app.services.conta_agua_service import ContaAguaService
from app.services.notificacao_service import NotificacaoService
from app.core.datetime_utils import BRAZIL_TZ, UTC_TZ, limites_do_dia_atual_em_utc


class ConsumoAtipicoService:

    @staticmethod
    def get_consumo_hoje(device_id: str) -> dict:
        inicio_utc, fim_utc = limites_do_dia_atual_em_utc()
        litros_hoje = MedicaoRepository.sum_volume_between(device_id, inicio_utc, fim_utc)

        return {
            "deviceId": device_id,
            "consumoHojeLitros": round(litros_hoje, 3),
            "consumoHojeM3": round(litros_hoje / 1000, 5),
        }

    @staticmethod
    def get_status_consumo(device_id: str, user_email: str) -> dict:
        consumo_hoje = ConsumoAtipicoService.get_consumo_hoje(device_id)
        referencia = ContaAguaService.get_daily_reference(user_email)

        consumo_m3 = consumo_hoje["consumoHojeM3"]
        referencia_m3 = referencia["referenciaDiariaM3"]

        atipico = consumo_m3 > referencia_m3
        variacao_percentual = None
        if referencia_m3 > 0:
            variacao_percentual = round(((consumo_m3 - referencia_m3) / referencia_m3) * 100, 1)

        return {
            "deviceId": consumo_hoje["deviceId"],
            "consumoHojeLitros": consumo_hoje["consumoHojeLitros"],
            "consumoHojeM3": consumo_m3,
            "referenciaDiariaM3": referencia_m3,
            "variacaoPercentual": variacao_percentual,
            "atipico": atipico,
        }

    @staticmethod
    def get_historico_diario(device_id: str, user_email: str, dias: int = 14) -> dict:
        agora_local = datetime.now(BRAZIL_TZ)
        inicio_local = (agora_local - timedelta(days=dias - 1)).replace(hour=0, minute=0, second=0, microsecond=0)
        inicio_utc = inicio_local.astimezone(UTC_TZ).replace(tzinfo=None)

        medicoes = MedicaoRepository.find_volumes_since(device_id, inicio_utc)

        totais_por_dia = {}
        for medicao in medicoes:
            timestamp_utc = medicao["timestamp"].replace(tzinfo=UTC_TZ)
            data_local = timestamp_utc.astimezone(BRAZIL_TZ).date()
            chave = data_local.isoformat()
            totais_por_dia[chave] = totais_por_dia.get(chave, 0) + medicao.get("volume", 0)

        serie = []
        for i in range(dias):
            data = (inicio_local + timedelta(days=i)).date()
            chave = data.isoformat()
            litros = totais_por_dia.get(chave, 0)
            serie.append({
                "data": chave,
                "consumoLitros": round(litros, 3),
                "consumoM3": round(litros / 1000, 5),
            })

        referencia_m3 = None
        referencia_litros = None
        try:
            referencia = ContaAguaService.get_daily_reference(user_email)
            referencia_m3 = referencia["referenciaDiariaM3"]
            referencia_litros = referencia["referenciaDiariaLitros"]
        except HTTPException:
            pass

        return {
            "deviceId": device_id,
            "referenciaDiariaM3": referencia_m3,
            "referenciaDiariaLitros": referencia_litros,
            "serie": serie,
        }

    @staticmethod
    def verificar_e_notificar(device_id: str, user: dict):
        """Chamado depois que uma medição é salva. Reaproveita get_consumo_hoje
        e get_daily_reference — não recalcula nada, só decide se notifica."""
        try:
            referencia = ContaAguaService.get_daily_reference(user["email"])
        except HTTPException as exc:
            if exc.status_code == 422:
                NotificacaoService.notificar_referencia_pendente(device_id, user)
                return
            raise

        consumo_hoje = ConsumoAtipicoService.get_consumo_hoje(device_id)

        if consumo_hoje["consumoHojeM3"] > referencia["referenciaDiariaM3"]:
            NotificacaoService.notificar_consumo_atipico(
                device_id,
                user,
                consumo_litros=consumo_hoje["consumoHojeLitros"],
                referencia_litros=referencia["referenciaDiariaLitros"],
            )