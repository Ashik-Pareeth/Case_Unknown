"""
Interactive Puzzle Mini-Game Engine for Case Unknown.

Provides:
- NumberLockPuzzle: Rotary dial combination lock with clues and digit controls.
- TileAlignPuzzle: Symbol/gear alignment puzzle with rotation controls and visual alignment targets.
- BasePuzzle: Common modal framework with keyboard and mouse interaction support.
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
    UI_ACCENT_GOLD,
    UI_SUCCESS_GREEN,
)


class BasePuzzle:
    """Base class for puzzle overlays."""

    def __init__(self, title: str, hint: str, reward_name: str):
        self.title = title
        self.hint = hint
        self.reward_name = reward_name
        self.is_solved = False
        self.is_closed = False
        self.show_hint = False
        self.feedback_message = ""
        self.feedback_timer = 0.0
        self.feedback_color = UI_TEXT_MUTED

        # Modal Dimensions
        self.modal_w = 640
        self.modal_h = 470
        self.modal_x = (SCREEN_WIDTH - self.modal_w) // 2
        self.modal_y = (SCREEN_HEIGHT - self.modal_h) // 2
        self.modal_rect = pygame.Rect(self.modal_x, self.modal_y, self.modal_w, self.modal_h)


        # Fonts
        pygame.font.init()
        self.font_title = pygame.font.SysFont("georgia", 20, bold=True)
        self.font_sub = pygame.font.SysFont("segoeui", 14)
        self.font_dial = pygame.font.SysFont("georgia", 32, bold=True)
        self.font_btn = pygame.font.SysFont("segoeui", 13, bold=True)
        self.font_hint = pygame.font.SysFont("georgia", 14, italic=True)

        # Interactive Button Rectangles (cached for mouse clicks)
        self.btn_check_rect = pygame.Rect(self.modal_x + self.modal_w // 2 - 140, self.modal_y + self.modal_h - 68, 130, 36)
        self.btn_hint_rect = pygame.Rect(self.modal_x + self.modal_w // 2 + 10, self.modal_y + self.modal_h - 68, 130, 36)
        self.btn_close_rect = pygame.Rect(self.modal_x + self.modal_w - 42, self.modal_y + 12, 30, 30)

    def set_feedback(self, text: str, color=UI_TEXT_MUTED, duration: float = 2.5):
        self.feedback_message = text
        self.feedback_color = color
        self.feedback_timer = duration

    def update(self, delta_time: float):
        if self.feedback_timer > 0:
            self.feedback_timer -= delta_time
            if self.feedback_timer <= 0:
                self.feedback_message = ""

    def draw_modal_frame(self, surface: pygame.Surface):
        # 1. Dark backdrop dim
        backdrop = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        backdrop.fill((8, 10, 14, 215))
        surface.blit(backdrop, (0, 0))

        # 2. Main Puzzle Panel
        panel = pygame.Surface((self.modal_w, self.modal_h), pygame.SRCALPHA)
        panel.fill(UI_PANEL_BG)
        surface.blit(panel, (self.modal_x, self.modal_y))

        # 3. Antique Brass Border & Rivets
        pygame.draw.rect(surface, UI_PANEL_BORDER, self.modal_rect, 2, border_radius=8)
        inner_rect = self.modal_rect.inflate(-8, -8)
        pygame.draw.rect(surface, (60, 52, 38), inner_rect, 1, border_radius=6)

        # Brass corner rivets
        for cx, cy in [
            (self.modal_rect.left + 12, self.modal_rect.top + 12),
            (self.modal_rect.right - 12, self.modal_rect.top + 12),
            (self.modal_rect.left + 12, self.modal_rect.bottom - 12),
            (self.modal_rect.right - 12, self.modal_rect.bottom - 12),
        ]:
            pygame.draw.circle(surface, UI_ACCENT_GOLD, (cx, cy), 3)

        # Header Title Bar
        title_surf = self.font_title.render(self.title, True, UI_TEXT_TITLE)
        surface.blit(title_surf, (self.modal_x + 24, self.modal_y + 18))

        sub_surf = self.font_sub.render(f"Reward: {self.reward_name}", True, UI_TEXT_MUTED)
        surface.blit(sub_surf, (self.modal_x + 24, self.modal_y + 46))

        # Close [X] Button
        mouse_pos = pygame.mouse.get_pos()
        close_hover = self.btn_close_rect.collidepoint(mouse_pos)
        close_bg = (180, 50, 50) if close_hover else (45, 50, 60)
        pygame.draw.rect(surface, close_bg, self.btn_close_rect, border_radius=4)
        pygame.draw.rect(surface, UI_PANEL_BORDER, self.btn_close_rect, 1, border_radius=4)
        close_text = self.font_btn.render("X", True, (240, 240, 240))
        surface.blit(close_text, close_text.get_rect(center=self.btn_close_rect.center))

        # Bottom Action Buttons
        check_hover = self.btn_check_rect.collidepoint(mouse_pos)
        check_color = (60, 110, 75) if check_hover else (35, 65, 45)
        if self.is_solved:
            check_color = (40, 140, 70)
        pygame.draw.rect(surface, check_color, self.btn_check_rect, border_radius=5)
        pygame.draw.rect(surface, UI_SUCCESS_GREEN if self.is_solved else UI_PANEL_BORDER, self.btn_check_rect, 1, border_radius=5)
        check_label = "UNLOCKED!" if self.is_solved else "UNLOCK [ENTER]"
        btn_check_surf = self.font_btn.render(check_label, True, (240, 245, 240))
        surface.blit(btn_check_surf, btn_check_surf.get_rect(center=self.btn_check_rect.center))

        hint_hover = self.btn_hint_rect.collidepoint(mouse_pos)
        hint_color = (75, 65, 40) if hint_hover else (45, 40, 30)
        pygame.draw.rect(surface, hint_color, self.btn_hint_rect, border_radius=5)
        pygame.draw.rect(surface, UI_PANEL_BORDER, self.btn_hint_rect, 1, border_radius=5)
        hint_label = "HIDE HINT [H]" if self.show_hint else "VIEW HINT [H]"
        btn_hint_surf = self.font_btn.render(hint_label, True, UI_ACCENT_GOLD)
        surface.blit(btn_hint_surf, btn_hint_surf.get_rect(center=self.btn_hint_rect.center))

        # Hint Box (when toggled with multi-line word wrapping)
        if self.show_hint:
            full_hint_text = f"Detective Note: \"{self.hint}\""
            max_hint_w = self.modal_w - 90
            words = full_hint_text.split(" ")
            hint_lines = []
            cur_line = []
            for w in words:
                test = " ".join(cur_line + [w])
                if self.font_hint.size(test)[0] <= max_hint_w:
                    cur_line.append(w)
                else:
                    hint_lines.append(" ".join(cur_line))
                    cur_line = [w]
            if cur_line:
                hint_lines.append(" ".join(cur_line))

            box_h = max(48, 16 + len(hint_lines) * 20)
            hint_box_rect = pygame.Rect(self.modal_x + 30, self.modal_y + self.modal_h - 78 - box_h, self.modal_w - 60, box_h)
            pygame.draw.rect(surface, (18, 22, 28, 245), hint_box_rect, border_radius=5)
            pygame.draw.rect(surface, (140, 115, 65), hint_box_rect, 1, border_radius=5)

            hy = hint_box_rect.y + 10
            for line in hint_lines:
                ht_surf = self.font_hint.render(line, True, (240, 225, 175))
                surface.blit(ht_surf, (hint_box_rect.x + 14, hy))
                hy += 20

        # Feedback Message Banner
        if self.feedback_message:
            fb_surf = self.font_btn.render(self.feedback_message, True, self.feedback_color)
            fb_rect = fb_surf.get_rect(center=(self.modal_x + self.modal_w // 2, self.modal_y + self.modal_h - 146))
            surface.blit(fb_surf, fb_rect)



class NumberLockPuzzle(BasePuzzle):
    """
    Rotary Tumbler Combination Lock.
    Player adjusts digit wheels using Left/Right to select, Up/Down or +/- buttons to change.
    """

    def __init__(self, title: str, target_code: list[int], hint: str, reward_name: str):
        super().__init__(title, hint, reward_name)
        self.target_code = list(target_code)
        self.num_digits = len(target_code)
        self.current_code = [0] * self.num_digits
        self.selected_idx = 0

        # Calculate dial bounding boxes
        self.dial_w = 64
        self.dial_h = 96
        dial_spacing = 30
        total_dials_w = self.num_digits * self.dial_w + (self.num_digits - 1) * dial_spacing
        start_x = self.modal_x + (self.modal_w - total_dials_w) // 2
        dial_y = self.modal_y + 140

        self.dial_rects = []
        self.btn_up_rects = []
        self.btn_down_rects = []

        for i in range(self.num_digits):
            dx = start_x + i * (self.dial_w + dial_spacing)
            self.dial_rects.append(pygame.Rect(dx, dial_y, self.dial_w, self.dial_h))
            self.btn_up_rects.append(pygame.Rect(dx + 12, dial_y - 30, self.dial_w - 24, 22))
            self.btn_down_rects.append(pygame.Rect(dx + 12, dial_y + self.dial_h + 8, self.dial_w - 24, 22))


    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_closed = True
                return True
            elif event.key == pygame.K_h:
                self.show_hint = not self.show_hint
                return True
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.check_solution()
                return True
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected_idx = (self.selected_idx - 1) % self.num_digits
                return True
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected_idx = (self.selected_idx + 1) % self.num_digits
                return True
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.current_code[self.selected_idx] = (self.current_code[self.selected_idx] + 1) % 10
                return True
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.current_code[self.selected_idx] = (self.current_code[self.selected_idx] - 1) % 10
                return True
            elif pygame.K_0 <= event.key <= pygame.K_9:
                # Direct digit input
                digit = event.key - pygame.K_0
                self.current_code[self.selected_idx] = digit
                self.selected_idx = (self.selected_idx + 1) % self.num_digits
                return True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mpos = event.pos
            if self.btn_close_rect.collidepoint(mpos):
                self.is_closed = True
                return True
            if self.btn_hint_rect.collidepoint(mpos):
                self.show_hint = not self.show_hint
                return True
            if self.btn_check_rect.collidepoint(mpos):
                self.check_solution()
                return True

            # Check dial buttons
            for i in range(self.num_digits):
                if self.btn_up_rects[i].collidepoint(mpos):
                    self.selected_idx = i
                    self.current_code[i] = (self.current_code[i] + 1) % 10
                    return True
                if self.btn_down_rects[i].collidepoint(mpos):
                    self.selected_idx = i
                    self.current_code[i] = (self.current_code[i] - 1) % 10
                    return True
                if self.dial_rects[i].collidepoint(mpos):
                    self.selected_idx = i
                    self.current_code[i] = (self.current_code[i] + 1) % 10
                    return True

        return False

    def check_solution(self):
        if self.current_code == self.target_code:
            self.is_solved = True
            self.set_feedback("SUCCESS! The tumbler clicks open!", UI_SUCCESS_GREEN, 5.0)
        else:
            self.set_feedback("INCORRECT COMBINATION. The mechanism resists.", UI_HIGHLIGHT_RED, 2.5)

    def draw(self, surface: pygame.Surface):
        self.draw_modal_frame(surface)

        # Instructions Banner
        instr_surf = self.font_sub.render("Align the tumbler dials to unlock the vault. Use [WASD / Arrows / Click]", True, UI_TEXT_MUTED)
        surface.blit(instr_surf, (self.modal_x + 24, self.modal_y + 76))

        mpos = pygame.mouse.get_pos()

        # Render each Tumbler Dial
        for i in range(self.num_digits):
            d_rect = self.dial_rects[i]
            is_active = (i == self.selected_idx)

            # Up Button [+]
            up_r = self.btn_up_rects[i]
            up_hover = up_r.collidepoint(mpos)
            pygame.draw.rect(surface, (60, 68, 80) if up_hover else (35, 40, 48), up_r, border_radius=3)
            pygame.draw.rect(surface, UI_ACCENT_GOLD if up_hover else (70, 75, 85), up_r, 1, border_radius=3)
            up_txt = self.font_btn.render("+", True, UI_ACCENT_GOLD if up_hover else UI_TEXT_BODY)
            surface.blit(up_txt, up_txt.get_rect(center=up_r.center))

            # Tumbler Barrel
            barrel_surf = pygame.Surface((self.dial_w, self.dial_h), pygame.SRCALPHA)
            barrel_surf.fill((16, 18, 24))
            pygame.draw.rect(barrel_surf, (35, 40, 50), (0, 0, self.dial_w, self.dial_h))
            # Barrel cylinder gradient simulation
            pygame.draw.rect(barrel_surf, (20, 24, 30), (0, 0, self.dial_w, 20))
            pygame.draw.rect(barrel_surf, (20, 24, 30), (0, self.dial_h - 20, self.dial_w, 20))
            surface.blit(barrel_surf, d_rect)

            border_color = UI_ACCENT_GOLD if is_active else (80, 85, 95)
            border_w = 3 if is_active else 1
            pygame.draw.rect(surface, border_color, d_rect, border_w, border_radius=4)

            # Digit Text
            digit_color = (255, 230, 160) if is_active else (220, 225, 235)
            digit_surf = self.font_dial.render(str(self.current_code[i]), True, digit_color)
            surface.blit(digit_surf, digit_surf.get_rect(center=d_rect.center))

            # Down Button [-]
            down_r = self.btn_down_rects[i]
            down_hover = down_r.collidepoint(mpos)
            pygame.draw.rect(surface, (60, 68, 80) if down_hover else (35, 40, 48), down_r, border_radius=3)
            pygame.draw.rect(surface, UI_ACCENT_GOLD if down_hover else (70, 75, 85), down_r, 1, border_radius=3)
            down_txt = self.font_btn.render("-", True, UI_ACCENT_GOLD if down_hover else UI_TEXT_BODY)
            surface.blit(down_txt, down_txt.get_rect(center=down_r.center))


class TileAlignPuzzle(BasePuzzle):
    """
    Forensic Tile / Gear Alignment Puzzle.
    Player rotates 4 circular dials/tiles so that the directional pointers or symbols match
    the required sequence (0: North, 90: East, 180: South, 270: West).
    """

    def __init__(self, title: str, target_angles: list[int], hint: str, reward_name: str):
        super().__init__(title, hint, reward_name)
        self.target_angles = list(target_angles)  # e.g. [0, 90, 180, 270]
        self.num_tiles = len(target_angles)
        # Start in scrambled state
        self.current_angles = [(target_angles[i] + 90 * (i + 1)) % 360 for i in range(self.num_tiles)]
        self.selected_idx = 0

        # Symbols / Labels
        self.labels = ["DIAL I", "DIAL II", "DIAL III", "DIAL IV"]
        self.tile_size = 90
        spacing = 28
        total_w = self.num_tiles * self.tile_size + (self.num_tiles - 1) * spacing
        start_x = self.modal_x + (self.modal_w - total_w) // 2
        tile_y = self.modal_y + 130

        self.tile_rects = []
        for i in range(self.num_tiles):
            tx = start_x + i * (self.tile_size + spacing)
            self.tile_rects.append(pygame.Rect(tx, tile_y, self.tile_size, self.tile_size))


    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_closed = True
                return True
            elif event.key == pygame.K_h:
                self.show_hint = not self.show_hint
                return True
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.check_solution()
                return True
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected_idx = (self.selected_idx - 1) % self.num_tiles
                return True
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected_idx = (self.selected_idx + 1) % self.num_tiles
                return True
            elif event.key in (pygame.K_UP, pygame.K_w, pygame.K_r):
                # Rotate clockwise 90 degrees
                self.current_angles[self.selected_idx] = (self.current_angles[self.selected_idx] + 90) % 360
                return True
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                # Rotate counter-clockwise 90 degrees
                self.current_angles[self.selected_idx] = (self.current_angles[self.selected_idx] - 90) % 360
                return True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mpos = event.pos
            if self.btn_close_rect.collidepoint(mpos):
                self.is_closed = True
                return True
            if self.btn_hint_rect.collidepoint(mpos):
                self.show_hint = not self.show_hint
                return True
            if self.btn_check_rect.collidepoint(mpos):
                self.check_solution()
                return True

            for i in range(self.num_tiles):
                if self.tile_rects[i].collidepoint(mpos):
                    self.selected_idx = i
                    # Click rotates 90 degrees
                    self.current_angles[i] = (self.current_angles[i] + 90) % 360
                    return True

        return False

    def check_solution(self):
        if self.current_angles == self.target_angles:
            self.is_solved = True
            self.set_feedback("MECHANISM ALIGNED! The vault unlocks!", UI_SUCCESS_GREEN, 5.0)
        else:
            self.set_feedback("MISALIGNED. Pins fail to connect.", UI_HIGHLIGHT_RED, 2.5)

    def draw(self, surface: pygame.Surface):
        self.draw_modal_frame(surface)

        # Instructions
        instr_surf = self.font_sub.render("Rotate each forensic tumbler to the required angle [Click or A/D to select, W/S to rotate]", True, UI_TEXT_MUTED)
        surface.blit(instr_surf, (self.modal_x + 24, self.modal_y + 76))

        for i in range(self.num_tiles):
            rect = self.tile_rects[i]
            is_active = (i == self.selected_idx)
            center = rect.center
            radius = self.tile_size // 2 - 4

            # Dial Backplate
            pygame.draw.circle(surface, (25, 29, 36), center, radius)
            pygame.draw.circle(surface, (40, 46, 56), center, radius - 4)

            # Outer border / selection indicator
            border_c = UI_ACCENT_GOLD if is_active else (80, 85, 95)
            pygame.draw.circle(surface, border_c, center, radius, 3 if is_active else 1)

            # 4 Cardinal tick marks (N, E, S, W)
            for angle in [0, 90, 180, 270]:
                rad = math.radians(angle - 90)
                tx1 = center[0] + (radius - 10) * math.cos(rad)
                ty1 = center[1] + (radius - 10) * math.sin(rad)
                tx2 = center[0] + (radius - 4) * math.cos(rad)
                ty2 = center[1] + (radius - 4) * math.sin(rad)
                pygame.draw.line(surface, (120, 110, 85), (tx1, ty1), (tx2, ty2), 2)

            # Directional Needle / Gear Arrow
            cur_angle = self.current_angles[i]
            rad = math.radians(cur_angle - 90)
            tip_x = center[0] + (radius - 12) * math.cos(rad)
            tip_y = center[1] + (radius - 12) * math.sin(rad)

            tail_rad = math.radians(cur_angle + 90)
            tail_x = center[0] + 12 * math.cos(tail_rad)
            tail_y = center[1] + 12 * math.sin(tail_rad)

            side1_rad = math.radians(cur_angle)
            side1_x = center[0] + 7 * math.cos(side1_rad)
            side1_y = center[1] + 7 * math.sin(side1_rad)

            side2_rad = math.radians(cur_angle + 180)
            side2_x = center[0] + 7 * math.cos(side2_rad)
            side2_y = center[1] + 7 * math.sin(side2_rad)

            needle_poly = [(tip_x, tip_y), (side1_x, side1_y), (tail_x, tail_y), (side2_x, side2_y)]
            needle_col = (235, 195, 100) if is_active else (180, 150, 80)
            pygame.draw.polygon(surface, needle_col, needle_poly)
            pygame.draw.polygon(surface, (80, 60, 20), needle_poly, 1)

            # Center Brass Pivot
            pygame.draw.circle(surface, UI_ACCENT_GOLD, center, 5)
            pygame.draw.circle(surface, (20, 20, 20), center, 2)

            # Label below tile
            lbl_surf = self.font_btn.render(self.labels[i % len(self.labels)], True, UI_TEXT_MUTED)
            surface.blit(lbl_surf, lbl_surf.get_rect(center=(center[0], rect.bottom + 16)))
