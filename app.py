from flask import Flask, jsonify, request
import datetime


app = Flask(__name__)

# In-memory cache for game rankings
cache = {}


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
