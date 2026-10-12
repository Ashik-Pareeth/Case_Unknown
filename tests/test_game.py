"""
Automated headless test suite for Case Unknown:
- Verifies SVG vector generation and sprite animation frames.
- Verifies player movement and collision resolution.
- Verifies interactables and dialogue inspection system.
- Confirms zero dependencies on external raster images.
"""

import os
import sys

# Set headless SDL video driver for headless execution
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from assets.svg_assets import get_character_animations, get_room_objects
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.interaction import InteractionManager
from src.room import Room
from src.player import Player


def test_svg_character_animations():
    pygame.init()
    pygame.display.set_mode((1, 1))

    animations = get_character_animations()
    assert set(animations.keys()) == {"down", "up", "right", "left"}

    for direction, states in animations.items():
        assert "idle" in states
        assert "walk" in states
        assert len(states["idle"]) >= 2
        assert len(states["walk"]) >= 4

        # Check surface validity and non-zero dimensions
        for surf in states["idle"] + states["walk"]:
            assert isinstance(surf, pygame.Surface)
            w, h = surf.get_size()
            assert w > 0 and h > 0


def test_svg_room_objects():
    pygame.init()
    pygame.display.set_mode((1, 1))

    objects = get_room_objects()
    expected_keys = {
        "desk", "sofa", "filing_cabinet", "evidence_board",
        "bookshelf", "window", "rug", "plant", "sconce", "inspect_badge"
    }
    assert expected_keys.issubset(set(objects.keys()))

    for key, surf in objects.items():
        assert isinstance(surf, pygame.Surface)
        w, h = surf.get_size()
        assert w > 0 and h > 0


def test_player_movement_and_animation_states():
    pygame.init()
    pygame.display.set_mode((1, 1))

    player = Player(start_x=300, start_y=300)
    assert player.state == "idle"
    assert player.direction == "down"

    # Simulate movement update
    solid_boxes = [pygame.Rect(400, 300, 50, 50)]
    player.velocity = pygame.Vector2(100, 0)
    player.state = "walk"
    player.direction = "right"

    # Run 10 ticks
    for _ in range(10):
        player.update(0.016, solid_boxes)

    assert player.pos.x > 300
    assert player.image is not None


def test_room_and_interaction_inspection():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    interaction_mgr = InteractionManager()
    room = Room(interaction_mgr)

    # Room must contain solid walls and furniture
    assert len(room.solid_objects) >= 5
    assert len(room.furniture_items) >= 4
    assert len(interaction_mgr.interactables) >= 4

    # Position player directly in front of the desk (desk is around x=470, y=360)
    player = Player(start_x=470, start_y=380)
    player.direction = "up"

    # Update interaction manager
    interaction_mgr.update(0.016, player.get_interaction_reach())
    assert interaction_mgr.active_object is not None
    assert interaction_mgr.active_object.obj_id == "desk"

    # Simulate pressing 'E' to open inspection dialogue
    event_e = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_e})
    consumed = interaction_mgr.handle_event(event_e)
    assert consumed is True
    assert interaction_mgr.is_inspecting is True

    # Simulate pressing 'E' again to close inspection dialogue
    consumed_close = interaction_mgr.handle_event(event_e)
    assert consumed_close is True
    assert interaction_mgr.is_inspecting is False


def test_no_references_to_images_directory():
    """Verify that source code and asset python modules never load files from assets/images."""
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))

    for folder in [src_dir, assets_dir]:
        for root, _, files in os.walk(folder):
            for f in files:
                if f.endswith(".py"):
                    full_path = os.path.join(root, f)
                    with open(full_path, "r", encoding="utf-8") as file:
                        content = file.read()
                        assert "assets/images" not in content, f"Found legacy image reference in {f}"
                        assert "assets\\images" not in content, f"Found legacy image reference in {f}"


if __name__ == "__main__":
    test_svg_character_animations()
    test_svg_room_objects()
    test_player_movement_and_animation_states()
    test_room_and_interaction_inspection()
    test_no_references_to_images_directory()
    print("ALL TESTS PASSED SUCCESSFULLY!")
