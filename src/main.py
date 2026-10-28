"""
Case Unknown — Main Game Application.

A 2D single-player detective mystery game built with pure Python, Pygame, and SVG vector graphics.
Strictly adheres to directives.txt:
- Progression through narrative understanding and world unlocking (no traditional RPG XP).
- Evidence states: Undiscovered -> Discovered -> Recorded -> Connected.
- Level 1 Investigation: The Silent Witness (4 interconnected rooms).
- Inspection panel with full readable transcripts and recorded indicators.
- 3-tab Evidence Journal: Discovered Evidence, Clue Connections, Active Leads.
- Local JSON save/load persistence.
"""

from __future__ import annotations
import sys
import os

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TITLE,
    COLOR_BG,
    UI_PANEL_BG,
    UI_PANEL_BORDER,
    UI_TEXT_TITLE,
    FULLSCREEN,
    STATE_MENU,
    STATE_PLAYING,
    STATE_PUZZLE,
    STATE_MAP,
    STATE_JOURNAL,
    STATE_REVEAL,
)
from src.player import Player
from src.room import Room
from src.rooms_data import ROOMS_DATA
from src.interaction import InteractionManager
from src.treasure import TreasureManager
from src.map_view import PrecinctMapView
from src.menu import MenuSystem
from src.evidence_manager import EvidenceManager
from src.journal_view import JournalView
from src.save_manager import SaveManager
from src.evidence_reveal import EvidenceRevealModal
from src.puzzles import NumberLockPuzzle


def main():
    pygame.init()
    pygame.font.init()

    flags = pygame.SCALED
    if FULLSCREEN:
        flags |= pygame.FULLSCREEN

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Core Investigative Systems
    evidence_mgr = EvidenceManager()
    save_mgr = SaveManager()
    treasure_mgr = TreasureManager()
    interaction_mgr = InteractionManager(evidence_mgr)
    journal_view = JournalView(evidence_mgr)
    menu = MenuSystem(treasure_mgr, evidence_mgr=evidence_mgr)
    map_view = PrecinctMapView(treasure_mgr)

    # Initial State: Attempt to load saved progress or start in Level 1 Room 1 (directives.txt §4)
    saved_state = save_mgr.load_game(evidence_mgr)
    if saved_state:
        current_room_id = saved_state["current_room_id"]
        visited_rooms = saved_state["visited_rooms"]
        player = Player(start_x=saved_state["player_pos"][0], start_y=saved_state["player_pos"][1])
        has_active_game = True
    else:
        current_room_id = "crime_scene"
        visited_rooms = {current_room_id}
        player = Player(start_x=SCREEN_WIDTH // 2, start_y=420)
        has_active_game = False

    room_data = ROOMS_DATA.get(current_room_id, ROOMS_DATA["crime_scene"])
    room = Room(interaction_mgr, current_room_id, room_data, treasure_mgr, evidence_mgr=evidence_mgr)

    active_puzzle = None
    active_treasure_id = None
    active_door_gate_id = None
    active_door_wall = None
    door_hints_shown = set()
    pending_passage_notice = None
    passage_notice_idle = 0.0
    active_reveal = None
    game_state = STATE_MENU

    running = True

    while running:
        delta_time = clock.tick(FPS) / 1000.0
        delta_time = min(delta_time, 0.05)

        # =============================================================
        # 1. EVENT PROCESSING
        # =============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            # Global display toggle
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_F11, pygame.K_f):
                pygame.display.toggle_fullscreen()
                continue

            # ---------------------------------------------------------
            # State: MENU
            # ---------------------------------------------------------
            if game_state == STATE_MENU:
                action = menu.handle_event(event, has_active_game)
                if action == "RESUME":
                    game_state = STATE_PLAYING
                elif action == "NEW_GAME":
                    evidence_mgr = EvidenceManager()
                    interaction_mgr.set_evidence_manager(evidence_mgr)
                    journal_view = JournalView(evidence_mgr)
                    menu.evidence_mgr = evidence_mgr
                    current_room_id = "crime_scene"
                    visited_rooms = {current_room_id}
                    room = Room(
                        interaction_mgr,
                        current_room_id,
                        ROOMS_DATA[current_room_id],
                        treasure_mgr,
                        evidence_mgr=evidence_mgr,
                    )
                    player = Player(start_x=SCREEN_WIDTH // 2, start_y=420)
                    has_active_game = True
                    game_state = STATE_PLAYING
                    save_mgr.save_game(current_room_id, (player.pos.x, player.pos.y), visited_rooms, evidence_mgr)
                elif action == "MAP":
                    game_state = STATE_MAP
                elif action == "JOURNAL":
                    game_state = STATE_JOURNAL
                elif action == "QUIT":
                    running = False
                    break

            # ---------------------------------------------------------
            # State: JOURNAL
            # ---------------------------------------------------------
            elif game_state == STATE_JOURNAL:
                if journal_view.handle_event(event):
                    game_state = STATE_PLAYING if has_active_game else STATE_MENU

            # ---------------------------------------------------------
            # State: MAP
            # ---------------------------------------------------------
            elif game_state == STATE_MAP:
                if map_view.handle_event(event):
                    game_state = STATE_PLAYING if has_active_game else STATE_MENU

            # ---------------------------------------------------------
            # State: PUZZLE
            # ---------------------------------------------------------
            elif game_state == STATE_PUZZLE:
                if active_puzzle:
                    active_puzzle.handle_event(event)
                    if active_puzzle.is_closed:
                        if active_door_gate_id:
                            if active_door_wall == "right":
                                player.pos.x -= 28
                            elif active_door_wall == "left":
                                player.pos.x += 28
                            elif active_door_wall == "top":
                                player.pos.y += 28
                            elif active_door_wall == "bottom":
                                player.pos.y -= 28
                            player.update_rects()
                        active_door_gate_id = None
                        active_door_wall = None
                        active_puzzle = None
                        active_treasure_id = None
                        game_state = STATE_PLAYING
                    elif active_puzzle.is_solved and active_door_gate_id:
                        evidence_mgr.unlocked_gates.add(active_door_gate_id)
                        evidence_mgr._queue_toast("PASSAGE UNLOCKED", "The keypad clicks open.")
                        active_door_gate_id = None
                        active_door_wall = None
                        active_puzzle = None
                        game_state = STATE_PLAYING
                    elif active_puzzle.is_solved and active_treasure_id:
                        treasure_mgr.unlock_treasure(active_treasure_id)
                        item = treasure_mgr.get_treasure(active_treasure_id)
                        room = Room(
                            interaction_mgr,
                            current_room_id,
                            ROOMS_DATA[current_room_id],
                            treasure_mgr,
                            evidence_mgr=evidence_mgr,
                        )
                        active_puzzle = None
                        active_treasure_id = None
                        if item:
                            active_reveal = EvidenceRevealModal(item)
                            game_state = STATE_REVEAL
                        else:
                            game_state = STATE_PLAYING

            # ---------------------------------------------------------
            # State: REVEAL
            # ---------------------------------------------------------
            elif game_state == STATE_REVEAL:
                if active_reveal:
                    if active_reveal.handle_event(event) or active_reveal.is_closed:
                        active_reveal = None
                        game_state = STATE_PLAYING

            # ---------------------------------------------------------
            # State: PLAYING
            # ---------------------------------------------------------
            elif game_state == STATE_PLAYING:
                # Key shortcuts
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = STATE_MENU
                        continue
                    elif event.key == pygame.K_j:
                        game_state = STATE_JOURNAL
                        continue
                    elif event.key in (pygame.K_m, pygame.K_TAB):
                        game_state = STATE_MAP
                        continue

                # Interaction modal / dialogue handling
                consumed = interaction_mgr.handle_event(event)
                if consumed and interaction_mgr.trigger_puzzle_request:
                    t_id = interaction_mgr.trigger_puzzle_request
                    interaction_mgr.trigger_puzzle_request = None
                    active_puzzle = treasure_mgr.create_puzzle(t_id)
                    if active_puzzle:
                        active_treasure_id = t_id
                        game_state = STATE_PUZZLE

        # =============================================================
        # 2. UPDATE GAME LOGIC
        # =============================================================
        evidence_mgr.update(delta_time)

        if game_state == STATE_MENU:
            menu.update(delta_time)

        elif game_state == STATE_MAP:
            map_view.update(delta_time)

        elif game_state == STATE_PUZZLE:
            if active_puzzle:
                active_puzzle.update(delta_time)

        elif game_state == STATE_REVEAL:
            if active_reveal:
                active_reveal.update(delta_time)
                if active_reveal.is_closed:
                    active_reveal = None
                    game_state = STATE_PLAYING

        elif game_state == STATE_PLAYING:
            if interaction_mgr.is_inspecting:
                player.state = "idle"
                player.velocity = pygame.Vector2(0, 0)
            else:
                player.handle_input()

            player.update(delta_time, room.solid_objects)
            interaction_mgr.update(delta_time, player.get_interaction_reach())

            # Door locks use found keys and keypad codes. Delay a blocked-door
            # notice until one second after the player stops trying.
            door = room.check_door_transitions(player.hitbox)
            if door and door.get("door_code"):
                locked_door = door["door"]
                active_door_gate_id = locked_door["gate_id"]
                active_door_wall = locked_door["wall"]
                active_puzzle = NumberLockPuzzle(
                    title="East Passage Keypad",
                    target_code=locked_door["pin_code"],
                    hint=locked_door.get("door_hint", "Examine the room for a clue."),
                    reward_name="Recording Room Access",
                )
                if active_door_gate_id not in door_hints_shown:
                    evidence_mgr._queue_toast(
                        "KEYPAD LOCKED",
                        "The keypad needs a code. Press H for a hint.",
                    )
                    door_hints_shown.add(active_door_gate_id)
                pending_passage_notice = None
                game_state = STATE_PUZZLE
            elif door and door.get("blocked"):
                msg = door["door"].get("gate_msg", "This passage is locked.")
                pending_passage_notice = ("PASSAGE RESTRICTED", msg)
                passage_notice_idle = 0.0
                wall = door["door"]["wall"]
                if wall == "right":
                    player.pos.x -= 16
                elif wall == "left":
                    player.pos.x += 16
                elif wall == "top":
                    player.pos.y += 16
                elif wall == "bottom":
                    player.pos.y -= 16
                player.update_rects()
            elif door:
                pending_passage_notice = None
                current_room_id = door["target_room"]
                visited_rooms.add(current_room_id)
                player.pos = pygame.Vector2(*door["target_pos"])
                player.update_rects()
                target_data = ROOMS_DATA.get(current_room_id, ROOMS_DATA["crime_scene"])
                room = Room(interaction_mgr, current_room_id, target_data, treasure_mgr, evidence_mgr=evidence_mgr)
                save_mgr.save_game(current_room_id, (player.pos.x, player.pos.y), visited_rooms, evidence_mgr)
            elif pending_passage_notice:
                passage_notice_idle += delta_time
                if passage_notice_idle >= 1.0:
                    title, msg = pending_passage_notice
                    evidence_mgr._queue_toast(title, msg)
                    pending_passage_notice = None

        # =============================================================
        # 3. RENDERING
        # =============================================================
        if game_state == STATE_MENU:
            menu.draw(screen, has_active_game)

        elif game_state in (STATE_PLAYING, STATE_PUZZLE, STATE_MAP, STATE_REVEAL, STATE_JOURNAL):
            screen.fill(COLOR_BG)

            # 3.1 Room Environment & Decor
            room.draw_background(screen)

            # 3.2 Depth-Sorted Entities
            draw_queue = []
            for item in room.furniture_items:
                draw_queue.append({
                    "sort_y": item["sort_y"],
                    "draw": lambda surf=item["surface"], rect=item["rect"]: screen.blit(surf, rect),
                })
            draw_queue.append({
                "sort_y": player.hitbox.bottom,
                "draw": lambda: player.draw(screen),
            })
            draw_queue.sort(key=lambda x: x["sort_y"])

            for element in draw_queue:
                element["draw"]()

            # 3.3 Atmospheric Lighting
            room.draw_lighting(screen)

            # 3.4 Floating Prompts & Inspection Panel
            if game_state == STATE_PLAYING:
                interaction_mgr.draw_prompt(screen)
                interaction_mgr.draw_dialogue(screen)

            # 3.6 Modals
            if game_state == STATE_JOURNAL:
                journal_view.render(screen)

            elif game_state == STATE_PUZZLE and active_puzzle:
                active_puzzle.draw(screen)

            elif game_state == STATE_MAP:
                map_view.draw(screen, current_room_id, visited_rooms)

            elif game_state == STATE_REVEAL and active_reveal:
                active_reveal.draw(screen)

            # 3.7 Subtle Journal Toast Notification (§2.3)
            evidence_mgr.render_toast(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
