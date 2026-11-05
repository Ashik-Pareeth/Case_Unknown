"""
Game Over Window for Case Unknown.

Displays an atmospheric noir modal when the detective is caught in an NPC's viewpoint / vision cone.
Allows restarting the case or returning to the title menu.
"""

from __future__ import annotations
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
    """Modal popup that displays when the player is spotted by an NPC patrol."""

    def __init__(self, reason: str = "Spotted by Precinct Patrol"):
        self.reason = reason
        self.anim_time = 0.0
        self.selected_idx = 0  # 0: RETRY, 1: MENU

        # Fonts
        pygame.font.init()
        self.font_kicker = pygame.font.SysFont("couriernew", 11, bold=True)
        self.font_title = pygame.font.SysFont("georgia", 34, bold=True)
        self.font_sub = pygame.font.SysFont("georgia", 13, italic=True)
        self.font_body = pygame.font.SysFont("segoeui", 13)
        self.font_badge = pygame.font.SysFont("segoeui", 11, bold=True)
        self.font_btn = pygame.font.SysFont("segoeui", 14, bold=True)
        self.font_btn_hint = pygame.font.SysFont("segoeui", 10)

        # Modal Dimensions
        self.width = 540
        self.height = 380
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Buttons
        btn_w = 360
        btn_h = 42
        btn_x = self.x + (self.width - btn_w) // 2
        self.btn_retry_rect = pygame.Rect(btn_x, self.y + 266, btn_w, btn_h)
        self.btn_menu_rect = pygame.Rect(btn_x, self.y + 318, btn_w, btn_h)
        self.buttons = [
            {"id": "RETRY", "rect": self.btn_retry_rect, "label": "RETRY INVESTIGATION", "hint": "[ENTER]"},
            {"id": "MENU", "rect": self.btn_menu_rect, "label": "RETURN TO MAIN MENU", "hint": "[ESC]"},
        ]

    def update(self, delta_time: float):
        self.anim_time += delta_time

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if self.anim_time < 0.15:
            return None  # Small debounce to prevent accidental dismissals

        # Mouse hover
        if event.type == pygame.MOUSEMOTION:
            for idx, btn in enumerate(self.buttons):
                if btn["rect"].collidepoint(event.pos):
                    self.selected_idx = idx
                    break

        # Mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    return btn["id"]

        # Keyboard navigation
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_idx = (self.selected_idx - 1) % len(self.buttons)
            elif event.key in (pygame.K_DOWN, pygame.K_s, pygame.K_TAB):
                self.selected_idx = (self.selected_idx + 1) % len(self.buttons)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.buttons[self.selected_idx]["id"]
            elif event.key == pygame.K_ESCAPE:
                return "MENU"
            elif event.key == pygame.K_r:
                return "RETRY"

        return None

    def draw(self, surface: pygame.Surface):
        # 1. Fullscreen dark backdrop with subtle noir red tint
        fade = min(1.0, self.anim_time * 3.5)
        backdrop = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((8, 10, 14, int(215 * fade)))
        surface.blit(backdrop, (0, 0))

        # Alert vignette border around screen
        vignette_alpha = int(45 * fade)
        if vignette_alpha > 0:
            vig = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(vig, (180, 40, 40, vignette_alpha), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 8)
            surface.blit(vig, (0, 0))

        # 2. Main Modal Card
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        panel.fill((22, 24, 29, 245))
        panel_rect = pygame.Rect(0, 0, self.width, self.height)

        # Borders
        pygame.draw.rect(panel, (160, 50, 50), panel_rect, 2, border_radius=8)
        pygame.draw.rect(panel, (65, 45, 45), panel_rect.inflate(-8, -8), 1, border_radius=6)

        # Left accent stripe (crimson warning)
        pygame.draw.rect(panel, UI_HIGHLIGHT_RED, (0, 0, 6, self.height), border_top_left_radius=8, border_bottom_left_radius=8)

        # Header banner area
        pygame.draw.rect(panel, (34, 26, 28), (6, 0, self.width - 6, 68), border_top_right_radius=8)
        pygame.draw.line(panel, (120, 50, 50), (6, 68), (self.width - 1, 68), 1)

        # Header kicker & title
        kicker = self.font_kicker.render("INCIDENT REPORT  /  DETECTIVE APPREHENDED", True, (215, 95, 95))
        panel.blit(kicker, (28, 14))

        title = self.font_title.render("GAME OVER", True, (235, 75, 75))
        panel.blit(title, (28, 28))

        sub = self.font_sub.render("Detected inside patrol viewpoint", True, (200, 175, 140))
        panel.blit(sub, (260, 40))

        # Divider line
        pygame.draw.line(panel, (75, 55, 55), (28, 82), (self.width - 28, 82), 1)

        # Body narrative lines
        lines = [
            "An autonomous patrol officer intercepted you in the sector viewpoint.",
            "Your unauthorized presence was logged and you were escorted out.",
            "All active investigative progress and case notes have been confiscated.",
        ]
        y_text = 98
        for line in lines:
            rendered = self.font_body.render(line, True, UI_TEXT_BODY)
            panel.blit(rendered, (28, y_text))
            y_text += 22

        # Status badge: "[ SAVE FILE CLEARED ]"
        badge_rect = pygame.Rect(28, 178, self.width - 56, 34)
        pygame.draw.rect(panel, (40, 20, 22), badge_rect, border_radius=4)
        pygame.draw.rect(panel, (180, 60, 60), badge_rect, 1, border_radius=4)

        badge_txt = self.font_badge.render("CASE FILE PURGED: save_game.json has been reset", True, (235, 120, 120))
        panel.blit(badge_txt, (badge_rect.centerx - badge_txt.get_width() // 2, badge_rect.centery - badge_txt.get_height() // 2))

        # Instructions / action prompt
        action_prompt = self.font_kicker.render("SELECT ACTION TO PROCEED", True, UI_TEXT_MUTED)
        panel.blit(action_prompt, (28, 230))
        pygame.draw.line(panel, (60, 50, 50), (28, 248), (self.width - 28, 248), 1)

        # Draw to screen surface
        surface.blit(panel, (self.x, self.y))

        # 3. Draw Buttons directly on surface for accurate mouse coordinate mapping
        for idx, btn in enumerate(self.buttons):
            b_rect = btn["rect"]
            is_selected = (idx == self.selected_idx)

            if is_selected:
                bg_color = (65, 30, 32)
                border_color = UI_ACCENT_GOLD
                border_w = 2
                text_color = (255, 235, 185)
            else:
                bg_color = (32, 34, 40)
                border_color = (100, 85, 75)
                border_w = 1
                text_color = UI_TEXT_BODY

            # Button background & border
            b_surf = pygame.Surface((b_rect.width, b_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(b_surf, (*bg_color, 240), (0, 0, b_rect.width, b_rect.height), border_radius=5)
            pygame.draw.rect(b_surf, border_color, (0, 0, b_rect.width, b_rect.height), border_w, border_radius=5)

            # Left selection indicator
            if is_selected:
                pygame.draw.rect(b_surf, UI_ACCENT_GOLD, (0, 0, 4, b_rect.height), border_top_left_radius=5, border_bottom_left_radius=5)

            surface.blit(b_surf, b_rect.topleft)

            # Button Label & Hint
            lbl = self.font_btn.render(btn["label"], True, text_color)
            surface.blit(lbl, (b_rect.centerx - lbl.get_width() // 2 - 18, b_rect.centery - lbl.get_height() // 2))

            hint = self.font_btn_hint.render(btn["hint"], True, UI_TEXT_MUTED if not is_selected else UI_ACCENT_GOLD)
            surface.blit(hint, (b_rect.right - hint.get_width() - 14, b_rect.centery - hint.get_height() // 2))

