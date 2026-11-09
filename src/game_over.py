from __future__ import annotations

import pygame

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class GameOverWindow:
    """Brief game-over popup shown before returning to the main menu."""

    DISPLAY_DURATION = 1.6

    @staticmethod
    def _lerp_color(a, b, t):
        return tuple(int(x + (y - x) * t) for x, y in zip(a, b))

    # Palette
    OVERLAY = (8, 10, 13)
    PANEL = (20, 23, 28)
    PANEL_BORDER = (42, 46, 53)

    TEXT_PRIMARY = (239, 236, 229)
    TEXT_SECONDARY = (157, 162, 170)
    TEXT_MUTED = (105, 112, 122)

    ACCENT = (193, 86, 76)

    def __init__(self, reason: str = "Spotted by Precinct Patrol"):
        pygame.font.init()

        self.reason = reason
        self.anim_time = 0.0

        # Typography
        self.font_title = pygame.font.SysFont("segoeui", 48, bold=True)
        self.font_subtitle = pygame.font.SysFont("segoeui", 19)
        self.font_body = pygame.font.SysFont("segoeui", 14)
        self.font_hint = pygame.font.SysFont("segoeui", 11)

        # Panel geometry
        self.width = 560
        self.height = 270

        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, delta_time: float):
        self.anim_time += delta_time
        return self.anim_time >= self.DISPLAY_DURATION

    def _render_wrapped_text(
        self,
        surface: pygame.Surface,
        text: str,
        font: pygame.font.Font,
        color: tuple,
        x: int,
        y: int,
        max_width: int,
    ):
        """Render text over multiple lines when necessary."""

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = (current_line + " " + word).strip()

            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        for line in lines:
            rendered = font.render(line, True, color)
            surface.blit(rendered, (x, y))
            y += font.get_linesize() + 4

    def draw(self, surface: pygame.Surface):

        # Smooth entrance
        fade = min(1.0, self.anim_time * 3.5)
        alpha = int(235 * fade)

        # Background dimming
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        overlay.fill((*self.OVERLAY, alpha))
        surface.blit(overlay, (0, 0))

        # Main panel
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        panel_rect = panel.get_rect()

        # Subtle shadow
        shadow = pygame.Surface((self.width + 24, self.height + 24), pygame.SRCALPHA)

        pygame.draw.rect(shadow, (0, 0, 0, 110), shadow.get_rect(), border_radius=16)

        shadow.set_alpha(int(180 * fade))

        surface.blit(shadow, (self.x - 12, self.y - 2))

        # Panel background
        pygame.draw.rect(panel, self.PANEL, panel_rect, border_radius=12)

        pygame.draw.rect(
            panel, self.PANEL_BORDER, panel_rect, width=1, border_radius=12
        )

        # Small accent line
        pygame.draw.rect(
            panel,
            self.ACCENT,
            (0, 0, self.width, 3),
            border_top_left_radius=12,
            border_top_right_radius=12,
        )

        # Status label
        status = self.font_hint.render("INVESTIGATION FAILED", True, self.ACCENT)

        panel.blit(status, (44, 48))

        # Main heading
        title = self.font_title.render("CAUGHT.", True, self.TEXT_PRIMARY)

        panel.blit(title, (40, 79))

        # Subtitle
        subtitle = self.font_subtitle.render(
            "Your cover has been blown.", True, self.TEXT_SECONDARY
        )

        panel.blit(subtitle, (44, 145))

        # Description
        self._render_wrapped_text(
            panel,
            self.reason,
            self.font_body,
            self.TEXT_MUTED,
            44,
            195,
            self.width - 88,
        )

        # Fade panel in
        panel.set_alpha(int(255 * fade))

        surface.blit(panel, (self.x, self.y))
