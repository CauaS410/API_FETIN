from app.database.mongodb import db


class ContaAguaRepository:

    collection = db["contas_agua"]

    @classmethod
    def create(cls, conta_data: dict):
        result = cls.collection.insert_one(conta_data)
        return str(result.inserted_id)

    @classmethod
    def find_by_user(cls, user_email: str, limit: int = None):
        cursor = cls.collection.find({"userEmail": user_email}).sort("createdAt", -1)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)