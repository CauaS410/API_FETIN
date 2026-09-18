from pydantic import BaseModel
from datetime import datetime


class NotificacaoResponseSchema(BaseModel):
    id: str
    deviceId: str
    type: str
    message: str
    createdAt: datetime
    read: bool