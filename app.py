from flask import Flask, jsonify, request
import datetime
import threading
import time

import json
import os

from games_cache import get_game_cache

app = Flask(__name__)

cache = get_game_cache()
MINUTES_IN_SECOND = 60


@app.route("/")
def health_check():
    return "alive", 200


@app.route("/game/<game>/rank")
def greet(game):
    name = request.args.get("name", "Guest")
    score = request.args.get("score")
    cache.add_rank_entry(game, name, score)
    return "OK", 200


@app.route("/game/<game>/ranks", methods=["GET"])
def get_ranks(game):
    order = request.args.get("order", "desc")
    sort_descending = order.lower() != "asc"
    rankings = cache.get_game_rankings(game, sort_descending)
    return jsonify(rankings), 200


@app.route("/games", methods=["GET"])
def get_games():
    return jsonify(list(cache.get_all_games())), 200


# Background scheduler to save cache
def save_cache_periodically():
    while True:
        cache.save_cache()
        time.sleep(MINUTES_IN_SECOND * 60)


@app.route("/cache/save", methods=["POST"])
def save_cache():
    cache.save_cache()
    return "Cache saved", 200


@app.route("/cache/cleanup", methods=["POST"])
def cleanup_cache():
    cache.clear_all_cache()
    return "Cache cleared", 200


if __name__ == "__main__":
    thread = threading.Thread(target=save_cache, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=8080)
