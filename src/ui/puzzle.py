"""Shared frame and controls for the game's lock and alignment puzzles."""

import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    UI_PANEL_BORDER,
    UI_ACCENT_GOLD,
    UI_SUCCESS_GREEN,
)
from src.ui.primitives import draw_noir_panel, draw_button


def draw_puzzle_frame(component, surface: pygame.Surface):
    backdrop = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    backdrop.fill((6, 9, 12, 170))
    surface.blit(backdrop, (0, 0))
    draw_noir_panel(surface, component.modal_rect)

    header = pygame.Rect(
        component.modal_x + 5, component.modal_y + 5, component.modal_w - 10, 72
    )
    pygame.draw.rect(
        surface,
        (30, 36, 37),
        header,
        border_top_left_radius=7,
        border_top_right_radius=7,
    )
    pygame.draw.rect(
        surface, (177, 143, 82), (component.modal_x, component.modal_y + 12, 4, 48)
    )
    component_label(
        surface,
        "FIELD MECHANISM  /  CASE ACCESS",
        component.font_kicker,
        (148, 162, 151),
        (component.modal_x + 24, component.modal_y + 12),
    )
    component_label(
        surface,
        component.title,
        component.font_title,
        (230, 218, 184),
        (component.modal_x + 24, component.modal_y + 31),
    )
    component_label(
        surface,
        component.reward_name,
        component.font_sub,
        (163, 163, 145),
        (component.modal_x + 25, component.modal_y + 55),
    )
    pygame.draw.line(
        surface,
        (76, 79, 70),
        (component.modal_x + 20, component.modal_y + 78),
        (component.modal_rect.right - 20, component.modal_y + 78),
        1,
    )

    mouse = pygame.mouse.get_pos()
    draw_button(
        surface,
        component.btn_close_rect,
        "X",
        component.font_btn,
        fill=(42, 48, 47),
        border=UI_PANEL_BORDER,
        text_color=(240, 240, 240),
        hover=component.btn_close_rect.collidepoint(mouse),
        radius=4,
    )
    check_fill = (
        (40, 140, 70)
        if component.is_solved
        else (
            (60, 110, 75)
            if component.btn_check_rect.collidepoint(mouse)
            else (35, 65, 45)
        )
    )
    draw_button(
        surface,
        component.btn_check_rect,
        "UNLOCKED!" if component.is_solved else "UNLOCK [ENTER]",
        component.font_btn,
        fill=check_fill,
        border=UI_SUCCESS_GREEN if component.is_solved else UI_PANEL_BORDER,
        text_color=(240, 245, 240),
        hover=component.btn_check_rect.collidepoint(mouse),
    )
    draw_button(
        surface,
        component.btn_hint_rect,
        "HIDE HINT [H]" if component.show_hint else "VIEW HINT [H]",
        component.font_btn,
        fill=(45, 40, 30),
        border=UI_PANEL_BORDER,
        text_color=UI_ACCENT_GOLD,
        hover=component.btn_hint_rect.collidepoint(mouse),
    )

    if component.show_hint:
        lines = wrap_text(
            f'Detective Note: "{component.hint}"',
            component.font_hint,
            component.modal_w - 90,
        )
        box_h = max(48, 16 + len(lines) * 20)
        box = pygame.Rect(
            component.modal_x + 30,
            component.modal_y + component.modal_h - 78 - box_h,
            component.modal_w - 60,
            box_h,
        )
        pygame.draw.rect(surface, (18, 22, 28), box, border_radius=5)
        pygame.draw.rect(surface, (140, 115, 65), box, 1, border_radius=5)
        for i, line in enumerate(lines):
            component_label(
                surface,
                line,
                component.font_hint,
                (240, 225, 175),
                (box.x + 14, box.y + 10 + i * 20),
            )
    if component.feedback_message:
        text = component.font_btn.render(
            component.feedback_message, True, component.feedback_color
        )
        surface.blit(
            text,
            text.get_rect(
                center=(
                    component.modal_x + component.modal_w // 2,
                    component.modal_y + component.modal_h - 146,
                )
            ),
        )


def component_label(surface, text, font, color, pos):
    surface.blit(font.render(text, True, color), pos)


def wrap_text(text, font, width):
    lines, current = [], []
    for word in text.split():
        candidate = " ".join(current + [word])
        if font.size(candidate)[0] <= width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines
