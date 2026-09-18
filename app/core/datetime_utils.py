from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")
UTC_TZ = ZoneInfo("UTC")


def limites_do_dia_atual_em_utc():
    agora_local = datetime.now(BRAZIL_TZ)
    inicio_local = agora_local.replace(hour=0, minute=0, second=0, microsecond=0)
    fim_local = inicio_local + timedelta(days=1)

    inicio_utc = inicio_local.astimezone(UTC_TZ).replace(tzinfo=None)
    fim_utc = fim_local.astimezone(UTC_TZ).replace(tzinfo=None)

    return inicio_utc, fim_utc