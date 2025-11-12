# 使用官方的 Python 3.11 基礎映像檔
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 開放應用程式 Port
EXPOSE 8080

# 定義環境變數 (可在運行時覆蓋)
ENV FLASK_APP=main.py

# 啟動應用程式
CMD ["python", "main.py"]
