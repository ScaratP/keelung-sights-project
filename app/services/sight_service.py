from app.models import Sight
from app.crawler import KeelungSightsCrawler
from app.repositories.sight_repository import SightRepository
from app.database import get_db

class SightService:
    ZONES = ["中山區", "信義區", "仁愛區", "中正區", "安樂區", "七堵區", "暖暖區"]
    
    def __init__(self):
        self.db = get_db()
        self.repo = SightRepository(self.db)
        self.crawler = KeelungSightsCrawler()
        
    def normalize_zone(self, zone: str) -> str:
        """
        將「七堵」、「七堵區」等輸入統一轉為完整行政區名稱，
        並檢查是否為基隆市有效行政區。
        """
        zone = zone.strip()
        if not zone.endswith("區"):
            zone += "區"
            
        if zone not in self.ZONES:
            raise ValueError(f"Invalid zone: {zone}。請輸入基隆市有效的行政區。")
        return zone
        
    def get_sights_by_zone(self, zone: str) -> list[Sight]:
        normalized_zone = self.normalize_zone(zone)
        
        sights = self.repo.get_sights_by_zone(normalized_zone)
        
        # 若資料庫沒有資料且未連線，退回空陣列
        return sights
        
    def refresh_sights(self) -> int:
        """
        呼叫爬蟲取得各區景點資料，並透過 Repository 將資料 upsert 到 MongoDB
        """
        if self.db is None:
            raise RuntimeError("Database not connected. Cannot refresh sights.")
            
        total_upserted = 0
        for zone in self.ZONES:
            sights = self.crawler.get_items(zone)
            if sights:
                self.repo.upsert_sights(sights)
                total_upserted += len(sights)
                
        return total_upserted
