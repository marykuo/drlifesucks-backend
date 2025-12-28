# backend

A simple Flask API for backend.

## Features

- Ranking game scores

## Local Development

```bash
pip install -r requirements.txt
```

### Environment Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Configure your environment variables in `config/settings.py` or set them in your system environment.

3. Test your GCS connection:

```bash
python test_gcs_connection.py
```

5. **Test CORS setup** (開發模式下):

```bash
python main.py
```

然後開啟 `cors_test.html` 在瀏覽器中測試 API

## Configuration Options

### CORS Configuration

**Development Mode (允許所有來源)**:

```env
CORS_ORIGINS=*
CORS_ALLOW_CREDENTIALS=true
```

**Production Mode (限制特定來源)**:

```env
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
CORS_ALLOW_CREDENTIALS=false
```

### Response Format

成功回應:

```json
{
  "status": "success",
  "data": {...},
  "message": "操作成功訊息"
}
```

錯誤回應:

```json
{
  "status": "error",
  "message": "錯誤訊息"
}
```

## Docker

### Build Docker Image

```bash
docker build -t backend .
```

### Run Docker Container

1. Using Environment Variables

```bash
docker run \
  -p 8080:8080 \
  -v $(pwd)/backend/files:/app/files \
  -e AUTO_SAVE_INTERVAL=30 \
  backend
```

docker run -p 8080:8080 -e AUTO_SAVE_INTERVAL=30 backend

2. Using Volume Mount for Configuration Files

```bash
docker run \
  -p 8080:8080 \
  -v $(pwd)/backend/files:/app/files \
  -v $(pwd)/backend/config/custom_settings.py:/app/config/settings.py \
  backend
```
