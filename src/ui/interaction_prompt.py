"""Context prompt shown for the nearest inspectable room object."""

import math
import pygame


class InteractionPrompt:
    def __init__(self, badge: pygame.Surface):
        self.badge = badge

    def draw(self, surface: pygame.Surface, position: tuple[int, int], time: float):
        x, y = position
        y += math.sin(time * 5.0) * 3.5
        surface.blit(self.badge, (x - self.badge.get_width() // 2, y - self.badge.get_height() // 2))
