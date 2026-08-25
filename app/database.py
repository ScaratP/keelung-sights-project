from pymongo import MongoClient
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

MONGODB_URI = os.getenv("MONGODB_URI")

class Database:
    client: MongoClient = None
    db = None

    @classmethod
    def connect(cls):
        if not MONGODB_URI:
            logger.warning("環境變數 MONGODB_URI 未設定。")
            return
        try:
            cls.client = MongoClient(MONGODB_URI)
            cls.db = cls.client.keelung_sights_db
            logger.info("MongoDB Atlas 連線成功。")
        except Exception as e:
            logger.error(f"MongoDB 連線失敗: {e}")

    @classmethod
    def close(cls):
        if cls.client:
            cls.client.close()
            logger.info("MongoDB 連線已關閉。")

def get_db():
    return Database.db
