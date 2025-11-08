# 使用官方的 Python 3.11 基礎映像檔
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY app.py .

# 開放應用程式 Port
EXPOSE 8080

# 定義環境變數
ENV FLASK_APP=app.py

# 啟動應用程式
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
