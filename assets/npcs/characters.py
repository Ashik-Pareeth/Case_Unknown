"""NPC character colorways built from the shared vector character generator."""

from dataclasses import replace
from functools import lru_cache

import pygame

from assets.characters import DETECTIVE_PALETTE, get_character_animations


NPC_PALETTES = (
    replace(
        DETECTIVE_PALETTE,
        coat_light="#33383d",
        coat_mid="#24292e",
        coat_dark="#171b20",
        coat_deep="#101317",
        coat_shadow="#0c0f12",
        coat_line_shadow="#0c0f12",
        coat_crease="#080a0d",
        coat_lapel_l="#171b20",
        coat_lapel_r="#101317",
        coat_up_mid="#24292e",
        coat_side_arm="#111519",
        coat_side_light="#30353a",
        coat_side_dark="#101317",
        coat_side_back_dark="#0c0f12",
        coat_lapel_side_base="#171b20",
        coat_lapel_side_light="#30353a",
        tie_red="#17191c",
        tie_highlight="#30343a",
    ),
    replace(
        DETECTIVE_PALETTE,
        coat_light="#292d32",
        coat_mid="#1c2025",
        coat_dark="#13171b",
        coat_deep="#0c0f13",
        coat_shadow="#090b0e",
        coat_line_shadow="#090b0e",
        coat_crease="#06080a",
        coat_lapel_l="#13171b",
        coat_lapel_r="#0c0f13",
        coat_up_mid="#1c2025",
        coat_side_arm="#0e1216",
        coat_side_light="#292d32",
        coat_side_dark="#0c0f13",
        coat_side_back_dark="#090b0e",
        coat_lapel_side_base="#13171b",
        coat_lapel_side_light="#292d32",
        tie_red="#121519",
        tie_highlight="#292d32",
    ),
)


@lru_cache(maxsize=len(NPC_PALETTES))
def get_npc_animations(palette_index: int = 0):
    """Return cached four-direction idle and walk frames for an NPC colorway."""
    base = get_character_animations(NPC_PALETTES[palette_index % len(NPC_PALETTES)])
    return {
        direction: {
            state: [_add_mask(frame, direction) for frame in frames]
            for state, frames in states.items()
        }
        for direction, states in base.items()
    }


def _add_mask(frame, direction):
    """Overlay a full robber-style face covering with narrow eye openings."""
    masked = frame.copy()
    if direction == "down":
        points = [(21, 13), (25, 11), (39, 11), (43, 13), (44, 20),
                  (41, 26), (36, 30), (28, 30), (22, 26), (19, 20)]
    elif direction in ("left", "right"):
        points = [(32, 12), (39, 11), (43, 15), (42, 21),
                  (39, 25), (34, 23), (31, 18)]
        if direction == "left":
            points = [(64 - x, y) for x, y in points]
    else:
        # Back view keeps the hat visible while covering the exposed nape.
        pygame.draw.polygon(masked, (8, 10, 13), [(22, 13), (42, 13), (42, 26), (37, 30), (27, 30), (22, 26)])
        return _add_oval_coat(masked, direction)

    pygame.draw.polygon(masked, (8, 10, 13), points)
    pygame.draw.line(masked, (46, 49, 52), points[1], points[2], 1)
    if direction == "down":
        eyes = ((24, 15), (35, 15))
    else:
        eye_x = 35 if direction == "right" else 26
        eyes = ((eye_x, 15),)
    for x, y in eyes:
        pygame.draw.ellipse(masked, (37, 40, 43), (x, y, 6, 2))
        pygame.draw.line(masked, (168, 153, 133), (x + 2, y + 1), (x + 4, y + 1), 1)
    return _add_oval_coat(masked, direction)


def _add_oval_coat(frame, direction):
    """Give the overcoat a broad, rounded silhouette while preserving the limbs."""
    if direction in ("left", "right"):
        body = pygame.Rect(17, 29, 32, 30)
    else:
        body = pygame.Rect(14, 29, 36, 30)
    pygame.draw.ellipse(frame, (12, 15, 19), body)
    pygame.draw.ellipse(frame, (39, 43, 47), body, 1)
    seam_x = body.centerx
    pygame.draw.line(frame, (25, 29, 33), (seam_x, body.y + 6), (seam_x, body.bottom - 5), 1)
    return frame
