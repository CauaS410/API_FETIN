import os
from dotenv import load_dotenv

load_dotenv()

WATER_TARIFF_PER_CUBIC_METER = 5.00  # valor tarifa

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
NOTIFICATIONS_ENABLED = os.getenv("NOTIFICATIONS_ENABLED", "false").lower() == "true"

NOTIFICATION_COOLDOWN_MINUTES = int(os.getenv("NOTIFICATION_COOLDOWN_MINUTES", "5"))