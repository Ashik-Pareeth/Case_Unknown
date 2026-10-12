"""
Case Unknown — Main Game Application.

A 2D detective mystery game built with Pygame and pure SVG vector assets.
"""

import sys
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
)
from src.player import Player
from src.room import Room
from src.interaction import InteractionManager


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Systems
    interaction_mgr = InteractionManager()
    room = Room(interaction_mgr)
    # Starting position: near center-bottom of the office
    player = Player(start_x=SCREEN_WIDTH // 2, start_y=420)

    # UI Fonts for HUD
    hud_font = pygame.font.SysFont("georgia", 13, bold=True)
    ctrl_font = pygame.font.SysFont("segoeui", 12)

    running = True

    while running:
        delta_time = clock.tick(FPS) / 1000.0
        # Clamp delta_time to avoid large physics steps on window drags
        delta_time = min(delta_time, 0.05)

        # -------------------------------------------------------------
        # 1. Event Handling
        # -------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            # Let interaction modal intercept inputs
            consumed = interaction_mgr.handle_event(event)
            if not consumed and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # -------------------------------------------------------------
        # 2. Update Game State
        # -------------------------------------------------------------
        if interaction_mgr.is_inspecting:
            # Freeze player movement while reading case clues
            player.state = "idle"
            player.velocity = pygame.Vector2(0, 0)
        else:
            player.handle_input()

        player.update(delta_time, room.solid_objects)
        interaction_mgr.update(delta_time, player.get_interaction_reach())

        # -------------------------------------------------------------
        # 3. Drawing & Layered Z-Sorting
        # -------------------------------------------------------------
        screen.fill(COLOR_BG)

        # 3.1 Room Floor, Walls & Wall Decor
        room.draw_background(screen)

        # 3.2 Depth-Sorted Entities (Player + Furniture)
        draw_queue = []

        # Add furniture
        for item in room.furniture_items:
            draw_queue.append({
                "sort_y": item["sort_y"],
                "draw": lambda surf=item["surface"], rect=item["rect"]: screen.blit(surf, rect),
            })

        # Add player
        draw_queue.append({
            "sort_y": player.hitbox.bottom,
            "draw": lambda: player.draw(screen),
        })

        # Sort ascending by foot/bottom Y position
        draw_queue.sort(key=lambda x: x["sort_y"])

        for element in draw_queue:
            element["draw"]()

        # 3.3 Atmospheric Ambient Lighting & Window Light Rays
        room.draw_lighting(screen)

        # 3.4 Interactive Floating Prompts & Modals
        interaction_mgr.draw_prompt(screen)
        interaction_mgr.draw_dialogue(screen)

        # 3.5 Top HUD Bar (Case Status & Controls)
        hud_badge_w = 420
        hud_badge_h = 28
        hud_surf = pygame.Surface((hud_badge_w, hud_badge_h), pygame.SRCALPHA)
        hud_surf.fill((16, 18, 22, 210))
        pygame.draw.rect(hud_surf, (80, 70, 52), (0, 0, hud_badge_w, hud_badge_h), 1, border_radius=4)
        screen.blit(hud_surf, (ROOM_X + 10, ROOM_Y - 38))

        status_text = hud_font.render("CASE UNKNOWN  |  PRECINCT OFFICE  —  TRAINEE DESK", True, (215, 185, 125))
        screen.blit(status_text, (ROOM_X + 22, ROOM_Y - 32))

        # Bottom Controls Hint
        ctrl_w = 340
        ctrl_h = 24
        ctrl_surf = pygame.Surface((ctrl_w, ctrl_h), pygame.SRCALPHA)
        ctrl_surf.fill((16, 18, 22, 180))
        pygame.draw.rect(ctrl_surf, (60, 55, 45), (0, 0, ctrl_w, ctrl_h), 1, border_radius=3)
        screen.blit(ctrl_surf, (SCREEN_WIDTH - ctrl_w - ROOM_X - 10, SCREEN_HEIGHT - 32))

        hint_text = ctrl_font.render("[WASD / ARROWS] Move    [E / SPACE] Inspect    [ESC] Quit", True, UI_TEXT_MUTED)
        screen.blit(hint_text, (SCREEN_WIDTH - ctrl_w - ROOM_X + 2, SCREEN_HEIGHT - 28))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
