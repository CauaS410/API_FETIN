from pydantic import BaseModel, EmailStr, Field


class UserCreateSchema(BaseModel):
    name: str = Field(min_length=1, description="Name of the user")

    email: EmailStr = Field(description="Email of the user")

    cell: str = Field(min_length=1, description="Cell phone number of the user")

    deviceId: str = Field(min_length=1, description="Identificador do ESP32 vinculado a este usuário (ex: esp32-01)")

    password: str = Field(min_length=8, description="Password must be at least 8 characters long.")


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"