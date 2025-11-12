import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

import json
import os
import time

from config.settings import get_config


@dataclass
class RankEntry:
    name: str
    score: int
    time: float


class GameCache:

    def __init__(
        self,
        cache_file: str = "./files/games_cache.json",
        auto_save_interval: int = 600,
    ) -> None:
        """
        Initialize the GameCache instance.

        Parameters:
        cache_file (str): Path to the cache file
        env (str): Environment configuration ('development' or 'production')
        """
        print(
            f"Initializing GameCache with {cache_file} and auto-save interval {auto_save_interval} seconds"
        )

        self._cache_file = cache_file
        self._cache = {}
        self.load_cache()

        self._lock: threading.Lock = threading.Lock()

        self._auto_save_interval = auto_save_interval
        self._thread = threading.Thread(target=self._auto_save, daemon=True)
        self._thread.start()

    def add_rank_entry(
        self,
        game: str,
        name: str,
        score: int,
        timestamp: Optional[float] = None,
    ) -> bool:
        print(f"Adding {name} with score {score} to game {game}")
        if not all([game, name, score]):
            return False

        if timestamp is None:
            timestamp = datetime.now().timestamp()

        rank_entry = RankEntry(name=name, score=score, time=timestamp)

        with self._lock:
            if game not in self._cache:
                self._cache[game] = []
            self._cache[game].append(asdict(rank_entry))

        return True

    def get_game_rankings(self, game: str) -> List:
        print(f"Getting rankings for game {game}")
        with self._lock:
            if game not in self._cache:
                return []

            return self._cache[game].copy()

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
        if not os.path.exists(self._cache_file):
            print(f"Cache file {self._cache_file} does not exist.")
            return

        try:
            print(f"Loading cache from {self._cache_file}")
            with open(self._cache_file, "r", encoding="utf-8") as f:
                self._cache.update(json.load(f))
            print("Cache loaded successfully")
        except Exception as e:
            print(f"Failed to load {self._cache_file}: {e}")
            return True

    def clear_all_cache(self) -> None:
        print("Clearing all cache")
        with self._lock:
            self._cache.clear()

    def save_cache(self) -> bool:
        print(f"Saving cache to {self._cache_file}")
        with self._lock:
            cache_copy = self._cache.copy()

        try:
            print(f"Removing existing cache file {self._cache_file}")
            os.remove(self._cache_file)
        except Exception as e:
            print(f"Failed to remove cache file {self._cache_file}: {e}")

        try:
            with open(self._cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_copy, f, ensure_ascii=False, indent=2)

            print(f"Cache saved successfully to {self._cache_file}")
            return True
        except Exception as e:
            print(f"Failed to save cache to {self._cache_file}: {e}")

        return False

    def _auto_save(self) -> None:
        while True:
            print(f"{datetime.now().isoformat()} Starting auto-save timer")
            self.save_cache()
            time.sleep(self._auto_save_interval)


# Global cache instance for easy access
game_cache = None


def initialize_game_cache(auto_save_interval: int) -> None:
    global game_cache
    game_cache = GameCache(auto_save_interval=auto_save_interval)


def get_game_cache() -> GameCache:
    """
    Get the global GameCache instance.

    If the cache hasn't been initialized, it will be initialized with
    development environment settings.

    Returns:
        GameCache: The global cache instance
    """
    global game_cache
    if game_cache is None:
        initialize_game_cache(get_config("development").AUTO_SAVE_INTERVAL)
    return game_cache
