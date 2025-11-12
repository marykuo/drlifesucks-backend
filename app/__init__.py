from flask import Flask
from config.settings import get_config
from app.caches.games_cache import initialize_game_cache


def create_app(env="development"):
    config = get_config(env)

    app = Flask(__name__)
    app.config.from_object(config)

    initialize_game_cache(config.AUTO_SAVE_INTERVAL)

    # 註冊藍圖（Blueprints）
    from app.api.heartbeat import heartbeat_bp
    from app.api.game import game_bp

    app.register_blueprint(heartbeat_bp, url_prefix="/")
    app.register_blueprint(game_bp, url_prefix="/game")

    # 你也可以在這裡初始化資料庫、JWT、CORS 等擴充功能
    # e.g. db.init_app(app), jwt.init_app(app)

    return app
