from app.database.mongodb import db


class AnomaliaRepository:

    collection = db["anomalias"]

    @classmethod
    def create(cls, anomalia_data: dict):
        result = cls.collection.insert_one(anomalia_data)
        return str(result.inserted_id)