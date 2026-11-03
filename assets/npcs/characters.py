"""NPC character designs for Case Unknown.

Two archetypes:
  - MOB GRUNT  (indices 0 & 2): cartoon mob silhouette — huge oval black overcoat,
    full balaclava face mask, stubby legs. Used for street/exterior goons.
  - THE FIXER  (index 1): the sharply-dressed inner-room schemer, same body rig
    as the detective but with a midnight-navy suit, moustache and cigar.
"""

from dataclasses import replace
from functools import lru_cache

import pygame

from assets.characters import DETECTIVE_PALETTE, get_character_animations
from assets.renderer import render_svg

# =============================================================================
# THE FIXER  – palette-only variant of the detective rig (kept from v1)
# =============================================================================

FIXER_PALETTE = replace(
    DETECTIVE_PALETTE,
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
    belt="#1a1430",
    belt_dark="#120e22",
    belt_loop="#0c0a1a",
    # Silvery-white silk tie
    tie_red="#b8c0cc",
    tie_highlight="#d0d8e4",
    # Pale indoor complexion
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
    # Cold grey-blue eyes
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
    # Jet-black oily hair
    hair_dark="#060604",
    hair_main="#100e0c",
    hair_highlight="#1c1a18",
    hair_brow_front="#0a0806",
    brow_front="#100c08",
    brow_side="#0e0b04",
    # Navy trousers
    pants_left="#182030",
    pants_right="#141c28",
    pants_side_back="#101820",
    pants_side_front="#161e2a",
    # Polished gold
    brass="#e0b840",
    brass_dark="#c09828",
    brass_gold="#d4aa30",
    brass_side_gold="#cca028",
    brass_border="#a88018",
    # Crisp white shirt
    shirt_white="#eef2f6",
    shirt_shadow="#e0e6ec",
    shirt_side_shadow="#d4dce4",
    # Worn dark shoes
    shoe_black="#0e1014",
    shoe_leather="#181c22",
    shoe_leather_side="#181c24",
    shoe_darkest="#0a0c10",
    shoe_highlight="#222630",
    shoe_sole="#080a0e",
    shoe_heel_back="#181a1f",
)


def _fixer_face_overlay(frame: pygame.Surface, direction: str) -> pygame.Surface:
    """Add the Fixer's thin moustache and cigar to a rendered detective frame."""
    out = frame.copy()
    if direction == "down":
        # Moustache – two short dark strokes above the lip line
        pygame.draw.line(out, (20, 14, 8), (57, 44), (62, 43), 2)
        pygame.draw.line(out, (20, 14, 8), (67, 43), (72, 44), 2)
        # Cigar at right lip corner
        pygame.draw.rect(out, (200, 160, 80), pygame.Rect(70, 48, 8, 3), border_radius=1)
        pygame.draw.rect(out, (240, 220, 180), pygame.Rect(77, 48, 3, 3), border_radius=1)
        pygame.draw.circle(out, (220, 100, 40), (78, 49), 1)
    elif direction == "right":
        pygame.draw.line(out, (20, 14, 8), (33, 44), (38, 43), 2)
        pygame.draw.rect(out, (200, 160, 80), pygame.Rect(38, 46, 7, 2), border_radius=1)
        pygame.draw.circle(out, (220, 100, 40), (44, 47), 1)
    elif direction == "left":
        pygame.draw.line(out, (20, 14, 8), (26, 43), (31, 44), 2)
        pygame.draw.rect(out, (200, 160, 80), pygame.Rect(17, 46, 7, 2), border_radius=1)
        pygame.draw.circle(out, (220, 100, 40), (17, 47), 1)
    return out


def _get_fixer_animations():
    """Render The Fixer using the detective rig with a navy palette + face overlays."""
    base = get_character_animations(FIXER_PALETTE)
    result = {}
    for direction, states in base.items():
        result[direction] = {}
        for state, frames in states.items():
            result[direction][state] = [
                _fixer_face_overlay(f, direction) for f in frames
            ]
    return result


# =============================================================================
# MOB GRUNT  – fully custom cartoon SVG character
# =============================================================================
# All coordinates are in the 128×160 viewBox; final render is 64×80 px.
#
# Silhouette goals:
#   • Head  – large round oval, pure black balaclava, narrow white-ish eye slits
#   • Body  – huge barrel/oval overcoat, much wider than the detective
#   • Arms  – thick, hanging wide from the body sides
#   • Legs  – short stubs barely peeking under the coat hem
# =============================================================================

# Two subtle coat shade variants so the two grunt types aren't pixel-identical.
_GRUNT_COAT = ["#1c1f28", "#181b22"]   # index 0 = darker, index 1 = slightly blue-black


def _mob_defs_front(coat: str) -> str:
    return f"""  <defs>
    <linearGradient id="coatG" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#0e1016"/>
      <stop offset="35%"  stop-color="{coat}"/>
      <stop offset="65%"  stop-color="{coat}"/>
      <stop offset="100%" stop-color="#0a0c12"/>
    </linearGradient>
    <radialGradient id="headG" cx="45%" cy="38%" r="60%">
      <stop offset="0%"   stop-color="#22252e"/>
      <stop offset="100%" stop-color="#080a0e"/>
    </radialGradient>
    <radialGradient id="armG" cx="30%" cy="30%" r="70%">
      <stop offset="0%"   stop-color="#282c38"/>
      <stop offset="100%" stop-color="#0c0e14"/>
    </radialGradient>
  </defs>"""


def _mob_defs_back(coat: str) -> str:
    return f"""  <defs>
    <linearGradient id="coatG" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#0a0c12"/>
      <stop offset="50%"  stop-color="{coat}"/>
      <stop offset="100%" stop-color="#0a0c12"/>
    </linearGradient>
    <radialGradient id="headG" cx="55%" cy="38%" r="60%">
      <stop offset="0%"   stop-color="#22252e"/>
      <stop offset="100%" stop-color="#080a0e"/>
    </radialGradient>
  </defs>"""


def _mob_defs_side(coat: str) -> str:
    return f"""  <defs>
    <linearGradient id="coatG" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#0c0e14"/>
      <stop offset="40%"  stop-color="{coat}"/>
      <stop offset="100%" stop-color="#0a0c10"/>
    </linearGradient>
    <radialGradient id="headG" cx="60%" cy="38%" r="60%">
      <stop offset="0%"   stop-color="#22252e"/>
      <stop offset="100%" stop-color="#080a0e"/>
    </radialGradient>
  </defs>"""


# ---------------------------------------------------------------------------
# Front (down) view
# ---------------------------------------------------------------------------

def _mob_svg_front(
    bob_y: int = 0,
    l_leg_dx: int = 0, l_leg_dy: int = 0,
    r_leg_dx: int = 0, r_leg_dy: int = 0,
    l_arm_dy: int = 0, r_arm_dy: int = 0,
    coat_flare: int = 0,
    grunt_idx: int = 0,
) -> str:
    coat = _GRUNT_COAT[grunt_idx % len(_GRUNT_COAT)]
    defs = _mob_defs_front(coat)
    flare = abs(coat_flare)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 160" width="128" height="160">
{defs}

  <!-- Ground shadow -->
  <ellipse cx="64" cy="152" rx="{44 + flare}" ry="9" fill="#000000" opacity="0.38"/>

  <!-- Stubby legs -->
  <g transform="translate({l_leg_dx * 2}, {l_leg_dy * 2})">
    <rect x="47" y="114" width="17" height="28" rx="5" fill="#0c0e14"/>
    <path d="M43,136 Q55,131 65,136 L66,145 L42,145 Z" fill="#08090e"/>
    <line x1="43" y1="145" x2="66" y2="145" stroke="#050507" stroke-width="1.5"/>
  </g>
  <g transform="translate({r_leg_dx * 2}, {r_leg_dy * 2})">
    <rect x="68" y="114" width="17" height="28" rx="5" fill="#0c0e14"/>
    <path d="M65,136 Q77,131 87,136 L88,145 L64,145 Z" fill="#08090e"/>
    <line x1="64" y1="145" x2="88" y2="145" stroke="#050507" stroke-width="1.5"/>
  </g>

  <!-- Upper body group bobs with breathing -->
  <g transform="translate(0, {bob_y * 2})">

    <!-- === ARMS (behind body) === -->
    <!-- Left arm -->
    <g transform="translate(0, {l_arm_dy * 2})">
      <path d="M26,68 Q12,84 16,108 Q20,114 30,110 Q24,90 30,72 Z" fill="url(#armG)"/>
      <ellipse cx="22" cy="114" rx="10" ry="7" fill="#14161e"/>
      <!-- Knuckle hint -->
      <path d="M14,112 Q22,109 30,112" stroke="#0a0c12" stroke-width="1" fill="none"/>
    </g>
    <!-- Right arm -->
    <g transform="translate(0, {r_arm_dy * 2})">
      <path d="M102,68 Q116,84 112,108 Q108,114 98,110 Q104,90 98,72 Z" fill="url(#armG)"/>
      <ellipse cx="106" cy="114" rx="10" ry="7" fill="#14161e"/>
      <path d="M98,112 Q106,109 114,112" stroke="#0a0c12" stroke-width="1" fill="none"/>
    </g>

    <!-- === HUGE OVAL BODY / OVERCOAT === -->
    <!-- Drop shadow behind body -->
    <ellipse cx="65" cy="88" rx="{40 + flare}" ry="38" fill="#06080c" opacity="0.7"/>
    <!-- Main coat oval -->
    <ellipse cx="64" cy="86" rx="{38 + flare}" ry="36" fill="url(#coatG)"/>
    <!-- Coat top highlight curve -->
    <path d="M{26 - flare},72 Q64,62 {102 + flare},72"
          stroke="#2e3240" stroke-width="2" fill="none" opacity="0.5"/>

    <!-- Center coat seam -->
    <line x1="64" y1="56" x2="64" y2="114"
          stroke="#0a0c10" stroke-width="2" opacity="0.5"/>

    <!-- Lapels -->
    <polygon points="50,56 64,76 38,76" fill="#0e1016"/>
    <polygon points="78,56 64,76 90,76" fill="#0a0c12"/>
    <!-- Lapel edge lines -->
    <line x1="50" y1="56" x2="64" y2="76" stroke="#22252e" stroke-width="1" opacity="0.7"/>
    <line x1="78" y1="56" x2="64" y2="76" stroke="#1a1d26" stroke-width="1" opacity="0.7"/>

    <!-- White shirt collar triangle peek -->
    <polygon points="57,53 64,65 61,53" fill="#d8dde4"/>
    <polygon points="71,53 64,65 67,53" fill="#c8cdd6"/>

    <!-- Dark tie -->
    <polygon points="62,59 66,59 68,80 64,84 60,80" fill="#100c18"/>
    <line x1="64" y1="61" x2="64" y2="80"
          stroke="#1e1a2a" stroke-width="0.8" opacity="0.6"/>

    <!-- Coat buttons (simple, dark) -->
    <circle cx="64" cy="80" r="3"   fill="#18191e" stroke="#2a2d38" stroke-width="0.8"/>
    <circle cx="64" cy="92" r="3"   fill="#18191e" stroke="#2a2d38" stroke-width="0.8"/>
    <circle cx="64" cy="104" r="3"  fill="#18191e" stroke="#2a2d38" stroke-width="0.8"/>

    <!-- === BALACLAVA HEAD === -->
    <!-- Neck -->
    <rect x="56" y="44" width="16" height="14" rx="4" fill="#10121a"/>

    <!-- Head shadow/depth -->
    <ellipse cx="65" cy="30" rx="25" ry="27" fill="#06080c"/>
    <!-- Main head -->
    <ellipse cx="64" cy="28" rx="24" ry="26" fill="url(#headG)"/>
    <!-- Subtle top highlight -->
    <ellipse cx="60" cy="16" rx="13" ry="8" fill="#2e3240" opacity="0.22"/>

    <!-- Eye band – slightly recessed area across face -->
    <rect x="42" y="23" width="40" height="12" rx="6" fill="#10131c" opacity="0.85"/>

    <!-- Left eye slit -->
    <ellipse cx="53" cy="29" rx="8" ry="2.8" fill="#2a3350"/>
    <ellipse cx="53" cy="29" rx="6" ry="1.8" fill="#354060"/>
    <circle  cx="51" cy="28" r="1.4" fill="#4a5878" opacity="0.9"/>
    <circle  cx="51" cy="27.4" r="0.7" fill="#ffffff" opacity="0.55"/>

    <!-- Right eye slit -->
    <ellipse cx="75" cy="29" rx="8" ry="2.8" fill="#2a3350"/>
    <ellipse cx="75" cy="29" rx="6" ry="1.8" fill="#354060"/>
    <circle  cx="73" cy="28" r="1.4" fill="#4a5878" opacity="0.9"/>
    <circle  cx="73" cy="27.4" r="0.7" fill="#ffffff" opacity="0.55"/>

    <!-- Balaclava mouth stitching -->
    <path d="M50,40 Q64,45 78,40" stroke="#1a1d28" stroke-width="1.5" fill="none" opacity="0.8"/>
    <path d="M52,42 Q64,46 76,42" stroke="#14161e" stroke-width="1"   fill="none" opacity="0.6"/>

    <!-- Hat brim -->
    <ellipse cx="64" cy="6"  rx="36" ry="8"   fill="#0c0e14"/>
    <ellipse cx="64" cy="4"  rx="34" ry="7"   fill="#181b24"/>
    <!-- Hat crown -->
    <path d="M32,4 Q34,-8 64,-8 Q94,-8 96,4 Z" fill="#181b24"/>
    <path d="M38,2 Q64,6 90,2" stroke="#0a0c10" stroke-width="2" fill="none"/>
    <!-- Hat crease -->
    <path d="M46,-6 Q64,-2 82,-6" stroke="#0c0e14" stroke-width="2.5" fill="none"/>
    <!-- Hat band -->
    <path d="M32,4 Q64,8 96,4 L96,1 Q64,5 32,1 Z" fill="#0a0c10"/>

  </g>
</svg>"""


# ---------------------------------------------------------------------------
# Back (up) view
# ---------------------------------------------------------------------------

def _mob_svg_back(
    bob_y: int = 0,
    l_leg_dx: int = 0, l_leg_dy: int = 0,
    r_leg_dx: int = 0, r_leg_dy: int = 0,
    l_arm_dy: int = 0, r_arm_dy: int = 0,
    coat_flare: int = 0,
    grunt_idx: int = 0,
) -> str:
    coat = _GRUNT_COAT[grunt_idx % len(_GRUNT_COAT)]
    defs = _mob_defs_back(coat)
    flare = abs(coat_flare)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 160" width="128" height="160">
{defs}

  <!-- Ground shadow -->
  <ellipse cx="64" cy="152" rx="{44 + flare}" ry="9" fill="#000000" opacity="0.38"/>

  <!-- Stubby legs (back heels) -->
  <g transform="translate({l_leg_dx * 2}, {l_leg_dy * 2})">
    <rect x="47" y="114" width="17" height="28" rx="5" fill="#0c0e14"/>
    <rect x="44" y="136" width="22" height="8"  rx="3" fill="#080a10"/>
    <rect x="46" y="140" width="6"  height="4"  rx="1" fill="#060709"/>
  </g>
  <g transform="translate({r_leg_dx * 2}, {r_leg_dy * 2})">
    <rect x="68" y="114" width="17" height="28" rx="5" fill="#0c0e14"/>
    <rect x="66" y="136" width="22" height="8"  rx="3" fill="#080a10"/>
    <rect x="80" y="140" width="6"  height="4"  rx="1" fill="#060709"/>
  </g>

  <g transform="translate(0, {bob_y * 2})">

    <!-- Left arm (back view) -->
    <g transform="translate(0, {l_arm_dy * 2})">
      <path d="M26,68 Q12,84 16,108 Q20,114 30,110 Q24,90 30,72 Z" fill="#0e1018"/>
      <ellipse cx="22" cy="114" rx="10" ry="7" fill="#10121a"/>
    </g>
    <!-- Right arm (back view) -->
    <g transform="translate(0, {r_arm_dy * 2})">
      <path d="M102,68 Q116,84 112,108 Q108,114 98,110 Q104,90 98,72 Z" fill="#0e1018"/>
      <ellipse cx="106" cy="114" rx="10" ry="7" fill="#10121a"/>
    </g>

    <!-- Huge oval back coat -->
    <ellipse cx="65" cy="88" rx="{40 + flare}" ry="38" fill="#06080c" opacity="0.7"/>
    <ellipse cx="64" cy="86" rx="{38 + flare}" ry="36" fill="url(#coatG)"/>
    <!-- Back vent line -->
    <line x1="64" y1="68" x2="64" y2="116"
          stroke="#0a0c10" stroke-width="2.5" opacity="0.6"/>
    <!-- Coat back crease curves -->
    <path d="M{28 - flare},72 Q64,78 {100 + flare},72"
          stroke="#1a1d26" stroke-width="1.5" fill="none" opacity="0.4"/>
    <path d="M{30 - flare},84 Q64,90 {98 + flare},84"
          stroke="#1a1d26" stroke-width="1"   fill="none" opacity="0.3"/>
    <!-- Back collar -->
    <rect x="54" y="48" width="20" height="10" rx="4" fill="#0e1018"/>

    <!-- Neck (back) -->
    <rect x="56" y="44" width="16" height="12" rx="4" fill="#0e1018"/>

    <!-- Back of balaclava head (just a dark oval, no features) -->
    <ellipse cx="65" cy="30" rx="25" ry="27" fill="#06080c"/>
    <ellipse cx="64" cy="28" rx="24" ry="26" fill="url(#headG)"/>
    <!-- Subtle back-of-head highlight -->
    <ellipse cx="68" cy="16" rx="12" ry="7" fill="#2a2e3a" opacity="0.2"/>
    <!-- Balaclava back neckline stitching -->
    <path d="M46,46 Q64,50 82,46" stroke="#14161e" stroke-width="1.5" fill="none"/>

    <!-- Hat back -->
    <ellipse cx="64" cy="6"  rx="36" ry="8"   fill="#0c0e14"/>
    <ellipse cx="64" cy="4"  rx="34" ry="7"   fill="#181b24"/>
    <path d="M32,4 Q34,-8 64,-8 Q94,-8 96,4 Z" fill="#181b24"/>
    <path d="M46,-6 Q64,-2 82,-6" stroke="#0c0e14" stroke-width="2.5" fill="none"/>
    <path d="M32,4 Q64,8 96,4 L96,1 Q64,5 32,1 Z" fill="#0a0c10"/>

  </g>
</svg>"""


# ---------------------------------------------------------------------------
# Side (right) view
# ---------------------------------------------------------------------------

def _mob_svg_side(
    bob_y: int = 0,
    f_leg_dx: int = 0, f_leg_dy: int = 0,
    b_leg_dx: int = 0, b_leg_dy: int = 0,
    f_arm_rot: int = 0,
    coat_flare: int = 0,
    grunt_idx: int = 0,
) -> str:
    coat = _GRUNT_COAT[grunt_idx % len(_GRUNT_COAT)]
    defs = _mob_defs_side(coat)
    flare = abs(coat_flare)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 160" width="128" height="160">
{defs}

  <!-- Ground shadow -->
  <ellipse cx="62" cy="152" rx="{38 + flare * 2}" ry="8" fill="#000000" opacity="0.36"/>

  <!-- Back leg -->
  <g transform="translate({b_leg_dx * 2}, {b_leg_dy * 2})">
    <rect x="50" y="114" width="16" height="28" rx="5" fill="#0a0c12"/>
    <path d="M47,136 Q57,132 67,136 L68,145 L46,145 Z" fill="#07080d"/>
  </g>

  <!-- Front leg -->
  <g transform="translate({f_leg_dx * 2}, {f_leg_dy * 2})">
    <rect x="60" y="114" width="16" height="28" rx="5" fill="#0c0e16"/>
    <path d="M57,136 Q67,131 80,136 L81,145 L56,145 Z" fill="#09090f"/>
    <line x1="56" y1="145" x2="82" y2="145" stroke="#050507" stroke-width="1.5"/>
  </g>

  <g transform="translate(0, {bob_y * 2})">

    <!-- Back arm (behind body) -->
    <path d="M38,66 Q26,80 28,104 Q32,110 40,108 Q36,88 40,70 Z" fill="#0c0e16"/>
    <ellipse cx="33" cy="110" rx="8" ry="6" fill="#10121a"/>

    <!-- Side oval body – slightly shallower depth from profile -->
    <ellipse cx="64" cy="88" rx="{34 + flare}" ry="38" fill="#06080c" opacity="0.7"/>
    <ellipse cx="63" cy="86" rx="{32 + flare}" ry="36" fill="url(#coatG)"/>
    <!-- Side coat highlight -->
    <path d="M{31 - flare},68 Q63,60 {94 + flare},72"
          stroke="#2a2e3c" stroke-width="1.5" fill="none" opacity="0.4"/>
    <!-- Coat vent back edge -->
    <line x1="{31 - flare}" y1="70" x2="{29 - flare}" y2="116"
          stroke="#0a0c10" stroke-width="1.5" opacity="0.5"/>

    <!-- Front coat edge / lapel -->
    <path d="M84,56 Q90,68 88,88 L88,114 Q86,116 84,114 L82,88 Q80,68 84,56 Z"
          fill="#0e1018"/>
    <!-- Shirt collar side -->
    <polygon points="78,52 86,54 84,62 78,58" fill="#c8cdd6"/>
    <!-- Tie side -->
    <polygon points="80,56 84,57 83,78 80,80 79,62" fill="#100c18"/>

    <!-- Front arm (swinging) -->
    <g transform="rotate({f_arm_rot}, 84, 70)">
      <path d="M80,66 Q90,80 88,104 Q84,112 76,108 Q80,88 76,70 Z" fill="#1a1e2a"/>
      <ellipse cx="83" cy="110" rx="9" ry="7" fill="#14161e"/>
      <path d="M76,108 Q83,105 90,108" stroke="#0a0c12" stroke-width="1" fill="none"/>
    </g>

    <!-- Coat button strip (side, one visible column) -->
    <circle cx="83" cy="78"  r="2.5" fill="#18191e" stroke="#2a2d38" stroke-width="0.8"/>
    <circle cx="84" cy="90"  r="2.5" fill="#18191e" stroke="#2a2d38" stroke-width="0.8"/>
    <circle cx="85" cy="102" r="2.5" fill="#18191e" stroke="#2a2d38" stroke-width="0.8"/>

    <!-- Neck (side) -->
    <path d="M58,44 Q56,50 58,56 L72,56 Q70,50 68,44 Z" fill="#10121a"/>

    <!-- Balaclava head (side) – round with one eye slit -->
    <ellipse cx="65" cy="30" rx="22" ry="25" fill="#06080c"/>
    <ellipse cx="64" cy="28" rx="21" ry="24" fill="url(#headG)"/>
    <!-- Profile forehead / face contour (slight forward jut) -->
    <path d="M72,10 L78,16 Q80,22 76,28 Q80,30 78,36 Q76,40 72,42 Q68,44 62,43 L56,40 Z"
          fill="url(#headG)"/>
    <!-- Eye band -->
    <rect x="68" y="24" width="14" height="10" rx="4" fill="#10131c" opacity="0.85"/>
    <!-- Single eye slit -->
    <ellipse cx="75" cy="29" rx="6" ry="2.4" fill="#2a3350"/>
    <ellipse cx="75" cy="29" rx="4.5" ry="1.6" fill="#354060"/>
    <circle  cx="73" cy="28" r="1.2" fill="#4a5878" opacity="0.9"/>
    <circle  cx="73" cy="27.4" r="0.6" fill="#ffffff" opacity="0.55"/>

    <!-- Balaclava mouth side stitching -->
    <path d="M68,40 Q74,44 78,42" stroke="#1a1d28" stroke-width="1.2" fill="none"/>

    <!-- Hat side profile -->
    <path d="M32,18 Q62,22 88,22 L86,24 Q62,24 32,20 Z" fill="#0c0e14" opacity="0.5"/>
    <ellipse cx="62" cy="16" rx="30" ry="5.5" fill="#0c0e14" transform="rotate(-3 62 16)"/>
    <ellipse cx="62" cy="15" rx="28" ry="4.8" fill="#181b24" transform="rotate(-3 62 15)"/>
    <path d="M38,14 Q44,4 62,3 Q76,4 84,14 Z" fill="#181b24"/>
    <path d="M48,4 Q62,8 76,4" stroke="#0a0c10" stroke-width="2" fill="none"/>
    <path d="M38,14 Q62,17 84,14 L84,12 Q62,15 38,12 Z" fill="#0a0c10"/>

  </g>
</svg>"""


# ---------------------------------------------------------------------------
# Animation builder for mob grunt
# ---------------------------------------------------------------------------

def _get_grunt_animations(grunt_idx: int) -> dict:
    """Render all four-direction idle + walk frames for a cartoon mob grunt."""
    W, H = 64, 80

    def _r(fn, **kw):
        return render_svg(fn(grunt_idx=grunt_idx, **kw), W, H)

    # --- Down ---
    down_idle = [
        _r(_mob_svg_front, bob_y=0),
        _r(_mob_svg_front, bob_y=1),
    ]
    down_walk = [
        _r(_mob_svg_front, bob_y=0, l_leg_dx=-1, l_leg_dy=-3, r_leg_dx=1,  r_leg_dy=2,  l_arm_dy=2,  r_arm_dy=-2, coat_flare=2),
        _r(_mob_svg_front, bob_y=1),
        _r(_mob_svg_front, bob_y=0, l_leg_dx=1,  l_leg_dy=2,  r_leg_dx=-1, r_leg_dy=-3, l_arm_dy=-2, r_arm_dy=2,  coat_flare=-2),
        _r(_mob_svg_front, bob_y=1),
    ]

    # --- Up ---
    up_idle = [
        _r(_mob_svg_back, bob_y=0),
        _r(_mob_svg_back, bob_y=1),
    ]
    up_walk = [
        _r(_mob_svg_back, bob_y=0, l_leg_dx=-1, l_leg_dy=-3, r_leg_dx=1,  r_leg_dy=2,  l_arm_dy=2,  r_arm_dy=-2, coat_flare=2),
        _r(_mob_svg_back, bob_y=1),
        _r(_mob_svg_back, bob_y=0, l_leg_dx=1,  l_leg_dy=2,  r_leg_dx=-1, r_leg_dy=-3, l_arm_dy=-2, r_arm_dy=2,  coat_flare=-2),
        _r(_mob_svg_back, bob_y=1),
    ]

    # --- Right ---
    right_idle = [
        _r(_mob_svg_side, bob_y=0),
        _r(_mob_svg_side, bob_y=1),
    ]
    right_walk = [
        _r(_mob_svg_side, bob_y=0, f_leg_dx=4,  f_leg_dy=-2, b_leg_dx=-4, b_leg_dy=2,  f_arm_rot=-14, coat_flare=3),
        _r(_mob_svg_side, bob_y=1, f_leg_dx=1,  f_leg_dy=0,  b_leg_dx=-1, b_leg_dy=0,  f_arm_rot=-4,  coat_flare=1),
        _r(_mob_svg_side, bob_y=0, f_leg_dx=-4, f_leg_dy=2,  b_leg_dx=4,  b_leg_dy=-2, f_arm_rot=14,  coat_flare=2),
        _r(_mob_svg_side, bob_y=1, f_leg_dx=-1, f_leg_dy=0,  b_leg_dx=1,  b_leg_dy=0,  f_arm_rot=4,   coat_flare=1),
    ]

    # Left is a horizontal flip of right
    left_idle = [pygame.transform.flip(s, True, False) for s in right_idle]
    left_walk  = [pygame.transform.flip(s, True, False) for s in right_walk]

    return {
        "down":  {"idle": down_idle,  "walk": down_walk},
        "up":    {"idle": up_idle,    "walk": up_walk},
        "right": {"idle": right_idle, "walk": right_walk},
        "left":  {"idle": left_idle,  "walk": left_walk},
    }


# =============================================================================
# Public API
# =============================================================================

# Exposed palette objects (for any code that reads palette colours directly)
NPC_PALETTES = (None, FIXER_PALETTE, None)   # indices 0 & 2 use custom SVG; no palette needed

NPC_NAMES = ("The Mob Grunt", "The Fixer", "The Mob Grunt (Alt)")

# Map each palette index to which renderer to use
_GRUNT_INDICES = {0: 0, 2: 1}   # palette_index → grunt_idx for _GRUNT_COAT


@lru_cache(maxsize=3)
def get_npc_animations(palette_index: int = 0):
    """Return cached four-direction idle+walk frames for the given NPC archetype.

    palette_index:
      0 – Mob Grunt (darker charcoal coat)
      1 – The Fixer (inner-room schemer, detective rig with navy suit)
      2 – Mob Grunt Alt (slightly blue-black coat)
    """
    if palette_index == 1:
        return _get_fixer_animations()
    grunt_idx = _GRUNT_INDICES.get(palette_index, 0)
    return _get_grunt_animations(grunt_idx)
