from __future__ import annotations

import pygame
import math

from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class GameOverWindow:
    """Animated game-over popup that waits for player input."""

    FADE_IN_DURATION = 0.30
    INPUT_DELAY = 0.35

    # Palette
    OVERLAY = (8, 10, 13)
    PANEL = (23, 26, 31)
    PANEL_BORDER = (48, 53, 61)

    TEXT_PRIMARY = (239, 236, 229)
    TEXT_SECONDARY = (165, 169, 176)
    TEXT_MUTED = (112, 119, 128)

    ACCENT = (193, 86, 76)

    def __init__(
        self,
        reason: str = "A patrol officer spotted you.",
        image_path: str | None = None,
    ):
        pygame.font.init()

        self.reason = reason
        self.anim_time = 0.0
        self.finished = False

        # Typography
        self.font_title = pygame.font.SysFont("segoeui", 38, bold=True)
        self.font_subtitle = pygame.font.SysFont("segoeui", 17)
        self.font_body = pygame.font.SysFont("segoeui", 14)
        self.font_label = pygame.font.SysFont("segoeui", 10, bold=True)
        self.font_prompt = pygame.font.SysFont("segoeui", 11, bold=True)

        # Popup geometry
        self.width = 500
        self.height = 250

        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Image area
        self.image_rect = pygame.Rect(22, 22, 170, 206)

        self.image = self._load_image(image_path)

        # Reusable surfaces
        self.overlay_surface = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )

        self.panel_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.shadow_surface = pygame.Surface(
            (self.width + 24, self.height + 24), pygame.SRCALPHA
        )

        self._draw_shadow()

    # ---------------------------------------------------------
    # IMAGE HANDLING
    # ---------------------------------------------------------

    def _load_image(self, image_path: str | None):

        if not image_path:
            return None

        try:
            image = pygame.image.load(image_path).convert_alpha()

            return pygame.transform.smoothscale(image, self.image_rect.size)

        except (pygame.error, FileNotFoundError) as exc:
            print(f"Game-over image could not be loaded: {exc}")
            return None

    def _draw_image(self, surface: pygame.Surface):

        rect = self.image_rect

        pygame.draw.rect(surface, (14, 17, 21), rect, border_radius=8)

        if self.image:

            image_surface = pygame.Surface(rect.size, pygame.SRCALPHA)

            image_surface.blit(self.image, (0, 0))

            mask = pygame.Surface(rect.size, pygame.SRCALPHA)

            pygame.draw.rect(
                mask, (255, 255, 255, 255), mask.get_rect(), border_radius=7
            )

            image_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            surface.blit(image_surface, rect.topleft)

        else:

            placeholder = self.font_label.render("IMAGE", True, self.TEXT_MUTED)

            surface.blit(placeholder, placeholder.get_rect(center=rect.center))

        pygame.draw.rect(surface, self.PANEL_BORDER, rect, width=1, border_radius=8)

    # ---------------------------------------------------------
    # INPUT HANDLING
    # ---------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Dismiss popup on any key press or mouse click."""

        if self.finished:
            return False

        # Prevent the triggering gameplay input from dismissing
        # the popup immediately.
        if self.anim_time < self.INPUT_DELAY:
            return False

        if event.type == pygame.KEYDOWN:
            self.finished = True
            return True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (1, 2, 3):
                self.finished = True
                return True

        return False

    # ---------------------------------------------------------
    # ANIMATION
    # ---------------------------------------------------------

    def update(self, delta_time: float) -> bool:

        if not self.finished:
            self.anim_time += delta_time

        return self.finished

    def _get_animation(self):

        fade = min(1.0, self.anim_time / self.FADE_IN_DURATION)

        # Subtle scale settling
        scale = 0.96 + 0.04 * fade

        return fade, scale

    # ---------------------------------------------------------
    # TEXT
    # ---------------------------------------------------------

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

            y += font.get_linesize() + 5

    # ---------------------------------------------------------
    # SHADOW
    # ---------------------------------------------------------

    def _draw_shadow(self):

        pygame.draw.rect(
            self.shadow_surface,
            (0, 0, 0, 120),
            self.shadow_surface.get_rect(),
            border_radius=16,
        )

    # ---------------------------------------------------------
    # DRAW
    # ---------------------------------------------------------

    def draw(self, surface: pygame.Surface):

        if self.finished:
            return

        fade, scale = self._get_animation()

        # Background dimming
        self.overlay_surface.fill((0, 0, 0, 0))

        self.overlay_surface.fill((*self.OVERLAY, int(205 * fade)))

        surface.blit(self.overlay_surface, (0, 0))

        # Panel scale
        scaled_width = int(self.width * scale)
        scaled_height = int(self.height * scale)

        # Build panel
        panel = self.panel_surface
        panel.fill((0, 0, 0, 0))

        pygame.draw.rect(panel, self.PANEL, panel.get_rect(), border_radius=12)

        pygame.draw.rect(
            panel, self.PANEL_BORDER, panel.get_rect(), width=1, border_radius=12
        )

        # Accent line
        pygame.draw.rect(
            panel,
            self.ACCENT,
            (0, 0, self.width, 3),
            border_top_left_radius=12,
            border_top_right_radius=12,
        )

        # Image
        self._draw_image(panel)

        # Text section
        text_x = 218

        # Status
        status = self.font_label.render("INVESTIGATION FAILED", True, self.ACCENT)

        panel.blit(status, (text_x, 48))

        # Heading
        title = self.font_title.render("CAUGHT.", True, self.TEXT_PRIMARY)

        panel.blit(title, (text_x - 2, 76))

        # Subtitle
        subtitle = self.font_subtitle.render(
            "Your cover has been blown.", True, self.TEXT_SECONDARY
        )

        panel.blit(subtitle, (text_x, 132))

        # Divider
        pygame.draw.line(
            panel, self.PANEL_BORDER, (text_x, 166), (self.width - 24, 166), 1
        )

        # Reason
        self._render_wrapped_text(
            panel,
            self.reason,
            self.font_body,
            self.TEXT_MUTED,
            text_x,
            183,
            self.width - text_x - 24,
        )

        # Animated continuation prompt
        if self.anim_time >= self.FADE_IN_DURATION:

            pulse = 0.65 + 0.35 * math.sin(self.anim_time * 3.0)

            prompt_color = tuple(int(c * pulse) for c in self.TEXT_MUTED)

            prompt = self.font_prompt.render(
                "PRESS ANY KEY OR CLICK TO CONTINUE", True, prompt_color
            )

            prompt_rect = prompt.get_rect(center=(self.width // 2, self.height - 14))

            panel.blit(prompt, prompt_rect)

        # Scale panel
        scaled_panel = pygame.transform.smoothscale(
            panel, (scaled_width, scaled_height)
        )

        scaled_panel.set_alpha(int(255 * fade))

        # Center panel
        panel_x = self.x + (self.width - scaled_width) // 2

        panel_y = self.y + (self.height - scaled_height) // 2

        # Shadow
        shadow = self.shadow_surface.copy()
        shadow.set_alpha(int(180 * fade))

        surface.blit(shadow, (panel_x - 12, panel_y - 2))

        surface.blit(scaled_panel, (panel_x, panel_y))
