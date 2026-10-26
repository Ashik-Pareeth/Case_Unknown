"""
Main Menu, In-Game Pause System, and Evidence Dossier for Case Unknown.

Provides:
- Title Menu with 'New Game', 'Resume', 'Precinct Map', 'Evidence Dossier', 'Controls', 'Quit'.
- Evidence Dossier view listing recovered clues, items, and case completion rate.
- Controls & Keybindings reference screen.
- Keyboard (WASD/Arrows/Enter/Esc) and Mouse interaction support.
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
    UI_ACCENT_GOLD,
    UI_SUCCESS_GREEN,
    UI_HIGHLIGHT_RED,
)
from typing import Optional
from src.treasure import TreasureManager
from src.experience import ExperienceManager
from assets.svg_assets import get_character_animations


class MenuSystem:
    """Manages the title screen, in-game pause menu, and dossier sub-screens."""

    def __init__(self, treasure_mgr: TreasureManager, exp_mgr: Optional[ExperienceManager] = None):
        self.treasure_mgr = treasure_mgr
        self.exp_mgr = exp_mgr
        self.current_screen = "MAIN"  # "MAIN", "EVIDENCE", "CONTROLS"
        self.selected_idx = 0
        self.anim_time = 0.0

        # Fonts
        pygame.font.init()
        self.font_logo = pygame.font.SysFont("georgia", 36, bold=True)
        self.font_sublogo = pygame.font.SysFont("georgia", 14, italic=True)
        self.font_btn = pygame.font.SysFont("segoeui", 16, bold=True)
        self.font_card_title = pygame.font.SysFont("georgia", 15, bold=True)
        self.font_card_body = pygame.font.SysFont("segoeui", 12)
        self.font_card_sub = pygame.font.SysFont("segoeui", 11, italic=True)
        self.font_kicker = pygame.font.SysFont("segoeui", 10, bold=True)
        self.detective = get_character_animations()["down"]["idle"][0]

        # Main Menu Options
        self.menu_options = [
            {"id": "RESUME", "label": "RESUME INVESTIGATION"},
            {"id": "NEW_GAME", "label": "NEW CASE FILE"},
            {"id": "MAP", "label": "PRECINCT BLUEPRINT MAP [M]"},
            {"id": "EVIDENCE", "label": "CASE EVIDENCE DOSSIER"},
            {"id": "CONTROLS", "label": "INVESTIGATION CONTROLS"},
            {"id": "QUIT", "label": "EXIT GAME"},
        ]

        # Button Rectangles
        self.btn_rects = []
        btn_w = 340
        btn_h = 44
        btn_spacing = 14
        start_y = 252
        for i in range(len(self.menu_options)):
            bx = (SCREEN_WIDTH - btn_w) // 2
            by = start_y + i * (btn_h + btn_spacing)
            self.btn_rects.append(pygame.Rect(bx, by, btn_w, btn_h))

    def update(self, delta_time: float):
        self.anim_time += delta_time

    def handle_event(self, event: pygame.event.Event, has_active_game: bool) -> str | None:
        """
        Processes menu navigation and returns an action identifier when a button is clicked.
        Returns: 'RESUME', 'NEW_GAME', 'MAP', 'QUIT', or None.
        """
        # If in sub-screens, ESC returns to MAIN menu
        if self.current_screen in ("EVIDENCE", "CONTROLS"):
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                self.current_screen = "MAIN"
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.current_screen = "MAIN"
                return None
            return None

        # Main Menu Navigation
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_idx = (self.selected_idx - 1) % len(self.menu_options)
                # Skip disabled resume if no active game
                if not has_active_game and self.menu_options[self.selected_idx]["id"] == "RESUME":
                    self.selected_idx = (self.selected_idx - 1) % len(self.menu_options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_idx = (self.selected_idx + 1) % len(self.menu_options)
                if not has_active_game and self.menu_options[self.selected_idx]["id"] == "RESUME":
                    self.selected_idx = (self.selected_idx + 1) % len(self.menu_options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self._trigger_option(self.menu_options[self.selected_idx]["id"], has_active_game)
            elif event.key == pygame.K_ESCAPE and has_active_game:
                return "RESUME"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mpos = event.pos
            for i, rect in enumerate(self.btn_rects):
                if rect.collidepoint(mpos):
                    opt_id = self.menu_options[i]["id"]
                    return self._trigger_option(opt_id, has_active_game)

        # Mouse hover update
        mpos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.btn_rects):
            if rect.collidepoint(mpos):
                if has_active_game or self.menu_options[i]["id"] != "RESUME":
                    self.selected_idx = i

        return None

    def _trigger_option(self, option_id: str, has_active_game: bool) -> str | None:
        if option_id == "RESUME":
            if has_active_game:
                return "RESUME"
            return None
        elif option_id == "NEW_GAME":
            return "NEW_GAME"
        elif option_id == "MAP":
            return "MAP"
        elif option_id == "EVIDENCE":
            return "JOURNAL"
        elif option_id == "CONTROLS":
            self.current_screen = "CONTROLS"
            return None
        elif option_id == "QUIT":
            return "QUIT"
        return None

    def draw(self, surface: pygame.Surface, has_active_game: bool):
        # Illustrated noir title card, with a desk lamp pool and the detective as a visual anchor.
        surface.fill((9, 12, 17))
        for x in range(0, SCREEN_WIDTH, 48):
            pygame.draw.line(surface, (13, 17, 23), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 48):
            pygame.draw.line(surface, (13, 17, 23), (0, y), (SCREEN_WIDTH, y), 1)
        glow = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for radius, alpha in ((230, 7), (165, 10), (95, 14)):
            pygame.draw.circle(glow, (224, 174, 83, alpha), (SCREEN_WIDTH - 145, 215), radius)
        surface.blit(glow, (0, 0))

        # Rain-lit window and warm desk silhouette frame the title without competing with it.
        pygame.draw.rect(surface, (18, 27, 37), (58, 54, 210, 142), border_radius=4)
        pygame.draw.rect(surface, (93, 126, 145), (58, 54, 210, 142), 2, border_radius=4)
        for x in range(72, 260, 22):
            pygame.draw.line(surface, (50, 78, 94), (x, 60), (x - 34, 190), 1)
        pygame.draw.line(surface, (93, 126, 145), (163, 57), (163, 193), 3)
        pygame.draw.line(surface, (93, 126, 145), (61, 124), (265, 124), 3)
        pygame.draw.rect(surface, (47, 32, 24), (0, 540, SCREEN_WIDTH, 100))
        pygame.draw.line(surface, (119, 83, 47), (0, 540), (SCREEN_WIDTH, 540), 2)
        for y in range(557, 640, 24):
            pygame.draw.line(surface, (63, 45, 33), (0, y), (SCREEN_WIDTH, y), 1)
        pygame.draw.ellipse(surface, (5, 7, 10), (SCREEN_WIDTH - 285, 503, 225, 34))
        surface.blit(self.detective, (SCREEN_WIDTH - 240, 420))
        pygame.draw.rect(surface, (49, 33, 24), (SCREEN_WIDTH - 332, 485, 200, 18), border_radius=4)
        pygame.draw.rect(surface, (150, 108, 57), (SCREEN_WIDTH - 332, 485, 200, 18), 1, border_radius=4)
        pygame.draw.line(surface, (224, 182, 90), (SCREEN_WIDTH - 205, 485), (SCREEN_WIDTH - 182, 409), 3)
        pygame.draw.circle(surface, (255, 220, 132), (SCREEN_WIDTH - 181, 404), 9)

        # Title lockup
        title_x, title_y = 315, 58
        kicker = self.font_kicker.render("PRECINCT 13  /  CASE FILE 001", True, (126, 160, 174))
        surface.blit(kicker, (title_x + 4, title_y))
        shadow_txt = self.font_logo.render("CASE UNKNOWN", True, (5, 7, 9))
        logo_txt = self.font_logo.render("CASE UNKNOWN", True, (240, 210, 145))
        surface.blit(shadow_txt, (title_x + 6, title_y + 28))
        surface.blit(logo_txt, (title_x + 3, title_y + 25))
        sub_txt = self.font_sublogo.render("The Midnight Syndicate Mystery", True, (170, 145, 105))
        surface.blit(sub_txt, (title_x + 6, title_y + 70))
        div_y = title_y + 100
        pygame.draw.line(surface, (78, 71, 55), (title_x + 4, div_y), (SCREEN_WIDTH - 72, div_y), 1)
        pygame.draw.circle(surface, UI_ACCENT_GOLD, (title_x + 4, div_y), 3)

        if self.current_screen == "MAIN":
            self._draw_main_menu(surface, has_active_game)
        elif self.current_screen == "EVIDENCE":
            self._draw_evidence_dossier(surface)
        elif self.current_screen == "CONTROLS":
            self._draw_controls(surface)

    def _draw_main_menu(self, surface: pygame.Surface, has_active_game: bool):
        mpos = pygame.mouse.get_pos()

        menu_panel = pygame.Surface((388, 382), pygame.SRCALPHA)
        menu_panel.fill((10, 14, 20, 218))
        panel_rect = menu_panel.get_rect(center=(SCREEN_WIDTH // 2, 401))
        surface.blit(menu_panel, panel_rect)
        pygame.draw.rect(surface, (63, 69, 72), panel_rect, 1, border_radius=8)
        pygame.draw.line(surface, (178, 142, 79), (panel_rect.x + 18, panel_rect.y + 14),
                         (panel_rect.x + 70, panel_rect.y + 14), 2)
        section_label = self.font_kicker.render("INVESTIGATION DESK", True, (127, 151, 160))
        surface.blit(section_label, (panel_rect.x + 18, panel_rect.y + 21))

        for i, opt in enumerate(self.menu_options):
            rect = self.btn_rects[i]
            opt_id = opt["id"]
            is_disabled = (opt_id == "RESUME" and not has_active_game)
            is_selected = (i == self.selected_idx and not is_disabled)
            is_hover = rect.collidepoint(mpos) and not is_disabled

            # Button Background
            if is_disabled:
                bg_col = (20, 22, 26)
                border_col = (45, 50, 58)
                text_col = (75, 80, 90)
            elif is_selected or is_hover:
                bg_col = (40, 48, 62)
                border_col = UI_ACCENT_GOLD
                text_col = (255, 235, 175)
            else:
                bg_col = (24, 28, 36)
                border_col = (80, 85, 95)
                text_col = (210, 215, 225)

            pygame.draw.rect(surface, bg_col, rect, border_radius=6)
            pygame.draw.rect(surface, border_col, rect, 2 if (is_selected or is_hover) else 1, border_radius=6)

            # Fine inset edge and quiet brass rail give the controls a tactile dossier feel.
            if not is_disabled:
                pygame.draw.line(surface, (75, 66, 49) if not (is_selected or is_hover) else (186, 148, 81),
                                 (rect.left + 10, rect.bottom - 3), (rect.right - 10, rect.bottom - 3), 1)

            # Left selection indicator
            if is_selected and not is_disabled:
                pygame.draw.circle(surface, UI_ACCENT_GOLD, (rect.left + 16, rect.centery), 4)

            # Button Text
            btn_txt = self.font_btn.render(opt["label"], True, text_col)
            surface.blit(btn_txt, btn_txt.get_rect(center=rect.center))

        # Bottom status
        prog = self.treasure_mgr.get_progress_percentage()
        unlocked_count = len(self.treasure_mgr.get_all_unlocked())
        total_count = len(self.treasure_mgr.treasures)

        if self.exp_mgr:
            lvl, rank_name = self.exp_mgr.level_and_rank
            status_line = (
                f"Rank: LVL {lvl} {rank_name}  •  Evidence: {unlocked_count}/{total_count} ({prog}% Complete)  •  EXP: {self.exp_mgr.total_exp}"
            )
        else:
            status_line = (
                f"Case Investigation Status: {unlocked_count}/{total_count} Evidence Items Recovered ({prog}% Complete)"
            )

        footer_txt = self.font_card_sub.render(status_line, True, UI_TEXT_MUTED)
        surface.blit(footer_txt, ((SCREEN_WIDTH - footer_txt.get_width()) // 2, SCREEN_HEIGHT - 35))

    def _draw_evidence_dossier(self, surface: pygame.Surface):
        # Modal Box (expanded geometry for perfect card margins)
        box_w = 750
        box_h = 430
        box_x = (SCREEN_WIDTH - box_w) // 2
        box_y = 145
        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

        pygame.draw.rect(surface, (18, 22, 28, 245), box_rect, border_radius=8)
        pygame.draw.rect(surface, UI_PANEL_BORDER, box_rect, 2, border_radius=8)

        # Header Title
        d_title = self.font_card_title.render("CASE EVIDENCE DOSSIER — CONFIDENTIAL RECOVERIES", True, UI_TEXT_TITLE)
        surface.blit(d_title, (box_x + 20, box_y + 14))

        # Detective Rank Credential (Header Right)
        if self.exp_mgr:
            lvl, rank_name = self.exp_mgr.level_and_rank
            rank_txt = self.font_card_sub.render(
                f"DETECTIVE: LVL {lvl} {rank_name.upper()}  |  {self.exp_mgr.total_exp} EXP",
                True,
                UI_ACCENT_GOLD,
            )
            surface.blit(rank_txt, (box_x + box_w - rank_txt.get_width() - 20, box_y + 16))

        # List all 5 treasures
        items = list(self.treasure_mgr.treasures.values())
        card_w = box_w - 40
        card_h = 62
        card_spacing = 8
        start_y = box_y + 44

        for i, item in enumerate(items):
            c_rect = pygame.Rect(box_x + 20, start_y + i * (card_h + card_spacing), card_w, card_h)

            if item.is_unlocked:
                bg = (24, 34, 28)
                border_c = UI_SUCCESS_GREEN
                name_c = (235, 245, 235)
                status_badge = "[RECOVERED]"
                badge_c = UI_SUCCESS_GREEN
                desc_text = f"{item.reward_name}: {item.reward_description}"
            else:
                bg = (20, 22, 28)
                border_c = (60, 65, 75)
                name_c = (140, 145, 155)
                status_badge = "[LOCKED]"
                badge_c = UI_HIGHLIGHT_RED
                desc_text = f"Classified Vault in {item.name}. Solve the room puzzle to unlock."

            pygame.draw.rect(surface, bg, c_rect, border_radius=5)
            pygame.draw.rect(surface, border_c, c_rect, 1, border_radius=5)

            # Name & Badge
            t_name = self.font_card_title.render(f"{i+1}. {item.name}", True, name_c)
            surface.blit(t_name, (c_rect.x + 12, c_rect.y + 7))

            badge_s = self.font_card_sub.render(status_badge, True, badge_c)
            surface.blit(badge_s, (c_rect.right - badge_s.get_width() - 12, c_rect.y + 9))

            # Word-wrap description text to eliminate any overflow
            max_desc_w = card_w - 24
            words = desc_text.split(" ")
            desc_lines = []
            cur_line = []
            for w in words:
                test_str = " ".join(cur_line + [w])
                if self.font_card_body.size(test_str)[0] <= max_desc_w:
                    cur_line.append(w)
                else:
                    if cur_line:
                        desc_lines.append(" ".join(cur_line))
                    cur_line = [w]
            if cur_line:
                desc_lines.append(" ".join(cur_line))

            desc_y = c_rect.y + 27
            for d_line in desc_lines[:2]:
                desc_s = self.font_card_body.render(
                    d_line,
                    True,
                    (195, 200, 210) if item.is_unlocked else (120, 125, 135),
                )
                surface.blit(desc_s, (c_rect.x + 12, desc_y))
                desc_y += 15

        # Close hint
        close_txt = self.font_card_sub.render("Click anywhere or press [ESC] to return to Main Menu", True, UI_ACCENT_GOLD)
        surface.blit(close_txt, ((SCREEN_WIDTH - close_txt.get_width()) // 2, box_rect.bottom - 22))

    def _draw_controls(self, surface: pygame.Surface):
        box_w = 640
        box_h = 360
        box_x = (SCREEN_WIDTH - box_w) // 2
        box_y = 190
        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

        pygame.draw.rect(surface, (18, 22, 28, 245), box_rect, border_radius=8)
        pygame.draw.rect(surface, UI_PANEL_BORDER, box_rect, 2, border_radius=8)

        # Title
        c_title = self.font_card_title.render("INVESTIGATION CONTROLS & MANUAL", True, UI_TEXT_TITLE)
        surface.blit(c_title, (box_x + 24, box_y + 18))

        controls_list = [
            ("WASD / Arrows", "Move Detective through rooms and corridors"),
            ("E / Spacebar", "Inspect clues, documents, and open rooms"),
            ("J", "Open Investigation Journal (Evidence, Connections, Leads)"),
            ("M / TAB", "Open Precinct Blueprint Floor Plan Map"),
            ("ESC", "Pause game / Open Main Menu / Close modals"),
            ("F11 / F", "Toggle Fullscreen display mode"),
            ("Mouse Click", "Click buttons, rotate dials, and select options"),
        ]

        text_y = box_y + 55
        for key, desc in controls_list:
            key_s = self.font_btn.render(f"[{key}]", True, UI_ACCENT_GOLD)
            surface.blit(key_s, (box_x + 30, text_y))

            desc_s = self.font_card_body.render(desc, True, UI_TEXT_BODY)
            surface.blit(desc_s, (box_x + 220, text_y + 2))

            text_y += 34

        # Close hint
        close_txt = self.font_card_sub.render("Click anywhere or press [ESC] to return to Main Menu", True, UI_ACCENT_GOLD)
        surface.blit(close_txt, ((SCREEN_WIDTH - close_txt.get_width()) // 2, box_rect.bottom - 24))
