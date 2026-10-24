"""
Precinct Blueprint Floor Plan Map Overlay for Case Unknown.

Renders an architectural blueprint of the precinct, illustrating interconnected rooms,
the player's current location, doorway corridors, and recovered/locked treasure points.
"""

import math
import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    UI_PANEL_BG,
    UI_PANEL_BORDER,
    UI_TEXT_TITLE,
    UI_TEXT_BODY,
    UI_TEXT_MUTED,
    UI_ACCENT_GOLD,
    UI_SUCCESS_GREEN,
    UI_HIGHLIGHT_RED,
)
from src.treasure import TreasureManager


class PrecinctMapView:
    """Renders the detective blueprint map of all connected precinct sectors."""

    def __init__(self, treasure_mgr: TreasureManager):
        self.treasure_mgr = treasure_mgr
        self.anim_time = 0.0

        # Modal bounds
        self.map_w = 780
        self.map_h = 520
        self.map_x = (SCREEN_WIDTH - self.map_w) // 2
        self.map_y = (SCREEN_HEIGHT - self.map_h) // 2
        self.map_rect = pygame.Rect(self.map_x, self.map_y, self.map_w, self.map_h)

        # Fonts
        pygame.font.init()
        self.font_title = pygame.font.SysFont("georgia", 22, bold=True)
        self.font_sub = pygame.font.SysFont("segoeui", 13)
        self.font_room_name = pygame.font.SysFont("georgia", 13, bold=True)
        self.font_room_sub = pygame.font.SysFont("segoeui", 11)
        self.font_status = pygame.font.SysFont("segoeui", 11, bold=True)
        self.font_legend = pygame.font.SysFont("segoeui", 12)

        # Blueprint room coordinates on map canvas
        # Layout:
        #           [Morgue]
        #              |
        # [Office] - [Archive] - [Interrogation]
        #              |
        #           [Lockup]
        cx = self.map_x + self.map_w // 2
        cy = self.map_y + self.map_h // 2 - 10
        rw = 185
        rh = 92

        self.room_nodes = {
            "morgue": {
                "name": "COLD STORAGE / MORGUE",
                "sub": "Sector 03 — Pathology",
                "rect": pygame.Rect(cx - rw // 2, cy - rh - 48, rw, rh),
                "treasure_id": "morgue_locker",
            },
            "office": {
                "name": "DETECTIVE OFFICE",
                "sub": "Sector 01 — Squad Room",
                "rect": pygame.Rect(cx - rw - rw // 2 - 40, cy - rh // 2, rw, rh),
                "treasure_id": "office_safe",
            },
            "archive": {
                "name": "EVIDENCE ARCHIVE",
                "sub": "Sector 02 — Central Vault",
                "rect": pygame.Rect(cx - rw // 2, cy - rh // 2, rw, rh),
                "treasure_id": "archive_vault",
            },
            "interrogation": {
                "name": "INTERROGATION ROOM",
                "sub": "Sector 05 — Witness Booth",
                "rect": pygame.Rect(cx + rw // 2 + 40, cy - rh // 2, rw, rh),
                "treasure_id": "interrogation_box",
            },
            "lockup": {
                "name": "DETENTION LOCKUP",
                "sub": "Sector 04 — Cell Block",
                "rect": pygame.Rect(cx - rw // 2, cy + rh // 2 + 48, rw, rh),
                "treasure_id": "lockup_stash",
            },
        }


        # Corridors connecting rooms
        self.corridors = [
            ("office", "archive"),
            ("archive", "morgue"),
            ("archive", "interrogation"),
            ("archive", "lockup"),
            ("office", "lockup"),
        ]

    def update(self, delta_time: float):
        self.anim_time += delta_time

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_m, pygame.K_ESCAPE, pygame.K_TAB):
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Clicking close button or outside
            return True
        return False

    def draw(self, surface: pygame.Surface, current_room_id: str, visited_rooms: set):
        # 1. Dark Blueprint Backdrop
        backdrop = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((6, 8, 12, 225))
        surface.blit(backdrop, (0, 0))

        # 2. Main Map Panel
        panel = pygame.Surface((self.map_w, self.map_h), pygame.SRCALPHA)
        panel.fill((16, 22, 30, 245))
        surface.blit(panel, (self.map_x, self.map_y))

        # 3. Blueprint Grid Lines
        grid_step = 26
        for gx in range(self.map_x, self.map_x + self.map_w, grid_step):
            pygame.draw.line(surface, (24, 34, 46), (gx, self.map_y), (gx, self.map_y + self.map_h), 1)
        for gy in range(self.map_y, self.map_y + self.map_h, grid_step):
            pygame.draw.line(surface, (24, 34, 46), (self.map_x, gy), (self.map_x + self.map_w, gy), 1)

        # 4. Antique Brass / Blueprint Border
        pygame.draw.rect(surface, (80, 140, 190), self.map_rect, 2, border_radius=6)
        pygame.draw.rect(surface, (40, 70, 95), self.map_rect.inflate(-8, -8), 1, border_radius=4)

        # Header Title
        title_surf = self.font_title.render("PRECINCT 13 — BLUEPRINT FLOOR PLAN", True, (215, 235, 255))
        surface.blit(title_surf, (self.map_x + 28, self.map_y + 18))

        sub_surf = self.font_sub.render(
            f"Case Progress: {self.treasure_mgr.get_progress_percentage()}% Unlocked   |   Press [M / ESC] to exit map",
            True,
            (140, 180, 215),
        )
        surface.blit(sub_surf, (self.map_x + 28, self.map_y + 48))

        # 5. Hallway Corridors
        for r1_key, r2_key in self.corridors:
            r1 = self.room_nodes[r1_key]["rect"]
            r2 = self.room_nodes[r2_key]["rect"]
            c1 = r1.center
            c2 = r2.center

            # Draw double-lined blueprint corridor
            pygame.draw.line(surface, (50, 90, 130), c1, c2, 6)
            pygame.draw.line(surface, (20, 36, 52), c1, c2, 2)

        # 6. Room Nodes
        for r_id, node in self.room_nodes.items():
            r_rect = node["rect"]
            is_current = (r_id == current_room_id)
            is_visited = (r_id in visited_rooms)

            # Background box
            if is_current:
                box_bg = (35, 48, 65)
                border_color = UI_ACCENT_GOLD
                border_w = 3
            elif is_visited:
                box_bg = (22, 32, 44)
                border_color = (80, 140, 190)
                border_w = 2
            else:
                box_bg = (14, 20, 28)
                border_color = (45, 65, 85)
                border_w = 1

            pygame.draw.rect(surface, box_bg, r_rect, border_radius=6)
            pygame.draw.rect(surface, border_color, r_rect, border_w, border_radius=6)

            # Room Titles
            title_col = (255, 235, 175) if is_current else (225, 235, 245) if is_visited else (120, 135, 150)
            name_surf = self.font_room_name.render(node["name"], True, title_col)
            surface.blit(name_surf, (r_rect.x + 10, r_rect.y + 10))

            sub_col = UI_ACCENT_GOLD if is_current else (140, 170, 195) if is_visited else (80, 95, 110)
            sub_s = self.font_room_sub.render(node["sub"], True, sub_col)
            surface.blit(sub_s, (r_rect.x + 10, r_rect.y + 28))

            # Treasure Status Badge
            t_id = node["treasure_id"]
            is_unlocked = self.treasure_mgr.is_unlocked(t_id)

            if is_unlocked:
                status_txt = "[SOLVED]"
                status_col = UI_SUCCESS_GREEN
            elif is_visited:
                status_txt = "[LOCKED]"
                status_col = UI_ACCENT_GOLD
            else:
                status_txt = "[UNKNOWN]"
                status_col = (100, 115, 130)

            badge_surf = self.font_status.render(status_txt, True, status_col)
            surface.blit(badge_surf, (r_rect.x + 10, r_rect.bottom - 22))

            # Current Player Indicator (Pulsing Pin)
            if is_current:
                pulse = (math.sin(self.anim_time * 6.0) + 1.0) * 0.5
                pin_r = int(6 + pulse * 3)
                pin_center = (r_rect.right - 22, r_rect.bottom - 16)

                # Glowing halo
                halo_surf = pygame.Surface((36, 36), pygame.SRCALPHA)
                pygame.draw.circle(halo_surf, (255, 215, 90, int(60 + pulse * 90)), (18, 18), pin_r + 5)
                surface.blit(halo_surf, (pin_center[0] - 18, pin_center[1] - 18))

                # Gold Center Pin
                pygame.draw.circle(surface, UI_ACCENT_GOLD, pin_center, 5)
                pygame.draw.circle(surface, (20, 20, 20), pin_center, 2)

                # "YOU" Label
                you_surf = self.font_status.render("YOU", True, UI_ACCENT_GOLD)
                surface.blit(you_surf, (pin_center[0] - 32, pin_center[1] - 6))

        # 7. Bottom Legend
        legend_y = self.map_y + self.map_h - 32
        legend_surf = self.font_legend.render(
            "LEGEND:   ● Gold Pin = You Are Here   |   [SOLVED] Unlocked   |   [LOCKED] Vault   |   [M / ESC] Exit Map",
            True,
            (160, 190, 220),
        )
        surface.blit(legend_surf, (self.map_x + 28, legend_y))

