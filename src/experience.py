"""
Experience & Detective Rank Progression System for Case Unknown.

Provides:
- EXP gain tracking for uncovering case evidence and solving precinct puzzles.
- Detective ranking ladder from Junior Trainee to Chief Superintendent.
- Animated floating notification toasts for EXP gain and Rank promotions.
- Reusable HUD widgets showing current level, rank title, and progress bar.
"""

import math
import pygame
from src.settings import (
    SCREEN_WIDTH,
    UI_PANEL_BG,
    UI_PANEL_BORDER,
    UI_TEXT_TITLE,
    UI_TEXT_BODY,
    UI_TEXT_MUTED,
    UI_ACCENT_GOLD,
    UI_SUCCESS_GREEN,
)

RANKS = [
    (0, 1, "Junior Trainee"),
    (150, 2, "Field Detective"),
    (300, 3, "Senior Investigator"),
    (450, 4, "Lead Inspector"),
    (600, 5, "Chief Superintendent"),
]


class ExperienceManager:
    """Manages player EXP, Detective Rank progression, and level-up toast notifications."""

    def __init__(self):
        self.total_exp = 0
        self.notification_queue = []
        self.active_notification = None
        self.notif_timer = 0.0
        self.notif_duration = 3.8

        pygame.font.init()
        self.font_notif_title = pygame.font.SysFont("georgia", 15, bold=True)
        self.font_notif_body = pygame.font.SysFont("segoeui", 12)
        self.font_hud = pygame.font.SysFont("segoeui", 11, bold=True)
        self.font_hud_sub = pygame.font.SysFont("segoeui", 10)

    @property
    def level_and_rank(self) -> tuple[int, str]:
        """Returns (level, rank_name) according to total_exp."""
        current_lvl = 1
        current_rank = "Junior Trainee"
        for thresh, lvl, r_name in RANKS:
            if self.total_exp >= thresh:
                current_lvl = lvl
                current_rank = r_name
        return current_lvl, current_rank

    def get_level_progress(self) -> tuple[int, int, float]:
        """Returns (exp_in_level, exp_needed, progress_ratio_0_to_1)."""
        lvl, _ = self.level_and_rank
        if lvl >= 5:
            return 150, 150, 1.0

        current_thresh = 150 * (lvl - 1)
        next_thresh = 150 * lvl
        exp_in_level = self.total_exp - current_thresh
        needed = next_thresh - current_thresh
        ratio = max(0.0, min(1.0, exp_in_level / needed))
        return exp_in_level, needed, ratio

    def add_experience(self, amount: int, reason: str = "Evidence Recovered") -> dict:
        """Awards EXP, checks for promotion, and enqueues a celebratory toast notification."""
        old_lvl, _ = self.level_and_rank
        self.total_exp += amount
        new_lvl, new_rank = self.level_and_rank
        leveled_up = new_lvl > old_lvl

        notif_data = {
            "amount": amount,
            "reason": reason,
            "leveled_up": leveled_up,
            "new_rank": new_rank,
            "new_lvl": new_lvl,
        }
        self.notification_queue.append(notif_data)

        return {
            "gained": amount,
            "total_exp": self.total_exp,
            "leveled_up": leveled_up,
            "new_level": new_lvl,
            "rank": new_rank,
        }

    def update(self, delta_time: float):
        """Updates toast notification timers and transitions between notifications."""
        if self.active_notification is not None:
            self.notif_timer -= delta_time
            if self.notif_timer <= 0:
                self.active_notification = None
                self.notif_timer = 0.0

        if self.active_notification is None and self.notification_queue:
            self.active_notification = self.notification_queue.pop(0)
            self.notif_timer = self.notif_duration

    def draw_notification(self, surface: pygame.Surface):
        """Draws floating animated toast notification at the top-center of the screen."""
        if self.active_notification is None:
            return

        data = self.active_notification
        # Animation: Slide down and fade out
        anim_progress = (self.notif_duration - self.notif_timer) / self.notif_duration
        # Slide down from y = -60 to y = 58
        if anim_progress < 0.15:
            t = anim_progress / 0.15
            toast_y = int(-50 + 108 * (1 - (1 - t) ** 3))
            alpha = int(255 * t)
        elif anim_progress > 0.85:
            t = (anim_progress - 0.85) / 0.15
            toast_y = 58
            alpha = int(255 * (1 - t))
        else:
            toast_y = 58
            alpha = 255

        toast_w = 340
        toast_h = 52
        toast_x = (SCREEN_WIDTH - toast_w) // 2

        toast_surf = pygame.Surface((toast_w, toast_h), pygame.SRCALPHA)
        toast_surf.fill((18, 22, 28, min(245, alpha)))
        pygame.draw.rect(toast_surf, UI_ACCENT_GOLD, (0, 0, toast_w, toast_h), 2, border_radius=6)
        pygame.draw.rect(toast_surf, (80, 65, 35), (2, 2, toast_w - 4, toast_h - 4), 1, border_radius=4)

        # Star icon
        pygame.draw.circle(toast_surf, UI_ACCENT_GOLD, (24, toast_h // 2), 12)
        pygame.draw.circle(toast_surf, (20, 20, 20), (24, toast_h // 2), 4)

        if data["leveled_up"]:
            title_txt = f"PROMOTED! {data['new_rank'].upper()}"
            title_col = UI_SUCCESS_GREEN
            sub_txt = f"+{data['amount']} EXP  •  Rank Level {data['new_lvl']} Achieved!"
        else:
            title_txt = f"+{data['amount']} EXP AWARDED"
            title_col = UI_ACCENT_GOLD
            sub_txt = f"{data['reason']}  •  Total EXP: {self.total_exp}"

        t_surf = self.font_notif_title.render(title_txt, True, title_col)
        toast_surf.blit(t_surf, (46, 8))

        s_surf = self.font_notif_body.render(sub_txt, True, (215, 220, 230))
        toast_surf.blit(s_surf, (46, 28))

        surface.blit(toast_surf, (toast_x, toast_y))

    def draw_hud_widget(self, surface: pygame.Surface, x: int, y: int, width: int = 240, height: int = 32):
        """Draws compact EXP progress bar and Rank title on HUD bars."""
        lvl, rank_name = self.level_and_rank
        exp_in, exp_needed, ratio = self.get_level_progress()

        # Background badge
        bg_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        bg_surf.fill((16, 20, 26, 215))
        pygame.draw.rect(bg_surf, (70, 60, 45), (0, 0, width, height), 1, border_radius=4)
        surface.blit(bg_surf, (x, y))

        # Title: Level and Rank
        lvl_text = f"LVL {lvl}  |  {rank_name}"
        t_surf = self.font_hud.render(lvl_text, True, (240, 215, 150))
        surface.blit(t_surf, (x + 8, y + 4))

        # Mini Progress Bar
        bar_x = x + 8
        bar_y = y + 20
        bar_w = width - 16
        bar_h = 6

        pygame.draw.rect(surface, (25, 30, 38), (bar_x, bar_y, bar_w, bar_h), border_radius=2)
        fill_w = max(2, int(bar_w * ratio))
        pygame.draw.rect(surface, UI_ACCENT_GOLD, (bar_x, bar_y, fill_w, bar_h), border_radius=2)
        pygame.draw.rect(surface, (90, 75, 45), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=2)
