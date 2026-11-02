"""Evidence-reader visual helpers for inspection panels and transcripts."""

import pygame
from src.ui.primitives import draw_noir_panel


class EvidenceReaderFrame:
    """Draws the shared dossier frame used by evidence and object inspection."""

    @staticmethod
    def draw(surface: pygame.Surface, rect: pygame.Rect):
        draw_noir_panel(surface, rect, fill=(19, 23, 25), border=(122, 105, 72))
        pygame.draw.rect(surface, (46, 48, 43), rect.inflate(-8, -8), 1, border_radius=6)
        pygame.draw.rect(surface, (173, 139, 79), (rect.x, rect.y, 5, rect.height), border_top_left_radius=8, border_bottom_left_radius=8)

    @staticmethod
    def draw_content(surface: pygame.Surface, rect: pygame.Rect):
        pygame.draw.rect(surface, (23, 27, 28), rect, border_radius=4)
        pygame.draw.rect(surface, (61, 65, 60), rect, 1, border_radius=4)
