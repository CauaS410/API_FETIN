from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from fastapi import HTTPException
from app.repositories.medicao_repository import MedicaoRepository
from app.services.conta_agua_service import ContaAguaService

BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")
UTC_TZ = ZoneInfo("UTC")


class ConsumoAtipicoService:

    @staticmethod
    def _limites_do_dia_atual_em_utc():
        agora_local = datetime.now(BRAZIL_TZ)
        inicio_local = agora_local.replace(hour=0, minute=0, second=0, microsecond=0)
        fim_local = inicio_local + timedelta(days=1)

        inicio_utc = inicio_local.astimezone(UTC_TZ).replace(tzinfo=None)
        fim_utc = fim_local.astimezone(UTC_TZ).replace(tzinfo=None)

        return inicio_utc, fim_utc

    @staticmethod
    def get_consumo_hoje(device_id: str) -> dict:
        inicio_utc, fim_utc = ConsumoAtipicoService._limites_do_dia_atual_em_utc()
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