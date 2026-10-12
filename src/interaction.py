"""
Interaction system handling proximity detection, floating prompts, and clue inspection dialogues.
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
    UI_HIGHLIGHT_RED,
)
from assets.svg_assets import render_svg, SVG_INTERACTION_BADGE


class Interactable:
    def __init__(self, obj_id: str, name: str, description: str, trigger_rect: pygame.Rect, badge_pos: tuple[int, int]):
        self.obj_id = obj_id
        self.name = name
        self.description = description
        self.trigger_rect = trigger_rect
        self.badge_pos = badge_pos


class InteractionManager:
    def __init__(self):
        self.interactables: list[Interactable] = []
        self.active_object: Interactable | None = None
        self.is_inspecting: bool = False
        self.anim_time = 0.0

        # Load badge icon surface
        self.badge_surface = render_svg(SVG_INTERACTION_BADGE, 54, 28)

        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.SysFont("georgia", 20, bold=True)
        self.body_font = pygame.font.SysFont("segoeui", 16)
        self.hint_font = pygame.font.SysFont("segoeui", 13, italic=True)

    def add_object(self, obj_id: str, name: str, description: str, trigger_rect: pygame.Rect, badge_pos: tuple[int, int]):
        self.interactables.append(Interactable(obj_id, name, description, trigger_rect, badge_pos))

    def update(self, delta_time: float, player_reach: pygame.Rect):
        self.anim_time += delta_time

        # If dialog is currently open, don't change active target
        if self.is_inspecting:
            return

        # Find closest interactable colliding with player reach
        self.active_object = None
        min_dist = float("inf")
        reach_center = player_reach.center

        for item in self.interactables:
            if player_reach.colliderect(item.trigger_rect):
                dist = math.hypot(reach_center[0] - item.trigger_rect.centerx,
                                  reach_center[1] - item.trigger_rect.centery)
                if dist < min_dist:
                    min_dist = dist
                    self.active_object = item

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Processes key presses for opening and closing inspection modal.
        Returns True if the event was consumed by the interaction system.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_e, pygame.K_SPACE):
                if self.is_inspecting:
                    self.is_inspecting = False
                    return True
                elif self.active_object is not None:
                    self.is_inspecting = True
                    return True
            elif event.key == pygame.K_ESCAPE and self.is_inspecting:
                self.is_inspecting = False
                return True
        return False

    def draw_prompt(self, surface: pygame.Surface):
        """Draws floating [E] interaction prompt with gentle bobbing effect."""
        if self.active_object is None or self.is_inspecting:
            return

        bx, by = self.active_object.badge_pos
        float_offset = math.sin(self.anim_time * 5.0) * 3.5
        prompt_x = bx - self.badge_surface.get_width() // 2
        prompt_y = by - self.badge_surface.get_height() // 2 + float_offset

        surface.blit(self.badge_surface, (prompt_x, prompt_y))

    def draw_dialogue(self, surface: pygame.Surface):
        """Renders the noir detective inspection panel overlay."""
        if not self.is_inspecting or self.active_object is None:
            return

        # Modal Dimensions
        panel_w = 640
        panel_h = 220
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = SCREEN_HEIGHT - panel_h - 40

        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        # Semi-transparent background surface
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill(UI_PANEL_BG)

        # Decorative Brass Border
        pygame.draw.rect(panel_surf, UI_PANEL_BORDER, (0, 0, panel_w, panel_h), 2, border_radius=8)
        pygame.draw.rect(panel_surf, (80, 65, 38), (4, 4, panel_w - 8, panel_h - 8), 1, border_radius=6)

        surface.blit(panel_surf, (panel_x, panel_y))

        # Title / Object Name
        title_surf = self.title_font.render(self.active_object.name.upper(), True, UI_TEXT_TITLE)
        surface.blit(title_surf, (panel_x + 28, panel_y + 20))

        # Divider line
        div_y = panel_y + 48
        pygame.draw.line(surface, UI_PANEL_BORDER, (panel_x + 26, div_y), (panel_x + panel_w - 26, div_y), 1)

        # Word-wrapped Body Text
        words = self.active_object.description.split(" ")
        lines = []
        cur_line = []
        max_w = panel_w - 56

        for w in words:
            test_line = " ".join(cur_line + [w])
            if self.body_font.size(test_line)[0] <= max_w:
                cur_line.append(w)
            else:
                lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))

        text_y = div_y + 14
        for line in lines:
            rendered_line = self.body_font.render(line, True, UI_TEXT_BODY)
            surface.blit(rendered_line, (panel_x + 28, text_y))
            text_y += 24

        # Action hint footer
        hint_surf = self.hint_font.render("Press [E] or [SPACE] to close", True, UI_TEXT_MUTED)
        surface.blit(hint_surf, (panel_x + panel_w - hint_surf.get_width() - 28, panel_y + panel_h - 30))
