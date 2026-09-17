from pydantic import BaseModel
from typing import Optional


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    cell: Optional[str] = None
    deviceId: Optional[str] = None
    password: Optional[str] = None