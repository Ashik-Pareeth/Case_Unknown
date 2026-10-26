"""
Save & Load System for Case Unknown.

Strictly adheres to directives.txt §9:
- Local JSON save file tracking:
  - Current level and room ID.
  - Player coordinates.
  - Evidence discovered/recorded states (guaranteeing no duplicate awards).
  - Important evidence connections.
  - Unlocked room routes and gates.
  - Visited room set.
"""

from __future__ import annotations
import json
import os
import time
from src.evidence_manager import EvidenceManager

DEFAULT_SAVE_FILE = "save_game.json"


class SaveManager:
    """Manages serializing and loading the player's investigation progress."""

    def __init__(self, save_path: str = DEFAULT_SAVE_FILE):
        self.save_path = save_path

    def has_save(self) -> bool:
        """Returns True if a valid save file exists on disk."""
        return os.path.exists(self.save_path) and os.path.getsize(self.save_path) > 0

    def save_game(
        self,
        current_room_id: str,
        player_pos: tuple[float, float],
        visited_rooms: set[str],
        evidence_mgr: EvidenceManager,
        level: int = 1,
    ) -> bool:
        """Persists investigation state to local JSON file (§9)."""
        data = {
            "version": 1,
            "timestamp": time.time(),
            "level": level,
            "current_room_id": current_room_id,
            "player_pos": [player_pos[0], player_pos[1]],
            "visited_rooms": list(visited_rooms),
            "evidence_progression": evidence_mgr.export_save_data(),
        }

        try:
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, evidence_mgr: EvidenceManager) -> dict | None:
        """Loads and restores investigation state from save file."""
        if not self.has_save():
            return None

        try:
            with open(self.save_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Restore evidence state
            if "evidence_progression" in data:
                evidence_mgr.import_save_data(data["evidence_progression"])

            return {
                "level": data.get("level", 1),
                "current_room_id": data.get("current_room_id", "crime_scene"),
                "player_pos": tuple(data.get("player_pos", [480, 420])),
                "visited_rooms": set(data.get("visited_rooms", ["crime_scene"])),
            }
        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    def delete_save(self) -> bool:
        """Removes the save file if resetting state."""
        if os.path.exists(self.save_path):
            try:
                os.remove(self.save_path)
                return True
            except OSError:
                return False
        return False
