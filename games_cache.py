from typing import List, Optional
from dataclasses import dataclass
import datetime

import json
import os


@dataclass
class RankEntry:
    name: str
    score: str
    time: str


class GameCache:

    def __init__(self, cache_file: str = "cache.json") -> None:
        self.cache_file = cache_file
        self._cache = {}
        self.load_cache()

    def load_cache(self) -> bool:
        print(f"Loading cache from {self.cache_file}")
        if not os.path.exists("cache.json"):
            return

        try:
            print("Loading cache from cache.json")
            with open("cache.json", "r", encoding="utf-8") as f:
                self._cache.update(json.load(f))
            print("Cache loaded successfully")
        except Exception as e:
            print(f"Failed to load cache.json: {e}")
            return True

    def add_rank_entry(
        self, game: str, name: str, score: str, timestamp: Optional[str] = None
    ) -> bool:
        print(f"Adding {name} with score {score} to game {game}")
        if game and name and score:
            time = timestamp or datetime.datetime.now().isoformat()
            if game not in self._cache:
                self._cache[game] = []
            self._cache[game].append({"name": name, "score": score, "time": time})
            return True

    def get_game_rankings(self, game: str, sort_descending: bool = True) -> List:
        print(f"Getting rankings for game {game}")
        if game and game in self._cache:
            cache_sorted = sorted(
                self._cache[game],
                key=lambda x: float(x["score"]),
                reverse=sort_descending,
            )
            return cache_sorted

    def get_all_games(self) -> List[str]:
        print("Getting all games")
        return list(self._cache.keys())

    def get_game_count(self) -> int:
        print("Getting game count")
        return len(self._cache)

    def get_rank_count(self, game: str) -> int:
        print(f"Getting rank count for game {game}")
        return len(self._cache.get(game, []))

    def clear_game_rankings(self, game: str) -> bool:
        print(f"Clearing rankings for game {game}")
        if game in self._cache:
            del self._cache[game]
            return True
        return False

    def clear_all_cache(self) -> None:
        print("Clearing all cache")
        self._cache.clear()

    def save_cache(self) -> bool:
        print(f"Saving cache to {self.cache_file}")
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=2)
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
