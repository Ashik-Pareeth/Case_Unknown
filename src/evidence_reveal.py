"""
Animated Evidence Document & Crime Photograph Inspection Modal for Case Unknown.

Displays an animated confidential case file folder, polaroid photograph, case dossier report,
and experience reward banner whenever a puzzle is solved.
"""

import math
import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    UI_ACCENT_GOLD,
    UI_SUCCESS_GREEN,
    UI_HIGHLIGHT_RED,
)
from src.treasure import TreasureItem
from src.experience import ExperienceManager


class EvidenceRevealModal:
    """Animated confidential case file and photograph reveal screen."""

    def __init__(self, item: TreasureItem, exp_mgr: ExperienceManager):
        self.item = item
        self.exp_mgr = exp_mgr
        self.anim_time = 0.0
        self.is_closed = False

        # Fonts
        pygame.font.init()
        self.font_stamp = pygame.font.SysFont("impact", 17)
        self.font_header = pygame.font.SysFont("georgia", 18, bold=True)
        self.font_sub = pygame.font.SysFont("georgia", 12, italic=True)
        self.font_typewriter = pygame.font.SysFont("couriernew", 12, bold=True)
        self.font_btn = pygame.font.SysFont("segoeui", 13, bold=True)
        self.font_exp = pygame.font.SysFont("georgia", 13, bold=True)

        # Base Modal Dimensions
        self.target_w = 580
        self.target_h = 480
        self.target_x = (SCREEN_WIDTH - self.target_w) // 2
        self.target_y = (SCREEN_HEIGHT - self.target_h) // 2

        # Dismiss Button Rect
        self.btn_dismiss_rect = pygame.Rect(self.target_x + self.target_w // 2 - 130, self.target_y + self.target_h - 52, 260, 36)

    def update(self, delta_time: float):
        self.anim_time += delta_time

    def handle_event(self, event: pygame.event.Event) -> bool:
        if self.anim_time < 0.2:
            return False  # Debounce initial keypress from puzzle unlock

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_e, pygame.K_ESCAPE):
                self.is_closed = True
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_closed = True
            return True
        return False

    def draw(self, surface: pygame.Surface):
        # 1. Dark Vignette Backdrop (Fades in)
        fade_t = min(1.0, self.anim_time * 3.5)
        backdrop = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((6, 8, 12, int(230 * fade_t)))
        surface.blit(backdrop, (0, 0))

        # 2. Smooth Elastic Pop-in Scale Animation
        t = min(1.0, self.anim_time * 2.8)
        # Elastic ease-out
        scale = 1.0 - math.pow(2, -10 * t) * math.cos(t * math.pi * 1.5) if t < 1.0 else 1.0
        scale = max(0.2, min(1.05, scale))

        # Render document on an unscaled canvas first
        doc_surf = pygame.Surface((self.target_w, self.target_h), pygame.SRCALPHA)

        # Aged Manila File Folder Base
        pygame.draw.rect(doc_surf, (236, 226, 206), (0, 0, self.target_w, self.target_h), border_radius=8)
        # Manila tab top-left
        pygame.draw.polygon(doc_surf, (222, 210, 186), [(0, 0), (140, 0), (160, 22), (0, 22)])
        doc_tab_text = self.font_typewriter.render("CASE FILE #001", True, (90, 80, 65))
        doc_surf.blit(doc_tab_text, (16, 4))

        # Inner paper sheet
        sheet_rect = pygame.Rect(14, 26, self.target_w - 28, self.target_h - 40)
        pygame.draw.rect(doc_surf, (246, 242, 230), sheet_rect, border_radius=4)
        pygame.draw.rect(doc_surf, (200, 188, 164), sheet_rect, 1, border_radius=4)

        # Faint aged paper horizontal lines
        for ly in range(sheet_rect.top + 70, sheet_rect.bottom - 90, 22):
            pygame.draw.line(doc_surf, (228, 222, 208), (sheet_rect.left + 16, ly), (sheet_rect.right - 16, ly), 1)

        # Red Rubber Stamp: [CONFIDENTIAL EVIDENCE]
        stamp_text = self.font_stamp.render("EVIDENCE RECOVERED", True, (185, 45, 45))
        stamp_surf = pygame.Surface((stamp_text.get_width() + 16, stamp_text.get_height() + 8), pygame.SRCALPHA)
        pygame.draw.rect(stamp_surf, (185, 45, 45), (0, 0, stamp_surf.get_width(), stamp_surf.get_height()), 2, border_radius=4)
        stamp_surf.blit(stamp_text, (8, 4))
        # Rotate stamp slightly
        rotated_stamp = pygame.transform.rotate(stamp_surf, -7)
        doc_surf.blit(rotated_stamp, (sheet_rect.right - rotated_stamp.get_width() - 14, sheet_rect.top + 14))

        # Header Title
        title_surf = self.font_header.render(self.item.reward_name.upper(), True, (35, 30, 24))
        doc_surf.blit(title_surf, (sheet_rect.left + 20, sheet_rect.top + 18))

        sub_surf = self.font_sub.render(f"Recovered from: {self.item.name}", True, (105, 88, 65))
        doc_surf.blit(sub_surf, (sheet_rect.left + 20, sheet_rect.top + 42))

        # Thin brass divider
        pygame.draw.line(doc_surf, (180, 150, 105), (sheet_rect.left + 20, sheet_rect.top + 62), (sheet_rect.right - 20, sheet_rect.top + 62), 1)

        # 3. Polaroid Crime Scene Photograph / Evidence Artifact
        photo_x = sheet_rect.left + 22
        photo_y = sheet_rect.top + 80
        photo_w = 145
        photo_h = 165

        # Photo border (white polaroid cardboard)
        pygame.draw.rect(doc_surf, (255, 255, 255), (photo_x, photo_y, photo_w, photo_h), border_radius=3)
        pygame.draw.rect(doc_surf, (190, 185, 175), (photo_x, photo_y, photo_w, photo_h), 1, border_radius=3)

        # Photo image frame
        frame_x = photo_x + 8
        frame_y = photo_y + 8
        frame_w = photo_w - 16
        frame_h = 120
        pygame.draw.rect(doc_surf, (22, 26, 32), (frame_x, frame_y, frame_w, frame_h))

        # Draw thematic evidence illustration inside polaroid
        self._draw_photo_artwork(doc_surf, frame_x, frame_y, frame_w, frame_h)

        # Polaroid handwritten caption (centered within bottom chin)
        caption_s = self.font_typewriter.render("EXHIBIT #A", True, (85, 75, 65))
        caption_rect = caption_s.get_rect(center=(photo_x + photo_w // 2, photo_y + photo_h - 16))
        doc_surf.blit(caption_s, caption_rect)

        # 4. Typed Case Evidence Report (Wrapped text)
        report_x = photo_x + photo_w + 20
        report_y = photo_y + 4
        report_w = sheet_rect.right - report_x - 16

        # Description wrapped cleanly
        words = self.item.reward_description.split(" ")
        lines = []
        cur = []
        for w in words:
            test = " ".join(cur + [w])
            if self.font_typewriter.size(test)[0] <= report_w:
                cur.append(w)
            else:
                lines.append(" ".join(cur))
                cur = [w]
        if cur:
            lines.append(" ".join(cur))

        # Label: OFFICIAL FORENSIC MEMO
        memo_lbl = self.font_typewriter.render("FORENSIC RECORD:", True, (135, 60, 40))
        doc_surf.blit(memo_lbl, (report_x, report_y))
        report_y += 20

        for line in lines:
            line_s = self.font_typewriter.render(line, True, (45, 42, 38))
            doc_surf.blit(line_s, (report_x, report_y))
            report_y += 19

        # Clue summary
        report_y += 8
        hint_s = self.font_typewriter.render(f"STATUS: VERIFIED & LOGGED", True, (60, 110, 70))
        doc_surf.blit(hint_s, (report_x, report_y))

        # 5. Experience Gain Banner
        exp_box = pygame.Rect(sheet_rect.left + 20, sheet_rect.bottom - 110, sheet_rect.width - 40, 46)
        pygame.draw.rect(doc_surf, (30, 36, 44), exp_box, border_radius=5)
        pygame.draw.rect(doc_surf, UI_ACCENT_GOLD, exp_box, 1, border_radius=5)

        star_x = exp_box.left + 24
        star_y = exp_box.centery
        pygame.draw.circle(doc_surf, UI_ACCENT_GOLD, (star_x, star_y), 11)
        pygame.draw.circle(doc_surf, (25, 30, 38), (star_x, star_y), 4)

        lvl, rank_name = self.exp_mgr.level_and_rank
        exp_txt = self.font_exp.render(f"+150 EXP REWARDED!   Current Rank: LVL {lvl} {rank_name}", True, (245, 220, 150))
        doc_surf.blit(exp_txt, (star_x + 18, exp_box.y + 14))

        # 6. Action Button: [ FILE EVIDENCE & RESUME ]
        btn_r = pygame.Rect(sheet_rect.centerx - 130, sheet_rect.bottom - 48, 260, 34)
        mpos = pygame.mouse.get_pos()
        is_hover = self.btn_dismiss_rect.collidepoint(mpos)
        btn_bg = (40, 95, 55) if is_hover else (30, 70, 42)
        pygame.draw.rect(doc_surf, btn_bg, btn_r, border_radius=5)
        pygame.draw.rect(doc_surf, UI_SUCCESS_GREEN, btn_r, 1, border_radius=5)
        btn_s = self.font_btn.render("FILE EVIDENCE [SPACE / CLICK]", True, (245, 250, 245))
        doc_surf.blit(btn_s, btn_s.get_rect(center=btn_r.center))

        # Apply scale animation if scale != 1.0
        if abs(scale - 1.0) > 0.01:
            scaled_w = int(self.target_w * scale)
            scaled_h = int(self.target_h * scale)
            scaled_surf = pygame.transform.smoothscale(doc_surf, (scaled_w, scaled_h))
            draw_x = (SCREEN_WIDTH - scaled_w) // 2
            draw_y = (SCREEN_HEIGHT - scaled_h) // 2
            surface.blit(scaled_surf, (draw_x, draw_y))
        else:
            surface.blit(doc_surf, (self.target_x, self.target_y))

    def _draw_photo_artwork(self, surface: pygame.Surface, x: int, y: int, w: int, h: int):
        """Draws atmospheric mini vector artwork inside the polaroid photo frame."""
        cx = x + w // 2
        cy = y + h // 2

        # Sepia photo tint
        pygame.draw.rect(surface, (28, 24, 20), (x, y, w, h))

        item_id = self.item.item_id
        if item_id == "office_safe":
            # Golden Keycard
            card_rect = pygame.Rect(cx - 32, cy - 20, 64, 40)
            pygame.draw.rect(surface, (215, 175, 75), card_rect, border_radius=3)
            pygame.draw.rect(surface, (90, 70, 25), card_rect, 1, border_radius=3)
            pygame.draw.circle(surface, (255, 230, 140), (card_rect.left + 14, card_rect.centery), 6)
            for line_y in range(card_rect.top + 10, card_rect.bottom - 8, 8):
                pygame.draw.line(surface, (135, 105, 45), (card_rect.left + 26, line_y), (card_rect.right - 10, line_y), 2)

        elif item_id == "archive_vault":
            # Confidential Dossier with red twine spiral
            doss_rect = pygame.Rect(cx - 28, cy - 35, 56, 70)
            pygame.draw.rect(surface, (210, 195, 160), doss_rect, border_radius=2)
            pygame.draw.rect(surface, (140, 125, 95), doss_rect, 1)
            # Red spiral mark
            for r in [6, 12, 18]:
                pygame.draw.circle(surface, (190, 45, 45), (cx, cy), r, 2)

        elif item_id == "morgue_locker":
            # Glowing chemical specimen vial
            vial_rect = pygame.Rect(cx - 10, cy - 34, 20, 68)
            pygame.draw.rect(surface, (170, 215, 230), vial_rect, border_radius=6)
            pygame.draw.rect(surface, (50, 110, 130), vial_rect, 1, border_radius=6)
            # Blue chemical fluid
            fluid_rect = pygame.Rect(cx - 8, cy - 5, 16, 36)
            pygame.draw.rect(surface, (35, 170, 195), fluid_rect, border_radius=4)
            # Cork
            pygame.draw.rect(surface, (160, 120, 70), (cx - 7, cy - 40, 14, 8), border_radius=2)

        elif item_id == "lockup_stash":
            # Antique Diamond Locket
            pygame.draw.circle(surface, (220, 225, 235), (cx, cy), 22)
            pygame.draw.circle(surface, (150, 160, 175), (cx, cy), 22, 2)
            # Diamond shape inside
            diamond = [(cx, cy - 14), (cx + 12, cy), (cx, cy + 14), (cx - 12, cy)]
            pygame.draw.polygon(surface, (160, 215, 245), diamond)
            pygame.draw.polygon(surface, (255, 255, 255), diamond, 1)

        elif item_id == "interrogation_box":
            # Reel-to-Reel Audio Tape
            tape_rect = pygame.Rect(cx - 36, cy - 24, 72, 48)
            pygame.draw.rect(surface, (40, 45, 52), tape_rect, border_radius=4)
            pygame.draw.circle(surface, (180, 185, 195), (cx - 16, cy), 13)
            pygame.draw.circle(surface, (180, 185, 195), (cx + 16, cy), 13)
            pygame.draw.circle(surface, (20, 20, 20), (cx - 16, cy), 4)
            pygame.draw.circle(surface, (20, 20, 20), (cx + 16, cy), 4)
            pygame.draw.circle(surface, (215, 45, 45), (cx + 26, cy - 16), 2)  # REC LED

        else:
            # Generic Evidence Star
            pygame.draw.circle(surface, UI_ACCENT_GOLD, (cx, cy), 20)
            pygame.draw.circle(surface, (30, 30, 30), (cx, cy), 6)
