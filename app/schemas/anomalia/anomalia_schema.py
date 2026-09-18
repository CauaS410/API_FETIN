from pydantic import BaseModel, Field


class AnomaliaCreateSchema(BaseModel):
    deviceId: str = Field(min_length=1, description="Identificador do ESP32")
    type: str = Field(default="CONTINUOUS_FLOW", description="Tipo da anomalia detectada")
    durationSeconds: int = Field(gt=0, description="Duração do fluxo contínuo até o momento do envio, em segundos")