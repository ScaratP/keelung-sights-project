from app.models import Sight
from typing import List

class SightRepository:
    def __init__(self, db):
        self.collection = db["sights"] if db is not None else None
        
    def upsert_sights(self, sights: List[Sight]) -> None:
        if self.collection is None:
            return
            
        for sight in sights:
            # 依據 sight_name 為鍵值進行 upsert
            self.collection.update_one(
                {"sight_name": sight.sight_name},
                {"$set": sight.model_dump()},
                upsert=True
            )
            
    def get_sights_by_zone(self, zone: str) -> List[Sight]:
        if self.collection is None:
            return []
        cursor = self.collection.find({"zone": zone})
        return [Sight(**doc) for doc in cursor]
