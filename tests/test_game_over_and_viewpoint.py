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
        game_over.update(0.2)

        # Render onto screen
        game_over.draw(self.screen)

        # Default selected is RETRY
        self.assertEqual(game_over.selected_idx, 0)

        # Keyboard down to switch to MENU
        key_down_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN})
        action = game_over.handle_event(key_down_event)
        self.assertIsNone(action)
        self.assertEqual(game_over.selected_idx, 1)

        # Press ENTER on MENU
        enter_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN})
        action = game_over.handle_event(enter_event)
        self.assertEqual(action, "MENU")

        # Press ESC to exit to MENU
        esc_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE})
        action = game_over.handle_event(esc_event)
        self.assertEqual(action, "MENU")

        # Press R for RETRY shortcut
        r_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_r})
        action = game_over.handle_event(r_event)
        self.assertEqual(action, "RETRY")

        # Mouse click on RETRY button
        click_retry = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"button": 1, "pos": (game_over.btn_retry_rect.centerx, game_over.btn_retry_rect.centery)},
        )
        action = game_over.handle_event(click_retry)
        self.assertEqual(action, "RETRY")

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
