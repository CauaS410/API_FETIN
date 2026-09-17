from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.schemas.user.patch_user_schema import UserUpdateSchema
from app.schemas.user.user_schema import UserCreateSchema, UserLoginSchema
from app.core.security import hash_password, verify_password, create_access_token


class UserService:

    @staticmethod
    def create_user(user: UserCreateSchema):
        existing_user = UserRepository.find_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email informado já existe, por favor escolha outro")

        existing_device = UserRepository.find_by_device_id(user.deviceId)
        if existing_device:
            raise HTTPException(status_code=400, detail="Este deviceId já está vinculado a outro usuário")

        user_dict = user.model_dump()
        user_dict["password"] = hash_password(user_dict["password"])

        UserRepository.create(user_dict)

        return {"message": "Usuário criado com sucesso"}

    @staticmethod
    def update_user(current_user_email: str, user: UserUpdateSchema):
        existing_user = UserRepository.find_by_email(current_user_email)
        if not existing_user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        update_fields = user.model_dump(exclude_unset=True)

        if "deviceId" in update_fields:
            existing_device = UserRepository.find_by_device_id(update_fields["deviceId"])
            if existing_device and existing_device["email"] != current_user_email:
                raise HTTPException(status_code=400, detail="Este deviceId já está vinculado a outro usuário")

        if "password" in update_fields:
            update_fields["password"] = hash_password(update_fields["password"])

        if not update_fields:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        UserRepository.update(current_user_email, update_fields)

        return {"message": "Usuário atualizado com sucesso"}

    @staticmethod
    def login(credentials: UserLoginSchema):
        user = UserRepository.find_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user["password"]):
            raise HTTPException(status_code=401, detail="Email ou senha inválidos")

        access_token = create_access_token(data={"sub": user["email"]})

        return {"access_token": access_token, "token_type": "bearer"}