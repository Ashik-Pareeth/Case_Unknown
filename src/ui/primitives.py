"""Small visual primitives shared by the game's distinct UI groups."""

import pygame


def draw_noir_panel(surface: pygame.Surface, rect: pygame.Rect, *, fill=(22, 27, 29), border=(119, 104, 73), shadow=True):
    if shadow:
        pygame.draw.rect(surface, (4, 6, 7), rect.inflate(16, 16).move(0, 9), border_radius=11)
    pygame.draw.rect(surface, fill, rect, border_radius=8)
    pygame.draw.rect(surface, border, rect, 1, border_radius=8)
    pygame.draw.rect(surface, (45, 50, 49), rect.inflate(-8, -8), 1, border_radius=6)


def draw_label(surface: pygame.Surface, text: str, font: pygame.font.Font, color, position):
    surface.blit(font.render(text, True, color), position)


def draw_button(surface: pygame.Surface, rect: pygame.Rect, label: str, font: pygame.font.Font,
                *, fill, border, text_color, hover=False, border_width=1, radius=5):
    color = tuple(min(255, c + 18) for c in fill) if hover else fill
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, border_width, border_radius=radius)
    rendered = font.render(label, True, text_color)
    surface.blit(rendered, rendered.get_rect(center=rect.center))
