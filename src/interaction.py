"""
Interaction system handling proximity detection, floating prompts, and noir inspection panels.

Adheres to directives.txt §5:
- 3 object classifications: Environmental, Examinable, Evidence.
- Contextual proximity prompt ("E — Examine") within 40-55px.
- High-fidelity inspection panel displaying object name, type badge, description,
  full readable transcript/document text, and clear "RECORDED IN JOURNAL" state indicator.
- Reusable asset card displaying custom item/observation visuals (mostly PNGs), with
  the paper document visual serving as an elegant fallback.
"""

from __future__ import annotations
import math
import os
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
from src.ui.interaction_prompt import InteractionPrompt
from src.ui.evidence_reader import EvidenceReaderFrame
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
        key_id: str = "",
        image: str | pygame.Surface | None = None,
        image_path: str = "",
        card_side: str = "right",
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
        self.key_id = key_id
        self.image = image
        self.image_path = image_path
        self.card_side = card_side


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

        # Asset caches for inspection popup illustrations
        self._asset_cache: dict[str, pygame.Surface | None] = {}
        self._scaled_cache: dict[tuple[str, int, int], pygame.Surface] = {}
        self.default_card_side: str = "right"

        # Badge surface
        self.badge_surface = render_svg(SVG_INTERACTION_BADGE, 54, 28)
        self.prompt_ui = InteractionPrompt(self.badge_surface)

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
        key_id: str = "",
        image: str | pygame.Surface | None = None,
        image_path: str = "",
        card_side: str = "right",
        **kwargs,
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
                key_id=key_id,
                image=image,
                image_path=image_path,
                card_side=card_side,
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
                    if self.active_object.key_id and self.evidence_manager:
                        if self.evidence_manager.collect_key(self.active_object.key_id):
                            self.evidence_manager._queue_toast(
                                "KEY FOUND", "A hidden key has been added to your inventory."
                            )

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

        self.prompt_ui.draw(surface, self.active_object.badge_pos, self.anim_time)

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        """Wraps text cleanly into multiple lines based on maximum pixel width."""
        lines = []
        for paragraph in text.split("\n"):
            words = paragraph.split(" ")
            cur_line: list[str] = []
            for w in words:
                test_line = " ".join(cur_line + [w])
                if font.size(test_line)[0] <= max_width:
                    cur_line.append(w)
                else:
                    if cur_line:
                        lines.append(" ".join(cur_line))
                    cur_line = [w]
            if cur_line:
                lines.append(" ".join(cur_line))
        return lines

    def get_asset_surface(self, obj: Interactable) -> pygame.Surface | None:
        """Resolves and loads an asset image for the given object, with caching."""
        if obj is None:
            return None

        # Direct Surface provided
        if isinstance(obj.image, pygame.Surface):
            return obj.image

        # Candidate names to look for
        cache_key = f"{obj.obj_id}_{obj.image}_{obj.image_path}_{obj.key_id}_{obj.evidence_id}"
        if cache_key in self._asset_cache:
            return self._asset_cache[cache_key]

        candidates: list[str] = []
        if isinstance(obj.image, str) and obj.image.strip():
            candidates.append(obj.image.strip())
        if obj.image_path and obj.image_path.strip():
            candidates.append(obj.image_path.strip())

        # Automatic ID-based candidates
        for id_val in (obj.obj_id, obj.key_id, obj.evidence_id, obj.treasure_id):
            if id_val:
                clean_id = id_val.strip()
                candidates.extend([f"{clean_id}.png", f"{clean_id}.jpg", f"{clean_id}.jpeg"])

        # Semantic keywords (e.g. key)
        combined_text = f"{obj.obj_id} {obj.key_id} {obj.name}".lower()
        if "key" in combined_text:
            candidates.extend(["key.png", "brass_key.png"])
        if "watch" in combined_text or "chronometer" in combined_text:
            candidates.extend(["watch.png", "chronometer.png", "pocket_watch.png"])

        search_dirs = [
            "",
            "assets/assets",
            "assets",
            "assets/props",
            "assets/images",
            "assets/items",
            "assets/evidence",
        ]

        resolved_surface = None
        for cand in candidates:
            cand_norm = os.path.normpath(cand)
            possible_paths = (
                [cand_norm]
                if os.path.isabs(cand_norm)
                else [
                    os.path.normpath(os.path.join(sdir, cand)) if sdir else cand_norm
                    for sdir in search_dirs
                ]
            )
            for p in possible_paths:
                if os.path.isfile(p):
                    try:
                        surf = pygame.image.load(p)
                        if pygame.display.get_surface() is not None:
                            surf = surf.convert_alpha()
                        resolved_surface = surf
                        break
                    except Exception:
                        pass
            if resolved_surface is not None:
                break

        self._asset_cache[cache_key] = resolved_surface
        return resolved_surface

    def _draw_paper_fallback(self, surface: pygame.Surface, card: pygame.Rect):
        """Fallback paper-and-seal document graphic when no specific visual asset exists."""
        paper = pygame.Rect(card.centerx - 56, card.y + 25, 112, 170)
        pygame.draw.rect(surface, (198, 187, 161), paper, border_radius=2)
        pygame.draw.polygon(
            surface,
            (224, 214, 192),
            [
                (paper.right - 20, paper.top),
                (paper.right, paper.top + 20),
                (paper.right - 20, paper.top + 20),
            ],
        )
        pygame.draw.line(
            surface, (135, 125, 107), (paper.x + 13, paper.y + 24), (paper.right - 28, paper.y + 24), 2
        )
        for row in range(5):
            yy = paper.y + 45 + row * 17
            pygame.draw.line(
                surface,
                (149, 140, 122),
                (paper.x + 13, yy),
                (paper.right - (20 if row % 2 else 12), yy),
                1,
            )
        stamp = pygame.Rect(paper.centerx - 23, paper.y + 110, 46, 30)
        pygame.draw.ellipse(surface, (133, 75, 62), stamp, 2)
        pygame.draw.line(
            surface, (133, 75, 62), (stamp.x + 7, stamp.centery), (stamp.right - 7, stamp.centery), 2
        )
        glyph = self.badge_font.render("13", True, (189, 174, 139))
        surface.blit(glyph, (card.x + 16, card.bottom - 32))
        side_label = self.badge_font.render("CASE RECORD", True, (141, 145, 134))
        surface.blit(side_label, (card.x + 43, card.bottom - 31))

    def _draw_asset_card(
        self, surface: pygame.Surface, card: pygame.Rect, obj: Interactable, is_evidence: bool
    ):
        """Renders the visual asset card (custom PNG/surface or fallback document)."""
        pygame.draw.rect(surface, (31, 35, 34), card, border_radius=4)
        pygame.draw.rect(surface, (74, 77, 68), card, 1, border_radius=4)

        asset_surf = self.get_asset_surface(obj)
        if asset_surf is None:
            self._draw_paper_fallback(surface, card)
            return

        # Photo/specimen showcase inner frame
        inner_frame = pygame.Rect(card.x + 12, card.y + 14, card.width - 24, 224)
        pygame.draw.rect(surface, (18, 22, 23), inner_frame, border_radius=3)
        pygame.draw.rect(surface, (58, 62, 57), inner_frame, 1, border_radius=3)
        pygame.draw.rect(surface, (12, 15, 16), inner_frame.inflate(-4, -4), border_radius=2)

        # Scale and render asset surface
        max_w = max(1, inner_frame.width - 16)
        max_h = max(1, inner_frame.height - 16)
        scale_key = (f"{obj.obj_id}_{id(asset_surf)}", max_w, max_h)

        if scale_key not in self._scaled_cache:
            img_w, img_h = asset_surf.get_size()
            scale = min(max_w / max(1, img_w), max_h / max(1, img_h))
            scaled_w = max(1, int(img_w * scale))
            scaled_h = max(1, int(img_h * scale))
            self._scaled_cache[scale_key] = pygame.transform.smoothscale(
                asset_surf, (scaled_w, scaled_h)
            )

        scaled_img = self._scaled_cache[scale_key]
        surface.blit(scaled_img, scaled_img.get_rect(center=inner_frame.center))

        # Bottom descriptor & badge
        pygame.draw.line(
            surface, (58, 62, 57), (card.x + 16, card.y + 248), (card.right - 16, card.y + 248), 1
        )

        if obj.key_id:
            tag_text, tag_color = "KEY ITEM", (215, 185, 110)
        elif is_evidence:
            tag_text, tag_color = "EVIDENCE", (147, 178, 139)
        elif obj.is_treasure:
            tag_text, tag_color = "VALUABLE", (215, 185, 110)
        else:
            tag_text, tag_color = "FIELD ASSET", (167, 157, 130)

        tag_surf = self.badge_font.render(tag_text, True, tag_color)
        surface.blit(tag_surf, tag_surf.get_rect(center=(card.centerx, card.y + 266)))

        sub_label = self.badge_font.render("PRECINCT 13 ARCHIVE", True, (122, 128, 118))
        surface.blit(sub_label, sub_label.get_rect(center=(card.centerx, card.y + 288)))

    def draw_dialogue(self, surface: pygame.Surface):
        """Renders a quiet field-note panel with a readable transcript and item asset/fallback card."""
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
        EvidenceReaderFrame.draw(surface, outer)

        header = pygame.Rect(panel_x + 5, panel_y + 5, panel_w - 10, 76)
        pygame.draw.rect(surface, (27, 32, 33), header)
        pygame.draw.line(
            surface,
            (90, 82, 65),
            (panel_x + 25, header.bottom),
            (panel_x + panel_w - 25, header.bottom),
            1,
        )
        eyebrow = self.badge_font.render("FIELD NOTE   /   PRECINCT 13", True, (136, 154, 150))
        surface.blit(eyebrow, (panel_x + 28, panel_y + 13))
        title = self.title_font.render(obj.name, True, (235, 222, 190))
        surface.blit(title, (panel_x + 28, panel_y + 34))
        badge_text = "EVIDENCE FILED" if is_evidence else "OBSERVATION"
        badge_color = (147, 178, 139) if is_evidence else (167, 157, 130)
        badge = self.badge_font.render(badge_text, True, badge_color)
        badge_box = pygame.Rect(
            panel_x + panel_w - badge.get_width() - 50, panel_y + 27, badge.get_width() + 24, 24
        )
        pygame.draw.rect(surface, (34, 42, 39), badge_box, border_radius=3)
        pygame.draw.rect(surface, (85, 106, 82), badge_box, 1, border_radius=3)
        surface.blit(badge, badge.get_rect(center=badge_box.center))

        # Position asset card (defaulting to right side) and transcript content
        card_side = getattr(obj, "card_side", self.default_card_side)
        card_w = 170
        content_w = panel_w - card_w - 76  # 28px left margin + 20px gap + 28px right margin

        if card_side == "left":
            card = pygame.Rect(panel_x + 28, panel_y + 101, card_w, 320)
            content = pygame.Rect(panel_x + 28 + card_w + 20, panel_y + 101, content_w, 320)
        else:
            # Right side placement
            content = pygame.Rect(panel_x + 28, panel_y + 101, content_w, 320)
            card = pygame.Rect(panel_x + panel_w - card_w - 28, panel_y + 101, card_w, 320)

        # Draw the visual card (PNG/asset or paper fallback)
        self._draw_asset_card(surface, card, obj, is_evidence)

        # Draw the text and transcript content
        EvidenceReaderFrame.draw_content(surface, content)
        desc_lines = self._wrap_text(obj.description, self.body_font, content.width - 32)
        doc_lines = (
            self._wrap_text(obj.full_text, self.doc_font, content.width - 36)
            if obj.full_text
            else []
        )
        text_blocks = [("OBSERVATION", desc_lines, self.body_font, (219, 218, 207), 23)]
        if doc_lines:
            text_blocks.append(
                ("TRANSCRIPT / DOCUMENT", doc_lines, self.doc_font, (193, 197, 190), 20)
            )
        total_content_h = sum(
            27 + len(lines) * line_h + 18 for _, lines, _, _, line_h in text_blocks
        )
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
            status = self.hint_font.render(
                "Filed in the investigation journal", True, (158, 185, 143)
            )
        else:
            status = self.hint_font.render("An observation for the case file", True, (154, 153, 139))
        surface.blit(status, (panel_x + 30, footer_y + 10))
        hint = "SCROLL TO READ   ·   [E] CLOSE" if max_scroll else "[E] CLOSE   ·   [ESC] RETURN"
        hint_surf = self.hint_font.render(hint, True, (160, 163, 154))
        surface.blit(
            hint_surf, (panel_x + panel_w - hint_surf.get_width() - 28, footer_y + 10)
        )
