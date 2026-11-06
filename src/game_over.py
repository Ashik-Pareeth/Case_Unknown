"""
Production-ready Game Over Window for Case Unknown.

Provides an authentic noir investigative dossier modal when the detective
is intercepted within an autonomous NPC patrol's viewpoint / vision cone.
"""

from __future__ import annotations
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
    UI_HIGHLIGHT_RED,
    UI_ACCENT_GOLD,
)


class GameOverWindow:
    """Authentic noir incident dossier displayed upon patrol interception."""

    def __init__(self, reason: str = "Spotted by Precinct Patrol"):
        self.reason = reason
        self.anim_time = 0.0
        self.selected_idx = 0  # 0: RETRY, 1: MENU

        # Typography
        pygame.font.init()
        self.font_kicker = pygame.font.SysFont("couriernew", 11, bold=True)
        self.font_title = pygame.font.SysFont("georgia", 28, bold=True)
        self.font_sub = pygame.font.SysFont("georgia", 12, italic=True)
        self.font_stamp = pygame.font.SysFont("impact", 16)
        self.font_label = pygame.font.SysFont("couriernew", 10, bold=True)
        self.font_heading = pygame.font.SysFont("georgia", 13, bold=True)
        self.font_body = pygame.font.SysFont("segoeui", 12)
        self.font_badge_title = pygame.font.SysFont("segoeui", 11, bold=True)
        self.font_badge_sub = pygame.font.SysFont("segoeui", 10)
        self.font_btn = pygame.font.SysFont("segoeui", 13, bold=True)
        self.font_btn_hint = pygame.font.SysFont("couriernew", 10, bold=True)

        # Modal Geometry (620 x 440 centered in 960 x 640 screen)
        self.width = 620
        self.height = 440
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Action Buttons (horizontal side-by-side)
        btn_w = 275
        btn_h = 44
        btn_y = self.y + 372
        self.btn_retry_rect = pygame.Rect(self.x + 26, btn_y, btn_w, btn_h)
        self.btn_menu_rect = pygame.Rect(self.x + 319, btn_y, btn_w, btn_h)

        self.buttons = [
            {
                "id": "RETRY",
                "rect": self.btn_retry_rect,
                "label": "RETRY INVESTIGATION",
                "hint": "ENTER",
            },
            {
                "id": "MENU",
                "rect": self.btn_menu_rect,
                "label": "RETURN TO MAIN MENU",
                "hint": "ESC",
            },
        ]

    def update(self, delta_time: float):
        self.anim_time += delta_time

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.anim_time < 0.12:
            return None  # Brief debounce

        # Mouse hover tracking
        if event.type == pygame.MOUSEMOTION:
            for idx, btn in enumerate(self.buttons):
                if btn["rect"].collidepoint(event.pos):
                    self.selected_idx = idx
                    break

        # Mouse click activation
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    return btn["id"]

        # Keyboard navigation
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                             pygame.K_TAB, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d):
                self.selected_idx = 1 - self.selected_idx
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.buttons[self.selected_idx]["id"]
            elif event.key == pygame.K_ESCAPE:
                return "MENU"
            elif event.key == pygame.K_r:
                return "RETRY"

        return None

    def draw(self, surface: pygame.Surface):
        fade = min(1.0, self.anim_time * 3.5)

        # 1. Dark noir vignette backdrop
        backdrop = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((6, 8, 11, int(220 * fade)))
        surface.blit(backdrop, (0, 0))

        # Alert perimeter glow
        vignette_alpha = int(40 * fade)
        if vignette_alpha > 0:
            vig = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(vig, (160, 35, 35, vignette_alpha), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 8)
            surface.blit(vig, (0, 0))

        # 2. Drop Shadow for depth
        shadow_rect = self.rect.inflate(18, 18).move(0, 10)
        shadow = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(shadow, (3, 4, 6, int(180 * fade)), shadow.get_rect(), border_radius=12)
        surface.blit(shadow, shadow_rect.topleft)

        # 3. Main Dossier Panel Canvas
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel.fill((21, 24, 27))
        panel_rect = pygame.Rect(0, 0, self.width, self.height)

        # Outer antique brass border and inner oxblood hairline
        pygame.draw.rect(panel, (132, 112, 78), panel_rect, 1, border_radius=8)
        pygame.draw.rect(panel, (60, 42, 44), panel_rect.inflate(-6, -6), 1, border_radius=6)

        # Left bound spine with gold rivet accents
        pygame.draw.rect(panel, (165, 45, 45), (0, 0, 6, self.height), border_top_left_radius=8, border_bottom_left_radius=8)
        pygame.draw.rect(panel, (196, 162, 94), (6, 0, 1, self.height))
        for rivet_y in (24, self.height // 2, self.height - 24):
            pygame.draw.circle(panel, (218, 182, 110), (3, rivet_y), 2)

        # -------------------------------------------------------------
        # Header Section (Banner, Kicker, Title, Rubber Stamp)
        # -------------------------------------------------------------
        header_h = 74
        pygame.draw.rect(panel, (29, 32, 35), (7, 1, self.width - 8, header_h), border_top_right_radius=8)
        pygame.draw.line(panel, (68, 72, 70), (7, header_h), (self.width - 2, header_h), 1)

        # Kicker
        kicker = self.font_kicker.render("INCIDENT DOSSIER  //  PRECINCT SECURITY BREACH", True, (205, 100, 100))
        panel.blit(kicker, (28, 14))

        # Main Title
        title = self.font_title.render("GAME OVER", True, (240, 85, 85))
        panel.blit(title, (28, 30))

        # Subtitle
        sub = self.font_sub.render("Field operative compromised inside patrol viewpoint", True, (190, 185, 170))
        panel.blit(sub, (220, 42))

        # Official Rubber Stamp Badge
        stamp_w, stamp_h = 142, 32
        stamp_x = self.width - stamp_w - 24
        stamp_y = 20
        stamp_rect = pygame.Rect(stamp_x, stamp_y, stamp_w, stamp_h)

        pygame.draw.rect(panel, (38, 18, 21), stamp_rect, border_radius=4)
        pygame.draw.rect(panel, (185, 55, 55), stamp_rect, 2, border_radius=4)
        pygame.draw.rect(panel, (110, 38, 42), stamp_rect.inflate(-4, -4), 1, border_radius=2)

        stamp_text = self.font_stamp.render("APPREHENDED", True, (235, 95, 95))
        panel.blit(stamp_text, stamp_text.get_rect(center=stamp_rect.center))

        # -------------------------------------------------------------
        # Left Column: Surveillance Polaroid Photograph
        # -------------------------------------------------------------
        photo_rect = pygame.Rect(26, 88, 190, 268)
        pygame.draw.rect(panel, (15, 18, 20), photo_rect, border_radius=4)
        pygame.draw.rect(panel, (85, 88, 80), photo_rect, 1, border_radius=4)

        # Inner surveillance screen viewport
        view_rect = pygame.Rect(photo_rect.x + 8, photo_rect.y + 8, photo_rect.width - 16, photo_rect.height - 38)
        pygame.draw.rect(panel, (12, 14, 18), view_rect)
        self._draw_surveillance_artwork(panel, view_rect.x, view_rect.y, view_rect.width, view_rect.height)

        # Surveillance Caption
        caption = self.font_kicker.render("LOG: CAM-SECTOR-04", True, (155, 158, 145))
        panel.blit(caption, caption.get_rect(center=(photo_rect.centerx, photo_rect.bottom - 15)))

        # -------------------------------------------------------------
        # Right Column: Incident Briefing & Case Purge Callout
        # -------------------------------------------------------------
        col_x = 234
        cur_y = 92

        # Metadata Row 1: SECTOR
        lbl_sector = self.font_label.render("SECTOR", True, (176, 143, 83))
        panel.blit(lbl_sector, (col_x, cur_y))
        cur_y += 16
        txt_sector = self.font_heading.render("Restricted Precinct Corridors", True, (225, 222, 210))
        panel.blit(txt_sector, (col_x, cur_y))
        cur_y += 24

        pygame.draw.line(panel, (52, 57, 56), (col_x, cur_y), (self.width - 26, cur_y), 1)
        cur_y += 12

        # Metadata Row 2: INCIDENT REPORT
        lbl_report = self.font_label.render("INCIDENT REPORT", True, (176, 143, 83))
        panel.blit(lbl_report, (col_x, cur_y))
        cur_y += 18

        narrative_lines = [
            "An autonomous patrol officer intercepted you inside the sector",
            "viewpoint. Undercover credentials were systematically revoked,",
            "and all recovered evidence materials have been confiscated.",
        ]
        for line in narrative_lines:
            rendered = self.font_body.render(line, True, (200, 204, 208))
            panel.blit(rendered, (col_x, cur_y))
            cur_y += 20

        cur_y += 10

        # Purge Warning Callout Box
        callout_w = self.width - col_x - 26
        callout_h = 56
        callout_rect = pygame.Rect(col_x, cur_y, callout_w, callout_h)

        pygame.draw.rect(panel, (34, 18, 20), callout_rect, border_radius=4)
        pygame.draw.rect(panel, (168, 52, 52), callout_rect, 1, border_radius=4)

        # Alert Tag
        alert_tag = self.font_label.render("FILE STATUS: PURGED", True, (240, 95, 95))
        panel.blit(alert_tag, (col_x + 12, cur_y + 10))

        # Alert Description
        alert_desc = self.font_badge_sub.render(
            "Local save_game.json has been cleared. Investigation must be restarted.",
            True,
            (215, 195, 195),
        )
        panel.blit(alert_desc, (col_x + 12, cur_y + 28))

        # Draw compiled panel onto main screen
        surface.blit(panel, (self.x, self.y))

        # -------------------------------------------------------------
        # Action Buttons (Clean, High-Contrast Noir Styling)
        # -------------------------------------------------------------
        for idx, btn in enumerate(self.buttons):
            b_rect = btn["rect"]
            is_active = (idx == self.selected_idx)

            if is_active:
                fill_color = (52, 28, 30)
                border_color = UI_ACCENT_GOLD
                border_width = 2
                text_color = (255, 238, 195)
                hint_color = UI_ACCENT_GOLD
            else:
                fill_color = (28, 32, 36)
                border_color = (95, 88, 76)
                border_width = 1
                text_color = (210, 214, 218)
                hint_color = (145, 148, 140)

            # Button panel
            btn_surf = pygame.Surface((b_rect.width, b_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(btn_surf, (*fill_color, 245), (0, 0, b_rect.width, b_rect.height), border_radius=5)
            pygame.draw.rect(btn_surf, border_color, (0, 0, b_rect.width, b_rect.height), border_width, border_radius=5)

            # Left active accent highlight
            if is_active:
                pygame.draw.rect(btn_surf, UI_ACCENT_GOLD, (0, 0, 4, b_rect.height), border_top_left_radius=5, border_bottom_left_radius=5)

            surface.blit(btn_surf, b_rect.topleft)

            # Button Label
            lbl = self.font_btn.render(btn["label"], True, text_color)
            surface.blit(lbl, (b_rect.x + 18, b_rect.centery - lbl.get_height() // 2))

            # Key Shortcut Pill Badge
            hint_txt = self.font_btn_hint.render(btn["hint"], True, hint_color)
            pill_w = hint_txt.get_width() + 14
            pill_h = 22
            pill_rect = pygame.Rect(b_rect.right - pill_w - 12, b_rect.centery - pill_h // 2, pill_w, pill_h)

            pill_bg = (42, 22, 24) if is_active else (22, 25, 28)
            pill_border = UI_ACCENT_GOLD if is_active else (75, 78, 80)
            pygame.draw.rect(surface, pill_bg, pill_rect, border_radius=3)
            pygame.draw.rect(surface, pill_border, pill_rect, 1, border_radius=3)
            surface.blit(hint_txt, hint_txt.get_rect(center=pill_rect.center))

    def _draw_surveillance_artwork(self, surface: pygame.Surface, x: int, y: int, w: int, h: int):
        """Draws bespoke vector noir surveillance artwork (viewpoint cone caught silhouette)."""
        cx = x + w // 2
        cy = y + h // 2

        # 1. Dark noir brick wall texture
        pygame.draw.rect(surface, (14, 17, 20), (x, y, w, h))
        for row in range(y + 8, y + h, 14):
            pygame.draw.line(surface, (22, 26, 31), (x, row), (x + w, row), 1)

        # 2. Overhead security camera / lantern spotlight
        cam_x, cam_y = cx, y + 12
        pygame.draw.rect(surface, (45, 50, 56), (cam_x - 14, cam_y - 8, 28, 12), border_radius=2)
        pygame.draw.circle(surface, (70, 76, 84), (cam_x, cam_y), 6)

        # Pulsing recording lens LED
        pulse = 0.5 + 0.5 * math.sin(self.anim_time * 6.0)
        red_val = int(180 + 75 * pulse)
        pygame.draw.circle(surface, (red_val, 40, 40), (cam_x, cam_y), 3)

        # 3. Translucent viewpoint searchlight cone
        light_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        beam_points = [
            (cam_x - x, cam_y - y + 4),
            (w + 10, h),
            (-10, h),
        ]
        pygame.draw.polygon(light_surf, (235, 185, 80, 42), beam_points)
        pygame.draw.line(light_surf, (240, 195, 95, 95), beam_points[0], beam_points[1], 1)
        pygame.draw.line(light_surf, (240, 195, 95, 95), beam_points[0], beam_points[2], 1)
        surface.blit(light_surf, (x, y))

        # 4. Noir Detective Silhouette standing inside cone
        det_cx = cx
        det_base = y + h - 16

        # Trench coat silhouette
        coat_points = [
            (det_cx - 18, det_base),
            (det_cx - 14, det_base - 58),
            (det_cx + 14, det_base - 58),
            (det_cx + 18, det_base),
        ]
        pygame.draw.polygon(surface, (10, 12, 14), coat_points)

        # Head / Collar
        pygame.draw.circle(surface, (10, 12, 14), (det_cx, det_base - 68), 10)

        # Fedora Hat
        pygame.draw.line(surface, (10, 12, 14), (det_cx - 18, det_base - 74), (det_cx + 18, det_base - 74), 3)
        pygame.draw.rect(surface, (10, 12, 14), (det_cx - 10, det_base - 84, 20, 10), border_radius=2)

        # 5. Surveillance HUD Overlay (Corner brackets and scanlines)
        b_len = 10
        hud_color = (200, 75, 75, 140)
        hud_surf = pygame.Surface((w, h), pygame.SRCALPHA)

        # Top-left
        pygame.draw.line(hud_surf, hud_color, (4, 4), (4 + b_len, 4), 1)
        pygame.draw.line(hud_surf, hud_color, (4, 4), (4, 4 + b_len), 1)
        # Top-right
        pygame.draw.line(hud_surf, hud_color, (w - 5, 4), (w - 5 - b_len, 4), 1)
        pygame.draw.line(hud_surf, hud_color, (w - 5, 4), (w - 5, 4 + b_len), 1)
        # Bottom-left
        pygame.draw.line(hud_surf, hud_color, (4, h - 5), (4 + b_len, h - 5), 1)
        pygame.draw.line(hud_surf, hud_color, (4, h - 5), (4, h - 5 - b_len), 1)
        # Bottom-right
        pygame.draw.line(hud_surf, hud_color, (w - 5, h - 5), (w - 5 - b_len, h - 5), 1)
        pygame.draw.line(hud_surf, hud_color, (w - 5, h - 5), (w - 5, h - 5 - b_len), 1)

        # Scanlines
        for scan_y in range(0, h, 4):
            pygame.draw.line(hud_surf, (0, 0, 0, 32), (0, scan_y), (w, scan_y), 1)

        surface.blit(hud_surf, (x, y))
