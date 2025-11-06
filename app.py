from flask import Flask, jsonify, request
import datetime
import threading
import time

import json
import os


app = Flask(__name__)

# In-memory cache for game rankings
cache = {}
MINUTES_IN_SECOND = 60


@app.route("/")
def health_check():
    return "alive", 200


@app.route("/rank")
def greet():
    game = request.args.get("game")
    name = request.args.get("name", "Guest")
    score = request.args.get("score")
    if game and name and score:
        time = datetime.datetime.now().isoformat()
        if game not in cache:
            cache[game] = []
        cache[game].append({"name": name, "score": score, "time": time})
    return "OK", 200


@app.route("/ranks", methods=["GET"])
def get_ranks():
    game = request.args.get("game")
    if game and game in cache:
        cache_sorted = sorted(
            cache[game], key=lambda x: float(x["score"]), reverse=True
        )
        return jsonify(cache_sorted), 200
    return jsonify([]), 200


# Background scheduler to save cache
def save_cache():
    while True:
        print("Saving cache to cache.json")
        with open("cache.json", "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        time.sleep(MINUTES_IN_SECOND * 60)


# Load cache from file
def load_cache():
    if not os.path.exists("cache.json"):
        return

    try:
        print("Loading cache from cache.json")
        with open("cache.json", "r", encoding="utf-8") as f:
            cache.update(json.load(f))
        print("Cache loaded successfully")
    except Exception as e:
        print(f"Failed to load cache.json: {e}")


if __name__ == "__main__":
    load_cache()
    thread = threading.Thread(target=save_cache, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=8080)
