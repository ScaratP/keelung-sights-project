# 採用輕量化的 Python 3.11 映像檔
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製環境需求檔並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案程式碼
COPY . .

# 宣告預設的環境變數，Render/Railway 會自動覆蓋 PORT
ENV PORT=8000

# 啟動 Uvicorn 伺服器
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
