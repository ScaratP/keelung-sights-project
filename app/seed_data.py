import logging
from app.services.sight_service import SightService
from app.database import Database

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("正在初始化資料庫連線...")
    Database.connect()
    
    try:
        print("開始執行爬蟲更新景點資料 (Seed Data)...")
        service = SightService()
        count = service.refresh_sights()
        print(f"成功 Upsert 了 {count} 筆景點資料到 MongoDB！")
    except Exception as e:
        print(f"初始化資料失敗: {e}")
    finally:
        Database.close()
