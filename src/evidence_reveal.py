"""Recovered evidence document and field photograph modal for Case Unknown."""

import math
import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    UI_ACCENT_GOLD,
)
from src.treasure import TreasureItem
from src.experience import ExperienceManager


class EvidenceRevealModal:
    """A restrained recovered-document reveal; accepts the old XP argument for compatibility."""

    def __init__(self, item: TreasureItem, exp_mgr: ExperienceManager | None = None):
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
        """Lay the recovered object into a field dossier without XP or rank UI."""
        fade_t = min(1.0, self.anim_time * 3.5)
        backdrop = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((5, 8, 10, int(208 * fade_t)))
        surface.blit(backdrop, (0, 0))

        t = min(1.0, self.anim_time * 2.8)
        scale = max(0.92, min(1.0, 1 - (1 - t) ** 3 * 0.08))
        panel = pygame.Surface((self.target_w, self.target_h), pygame.SRCALPHA)
        panel.fill((25, 30, 31))
        panel_rect = panel.get_rect()
        pygame.draw.rect(panel, (133, 116, 81), panel_rect, 1, border_radius=7)
        pygame.draw.rect(panel, (53, 59, 57), panel_rect.inflate(-8, -8), 1, border_radius=5)
        pygame.draw.rect(panel, (38, 45, 44), (1, 1, self.target_w - 2, 66), border_top_left_radius=7, border_top_right_radius=7)
        pygame.draw.rect(panel, (176, 143, 83), (0, 0, 5, self.target_h), border_top_left_radius=7, border_bottom_left_radius=7)

        kicker = self.font_typewriter.render("CASE FILE  /  RECOVERED MATERIAL", True, (153, 165, 151))
        panel.blit(kicker, (30, 18))
        title = self.font_header.render(self.item.reward_name, True, (233, 220, 185))
        panel.blit(title, (30, 37))
        stamp = self.font_stamp.render("RECOVERED", True, (183, 148, 99))
        stamp_rect = pygame.Rect(self.target_w - stamp.get_width() - 54, 25, stamp.get_width() + 22, 26)
        pygame.draw.rect(panel, (42, 49, 44), stamp_rect, border_radius=3)
        pygame.draw.rect(panel, (112, 111, 83), stamp_rect, 1, border_radius=3)
        panel.blit(stamp, stamp.get_rect(center=stamp_rect.center))
        pygame.draw.line(panel, (86, 91, 80), (28, 78), (self.target_w - 28, 78), 1)

        photo = pygame.Rect(30, 99, 205, 260)
        pygame.draw.rect(panel, (14, 19, 20), photo, border_radius=4)
        pygame.draw.rect(panel, (94, 97, 86), photo, 1, border_radius=4)
        image_rect = pygame.Rect(photo.x + 10, photo.y + 10, photo.width - 20, photo.height - 50)
        pygame.draw.rect(panel, (28, 31, 29), image_rect)
        self._draw_photo_artwork(panel, *image_rect)
        caption = self.font_typewriter.render("FIELD PHOTOGRAPH", True, (156, 157, 140))
        panel.blit(caption, caption.get_rect(center=(photo.centerx, photo.bottom - 21)))

        text_x, text_y = 260, 105
        source_label = self.font_typewriter.render("SOURCE", True, (177, 146, 92))
        panel.blit(source_label, (text_x, text_y))
        text_y += 23
        source = self.font_sub.render(self.item.name, True, (205, 205, 188))
        panel.blit(source, (text_x, text_y))
        text_y += 34
        pygame.draw.line(panel, (66, 73, 68), (text_x, text_y), (self.target_w - 30, text_y), 1)
        text_y += 18
        memo = self.font_typewriter.render("OBSERVATION", True, (177, 146, 92))
        panel.blit(memo, (text_x, text_y))
        text_y += 25
        report_w = self.target_w - text_x - 32
        words, lines, line = self.item.reward_description.split(), [], []
        for word in words:
            test = " ".join(line + [word])
            if self.font_sub.size(test)[0] <= report_w:
                line.append(word)
            else:
                lines.append(" ".join(line))
                line = [word]
        if line:
            lines.append(" ".join(line))
        for text_line in lines:
            panel.blit(self.font_sub.render(text_line, True, (207, 208, 195)), (text_x, text_y))
            text_y += 22

        note = self.font_sub.render("The item has been added to the case record.", True, (155, 181, 145))
        panel.blit(note, (text_x, max(text_y + 18, 318)))
        footer = pygame.Rect(20, self.target_h - 59, self.target_w - 40, 38)
        pygame.draw.rect(panel, (34, 41, 39), footer, border_radius=4)
        pygame.draw.rect(panel, (77, 91, 76), footer, 1, border_radius=4)
        action = self.font_btn.render("RETURN TO INVESTIGATION", True, (219, 220, 201))
        panel.blit(action, action.get_rect(center=(footer.centerx - 46, footer.centery)))
        keys = self.font_typewriter.render("ENTER", True, (191, 166, 108))
        panel.blit(keys, (footer.right - keys.get_width() - 12, footer.centery - keys.get_height() // 2))

        scaled = pygame.transform.smoothscale(panel, (int(self.target_w * scale), int(self.target_h * scale)))
        surface.blit(scaled, scaled.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

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
