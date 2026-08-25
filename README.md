# 基隆景點瀏覽器 (Keelung Sights)

這是一個包含前後端的全端景點應用程式，使用 FastAPI 提供 Web API，MongoDB Atlas 作為雲端資料庫，並透過 Bootstrap 與 Vanilla JS 實作響應式前端網頁 (RWD)。專案已完整容器化 (Dockerized) 並支援雲端部署。

## 📍 繳交網址資訊 (Submission URLs)

> **注意：** 請替換以下括號 `[...]` 中的內容為你真實的網址。

*   **GitHub Repo 網址：** `[請填入你的 GitHub Repo 網址]`
*   **雲端公開網址 (前端頁面)：** `[請填入你的 Render / Railway 公開網址]`
*   **FastAPI 文件網址：** `[請填入你的 Render / Railway 公開網址]/docs`

---

## 📂 專案檔案結構包含
本專案符合部署所需之核心檔案：
*   `requirements.txt`：Python 套件依賴清單。
*   `Dockerfile`：定義如何建置 Docker Image，並設定 `uvicorn` 綁定 `0.0.0.0` 與動態 `PORT`。
*   `.dockerignore`：避免將不必要的檔案 (如 `.env`, `.git`) 打包進 Image。
*   `.env.example`：環境變數範例檔，供本機端參考。
*   `.gitignore`：排除敏感與暫存檔案，確保真實密碼不被提交至 GitHub。
*   `README.md`：專案說明文件 (本檔案)。

---

## 💻 本機執行方式 (Local Execution)

1.  **安裝依賴套件：**
    請確保環境為 Python 3.11+，並執行以下指令：
    ```bash
    pip install -r requirements.txt
    ```
2.  **環境變數設定：**
    複製 `.env.example` 並重新命名為 `.env`。將你的 MongoDB Atlas 連線字串填入：
    ```text
    MONGODB_URI=mongodb+srv://<username>:<password>@cluster0...
    ```
3.  **初始化資料庫 (爬蟲播種)：**
    手動執行以下指令，透過 Service 層呼叫爬蟲，並寫入資料至 MongoDB：
    ```bash
    python -m app.seed_data
    ```
4.  **啟動 FastAPI 伺服器：**
    ```bash
    uvicorn app.main:app --reload
    ```
    *   **前端網頁：** 開啟瀏覽器前往 `http://127.0.0.1:8000`
    *   **API 文件：** 開啟瀏覽器前往 `http://127.0.0.1:8000/docs`

---

## 🐳 Docker 執行方式 (Docker Execution)

1.  **建立 Docker Image：**
    ```bash
    docker build -t keelung-sights .
    ```
2.  **運行 Docker Container：**
    容器啟動時已設定使用 `uvicorn` 並綁定 `0.0.0.0`。請透過 `-e` 傳入 MongoDB 連線字串：
    ```bash
    docker run -p 8000:8000 -e MONGODB_URI="你的真實連線字串" keelung-sights
    ```
    執行後，即可透過 `http://localhost:8000` 存取應用程式。

---

## ☁️ 雲端環境變數設定 (Cloud Environment Variables)

在雲端平台 (Render / Railway) 部署時，**絕對不可**將真實的帳號密碼寫入程式碼或提交 `.env` 檔至 GitHub。請在雲端平台的設定介面新增以下環境變數：

*   **`MONGODB_URI`**：請填寫 MongoDB Atlas 的真實連線字串。
    *(註：Atlas 的 Network Access 需允許對應的 IP 或設為 `0.0.0.0/0` 讓雲端平台順利連線)*
*   **`PORT`**：雲端平台通常會自動給定此變數，`Dockerfile` 內部已配置好透過 `$PORT` 來綁定服務連接埠。

---

## 🚀 雲端部署步驟 (以 Render/Railway 為例)

本專案採前後端整合部署 (Frontend 以 FastAPI `StaticFiles` 掛載)，因此只需進行單一服務部署。

1.  **推送到 GitHub：** 確保所有原始碼 (含 `Dockerfile`, `.env.example` 等) 已推送到你的公開 (Public) GitHub Repository。
2.  **建立雲端服務：** 登入 Render 或 Railway，選擇建立一個新的 **Web Service**，並綁定你的 GitHub Repo。
3.  **選擇環境：** 部署環境 (Runtime) 請選擇 **Docker**。
4.  **設定變數：** 在平台的 Environment Variables (環境變數) 區塊，新增 `MONGODB_URI` 並貼上連線字串。
5.  **完成部署：** 等待雲端平台自動建置 Image 並啟動服務。成功後，點擊平台提供的**公開網域**即可瀏覽景點前端頁面，並在網址後方加上 `/docs` 查看 API 文件。