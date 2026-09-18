from bson import ObjectId
from app.database.mongodb import db


class NotificacaoRepository:

    collection = db["notificacoes"]

    @classmethod
    def create(cls, notificacao_data: dict):
        result = cls.collection.insert_one(notificacao_data)
        return str(result.inserted_id)

    @classmethod
    def find_existing(cls, device_id: str, tipo: str, desde=None):
        query = {"deviceId": device_id, "type": tipo}
        if desde is not None:
            query["createdAt"] = {"$gte": desde}
        return cls.collection.find_one(query)

    @classmethod
    def find_by_user(cls, user_email: str, limit: int = 20):
        cursor = cls.collection.find({"userEmail": user_email}).sort("createdAt", -1).limit(limit)
        return list(cursor)

    @classmethod
    def mark_as_read(cls, notificacao_id: str, user_email: str):
        result = cls.collection.update_one(
            {"_id": ObjectId(notificacao_id), "userEmail": user_email},
            {"$set": {"read": True}}
        )
        return result.modified_count