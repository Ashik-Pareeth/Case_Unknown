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
        self.dialogue_scroll = 0
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
        if self.is_inspecting and event.type == pygame.MOUSEWHEEL:
            self.dialogue_scroll = max(0, self.dialogue_scroll - event.y * 36)
            return True
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
                    self.dialogue_scroll = 0

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
        """Renders a quiet field-note panel with a readable, scrollable transcript."""
        if not self.is_inspecting or self.active_object is None:
            return

        obj = self.active_object
        panel_w, panel_h = 760, 500
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2
        dim_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim_surf.fill((3, 6, 9, 176))
        surface.blit(dim_surf, (0, 0))

        is_evidence = obj.obj_type == TYPE_EVIDENCE
        outer = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        shadow = pygame.Surface((panel_w + 22, panel_h + 22), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 115), shadow.get_rect(), border_radius=12)
        surface.blit(shadow, (panel_x - 11, panel_y + 7))
        pygame.draw.rect(surface, (19, 23, 25), outer, border_radius=8)
        pygame.draw.rect(surface, (122, 105, 72), outer, 1, border_radius=8)
        pygame.draw.rect(surface, (46, 48, 43), outer.inflate(-8, -8), 1, border_radius=6)
        pygame.draw.rect(surface, (173, 139, 79), (panel_x, panel_y, 5, panel_h), border_top_left_radius=8, border_bottom_left_radius=8)

        header = pygame.Rect(panel_x + 5, panel_y + 5, panel_w - 10, 76)
        pygame.draw.rect(surface, (27, 32, 33), header)
        pygame.draw.line(surface, (90, 82, 65), (panel_x + 25, header.bottom), (panel_x + panel_w - 25, header.bottom), 1)
        eyebrow = self.badge_font.render("FIELD NOTE   /   PRECINCT 13", True, (136, 154, 150))
        surface.blit(eyebrow, (panel_x + 28, panel_y + 13))
        title = self.title_font.render(obj.name, True, (235, 222, 190))
        surface.blit(title, (panel_x + 28, panel_y + 34))
        badge_text = "EVIDENCE FILED" if is_evidence else "OBSERVATION"
        badge_color = (147, 178, 139) if is_evidence else (167, 157, 130)
        badge = self.badge_font.render(badge_text, True, badge_color)
        badge_box = pygame.Rect(panel_x + panel_w - badge.get_width() - 50, panel_y + 27, badge.get_width() + 24, 24)
        pygame.draw.rect(surface, (34, 42, 39), badge_box, border_radius=3)
        pygame.draw.rect(surface, (85, 106, 82), badge_box, 1, border_radius=3)
        surface.blit(badge, badge.get_rect(center=badge_box.center))

        # Evidence sketch card: a restrained paper-and-seal motif instead of a generic alert box.
        card = pygame.Rect(panel_x + 28, panel_y + 101, 160, 320)
        pygame.draw.rect(surface, (31, 35, 34), card, border_radius=4)
        pygame.draw.rect(surface, (74, 77, 68), card, 1, border_radius=4)
        paper = pygame.Rect(card.x + 24, card.y + 25, 112, 170)
        pygame.draw.rect(surface, (198, 187, 161), paper, border_radius=2)
        pygame.draw.polygon(surface, (224, 214, 192), [(paper.right - 20, paper.top), (paper.right, paper.top + 20), (paper.right - 20, paper.top + 20)])
        pygame.draw.line(surface, (135, 125, 107), (paper.x + 13, paper.y + 24), (paper.right - 28, paper.y + 24), 2)
        for row in range(5):
            yy = paper.y + 45 + row * 17
            pygame.draw.line(surface, (149, 140, 122), (paper.x + 13, yy), (paper.right - (20 if row % 2 else 12), yy), 1)
        stamp = pygame.Rect(paper.centerx - 23, paper.y + 110, 46, 30)
        pygame.draw.ellipse(surface, (133, 75, 62), stamp, 2)
        pygame.draw.line(surface, (133, 75, 62), (stamp.x + 7, stamp.centery), (stamp.right - 7, stamp.centery), 2)
        glyph = self.badge_font.render("13", True, (189, 174, 139))
        surface.blit(glyph, (card.x + 16, card.bottom - 32))
        side_label = self.badge_font.render("CASE RECORD", True, (141, 145, 134))
        surface.blit(side_label, (card.x + 43, card.bottom - 31))

        content = pygame.Rect(panel_x + 216, panel_y + 101, panel_w - 244, 320)
        pygame.draw.rect(surface, (23, 27, 28), content, border_radius=4)
        pygame.draw.rect(surface, (61, 65, 60), content, 1, border_radius=4)
        desc_lines = self._wrap_text(obj.description, self.body_font, content.width - 32)
        doc_lines = self._wrap_text(obj.full_text, self.doc_font, content.width - 36) if obj.full_text else []
        text_blocks = [("OBSERVATION", desc_lines, self.body_font, (219, 218, 207), 23)]
        if doc_lines:
            text_blocks.append(("TRANSCRIPT / DOCUMENT", doc_lines, self.doc_font, (193, 197, 190), 20))
        total_content_h = sum(27 + len(lines) * line_h + 18 for _, lines, _, _, line_h in text_blocks)
        visible_h = content.height - 16
        max_scroll = max(0, total_content_h - visible_h)
        self.dialogue_scroll = min(self.dialogue_scroll, max_scroll)
        old_clip = surface.get_clip()
        surface.set_clip(content)
        y = content.y + 14 - self.dialogue_scroll
        for section, lines, font, color, line_h in text_blocks:
            label = self.badge_font.render(section, True, (186, 151, 88))
            surface.blit(label, (content.x + 16, y))
            y += 27
            for line in lines:
                surface.blit(font.render(line, True, color), (content.x + 16, y))
                y += line_h
            y += 18
        surface.set_clip(old_clip)

        footer_y = panel_y + panel_h - 54
        if is_evidence:
            status = self.hint_font.render("Filed in the investigation journal", True, (158, 185, 143))
        else:
            status = self.hint_font.render("An observation for the case file", True, (154, 153, 139))
        surface.blit(status, (panel_x + 30, footer_y + 10))
        hint = "SCROLL TO READ   ·   [E] CLOSE" if max_scroll else "[E] CLOSE   ·   [ESC] RETURN"
        hint_surf = self.hint_font.render(hint, True, (160, 163, 154))
        surface.blit(hint_surf, (panel_x + panel_w - hint_surf.get_width() - 28, footer_y + 10))
