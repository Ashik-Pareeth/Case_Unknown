"""
Interaction system handling proximity detection, floating prompts, and noir inspection panels.

Adheres to directives.txt §5:
- 3 object classifications: Environmental, Examinable, Evidence.
- Contextual proximity prompt ("E — Examine") within 40-55px.
- High-fidelity inspection panel displaying object name, type badge, description,
  full readable transcript/document text, and clear "RECORDED IN JOURNAL" state indicator.
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
    UI_SUCCESS_GREEN,
)
from assets.svg_assets import render_svg, SVG_INTERACTION_BADGE
from src.evidence_manager import (
    TYPE_ENVIRONMENTAL,
    TYPE_EXAMINABLE,
    TYPE_EVIDENCE,
    EvidenceManager,
)


class Interactable:
    """Represents an interactable environmental element, clue, or evidence item."""

    def __init__(
        self,
        obj_id: str,
        name: str,
        description: str,
        trigger_rect: pygame.Rect,
        badge_pos: tuple[int, int],
        obj_type: str = TYPE_EXAMINABLE,
        evidence_id: str = "",
        full_text: str = "",
        is_treasure: bool = False,
        treasure_id: str = "",
    ):
        self.obj_id = obj_id
        self.name = name
        self.description = description
        self.trigger_rect = trigger_rect
        self.badge_pos = badge_pos
        self.obj_type = obj_type
        self.evidence_id = evidence_id or (obj_id if obj_type == TYPE_EVIDENCE else "")
        self.full_text = full_text
        self.is_treasure = is_treasure
        self.treasure_id = treasure_id


class InteractionManager:
    """Manages proximity checks, prompts, and the evidence inspection modal."""

    def __init__(self, evidence_manager: EvidenceManager | None = None):
        self.interactables: list[Interactable] = []
        self.active_object: Interactable | None = None
        self.is_inspecting: bool = False
        self.anim_time = 0.0
        self.trigger_puzzle_request: str | None = None
        self.treasure_manager = None
        self.evidence_manager: EvidenceManager | None = evidence_manager

        # Badge surface
        self.badge_surface = render_svg(SVG_INTERACTION_BADGE, 54, 28)

        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.SysFont("georgia", 18, bold=True)
        self.badge_font = pygame.font.SysFont("segoeui", 10, bold=True)
        self.body_font = pygame.font.SysFont("segoeui", 14)
        self.doc_font = pygame.font.SysFont("consolas", 12)
        self.hint_font = pygame.font.SysFont("segoeui", 12)

    def set_evidence_manager(self, evidence_manager: EvidenceManager):
        self.evidence_manager = evidence_manager

    def clear(self):
        """Clears all interactables when switching rooms."""
        self.interactables.clear()
        self.active_object = None
        self.is_inspecting = False
        self.trigger_puzzle_request = None

    def add_object(
        self,
        obj_id: str,
        name: str,
        description: str,
        trigger_rect: pygame.Rect,
        badge_pos: tuple[int, int],
        obj_type: str = TYPE_EXAMINABLE,
        evidence_id: str = "",
        full_text: str = "",
        is_treasure: bool = False,
        treasure_id: str = "",
    ):
        self.interactables.append(
            Interactable(
                obj_id=obj_id,
                name=name,
                description=description,
                trigger_rect=trigger_rect,
                badge_pos=badge_pos,
                obj_type=obj_type,
                evidence_id=evidence_id,
                full_text=full_text,
                is_treasure=is_treasure,
                treasure_id=treasure_id,
            )
        )

    def update(self, delta_time: float, player_reach: pygame.Rect):
        self.anim_time += delta_time

        if self.is_inspecting:
            return

        self.active_object = None
        min_dist = float("inf")
        reach_center = player_reach.center

        for item in self.interactables:
            if player_reach.colliderect(item.trigger_rect):
                dist = math.hypot(
                    reach_center[0] - item.trigger_rect.centerx,
                    reach_center[1] - item.trigger_rect.centery,
                )
                if dist < min_dist:
                    min_dist = dist
                    self.active_object = item

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Processes interaction input for examination dialogues."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_e, pygame.K_SPACE):
                if self.is_inspecting:
                    self.is_inspecting = False
                    return True
                elif self.active_object is not None:
                    # Backward compatibility for legacy puzzle triggers if any
                    if self.active_object.is_treasure and self.treasure_manager is not None:
                        t_id = self.active_object.treasure_id or self.active_object.obj_id
                        if not self.treasure_manager.is_unlocked(t_id):
                            self.trigger_puzzle_request = t_id
                            return True

                    # Open Inspection Panel
                    self.is_inspecting = True

                    # Automatically record in journal if it's an evidence object (§5.2, §5.3)
                    if self.active_object.obj_type == TYPE_EVIDENCE and self.evidence_manager:
                        e_id = self.active_object.evidence_id or self.active_object.obj_id
                        self.evidence_manager.record_evidence(e_id)

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

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        lines = []
        for raw_line in text.split("\n"):
            words = raw_line.split(" ")
            cur_line = []
            for w in words:
                test_str = " ".join(cur_line + [w])
                if font.size(test_str)[0] <= max_width:
                    cur_line.append(w)
                else:
                    if cur_line:
                        lines.append(" ".join(cur_line))
                    cur_line = [w]
            if cur_line:
                lines.append(" ".join(cur_line))
        return lines

    def draw_dialogue(self, surface: pygame.Surface):
        """Renders the comprehensive noir detective inspection panel overlay (§5.3)."""
        if not self.is_inspecting or self.active_object is None:
            return

        obj = self.active_object
        panel_w = 720
        max_w = panel_w - 60

        # Description lines
        desc_lines = self._wrap_text(obj.description, self.body_font, max_w)

        # Full transcript / document lines (if any)
        doc_lines = []
        if obj.full_text:
            doc_lines = self._wrap_text(obj.full_text, self.doc_font, max_w - 30)

        # Calculate heights
        header_h = 56
        desc_h = len(desc_lines) * 22
        doc_box_h = (len(doc_lines) * 18 + 24) if doc_lines else 0
        footer_h = 42
        total_h = header_h + desc_h + doc_box_h + footer_h + 20

        # Clamp max height to avoid offscreen
        panel_h = min(total_h, SCREEN_HEIGHT - 60)
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2

        # Dim background backdrop
        dim_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim_surf.fill((0, 0, 0, 110))
        surface.blit(dim_surf, (0, 0))

        # Panel surface
        panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel_surf.fill(UI_PANEL_BG)

        # Borders
        pygame.draw.rect(panel_surf, UI_PANEL_BORDER, (0, 0, panel_w, panel_h), 2, border_radius=8)
        pygame.draw.rect(panel_surf, (80, 65, 38), (4, 4, panel_w - 8, panel_h - 8), 1, border_radius=6)

        # Accent corner brackets
        bracket_color = UI_ACCENT_GOLD
        for cx, cy in [(12, 12), (panel_w - 20, 12), (12, panel_h - 20), (panel_w - 20, panel_h - 20)]:
            pygame.draw.rect(panel_surf, bracket_color, (cx, cy, 8, 8), width=1)

        surface.blit(panel_surf, (panel_x, panel_y))

        # Title & Badge
        title_surf = self.title_font.render(obj.name.upper(), True, UI_TEXT_TITLE)
        surface.blit(title_surf, (panel_x + 30, panel_y + 18))

        # Object Category Badge
        is_evidence = obj.obj_type == TYPE_EVIDENCE
        badge_text = "CRITICAL EVIDENCE" if is_evidence else "INVESTIGATIVE DETAIL"
        badge_color = UI_ACCENT_GOLD if is_evidence else UI_TEXT_MUTED
        badge_surf = self.badge_font.render(f"[{badge_text}]", True, badge_color)
        surface.blit(badge_surf, (panel_x + panel_w - badge_surf.get_width() - 30, panel_y + 22))

        # Divider line
        div_y = panel_y + 48
        pygame.draw.line(surface, UI_PANEL_BORDER, (panel_x + 28, div_y), (panel_x + panel_w - 28, div_y), 1)

        # Description Section
        cur_y = div_y + 14
        for d_line in desc_lines:
            line_surf = self.body_font.render(d_line, True, UI_TEXT_BODY)
            surface.blit(line_surf, (panel_x + 30, cur_y))
            cur_y += 22

        # Full Document / Transcript Box
        if doc_lines:
            cur_y += 6
            box_rect = pygame.Rect(panel_x + 30, cur_y, panel_w - 60, len(doc_lines) * 18 + 18)
            doc_bg = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
            doc_bg.fill((14, 16, 20, 220))
            surface.blit(doc_bg, (box_rect.x, box_rect.y))
            pygame.draw.rect(surface, (90, 80, 65), box_rect, width=1, border_radius=4)

            # Left amber accent bar on document
            pygame.draw.rect(surface, UI_ACCENT_GOLD, (box_rect.x, box_rect.y, 4, box_rect.height), border_top_left_radius=4, border_bottom_left_radius=4)

            doc_y = cur_y + 9
            for text_line in doc_lines:
                doc_s = self.doc_font.render(text_line, True, (215, 218, 222))
                surface.blit(doc_s, (box_rect.x + 14, doc_y))
                doc_y += 18

            cur_y = box_rect.bottom + 12

        # Evidence Status Stamp (§5.3 - "clear indication when the evidence has been recorded")
        if is_evidence:
            stamp_text = "✓ RECORDED IN EVIDENCE JOURNAL"
            stamp_color = UI_SUCCESS_GREEN
            stamp_surf = self.badge_font.render(stamp_text, True, stamp_color)
            surface.blit(stamp_surf, (panel_x + 30, panel_y + panel_h - 30))

        # Close Hint Footer
        hint_str = "Press [E] or [SPACE] to return to investigation"
        hint_surf = self.hint_font.render(hint_str, True, UI_TEXT_MUTED)
        surface.blit(hint_surf, (panel_x + panel_w - hint_surf.get_width() - 30, panel_y + panel_h - 30))
