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

        # Active case route: crime scene -> records -> recordings -> restricted office.
        cx = self.map_x + self.map_w // 2
        cy = self.map_y + self.map_h // 2 - 10
        rw = 185
        rh = 92

        self.room_nodes = {
            "crime_scene": {
                "name": "THE CRIME SCENE",
                "sub": "STUDY  /  MARTIN HALE",
                "rect": pygame.Rect(cx - 260 - rw // 2, cy - rh // 2, rw, rh),
            },
            "records_room": {
                "name": "RECORDS ROOM",
                "sub": "DIRECTORATE ARCHIVE",
                "rect": pygame.Rect(cx - rw // 2, cy - rh // 2, rw, rh),
            },
            "recording_room": {
                "name": "RECORDING ROOM",
                "sub": "AUDIO ARCHIVE",
                "rect": pygame.Rect(cx + 260 - rw // 2, cy - rh // 2, rw, rh),
            },
            "restricted_office": {
                "name": "RESTRICTED OFFICE",
                "sub": "DIRECTORATE  /  VOSS",
                "rect": pygame.Rect(cx + 260 - rw // 2, cy + rh // 2 + 42, rw, rh),
            },
        }

        # Corridors connecting the four locations in the active investigation.
        self.corridors = [
            ("crime_scene", "records_room"),
            ("records_room", "recording_room"),
            ("recording_room", "restricted_office"),
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

        # 2. Main Map Panel and inset drafting field
        panel = pygame.Surface((self.map_w, self.map_h), pygame.SRCALPHA)
        panel.fill((10, 18, 27, 248))
        surface.blit(panel, (self.map_x, self.map_y))
        pygame.draw.rect(surface, (5, 8, 13), self.map_rect.inflate(10, 10), border_radius=10)
        pygame.draw.rect(surface, (15, 24, 34), self.map_rect, border_radius=7)
        pygame.draw.rect(surface, (75, 126, 158), self.map_rect, 2, border_radius=7)

        # 3. Blueprint Grid Lines
        grid_step = 26
        for gx in range(self.map_x, self.map_x + self.map_w, grid_step):
            pygame.draw.line(surface, (24, 34, 46), (gx, self.map_y), (gx, self.map_y + self.map_h), 1)
        for gy in range(self.map_y, self.map_y + self.map_h, grid_step):
            pygame.draw.line(surface, (24, 34, 46), (self.map_x, gy), (self.map_x + self.map_w, gy), 1)

        # 4. Blueprint frame and registration marks
        pygame.draw.rect(surface, (32, 61, 81), self.map_rect.inflate(-8, -8), 1, border_radius=4)
        for px, py, sx, sy in ((self.map_x + 12, self.map_y + 12, 1, 1),
                               (self.map_x + self.map_w - 12, self.map_y + 12, -1, 1),
                               (self.map_x + 12, self.map_y + self.map_h - 12, 1, -1),
                               (self.map_x + self.map_w - 12, self.map_y + self.map_h - 12, -1, -1)):
            pygame.draw.line(surface, (103, 157, 183), (px, py), (px + sx * 14, py), 2)
            pygame.draw.line(surface, (103, 157, 183), (px, py), (px, py + sy * 14), 2)

        # Header Title
        title_surf = self.font_title.render("CASE AREA — FIELD MAP", True, (215, 235, 255))
        surface.blit(title_surf, (self.map_x + 28, self.map_y + 18))

        visited_count = sum(room_id in visited_rooms for room_id in self.room_nodes)
        sub_surf = self.font_sub.render(
            f"Locations visited: {visited_count}/{len(self.room_nodes)}   |   Press [M / ESC] to close",
            True,
            (140, 180, 215),
        )
        surface.blit(sub_surf, (self.map_x + 28, self.map_y + 48))
        # North marker and drafting scale
        compass_x, compass_y = self.map_x + self.map_w - 42, self.map_y + 37
        pygame.draw.circle(surface, (54, 83, 102), (compass_x, compass_y), 17, 1)
        pygame.draw.polygon(surface, (225, 191, 119), [(compass_x, compass_y - 12), (compass_x - 4, compass_y + 4), (compass_x, compass_y + 1), (compass_x + 4, compass_y + 4)])
        surface.blit(self.font_status.render("N", True, (189, 215, 229)), (compass_x - 4, compass_y - 29))

        # 5. Hallway Corridors
        for r1_key, r2_key in self.corridors:
            if r1_key not in visited_rooms or r2_key not in visited_rooms:
                continue
            r1 = self.room_nodes[r1_key]["rect"]
            r2 = self.room_nodes[r2_key]["rect"]
            c1 = r1.center
            c2 = r2.center

            # Draw double-lined blueprint corridor
            pygame.draw.line(surface, (31, 62, 81), c1, c2, 10)
            pygame.draw.line(surface, (83, 139, 162), c1, c2, 2)
            pygame.draw.circle(surface, (129, 176, 192), c1, 3)
            pygame.draw.circle(surface, (129, 176, 192), c2, 3)

        # 6. Room Nodes
        for r_id, node in self.room_nodes.items():
            r_rect = node["rect"]
            is_current = (r_id == current_room_id)
            is_visited = (r_id in visited_rooms)
            if not is_visited:
                continue

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
            # Room plan details: top rail, door notches, and a simple interior layout.
            rail = (UI_ACCENT_GOLD if is_current else (71, 117, 141) if is_visited else (42, 61, 76))
            pygame.draw.line(surface, rail, (r_rect.x + 9, r_rect.y + 4), (r_rect.right - 9, r_rect.y + 4), 2)
            for dx in (r_rect.centerx - 9, r_rect.centerx + 9):
                pygame.draw.line(surface, (9, 15, 21), (dx, r_rect.bottom - 2), (dx, r_rect.bottom + 2), 3)
            # Room Titles
            title_col = (255, 235, 175) if is_current else (225, 235, 245) if is_visited else (120, 135, 150)
            room_name = node["name"]
            while room_name and self.font_room_name.size(room_name)[0] > r_rect.width - 20:
                room_name = room_name[:-1]
            if room_name != node["name"]:
                room_name = room_name.rstrip(" /-") + "…"
            name_surf = self.font_room_name.render(room_name, True, title_col)
            surface.blit(name_surf, (r_rect.x + 10, r_rect.y + 10))

            sub_col = UI_ACCENT_GOLD if is_current else (140, 170, 195) if is_visited else (80, 95, 110)
            sub_s = self.font_room_sub.render(node["sub"], True, sub_col)
            surface.blit(sub_s, (r_rect.x + 10, r_rect.y + 28))

            # Case-location status follows the active story's visited-room state.
            if is_current:
                status_txt = "HERE"
                status_col = UI_ACCENT_GOLD
            elif is_visited:
                status_txt = "VISITED"
                status_col = UI_SUCCESS_GREEN
            else:
                status_txt = "NOT CURRENT"
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
            "LOCATIONS ARE ADDED AS YOU VISIT THEM     •     [M / ESC] CLOSE MAP",
            True,
            (160, 190, 220),
        )
        surface.blit(legend_surf, (self.map_x + 28, legend_y))

