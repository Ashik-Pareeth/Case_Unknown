"""
Headless preview renderer generating screenshots of all rooms, the blueprint map,
the puzzles, and the main menu for visual verification.
"""

import os
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BG
from src.rooms_data import ROOMS_DATA
from src.room import Room
from src.player import Player
from src.interaction import InteractionManager
from src.treasure import TreasureManager
from src.map_view import PrecinctMapView
from src.menu import MenuSystem


def render_all_previews():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "output"))
    os.makedirs(output_dir, exist_ok=True)

    treasure_mgr = TreasureManager()
    interaction_mgr = InteractionManager()

    # 1. Render all 5 rooms
    for r_id in ["office", "archive", "morgue", "lockup", "interrogation"]:
        screen.fill(COLOR_BG)
        room = Room(interaction_mgr, r_id, ROOMS_DATA[r_id], treasure_mgr)
        player = Player(start_x=SCREEN_WIDTH // 2, start_y=380)

        room.draw_background(screen)
        # Depth-sorted entities
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
        for el in draw_queue:
            el["draw"]()

        room.draw_lighting(screen)
        interaction_mgr.draw_prompt(screen)

        filepath = os.path.join(output_dir, f"preview_room_{r_id}.png")
        pygame.image.save(screen, filepath)
        print(f"Saved room preview: {filepath}")

    # 2. Render Blueprint Map View
    map_view = PrecinctMapView(treasure_mgr)
    map_view.draw(screen, "office", {"office", "archive", "morgue"})
    map_path = os.path.join(output_dir, "preview_blueprint_map.png")
    pygame.image.save(screen, map_path)
    print(f"Saved map preview: {map_path}")

    # 3. Render Number Lock Puzzle
    screen.fill(COLOR_BG)
    room = Room(interaction_mgr, "office", ROOMS_DATA["office"], treasure_mgr)
    room.draw_background(screen)
    num_puzzle = treasure_mgr.create_puzzle("office_safe")
    num_puzzle.show_hint = True
    num_puzzle.draw(screen)
    num_path = os.path.join(output_dir, "preview_puzzle_number_lock.png")
    pygame.image.save(screen, num_path)
    print(f"Saved number lock puzzle preview: {num_path}")

    # 4. Render Tile Align Puzzle
    screen.fill(COLOR_BG)
    tile_puzzle = treasure_mgr.create_puzzle("archive_vault")
    tile_puzzle.show_hint = True
    tile_puzzle.draw(screen)
    tile_path = os.path.join(output_dir, "preview_puzzle_tile_align.png")
    pygame.image.save(screen, tile_path)
    print(f"Saved tile align puzzle preview: {tile_path}")

    # 5. Render Main Menu
    menu = MenuSystem(treasure_mgr)
    menu.draw(screen, has_active_game=True)
    menu_path = os.path.join(output_dir, "preview_main_menu.png")
    pygame.image.save(screen, menu_path)
    print(f"Saved menu preview: {menu_path}")

    # 6. Render Evidence Dossier Screen
    exp_mgr = ExperienceManager()
    exp_mgr.add_experience(150, "Recovered Keycard")
    treasure_mgr.unlock_treasure("office_safe")
    menu = MenuSystem(treasure_mgr, exp_mgr)
    menu.current_screen = "EVIDENCE"
    menu.draw(screen, has_active_game=True)
    dossier_path = os.path.join(output_dir, "preview_evidence_dossier.png")
    pygame.image.save(screen, dossier_path)
    print(f"Saved evidence dossier preview: {dossier_path}")

    # 7. Render In-Game Screen with Dual HUD and EXP Toast Notification
    screen.fill(COLOR_BG)
    room = Room(interaction_mgr, "office", ROOMS_DATA["office"], treasure_mgr)
    player = Player(start_x=SCREEN_WIDTH // 2, start_y=380)
    room.draw_background(screen)
    player.draw(screen)
    room.draw_lighting(screen)

    # Top HUD
    from src.settings import ROOM_X, ROOM_Y, UI_ACCENT_GOLD
    hud_font = pygame.font.SysFont("georgia", 13, bold=True)
    hud_sub_font = pygame.font.SysFont("segoeui", 11)
    hud_w = 460
    hud_h = 32
    hud_surf = pygame.Surface((hud_w, hud_h), pygame.SRCALPHA)
    hud_surf.fill((16, 18, 22, 220))
    pygame.draw.rect(hud_surf, (80, 70, 52), (0, 0, hud_w, hud_h), 1, border_radius=4)
    screen.blit(hud_surf, (ROOM_X, ROOM_Y - 42))

    prog_pct = treasure_mgr.get_progress_percentage()
    sub_text = hud_sub_font.render(f"Evidence: 1/5 ({prog_pct}%)", True, UI_ACCENT_GOLD)
    sub_x = ROOM_X + hud_w - sub_text.get_width() - 12
    screen.blit(sub_text, (sub_x, ROOM_Y - 36))

    max_title_w = (sub_x - (ROOM_X + 12)) - 14
    title_str = room.name.upper()
    if hud_font.size(title_str)[0] > max_title_w:
        while title_str and hud_font.size(title_str + "...")[0] > max_title_w:
            title_str = title_str[:-1]
        title_str += "..."
    status_text = hud_font.render(title_str, True, (225, 195, 135))
    screen.blit(status_text, (ROOM_X + 12, ROOM_Y - 37))

    exp_mgr.draw_hud_widget(screen, ROOM_X + hud_w + 12, ROOM_Y - 42, width=228, height=32)
    exp_mgr.update(0.016)
    exp_mgr.draw_notification(screen)

    hud_path = os.path.join(output_dir, "preview_hud_with_exp.png")
    pygame.image.save(screen, hud_path)
    print(f"Saved HUD with EXP preview: {hud_path}")

    # 8. Render Evidence Reveal Modal (Manila Folder + Crime Scene Polaroid Photo)
    from src.evidence_reveal import EvidenceRevealModal
    screen.fill(COLOR_BG)
    room.draw_background(screen)
    item = treasure_mgr.get_treasure("office_safe")
    reveal_modal = EvidenceRevealModal(item, exp_mgr)
    reveal_modal.anim_time = 0.5  # Fully popped in
    reveal_modal.draw(screen)

    reveal_path = os.path.join(output_dir, "preview_evidence_reveal.png")
    pygame.image.save(screen, reveal_path)
    print(f"Saved evidence reveal modal preview: {reveal_path}")


if __name__ == "__main__":
    from src.experience import ExperienceManager
    render_all_previews()
