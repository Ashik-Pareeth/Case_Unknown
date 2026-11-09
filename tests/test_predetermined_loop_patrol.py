"""
Unit tests for predetermined looping NPC patrol paths and door-facing restrictions.
"""

import os
import unittest
import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"

from src.npc import AutonomousNPC, RoomNPCController, NPC_PATROL_PATHS, NPC_COUNT_PER_ROOM
from src.rooms_data import ROOMS_DATA
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, ROOM_X, ROOM_Y, ROOM_WIDTH, ROOM_HEIGHT, WALL_THICKNESS


class TestPredeterminedLoopPatrol(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.font.init()
        cls.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        rect = pygame.Rect(ROOM_X, ROOM_Y, ROOM_WIDTH, ROOM_HEIGHT)
        cls.floor_rect = pygame.Rect(
            rect.left + WALL_THICKNESS,
            rect.top + 80,
            rect.width - 2 * WALL_THICKNESS,
            rect.height - 80 - WALL_THICKNESS,
        )

    def test_paths_defined_for_all_patrolled_rooms(self):
        patrolled_rooms = [
            "office", "archive", "morgue", "lockup",
            "interrogation", "records_room", "recording_room", "restricted_office"
        ]
        for room_id in patrolled_rooms:
            self.assertIn(room_id, NPC_PATROL_PATHS)
            paths = NPC_PATROL_PATHS[room_id]
            self.assertGreaterEqual(len(paths), NPC_COUNT_PER_ROOM)
            for path in paths:
                # Must be a complicated loop with at least 6 waypoints
                self.assertGreaterEqual(len(path), 6)
                for pt in path:
                    self.assertTrue(self.floor_rect.collidepoint(pt), f"Point {pt} outside floor rect in {room_id}")

    def test_room_npc_controller_spawns_looping_npcs(self):
        solids = [pygame.Rect(f["hitbox"]) for f in ROOMS_DATA["office"].get("furniture", []) if "hitbox" in f]
        controller = RoomNPCController("office", self.floor_rect, solids)
        self.assertEqual(len(controller.npcs), NPC_COUNT_PER_ROOM)
        for npc in controller.npcs:
            self.assertGreaterEqual(len(npc.path), 6)

    def test_npcs_never_face_doors_for_extended_time_during_patrol(self):
        """Simulate 60 seconds of patrol in every room and verify door-facing time is strictly bounded."""
        for room_id in NPC_PATROL_PATHS:
            solids = [pygame.Rect(f["hitbox"]) for f in ROOMS_DATA[room_id].get("furniture", []) if "hitbox" in f]
            controller = RoomNPCController(room_id, self.floor_rect, solids)

            dt = 0.05
            for _ in range(1200):  # 1200 * 0.05 = 60.0 seconds of game simulation
                controller.update(dt, self.floor_rect, solids)
                for npc in controller.npcs:
                    # Assert door facing timer is strictly below 0.35s at all times
                    self.assertLessEqual(
                        npc.door_facing_timer,
                        0.35,
                        f"NPC in {room_id} at {npc.pos} pointed at door for {npc.door_facing_timer:.2f}s"
                    )
                    # When waiting/idling, direction must NEVER be pointing at a door
                    if npc.phase == "wait":
                        self.assertFalse(
                            npc.is_pointing_at_door(),
                            f"NPC in {room_id} idling while pointing at door ({npc.direction})"
                        )

    def test_path_remains_invisible(self):
        """Ensure no path lines or waypoint indicators are rendered in draw calls."""
        solids = [pygame.Rect(f["hitbox"]) for f in ROOMS_DATA["office"].get("furniture", []) if "hitbox" in f]
        controller = RoomNPCController("office", self.floor_rect, solids)
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Initial state before drawing
        surface.fill((0, 0, 0))
        for item in controller.draw_queue(surface):
            item["draw"]()

        # controller itself has no draw_path method and autonomous NPCs don't draw path markers
        for npc in controller.npcs:
            self.assertFalse(hasattr(npc, "draw_path"))
            self.assertFalse(hasattr(npc, "path_surface"))


if __name__ == "__main__":
    unittest.main()

