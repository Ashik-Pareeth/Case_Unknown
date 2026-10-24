"""
Case Unknown — Main Game Application.

A 2D detective mystery game built with pure Python, Pygame, and SVG vector graphics.
Features:
- Reusable, customizable room system across 5 interconnected sectors.
- Real-time blueprint precinct floor plan map tracking player location & treasure status.
- Environmental treasure points with rotary Number Lock and Tile Alignment puzzles.
- Integrated Main & Pause Menu system with New Game, Resume, Dossier, and Controls.
"""

import sys
import os

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ROOM_X,
    ROOM_Y,
    FPS,
    TITLE,
    COLOR_BG,
    UI_PANEL_BG,
    UI_PANEL_BORDER,
    UI_TEXT_TITLE,
    UI_TEXT_MUTED,
    UI_ACCENT_GOLD,
    FULLSCREEN,
    STATE_MENU,
    STATE_PLAYING,
    STATE_PUZZLE,
    STATE_MAP,
    STATE_REVEAL,
)
from src.player import Player
from src.room import Room
from src.rooms_data import ROOMS_DATA
from src.interaction import InteractionManager
from src.treasure import TreasureManager
from src.map_view import PrecinctMapView
from src.menu import MenuSystem
from src.experience import ExperienceManager
from src.evidence_reveal import EvidenceRevealModal


def main():
    pygame.init()
    pygame.font.init()

    flags = pygame.SCALED
    if FULLSCREEN:
        flags |= pygame.FULLSCREEN

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Core Systems
    exp_mgr = ExperienceManager()
    treasure_mgr = TreasureManager()
    interaction_mgr = InteractionManager()
    menu = MenuSystem(treasure_mgr, exp_mgr)
    map_view = PrecinctMapView(treasure_mgr)

    # Initial State
    current_room_id = "office"
    visited_rooms = {current_room_id}
    room = Room(interaction_mgr, current_room_id, ROOMS_DATA[current_room_id], treasure_mgr)
    player = Player(start_x=SCREEN_WIDTH // 2, start_y=420)

    active_puzzle = None
    active_treasure_id = None
    active_reveal = None
    has_active_game = False
    game_state = STATE_MENU

    # HUD Fonts
    hud_font = pygame.font.SysFont("georgia", 13, bold=True)
    hud_sub_font = pygame.font.SysFont("segoeui", 11)
    ctrl_font = pygame.font.SysFont("segoeui", 12)

    running = True

    while running:
        delta_time = clock.tick(FPS) / 1000.0
        delta_time = min(delta_time, 0.05)

        # =============================================================
        # 1. EVENT HANDLING
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
                    exp_mgr = ExperienceManager()
                    treasure_mgr = TreasureManager()
                    menu.treasure_mgr = treasure_mgr
                    menu.exp_mgr = exp_mgr
                    map_view.treasure_mgr = treasure_mgr
                    current_room_id = "office"
                    visited_rooms = {current_room_id}
                    room = Room(interaction_mgr, current_room_id, ROOMS_DATA[current_room_id], treasure_mgr)
                    player = Player(start_x=SCREEN_WIDTH // 2, start_y=420)
                    has_active_game = True
                    game_state = STATE_PLAYING
                elif action == "MAP":
                    game_state = STATE_MAP
                elif action == "QUIT":
                    running = False
                    break

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
                        active_puzzle = None
                        active_treasure_id = None
                        game_state = STATE_PLAYING
                    elif active_puzzle.is_solved and active_treasure_id:
                        treasure_mgr.unlock_treasure(active_treasure_id)
                        item = treasure_mgr.get_treasure(active_treasure_id)
                        # Re-setup room interactables to reflect unlocked state
                        room = Room(interaction_mgr, current_room_id, ROOMS_DATA[current_room_id], treasure_mgr)
                        active_puzzle = None
                        active_treasure_id = None
                        if item:
                            exp_mgr.add_experience(150, f"Recovered {item.reward_name}")
                            active_reveal = EvidenceRevealModal(item, exp_mgr)
                            game_state = STATE_REVEAL
                        else:
                            game_state = STATE_PLAYING

            # ---------------------------------------------------------
            # State: REVEAL (Evidence Recovered Document & Photo Modal)
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
        exp_mgr.update(delta_time)

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

            # Check Doorway transitions
            door = room.check_door_transitions(player.hitbox)
            if door:
                current_room_id = door["target_room"]
                visited_rooms.add(current_room_id)
                player.pos = pygame.Vector2(*door["target_pos"])
                player.update_rects()
                room = Room(interaction_mgr, current_room_id, ROOMS_DATA[current_room_id], treasure_mgr)

        # =============================================================
        # 3. RENDERING
        # =============================================================
        if game_state == STATE_MENU:
            menu.draw(screen, has_active_game)

        elif game_state in (STATE_PLAYING, STATE_PUZZLE, STATE_MAP, STATE_REVEAL):
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

            # 3.4 Floating Prompts & Dialogue
            if game_state == STATE_PLAYING:
                interaction_mgr.draw_prompt(screen)
                interaction_mgr.draw_dialogue(screen)

            # 3.5 Top HUD Bar (Case Status, Sector Name, Progress)
            hud_w = 460
            hud_h = 32
            hud_surf = pygame.Surface((hud_w, hud_h), pygame.SRCALPHA)
            hud_surf.fill((16, 18, 22, 220))
            pygame.draw.rect(hud_surf, (80, 70, 52), (0, 0, hud_w, hud_h), 1, border_radius=4)
            screen.blit(hud_surf, (ROOM_X, ROOM_Y - 42))

            prog_pct = treasure_mgr.get_progress_percentage()
            sub_text = hud_sub_font.render(
                f"Evidence: {len(treasure_mgr.get_all_unlocked())}/{len(treasure_mgr.treasures)} ({prog_pct}%)",
                True,
                UI_ACCENT_GOLD,
            )
            sub_x = ROOM_X + hud_w - sub_text.get_width() - 12
            screen.blit(sub_text, (sub_x, ROOM_Y - 36))

            # Sector Title (Dynamically bounded to prevent overlap with Evidence count)
            max_title_w = (sub_x - (ROOM_X + 12)) - 14
            title_str = room.name.upper()
            if hud_font.size(title_str)[0] > max_title_w:
                while title_str and hud_font.size(title_str + "...")[0] > max_title_w:
                    title_str = title_str[:-1]
                title_str += "..."
            status_text = hud_font.render(title_str, True, (225, 195, 135))
            screen.blit(status_text, (ROOM_X + 12, ROOM_Y - 37))

            # Top Right EXP Progress & Detective Rank Widget
            exp_mgr.draw_hud_widget(screen, ROOM_X + hud_w + 12, ROOM_Y - 42, width=228, height=32)

            # Bottom Controls Hint Bar
            ctrl_w = 540
            ctrl_h = 24
            ctrl_surf = pygame.Surface((ctrl_w, ctrl_h), pygame.SRCALPHA)
            ctrl_surf.fill((16, 18, 22, 190))
            pygame.draw.rect(ctrl_surf, (60, 55, 45), (0, 0, ctrl_w, ctrl_h), 1, border_radius=3)
            screen.blit(ctrl_surf, (SCREEN_WIDTH - ctrl_w - ROOM_X, SCREEN_HEIGHT - 32))

            hint_text = ctrl_font.render(
                "[WASD] Move   [E] Inspect / Unlock   [M] Map   [ESC] Menu   [F11] Fullscreen",
                True,
                UI_TEXT_MUTED,
            )
            screen.blit(hint_text, (SCREEN_WIDTH - ctrl_w - ROOM_X + 12, SCREEN_HEIGHT - 28))

            # 3.6 Modals (Puzzle / Map / Evidence Reveal)
            if game_state == STATE_PUZZLE and active_puzzle:
                active_puzzle.draw(screen)

            elif game_state == STATE_MAP:
                map_view.draw(screen, current_room_id, visited_rooms)

            elif game_state == STATE_REVEAL and active_reveal:
                active_reveal.draw(screen)

            # 3.7 Celebratory Toast Notification
            exp_mgr.draw_notification(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
