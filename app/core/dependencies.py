from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    email = payload.get("sub")
    user = UserRepository.find_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user

def get_authenticated_device_id(current_user: dict = Depends(get_current_user)) -> str:
    device_id = current_user.get("deviceId")
    if not device_id:
        raise HTTPException(
            status_code=404,
            detail="Usuário não possui um dispositivo (deviceId) vinculado ao seu perfil"
        )
    return device_id