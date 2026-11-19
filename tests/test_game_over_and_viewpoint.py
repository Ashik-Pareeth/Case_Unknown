"""
Unit tests for NPC viewpoint detection, save clearing, and Game Over popup.
"""

import json
import os
import tempfile
import unittest
import pygame

# Headless video driver for testing
os.environ["SDL_VIDEODRIVER"] = "dummy"

from src.npc import AutonomousNPC, RoomNPCController, point_in_polygon, polygon_collides_with_rect
from src.player import Player
from src.room import Room
from src.rooms_data import ROOMS_DATA
from src.interaction import InteractionManager
from src.evidence_manager import EvidenceManager
from src.save_manager import SaveManager
from src.game_over import GameOverWindow
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class TestGameOverAndViewpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.font.init()
        cls.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def test_vision_points_generation(self):
        npc = AutonomousNPC(start_pos=(300, 300), palette_index=0)
        npc.direction = "right"
        points = npc.get_vision_points()
        
        # Origin + arc points (angles from -35 to +35 step 5 => 15 angles)
        self.assertEqual(len(points), 16)
        origin = points[0]
        self.assertEqual(origin, (300, 300 - 48))

    def test_viewpoint_collision_detection(self):
        npc = AutonomousNPC(start_pos=(300, 300), palette_index=0)
        npc.direction = "right"
        # Origin is (300, 252), pointing right. Vision range = 190.
        
        # Player right in front of the NPC (within viewpoint)
        player_in_front = Player(start_x=380, start_y=280)
        self.assertTrue(npc.collides_with_vision(player_in_front))

        # Player behind the NPC
        player_behind = Player(start_x=200, start_y=280)
        self.assertFalse(npc.collides_with_vision(player_behind))

        # Player far away (beyond vision range 190)
        player_far = Player(start_x=600, start_y=280)
        self.assertFalse(npc.collides_with_vision(player_far))

        # Direct point collision
        self.assertTrue(npc.collides_with_vision((380, 252)))
        self.assertFalse(npc.collides_with_vision((150, 252)))

        # Direct rect collision
        rect_in_front = pygame.Rect(350, 240, 20, 20)
        self.assertTrue(npc.collides_with_vision(rect_in_front))

        # Detective walking below/outside the cone (should NOT be detected)
        detective_below_cone = Player(start_x=380, start_y=350)
        self.assertFalse(npc.collides_with_vision(detective_below_cone))

        # Detective behind a solid desk/obstacle (should NOT be detected)
        desk = pygame.Rect(340, 230, 30, 50)
        detective_behind_desk = Player(start_x=390, start_y=255)
        self.assertFalse(npc.collides_with_vision(detective_behind_desk, solid_objects=[desk]))

    def test_room_npc_controller_spotted(self):
        bounds = pygame.Rect(60, 130, 840, 460)
        solid_objects = []
        # 'office' has patrol NPCs
        controller = RoomNPCController("office", bounds, solid_objects)
        self.assertGreater(len(controller.npcs), 0)

        # Place target right at the first NPC's position facing
        first_npc = controller.npcs[0]
        first_npc.direction = "right"
        # Test with Player entity in front of the NPC
        player = Player(start_x=first_npc.pos.x + 80, start_y=first_npc.pos.y)
        self.assertTrue(controller.check_player_spotted(player, bounds=bounds))

        # Test with direct point along sightline
        spotted_point = (first_npc.pos.x + 50, first_npc.pos.y - 48)
        self.assertTrue(controller.check_player_spotted(spotted_point, bounds=bounds))

    def test_save_manager_clear_save(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            temp_path = tf.name

        try:
            save_mgr = SaveManager(save_path=temp_path)
            ev_mgr = EvidenceManager()

            # Save initial game state
            save_mgr.save_game(
                current_room_id="office",
                player_pos=(340.0, 455.0),
                visited_rooms={"office", "crime_scene"},
                evidence_mgr=ev_mgr,
            )
            self.assertTrue(save_mgr.has_save())
            loaded = save_mgr.load_game(ev_mgr)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded["current_room_id"], "office")

            # Clear save
            self.assertTrue(save_mgr.clear_save())
            self.assertFalse(save_mgr.has_save())
            self.assertIsNone(save_mgr.load_game(ev_mgr))

            # Verify file content is cleared JSON
            with open(temp_path, "r", encoding="utf-8") as f:
                content = json.load(f)
            self.assertEqual(content, {})

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_game_over_window_ui_and_events(self):
        game_over = GameOverWindow(reason="Test Interception")
        self.assertEqual(game_over.reason, "Test Interception")
        self.assertFalse(game_over.finished)

        # Before input delay, events are ignored
        game_over.update(0.1)
        game_over.draw(self.screen)
        key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        self.assertFalse(game_over.handle_event(key_event))
        self.assertFalse(game_over.finished)

        # After input delay (0.35s), key press dismisses the modal
        game_over.update(0.3)
        self.assertTrue(game_over.handle_event(key_event))
        self.assertTrue(game_over.finished)
        self.assertTrue(game_over.update(0.0))

    def test_full_detection_and_save_clearing_integration(self):
        """Simulates full detection cycle: save game -> player collides with NPC cone -> game over -> save cleared."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            temp_path = tf.name

        try:
            save_mgr = SaveManager(save_path=temp_path)
            ev_mgr = EvidenceManager()
            interaction_mgr = InteractionManager(ev_mgr)

            # 1. Setup save file with existing game
            save_mgr.save_game(
                current_room_id="office",
                player_pos=(340.0, 455.0),
                visited_rooms={"office", "crime_scene"},
                evidence_mgr=ev_mgr,
            )
            self.assertTrue(save_mgr.has_save())

            # 2. Setup room and player
            room = Room(interaction_mgr, "office", ROOMS_DATA["office"], evidence_mgr=ev_mgr)
            self.assertGreater(len(room.npc_controller.npcs), 0)
            npc = room.npc_controller.npcs[0]
            npc.direction = "down"

            # 3. Position player in the vision cone (pointing down from (npc.pos.x, npc.pos.y - 48))
            player = Player(start_x=npc.pos.x, start_y=npc.pos.y + 70)

            # 4. Check detection
            spotted = room.check_player_spotted(player)
            self.assertTrue(spotted)

            # 5. On detection: clear save and instantiate GameOverWindow
            if spotted:
                save_mgr.clear_save()
                game_over_modal = GameOverWindow()

            # 6. Verify save is cleared
            self.assertFalse(save_mgr.has_save())
            self.assertIsNone(save_mgr.load_game(ev_mgr))
            with open(temp_path, "r", encoding="utf-8") as f:
                self.assertEqual(f.read().strip(), "{}")

            # 7. Verify GameOverWindow is ready
            self.assertIsNotNone(game_over_modal)
            self.assertGreater(game_over_modal.rect.width, 0)
            self.assertGreater(game_over_modal.rect.height, 0)

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
