"""NPC gangster character colorways built from the shared vector character generator.

Three distinct mob archetypes, each with a unique palette and face overlay:
  0 – "The Enforcer"   : charcoal pinstripe suit, brutish scar, heavy stubble
  1 – "The Fixer"      : midnight navy suit, slicked hair, thin moustache, cigar
  2 – "The Lookout"    : dark olive suit, hollow cheeks, nervous narrow eyes
"""

from dataclasses import replace
from functools import lru_cache

import pygame

from assets.characters import DETECTIVE_PALETTE, get_character_animations


# ---------------------------------------------------------------------------
# Gangster Palettes
# ---------------------------------------------------------------------------

# Shared dark base overrides applied to all gangsters (shoes stay dark, brows dark)
_GANGSTER_BASE = dict(
    # Menacing dark brows (shared; individual palettes may not re-specify these)
    brow_front="#1a1208",
    brow_side="#0e0b04",
    # Dark, worn shoes
    shoe_black="#0e1014",
    shoe_leather="#181c22",
    shoe_leather_side="#181c24",
    shoe_darkest="#0a0c10",
    shoe_highlight="#222630",
    shoe_sole="#080a0e",
)

# 0 – The Enforcer: charcoal suit, heavy build, intimidating
ENFORCER_PALETTE = replace(
    DETECTIVE_PALETTE,
    **_GANGSTER_BASE,
    # Charcoal-grey pinstripe suit
    coat_light="#4a4f58",
    coat_mid="#393e47",
    coat_dark="#2e333b",
    coat_deep="#242930",
    coat_shadow="#1c2028",
    coat_line_shadow="#1c2028",
    coat_crease="#151920",
    coat_lapel_l="#2e333b",
    coat_lapel_r="#242930",
    coat_up_mid="#40454e",
    coat_side_arm="#343840",
    coat_side_light="#4a4f58",
    coat_side_dark="#242930",
    coat_side_back_dark="#1c2028",
    coat_lapel_side_base="#2e333b",
    coat_lapel_side_light="#4a4f58",
    # Belt buckle kept brass (gold watch chain feel)
    belt="#3a3040",
    belt_dark="#2a2232",
    belt_loop="#1e1828",
    # Crimson-black tie – blood red accent
    tie_red="#5c1010",
    tie_highlight="#7a1818",
    # Rougher skin: weathered, olive-tan complexion
    skin_light="#d4a070",
    skin_mid="#be8a58",
    skin_dark="#a87240",
    skin_shadow="#966030",
    skin_neck="#b87840",
    skin_side_base="#b07038",
    skin_side_mid="#cc9460",
    skin_side_light="#d8a870",
    cheek_flush="#c07040",
    cheek_flush_side="#b86838",
    nose_base="#9e6030",
    nose_dark="#7e4820",
    nostril_shadow="#6a3818",
    lip_upper="#8a4030",
    lip_lower="#9e5040",
    lip_side_upper="#7a3828",
    lip_side_lower="#8e4838",
    lip_corner="#6a2e20",
    jaw_line="#a06030",
    # Deep set, cold dark-brown eyes
    iris_mid="#3a2810",
    iris_deep="#201408",
    iris_dark="#100a04",
    iris_side_light="#4a3018",
    iris_side_mid="#281808",
    iris_side_dark="#140c04",
    eye_white="#d8dcd4",
    eye_side_white="#dce0d8",
    eye_pupil="#060402",
    eye_liner="#0e0804",
    eye_shadow="#a06838",
    eye_side_liner="#0a0604",
    # Dark charcoal-black hair
    hair_dark="#0e0a06",
    hair_main="#1a1410",
    hair_highlight="#28201a",
    hair_brow_front="#100c08",
    # Charcoal trousers
    pants_left="#282c34",
    pants_right="#242830",
    pants_side_back="#1c2028",
    pants_side_front="#262a32",
    # Worn brass – tarnished
    brass="#c49030",
    brass_dark="#9a7020",
    brass_gold="#b08028",
    brass_side_gold="#a87820",
    brass_border="#806018",
    # Dark shirt, black tie collar
    shirt_white="#c8cdd4",
    shirt_shadow="#b8bdc4",
    shirt_side_shadow="#a8adb6",
)

# 1 – The Fixer: midnight navy suit, oily slicked hair, thin moustache
FIXER_PALETTE = replace(
    DETECTIVE_PALETTE,
    **_GANGSTER_BASE,
    # Deep navy-blue pinstripe suit
    coat_light="#2a3550",
    coat_mid="#1e2840",
    coat_dark="#162030",
    coat_deep="#101828",
    coat_shadow="#0c1220",
    coat_line_shadow="#0c1220",
    coat_crease="#080e18",
    coat_lapel_l="#162030",
    coat_lapel_r="#101828",
    coat_up_mid="#222e48",
    coat_side_arm="#182438",
    coat_side_light="#2a3550",
    coat_side_dark="#101828",
    coat_side_back_dark="#0c1220",
    coat_lapel_side_base="#162030",
    coat_lapel_side_light="#2a3550",
    # Belt / details
    belt="#1a1430",
    belt_dark="#120e22",
    belt_loop="#0c0a1a",
    # Silvery-white silk tie – flash of class
    tie_red="#b8c0cc",
    tie_highlight="#d0d8e4",
    # Pale, indoor complexion – the backroom schemer
    skin_light="#f0d8c0",
    skin_mid="#dcc0a0",
    skin_dark="#c8a880",
    skin_shadow="#b89060",
    skin_neck="#d0b080",
    skin_side_base="#c8a870",
    skin_side_mid="#dcc0a0",
    skin_side_light="#ecd8b8",
    cheek_flush="#dca888",
    cheek_flush_side="#d4a080",
    nose_base="#c09060",
    nose_dark="#9e7040",
    nostril_shadow="#8a5e30",
    lip_upper="#a05848",
    lip_lower="#b86858",
    lip_side_upper="#905040",
    lip_side_lower="#a86050",
    lip_corner="#784038",
    jaw_line="#b88858",
    # Cold calculating grey-blue eyes
    iris_mid="#4a6080",
    iris_deep="#283848",
    iris_dark="#182030",
    iris_side_light="#586880",
    iris_side_mid="#304050",
    iris_side_dark="#1a2838",
    eye_white="#e8ecf0",
    eye_side_white="#ecf0f4",
    eye_pupil="#0a0e12",
    eye_liner="#1a1008",
    eye_shadow="#c0a878",
    eye_side_liner="#140c06",
    # Jet-black oily slicked hair
    hair_dark="#060604",
    hair_main="#100e0c",
    hair_highlight="#1c1a18",
    hair_brow_front="#0a0806",
    # Navy trousers
    pants_left="#182030",
    pants_right="#141c28",
    pants_side_back="#101820",
    pants_side_front="#161e2a",
    # Polished gold – the Fixer has money
    brass="#e0b840",
    brass_dark="#c09828",
    brass_gold="#d4aa30",
    brass_side_gold="#cca028",
    brass_border="#a88018",
    # Crisp white shirt
    shirt_white="#eef2f6",
    shirt_shadow="#e0e6ec",
    shirt_side_shadow="#d4dce4",
)

# 2 – The Lookout: dark olive-green suit, nervous, wiry, hollow-cheeked
LOOKOUT_PALETTE = replace(
    DETECTIVE_PALETTE,
    **_GANGSTER_BASE,
    # Dark olive-drab suit
    coat_light="#3a4030",
    coat_mid="#2e3428",
    coat_dark="#242920",
    coat_deep="#1c2018",
    coat_shadow="#141810",
    coat_line_shadow="#141810",
    coat_crease="#0e120c",
    coat_lapel_l="#242920",
    coat_lapel_r="#1c2018",
    coat_up_mid="#343a2c",
    coat_side_arm="#282e20",
    coat_side_light="#3a4030",
    coat_side_dark="#1c2018",
    coat_side_back_dark="#141810",
    coat_lapel_side_base="#242920",
    coat_lapel_side_light="#3a4030",
    # Belt
    belt="#28301c",
    belt_dark="#1c2414",
    belt_loop="#14180e",
    # Faded brown-earth tie – cheap, worn
    tie_red="#4a3020",
    tie_highlight="#6a4830",
    # Gaunt, ashy complexion – street-worn
    skin_light="#c8b090",
    skin_mid="#b09878",
    skin_dark="#9c8060",
    skin_shadow="#887050",
    skin_neck="#a88868",
    skin_side_base="#a08060",
    skin_side_mid="#b89880",
    skin_side_light="#c8b090",
    cheek_flush="#b07858",
    cheek_flush_side="#a87050",
    nose_base="#8c6040",
    nose_dark="#724830",
    nostril_shadow="#5e3c28",
    lip_upper="#785040",
    lip_lower="#8a5e4c",
    lip_side_upper="#684838",
    lip_side_lower="#7c5444",
    lip_corner="#583830",
    jaw_line="#8c6848",
    # Darting amber-hazel eyes – always watching
    iris_mid="#6a5020",
    iris_deep="#3c2c10",
    iris_dark="#201808",
    iris_side_light="#7a6028",
    iris_side_mid="#483418",
    iris_side_dark="#281e0c",
    eye_white="#d8d4cc",
    eye_side_white="#dcd8d0",
    eye_pupil="#080604",
    eye_liner="#120e06",
    eye_shadow="#9c7848",
    eye_side_liner="#0e0a04",
    # Unkempt dirty-brown hair
    hair_dark="#180e04",
    hair_main="#281808",
    hair_highlight="#382810",
    hair_brow_front="#1c1008",
    # Olive trousers
    pants_left="#242920",
    pants_right="#1e241c",
    pants_side_back="#181c14",
    pants_side_front="#222818",
    # Dull, cheap brass
    brass="#b08820",
    brass_dark="#887010",
    brass_gold="#9a7c18",
    brass_side_gold="#907618",
    brass_border="#6c5c10",
    # Off-white, worn shirt
    shirt_white="#d8d4c4",
    shirt_shadow="#c8c4b4",
    shirt_side_shadow="#b8b4a4",
)


NPC_PALETTES = (ENFORCER_PALETTE, FIXER_PALETTE, LOOKOUT_PALETTE)

# Human-readable names for UI / debug purposes
NPC_NAMES = ("The Enforcer", "The Fixer", "The Lookout")


# ---------------------------------------------------------------------------
# Face Overlays – gangster-style exposed faces with distinct features
# ---------------------------------------------------------------------------

# Scar geometry: list of (x1,y1,x2,y2) line segments per direction
_ENFORCER_SCAR = {
    "down": [(58, 30, 55, 44)],           # cheek scar, front face
    "left": [(32, 30, 34, 42)],           # mirrored profile scar
    "right": [(32, 30, 30, 42)],
    "up": [],
}

_FIXER_MOUSTACHE = {
    # Two short curved strokes above the mouth area (row ~y=43–46 in sprite)
    "down": [(57, 44, 62, 43), (67, 43, 72, 44)],
    "left": [(32, 44, 37, 43)],
    "right": [(29, 43, 34, 44)],
    "up": [],
}

_LOOKOUT_BAGS = {
    # Under-eye dark marks (tiredness / hollow cheeks)
    "down": [(49, 36, 55, 37), (73, 36, 79, 37)],
    "left": [(33, 36, 38, 37)],
    "right": [(26, 36, 31, 37)],
    "up": [],
}

# Per-palette overlay functions (index matches NPC_PALETTES)
_OVERLAY_DATA = [_ENFORCER_SCAR, _FIXER_MOUSTACHE, _LOOKOUT_BAGS]

# Stubble dot grid offsets relative to lower-face centre (dx, dy)
_STUBBLE_OFFSETS = [
    (-8, 4), (-5, 5), (-2, 6), (1, 6), (4, 5), (7, 4),
    (-7, 7), (-4, 8), (-1, 8), (2, 8), (5, 7),
    (-6, 10), (-3, 10), (0, 11), (3, 10), (6, 10),
]


def _apply_gangster_face(frame: pygame.Surface, direction: str, palette_index: int) -> pygame.Surface:
    """Overlay gangster-specific facial features without hiding the face."""
    result = frame.copy()
    overlay = _OVERLAY_DATA[palette_index]
    lines = overlay.get(direction, [])

    if palette_index == 0:  # Enforcer – scar + heavy stubble
        # Draw scar
        for x1, y1, x2, y2 in lines:
            pygame.draw.line(result, (180, 100, 80), (x1, y1), (x2, y2), 1)
            pygame.draw.line(result, (220, 140, 110), (x1 + 1, y1), (x2 + 1, y2), 1)
        # Draw stubble
        if direction == "down":
            cx, cy = 64, 42
            for dx, dy in _STUBBLE_OFFSETS:
                pygame.draw.circle(result, (50, 35, 25), (cx + dx, cy + dy), 1)
        elif direction in ("left", "right"):
            cx, cy = (38, 42) if direction == "right" else (26, 42)
            for dx, dy in _STUBBLE_OFFSETS[:8]:
                pygame.draw.circle(result, (50, 35, 25), (cx + dx // 2, cy + dy), 1)

    elif palette_index == 1:  # Fixer – thin moustache + cigar
        # Draw moustache strokes
        for x1, y1, x2, y2 in lines:
            pygame.draw.line(result, (20, 14, 8), (x1, y1), (x2, y2), 2)
        # Cigar stub at corner of mouth (front and side only)
        if direction == "down":
            pygame.draw.rect(result, (200, 160, 80), (70, 48, 8, 3), border_radius=1)
            pygame.draw.rect(result, (240, 220, 180), (77, 48, 3, 3), border_radius=1)
            pygame.draw.circle(result, (220, 100, 40), (78, 49), 1)  # lit ember
        elif direction == "right":
            pygame.draw.rect(result, (200, 160, 80), (38, 46, 7, 2), border_radius=1)
            pygame.draw.circle(result, (220, 100, 40), (44, 47), 1)

    elif palette_index == 2:  # Lookout – under-eye bags + nervous squint
        for x1, y1, x2, y2 in lines:
            pygame.draw.line(result, (80, 60, 40), (x1, y1), (x2, y2), 1)
        # Narrow the eyes slightly with a semi-transparent lid line
        if direction == "down":
            pygame.draw.line(result, (40, 28, 18, 120), (48, 33), (60, 33), 1)
            pygame.draw.line(result, (40, 28, 18, 120), (68, 33), (80, 33), 1)

    return result


def _add_pinstripe_suit(frame: pygame.Surface, direction: str, palette_index: int) -> pygame.Surface:
    """Draw subtle pinstripe lines over the torso area for a mob-suit look."""
    result = frame
    # Torso area differs slightly by direction
    if direction == "down":
        x_start, x_end = 38, 90
        y_top, y_bot = 58, 92
    elif direction == "up":
        x_start, x_end = 38, 90
        y_top, y_bot = 58, 92
    elif direction == "right":
        x_start, x_end = 28, 52
        y_top, y_bot = 58, 94
    else:  # left
        x_start, x_end = 12, 36
        y_top, y_bot = 58, 94

    # Pinstripe colour: slightly lighter than suit mid-tone
    stripe_colors = [
        (80, 86, 96, 60),   # Enforcer charcoal stripe
        (52, 68, 90, 60),   # Fixer navy stripe
        (66, 74, 56, 60),   # Lookout olive stripe
    ]
    sc = stripe_colors[palette_index % len(stripe_colors)]
    stripe_surf = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
    stripe_color = (sc[0], sc[1], sc[2], sc[3])
    for x in range(x_start + 4, x_end, 6):
        pygame.draw.line(stripe_surf, stripe_color, (x, y_top), (x, y_bot), 1)
    result.blit(stripe_surf, (0, 0))
    return result


def _add_pocket_square(frame: pygame.Surface, direction: str) -> pygame.Surface:
    """Add a white pocket square peeking out of the breast pocket (front view only)."""
    if direction != "down":
        return frame
    result = frame.copy()
    # Breast pocket area: upper-left of torso
    pts = [(48, 63), (53, 61), (55, 66), (50, 67)]
    pygame.draw.polygon(result, (220, 225, 230), pts)
    pygame.draw.polygon(result, (180, 185, 190), pts, 1)
    return result


# ---------------------------------------------------------------------------
# Animation builder
# ---------------------------------------------------------------------------


@lru_cache(maxsize=len(NPC_PALETTES))
def get_npc_animations(palette_index: int = 0):
    """Return cached four-direction idle and walk frames for an NPC gangster colorway."""
    idx = palette_index % len(NPC_PALETTES)
    base = get_character_animations(NPC_PALETTES[idx])
    result = {}
    for direction, states in base.items():
        result[direction] = {}
        for state, frames in states.items():
            processed = []
            for frame in frames:
                f = _add_pinstripe_suit(frame, direction, idx)
                f = _add_pocket_square(f, direction)
                f = _apply_gangster_face(f, direction, idx)
                processed.append(f)
            result[direction][state] = processed
    return result
