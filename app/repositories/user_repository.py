from app.database.mongodb import db


class UserRepository:

    collection = db["users"]

    @classmethod
    def create(cls, user_data):
        if not user_data.get("name") or not user_data.get("email"):
            raise ValueError("Nome e email são obrigatórios")
        result = cls.collection.insert_one(user_data)
        return str(result.inserted_id)

    @classmethod
    def find_by_email(cls, email):
        return cls.collection.find_one({"email": email})

    @classmethod
    def find_by_device_id(cls, device_id: str):
        return cls.collection.find_one({"deviceId": device_id})

    @classmethod
    def update(cls, email: str, update_fields: dict):
        result = cls.collection.update_one(
            {"email": email},
            {"$set": update_fields}
        )
        return result.modified_count