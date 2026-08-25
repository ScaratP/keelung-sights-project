from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.services.sight_service import SightService
from app.models import Sight
from app.database import Database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # App 啟動時建立 MongoDB 連線
    Database.connect()
    yield
    # App 關閉時中斷連線
    Database.close()

app = FastAPI(
    title="基隆景點瀏覽器 (Keelung Sights API)",
    description="取得基隆市各行政區景點資料的 Web API",
    version="1.0.0",
    lifespan=lifespan
)

# 設定 CORS 允許前端存取
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "database_connected": Database.db is not None}

@app.get("/sights", response_model=list[Sight], tags=["Sights"])
def get_sights(zone: str = Query(..., description="行政區名稱，例如：七堵、七堵區")):
    service = SightService()
    try:
        sights = service.get_sights_by_zone(zone)
        return sights
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 掛載靜態檔案以提供前端頁面 (StaticFiles 放最後以防覆蓋 API 路徑)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
