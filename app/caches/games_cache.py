import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

import json
import os


@dataclass
class RankEntry:
    name: str
    score: str
    time: str


class GameCache:

    def __init__(self, cache_file: str = "./files/games_cache.json") -> None:
        self.cache_file = cache_file
        self._cache = {}
        self._lock: threading.Lock = threading.Lock()
        self.load_cache()

    def add_rank_entry(
        self, game: str, name: str, score: str, timestamp: Optional[str] = None
    ) -> bool:
        print(f"Adding {name} with score {score} to game {game}")
        if not all([game, name, score]):
            return False

        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()

            if game not in self._cache:
                self._cache[game] = []
            self._cache[game].append({"name": name, "score": score, "time": timestamp})
            return True

    def get_game_rankings(self, game: str, sort_descending: bool = True) -> List:
        print(f"Getting rankings for game {game}")
        with self._lock:
            if game not in self._cache:
                rankings = self._cache[game].copy()

        try:
            # Sort by score (convert to float for proper numerical sorting)
            rankings.sort(key=lambda x: float(x["score"]), reverse=sort_descending)
        except (ValueError, TypeError):
            # If score conversion fails, sort as strings
            rankings.sort(key=lambda x: x["score"], reverse=sort_descending)

        return rankings

    def get_all_games(self) -> List[str]:
        print("Getting all games")
        with self._lock:
            return list(self._cache.keys())

    def get_game_count(self) -> int:
        print("Getting game count")
        with self._lock:
            return len(self._cache)

    def get_rank_count(self, game: str) -> int:
        print(f"Getting rank count for game {game}")
        with self._lock:
            return len(self._cache.get(game, []))

    def clear_game_rankings(self, game: str) -> bool:
        print(f"Clearing rankings for game {game}")
        with self._lock:
            if game in self._cache:
                del self._cache[game]
                return True
        return False

    def load_cache(self) -> bool:
        if not os.path.exists(self.cache_file):
            print(f"Cache file {self.cache_file} does not exist.")
            return

        try:
            print(f"Loading cache from {self.cache_file}")
            with open(self.cache_file, "r", encoding="utf-8") as f:
                self._cache.update(json.load(f))
            print("Cache loaded successfully")
        except Exception as e:
            print(f"Failed to load {self.cache_file}: {e}")
            return True

    def clear_all_cache(self) -> None:
        print("Clearing all cache")
        with self._lock:
            self._cache.clear()

    def save_cache(self) -> bool:
        print(f"Saving cache to {self.cache_file}")
        try:
            with self._lock:
                cache_copy = self._cache.copy()

            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_copy, f, ensure_ascii=False, indent=2)

            print(f"Cache saved successfully to {self.cache_file}")
            return True
        except Exception as e:
            print(f"Failed to save cache to {self.cache_file}: {e}")
        return False


# Global cache instance for easy access
game_cache = GameCache()


def get_game_cache() -> GameCache:
    """
    Get the global GameCache instance.

    Returns:
        GameCache: The global cache instance
    """
    return game_cache
