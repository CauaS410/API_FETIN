import re
from twilio.rest import Client
from app.core import config


class SmsService:
    _client = None

    @classmethod
    def _get_client(cls):
        if cls._client is None:
            cls._client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        return cls._client

    @staticmethod
    def _formatar_e164(cell: str) -> str:
        digitos = re.sub(r"\D", "", cell or "")
        if digitos.startswith("55"):
            return f"+{digitos}"
        return f"+55{digitos}"

    @staticmethod
    def send_sms(cell: str, message: str) -> bool:
        if not cell:
            print("SMS não enviado: usuário sem celular cadastrado.")
            return False

        numero = SmsService._formatar_e164(cell)

        if not config.NOTIFICATIONS_ENABLED:
            print(f"[SMS DESATIVADO - modo dev] Para {numero}: {message}")
            return True

        try:
            client = SmsService._get_client()
            client.messages.create(body=message, from_=config.TWILIO_FROM_NUMBER, to=numero)
            return True
        except Exception as exc:
            print(f"Falha ao enviar SMS para {numero}: {exc}")
            return False