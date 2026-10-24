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

    # Test dialogue drawing
    test_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    interaction_mgr.draw_dialogue(test_surf)

    # Simulate pressing 'E' again to close inspection dialogue
    consumed_close = interaction_mgr.handle_event(event_e)
    assert consumed_close is True
    assert interaction_mgr.is_inspecting is False

    # Test prompt drawing when active object is present
    interaction_mgr.draw_prompt(test_surf)



def test_reusable_multiple_rooms_and_doors():
    """Verify that the reusable Room class initializes all 5 sectors with doors and collision."""
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    from src.rooms_data import ROOMS_DATA
    from src.treasure import TreasureManager

    treasure_mgr = TreasureManager()
    interaction_mgr = InteractionManager()

    room_ids = ["office", "archive", "morgue", "lockup", "interrogation"]
    for r_id in room_ids:
        r = Room(interaction_mgr, r_id, ROOMS_DATA[r_id], treasure_mgr)
        assert r.room_id == r_id
        assert len(r.solid_objects) >= 4  # Boundary walls + furniture
        assert len(r.furniture_items) >= 2
        # Check doorways
        if r_id == "office":
            assert len(r.doorways) == 2  # right and bottom
        elif r_id == "archive":
            assert len(r.doorways) == 3  # left, top, right

        # Verify door trigger detection
        if r.doorways:
            door = r.doorways[0]
            # Place test rect on the door trigger
            transition = r.check_door_transitions(door["trigger_rect"])
            assert transition is not None
            assert transition["target_room"] == door["target_room"]


def test_treasure_manager_and_puzzles():
    """Verify treasure manager tracking, puzzle creation, and puzzle solving logic."""
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    from src.treasure import TreasureManager
    from src.puzzles import NumberLockPuzzle, TileAlignPuzzle

    tm = TreasureManager()
    assert len(tm.treasures) == 5
    assert tm.get_progress_percentage() == 0

    # 1. Test Number Lock Puzzle
    p1 = tm.create_puzzle("office_safe")
    assert isinstance(p1, NumberLockPuzzle)
    assert p1.is_solved is False

    # Simulate incorrect code
    p1.current_code = [0, 0, 0]
    p1.check_solution()
    assert p1.is_solved is False

    # Simulate correct code
    p1.current_code = [1, 9, 2]
    p1.check_solution()
    assert p1.is_solved is True

    # Unlock in manager
    tm.unlock_treasure("office_safe")
    assert tm.is_unlocked("office_safe") is True
    assert tm.get_progress_percentage() == 20

    # 2. Test Tile Align Puzzle
    p2 = tm.create_puzzle("archive_vault")
    assert isinstance(p2, TileAlignPuzzle)
    assert p2.is_solved is False

    # Correct alignment
    p2.current_angles = [0, 90, 180, 270]
    p2.check_solution()
    assert p2.is_solved is True

    tm.unlock_treasure("archive_vault")
    assert tm.get_progress_percentage() == 40


def test_blueprint_map_view():
    """Verify the blueprint map renders without errors and contains all sector nodes."""
    pygame.init()
    surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    from src.treasure import TreasureManager
    from src.map_view import PrecinctMapView

    tm = TreasureManager()
    map_view = PrecinctMapView(tm)

    assert len(map_view.room_nodes) == 5
    assert set(map_view.room_nodes.keys()) == {"office", "archive", "morgue", "lockup", "interrogation"}

    # Draw map
    map_view.draw(surf, "office", {"office", "archive"})

    # Test event handling
    event_m = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_m})
    assert map_view.handle_event(event_m) is True


def test_menu_system_navigation():
    """Verify MenuSystem options, input handling, and screen switching."""
    pygame.init()
    surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    from src.treasure import TreasureManager
    from src.menu import MenuSystem

    tm = TreasureManager()
    menu = MenuSystem(tm)

    # Initial state
    assert menu.current_screen == "MAIN"

    # When no active game, RESUME is disabled
    action_resume = menu.handle_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}), has_active_game=False)
    # Selected index initially is 0 (RESUME), so pressing enter when disabled should return None
    assert action_resume is None

    # New game selection
    menu.selected_idx = 1  # NEW_GAME
    action_new = menu.handle_event(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}), has_active_game=False)
    assert action_new == "NEW_GAME"

    # Draw menu
    menu.draw(surf, has_active_game=True)


def test_experience_system():
    """Verify player EXP progression, level promotion thresholds, and HUD widgets."""
    pygame.init()
    surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    from src.experience import ExperienceManager

    exp = ExperienceManager()
    lvl, rank = exp.level_and_rank
    assert lvl == 1
    assert rank == "Junior Trainee"
    assert exp.total_exp == 0

    # Progress at lvl 1
    cur, needed, ratio = exp.get_level_progress()
    assert cur == 0
    assert needed == 150
    assert ratio == 0.0

    # Gain 150 EXP -> Promote to LVL 2 Field Detective
    res = exp.add_experience(150, "Recovered Keycard")
    assert res["total_exp"] == 150
    assert res["leveled_up"] is True
    assert res["new_level"] == 2
    assert res["rank"] == "Field Detective"

    # Gain 150 EXP -> LVL 3 Senior Investigator
    res2 = exp.add_experience(150, "Recovered Syndicate Ledger")
    assert res2["new_level"] == 3
    assert res2["rank"] == "Senior Investigator"

    # Update timers and draw notifications & HUD widget
    exp.update(0.016)
    assert exp.active_notification is not None
    exp.draw_notification(surf)
    exp.draw_hud_widget(surf, 50, 10, width=220, height=32)


def test_evidence_reveal_modal():
    """Verify animated confidential evidence and crime scene photo reveal modal."""
    pygame.init()
    surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    from src.treasure import TreasureManager
    from src.experience import ExperienceManager
    from src.evidence_reveal import EvidenceRevealModal

    tm = TreasureManager()
    exp = ExperienceManager()

    for item_id, item in tm.treasures.items():
        modal = EvidenceRevealModal(item, exp)
        assert modal.is_closed is False
        assert modal.item.item_id == item_id

        # Update animation ticks
        modal.update(0.3)
        assert modal.anim_time >= 0.3

        # Draw modal with polaroid photo artwork and typewriter text
        modal.draw(surf)

        # Handle dismiss event (Spacebar)
        event_space = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})
        consumed = modal.handle_event(event_space)
        assert consumed is True
        assert modal.is_closed is True


def test_text_overflow_fixes():
    """Verify that long dialogue, long puzzle hints, and dossier cards wrap without crashing."""
    pygame.init()
    surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    from src.interaction import InteractionManager, Interactable
    from src.treasure import TreasureManager
    from src.menu import MenuSystem
    from src.experience import ExperienceManager
    from src.puzzles import NumberLockPuzzle

    # 1. Very long dialogue in dialogue box
    im = InteractionManager()
    long_desc = "A" * 50 + " " + "B" * 50 + " " + "This is an extremely long multi-line description that should wrap properly across many lines." * 3
    obj = Interactable("long_obj", "Extremely Long Object Name Over 40 Characters", long_desc, pygame.Rect(10, 10, 20, 20), (10, 10))
    im.active_object = obj
    im.is_inspecting = True
    im.draw_dialogue(surf)

    # 2. Very long hint in NumberLockPuzzle
    p = NumberLockPuzzle(
        title="Test Lock",
        target_code=[1, 2, 3],
        hint="This is a very long hint that previously caused text box overflowing because it exceeded the modal width boundary." * 2,
        reward_name="Reward Item"
    )
    p.show_hint = True
    p.draw(surf)

    # 3. Evidence dossier cards with both locked and unlocked items
    tm = TreasureManager()
    tm.unlock_treasure("office_safe")
    tm.unlock_treasure("archive_vault")
    exp = ExperienceManager()
    menu = MenuSystem(tm, exp)
    menu.current_screen = "EVIDENCE"
    menu.draw(surf, has_active_game=True)


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
    test_reusable_multiple_rooms_and_doors()
    test_treasure_manager_and_puzzles()
    test_blueprint_map_view()
    test_menu_system_navigation()
    test_no_references_to_images_directory()
    test_experience_system()
    test_evidence_reveal_modal()
    test_text_overflow_fixes()
    print("ALL TESTS PASSED SUCCESSFULLY!")


