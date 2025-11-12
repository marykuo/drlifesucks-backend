import os
from app import create_app

# Get environment from environment variable, default to development
env = os.getenv("APP_ENV", "development")
app = create_app(env=env)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
