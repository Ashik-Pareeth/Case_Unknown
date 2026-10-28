"""
Character Vector Graphics & Animation Engine for Case Unknown.

This module provides modular, parameterized SVG generation for the Trainee Detective
and future NPCs, along with 4-directional idle and walk animation frame generators.
"""

from dataclasses import dataclass
from pathlib import Path
import pygame
from assets.renderer import render_svg

# ---------------------------------------------------------------------------
# Character Color Palette
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CharacterPalette:
    """Color palette definition for characters (Trainee Detective and future NPCs)."""

    # Trench Coat & Lapels (Front & Back)
    coat_light: str = "#c9a470"
    coat_mid: str = "#b08b58"
    coat_dark: str = "#9e7b48"
    coat_deep: str = "#8c6a3b"
    coat_shadow: str = "#7a5c32"
    coat_line_shadow: str = "#7a5e32"
    coat_crease: str = "#684e27"
    coat_lapel_l: str = "#88683a"
    coat_lapel_r: str = "#7a5d34"
    coat_up_mid: str = "#b8935e"
    belt: str = "#6d532a"
    belt_dark: str = "#5c4422"
    belt_loop: str = "#4a361a"

    # Profile Coat
    coat_side_arm: str = "#967342"
    coat_side_light: str = "#caa470"
    coat_side_dark: str = "#8a6736"
    coat_side_back_dark: str = "#73552d"
    coat_lapel_side_base: str = "#a6814c"
    coat_lapel_side_light: str = "#bfa068"

    # Fedora Hat
    hat_crown_top: str = "#4a3e35"
    hat_crown_mid: str = "#382e25"
    hat_crown_dark: str = "#2d241d"
    hat_crown_base: str = "#221b15"
    hat_brim_base: str = "#2a221b"
    hat_band: str = "#15171a"
    hat_band_side: str = "#181a1d"
    hat_crease: str = "#1d1611"

    # Skin, Face & Features
    skin_light: str = "#f5d5a8"
    skin_mid: str = "#e8c08a"
    skin_dark: str = "#d4a872"
    skin_shadow: str = "#c99a62"
    skin_neck: str = "#e0b87e"
    skin_side_base: str = "#dcad78"
    skin_side_mid: str = "#ebd1a4"
    skin_side_light: str = "#f5dcba"
    cheek_flush: str = "#f5c090"
    cheek_flush_side: str = "#f0be92"
    nose_base: str = "#d4a060"
    nose_dark: str = "#b87840"
    nostril_shadow: str = "#9e6838"
    lip_upper: str = "#c07858"
    lip_lower: str = "#d4896a"
    lip_side_upper: str = "#b86b52"
    lip_side_lower: str = "#cb7e66"
    lip_corner: str = "#a0604a"
    jaw_line: str = "#be8a56"

    # Eyes & Iris (Front & Profile)
    iris_mid: str = "#5a7a3a"
    iris_deep: str = "#2e4a1c"
    iris_dark: str = "#1a2e10"
    iris_side_light: str = "#6b8f45"
    iris_side_mid: str = "#345420"
    iris_side_dark: str = "#1b2e11"
    eye_white: str = "#f0f4f0"
    eye_side_white: str = "#f4f6f4"
    eye_pupil: str = "#0e1a0a"
    eye_liner: str = "#3a2a10"
    eye_shadow: str = "#c4956a"
    eye_side_liner: str = "#221406"

    # Hair & Brows
    hair_dark: str = "#2a1a08"
    hair_main: str = "#3d2810"
    hair_highlight: str = "#5a3e22"
    hair_brow_front: str = "#3d2a10"
    brow_front: str = "#5c3d1a"
    brow_side: str = "#221406"

    # Shirt & Tie
    shirt_white: str = "#e8edf2"
    shirt_shadow: str = "#dde3e9"
    shirt_side_shadow: str = "#d0d8e0"
    tie_red: str = "#a82323"
    tie_highlight: str = "#c43030"

    # Brass Accents
    brass: str = "#dfb15b"
    brass_dark: str = "#b88c38"
    brass_gold: str = "#c99e3a"
    brass_side_gold: str = "#c49b32"
    brass_border: str = "#9e7b28"

    # Pants & Shoes
    pants_left: str = "#2a2e36"
    pants_right: str = "#262930"
    pants_side_back: str = "#20232a"
    pants_side_front: str = "#282c35"
    shoe_black: str = "#1a1c22"
    shoe_leather: str = "#242830"
    shoe_leather_side: str = "#242832"
    shoe_darkest: str = "#14161a"
    shoe_heel_back: str = "#181a1f"
    shoe_highlight: str = "#2e3340"
    shoe_sole: str = "#101216"


DETECTIVE_PALETTE = CharacterPalette()


# ---------------------------------------------------------------------------
# Shared SVG Defs Builders
# ---------------------------------------------------------------------------


def _svg_character_defs(p: CharacterPalette, view: str = "front") -> str:
    """Shared gradient and filter definitions for character views ('front', 'back', 'side')."""
    if view == "back":
        return f"""  <defs>
    <linearGradient id="coatGradUp" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p.coat_dark}"/>
      <stop offset="50%" stop-color="{p.coat_up_mid}"/>
      <stop offset="100%" stop-color="{p.coat_deep}"/>
    </linearGradient>
    <linearGradient id="hatGradUp" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{p.hat_crown_top}"/>
      <stop offset="100%" stop-color="{p.hat_crown_dark}"/>
    </linearGradient>
  </defs>"""
    elif view == "side":
        return f"""  <defs>
    <linearGradient id="coatGradSide" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p.coat_side_arm}"/>
      <stop offset="35%" stop-color="{p.coat_side_light}"/>
      <stop offset="80%" stop-color="{p.coat_mid}"/>
      <stop offset="100%" stop-color="{p.coat_side_dark}"/>
    </linearGradient>
    <linearGradient id="coatBackGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p.coat_side_back_dark}"/>
      <stop offset="100%" stop-color="{p.coat_deep}"/>
    </linearGradient>
    <linearGradient id="hatGradSide" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{p.hat_crown_top}"/>
      <stop offset="50%" stop-color="{p.hat_crown_mid}"/>
      <stop offset="100%" stop-color="{p.hat_crown_base}"/>
    </linearGradient>
    <linearGradient id="skinSide" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p.skin_side_base}"/>
      <stop offset="55%" stop-color="{p.skin_side_mid}"/>
      <stop offset="100%" stop-color="{p.skin_side_light}"/>
    </linearGradient>
    <radialGradient id="irisGradSide" cx="45%" cy="40%" r="55%">
      <stop offset="0%" stop-color="{p.iris_side_light}"/>
      <stop offset="60%" stop-color="{p.iris_side_mid}"/>
      <stop offset="100%" stop-color="{p.iris_side_dark}"/>
    </radialGradient>
  </defs>"""
    else:  # front / default
        return f"""  <defs>
    <linearGradient id="coatGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p.coat_mid}"/>
      <stop offset="50%" stop-color="{p.coat_light}"/>
      <stop offset="100%" stop-color="{p.coat_dark}"/>
    </linearGradient>
    <linearGradient id="hatGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{p.hat_crown_top}"/>
      <stop offset="100%" stop-color="{p.hat_crown_dark}"/>
    </linearGradient>
    <radialGradient id="skinGrad" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="{p.skin_light}"/>
      <stop offset="70%" stop-color="{p.skin_mid}"/>
      <stop offset="100%" stop-color="{p.skin_dark}"/>
    </radialGradient>
    <radialGradient id="irisGrad" cx="40%" cy="35%" r="60%">
      <stop offset="0%" stop-color="{p.iris_mid}"/>
      <stop offset="60%" stop-color="{p.iris_deep}"/>
      <stop offset="100%" stop-color="{p.iris_dark}"/>
    </radialGradient>
  </defs>"""


# ---------------------------------------------------------------------------
# Character Sub-Components: Front View (Facing Player)
# ---------------------------------------------------------------------------


def _svg_ground_shadow(cx: int, cy: int, rx: int, ry: int, opacity: float = 0.3) -> str:
    """Ground contact shadow ellipse."""
    return f"""  <!-- Ground contact shadow -->
  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000000" opacity="{opacity}"/>"""


def _svg_legs_front(
    l_dx: int, l_dy: int, r_dx: int, r_dy: int, p: CharacterPalette
) -> str:
    """Left and right legs with trousers and dress shoes (front view)."""
    return f"""  <!-- Left Leg and Shoe -->
  <g transform="translate({l_dx*2}, {l_dy*2})">
    <rect x="44" y="104" width="16" height="36" rx="4" fill="{p.pants_left}"/>
    <rect x="43" y="135" width="18" height="8" rx="3" fill="{p.shoe_black}"/>
    <path d="M41,138 Q50,135 59,138 L60,146 L40,146 Z" fill="{p.shoe_leather}"/>
  </g>

  <!-- Right Leg and Shoe -->
  <g transform="translate({r_dx*2}, {r_dy*2})">
    <rect x="68" y="104" width="16" height="36" rx="4" fill="{p.pants_right}"/>
    <rect x="67" y="135" width="18" height="8" rx="3" fill="{p.shoe_black}"/>
    <path d="M67,138 Q76,135 85,138 L86,146 L66,146 Z" fill="{p.shoe_leather}"/>
  </g>"""


def _svg_eye_front(cx: int, cy: int, p: CharacterPalette) -> str:
    """Reusable front-facing almond eye with gradient iris, specular highlights, and lashes."""
    return f"""    <ellipse cx="{cx}" cy="{cy}" rx="9" ry="6" fill="{p.eye_shadow}" opacity="0.25"/>
    <ellipse cx="{cx}" cy="{cy}" rx="7" ry="5" fill="{p.eye_white}"/>
    <ellipse cx="{cx}" cy="{cy}" rx="4.5" ry="4.5" fill="url(#irisGrad)"/>
    <circle cx="{cx}" cy="{cy}" r="2.5" fill="{p.eye_pupil}"/>
    <circle cx="{cx + 1.5}" cy="{cy - 1.5}" r="1.4" fill="#ffffff" opacity="0.9"/>
    <circle cx="{cx - 1.5}" cy="{cy + 1.5}" r="0.7" fill="#ffffff" opacity="0.4"/>
    <path d="M{cx - 7},{cy - 3} Q{cx},{cy - 6} {cx + 7},{cy - 3}" stroke="{p.eye_liner}" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <path d="M{cx - 7},{cy + 2} Q{cx},{cy + 5} {cx + 7},{cy + 2}" stroke="#9c7040" stroke-width="0.8" fill="none" opacity="0.5"/>
    <line x1="{cx - 6}" y1="{cy - 3}" x2="{cx - 7}" y2="{cy - 5}" stroke="{p.hair_dark}" stroke-width="1" stroke-linecap="round"/>
    <line x1="{cx - 2}" y1="{cy - 5}" x2="{cx - 2}" y2="{cy - 7}" stroke="{p.hair_dark}" stroke-width="1" stroke-linecap="round"/>
    <line x1="{cx + 2}" y1="{cy - 5}" x2="{cx + 3}" y2="{cy - 7}" stroke="{p.hair_dark}" stroke-width="1" stroke-linecap="round"/>
    <line x1="{cx + 6}" y1="{cy - 3}" x2="{cx + 7}" y2="{cy - 5}" stroke="{p.hair_dark}" stroke-width="1" stroke-linecap="round"/>"""


def _svg_ear_front(cx: int, cy: int, is_left: bool, p: CharacterPalette) -> str:
    """Left or right ear with inner lobe shading."""
    curve_offset = -3 if is_left else 3
    stroke_offset = -1 if is_left else 1
    return f"""    <ellipse cx="{cx}" cy="{cy}" rx="5" ry="8" fill="{p.skin_neck}"/>
    <ellipse cx="{cx}" cy="{cy}" rx="3" ry="5.5" fill="{p.skin_shadow}"/>
    <path d="M{cx + stroke_offset},30 Q{cx + curve_offset},34 {cx + stroke_offset},38" stroke="#b8864e" stroke-width="1" fill="none"/>"""


def _svg_torso_front(
    coat_flare: int, l_arm_dy: int, r_arm_dy: int, p: CharacterPalette
) -> str:
    """Upper body torso, coat, collar, crimson tie, brass buttons, and swinging arms (front view)."""
    return f"""    <!-- Trench Coat Tail and Flare -->
    <path d="M38,84 L{34 - coat_flare*2},116 L{94 + coat_flare*2},116 L90,84 Z" fill="{p.coat_dark}"/>
    <path d="M41,84 L{37 - coat_flare*2},112 L{91 + coat_flare*2},112 L87,84 Z" fill="url(#coatGrad)"/>
    <line x1="64" y1="86" x2="64" y2="112" stroke="{p.coat_line_shadow}" stroke-width="1.5" opacity="0.5"/>

    <!-- Left Arm -->
    <g transform="translate(0, {l_arm_dy*2})">
      <path d="M36,58 Q26,74 30,96 Q34,100 40,96 Q36,78 42,62 Z" fill="#967544"/>
      <rect x="28" y="90" width="14" height="6" rx="2" fill="{p.coat_shadow}"/>
      <ellipse cx="35" cy="99" rx="7" ry="5" fill="{p.skin_mid}"/>
      <path d="M30,97 Q35,94 40,97 L40,102 Q35,105 30,102 Z" fill="#dbb07a"/>
    </g>

    <!-- Right Arm -->
    <g transform="translate(0, {r_arm_dy*2})">
      <path d="M92,58 Q102,74 98,96 Q94,100 88,96 Q92,78 86,62 Z" fill="#967544"/>
      <rect x="86" y="90" width="14" height="6" rx="2" fill="{p.coat_shadow}"/>
      <ellipse cx="93" cy="99" rx="7" ry="5" fill="{p.skin_mid}"/>
      <path d="M88,97 Q93,94 98,97 L98,102 Q93,105 88,102 Z" fill="#dbb07a"/>
    </g>

    <!-- Main Coat Torso -->
    <path d="M40,56 L88,56 L90,92 L38,92 Z" fill="url(#coatGrad)"/>
    <path d="M40,60 Q64,56 88,60" stroke="{p.coat_shadow}" stroke-width="1.5" fill="none" opacity="0.7"/>

    <!-- Coat Lapels -->
    <polygon points="50,56 64,76 44,76" fill="{p.coat_lapel_l}"/>
    <polygon points="78,56 64,76 84,76" fill="{p.coat_lapel_r}"/>
    <line x1="50" y1="56" x2="64" y2="76" stroke="#5e4520" stroke-width="1" opacity="0.6"/>
    <line x1="78" y1="56" x2="64" y2="76" stroke="#5e4520" stroke-width="1" opacity="0.6"/>

    <!-- Shirt Collar -->
    <polygon points="56,54 64,66 60,54" fill="{p.shirt_white}"/>
    <polygon points="72,54 64,66 68,54" fill="{p.shirt_shadow}"/>
    <!-- Crimson Tie -->
    <polygon points="62,60 66,60 68,82 64,86 60,82" fill="{p.tie_red}"/>
    <line x1="64" y1="62" x2="64" y2="82" stroke="{p.tie_highlight}" stroke-width="0.8" opacity="0.6"/>

    <!-- Brass Buttons -->
    <circle cx="56" cy="80" r="3" fill="{p.brass}" stroke="{p.brass_dark}" stroke-width="0.5"/>
    <circle cx="72" cy="80" r="3" fill="{p.brass}" stroke="{p.brass_dark}" stroke-width="0.5"/>
    <circle cx="56" cy="90" r="3" fill="{p.brass}" stroke="{p.brass_dark}" stroke-width="0.5"/>
    <circle cx="72" cy="90" r="3" fill="{p.brass}" stroke="{p.brass_dark}" stroke-width="0.5"/>
    <circle cx="56" cy="80" r="1" fill="{p.brass_dark}"/>
    <circle cx="72" cy="80" r="1" fill="{p.brass_dark}"/>

    <!-- Coat Belt and Buckle -->
    <rect x="38" y="86" width="52" height="7" rx="2" fill="{p.belt}"/>
    <rect x="58" y="84" width="12" height="10" rx="2" fill="{p.brass}" stroke="{p.brass_dark}" stroke-width="1"/>
    <rect x="60" y="86" width="8" height="6" rx="1" fill="{p.brass_gold}"/>"""


def _svg_head_front(p: CharacterPalette) -> str:
    """Detective facial features, jaw, eyes, brows, nose, mouth, ears, and hair (front view)."""
    left_ear = _svg_ear_front(38, 34, True, p)
    right_ear = _svg_ear_front(90, 34, False, p)
    left_eye = _svg_eye_front(54, 32, p)
    right_eye = _svg_eye_front(74, 32, p)

    return f"""    <!-- Neck -->
    <rect x="56" y="38" width="16" height="14" rx="4" fill="{p.skin_neck}"/>
    <rect x="56" y="38" width="4" height="14" rx="2" fill="{p.skin_shadow}" opacity="0.5"/>
    <rect x="68" y="38" width="4" height="14" rx="2" fill="{p.skin_shadow}" opacity="0.5"/>

    <!-- Head Shape: angular young detective jaw -->
    <path d="M38,26 Q36,40 42,50 Q52,58 64,59 Q76,58 86,50 Q92,40 90,26 Z" fill="url(#skinGrad)"/>
    <ellipse cx="64" cy="26" rx="26" ry="22" fill="url(#skinGrad)"/>

    <!-- Left Ear -->
{left_ear}

    <!-- Right Ear -->
{right_ear}

    <!-- Cheekbones -->
    <ellipse cx="46" cy="40" rx="6" ry="4" fill="{p.cheek_flush}" opacity="0.4"/>
    <ellipse cx="82" cy="40" rx="6" ry="4" fill="{p.cheek_flush}" opacity="0.4"/>

    <!-- Eyebrows: angled detective look -->
    <path d="M46,24 Q56,20 62,22" stroke="{p.brow_front}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M66,22 Q72,20 82,24" stroke="{p.brow_front}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M46,25 Q56,21 62,23" stroke="{p.hair_brow_front}" stroke-width="1" fill="none" opacity="0.4"/>
    <path d="M66,23 Q72,21 82,25" stroke="{p.hair_brow_front}" stroke-width="1" fill="none" opacity="0.4"/>

    <!-- Left Eye -->
{left_eye}

    <!-- Right Eye -->
{right_eye}

    <!-- Nose -->
    <path d="M62,26 L60,38 Q64,42 68,38 L66,26" fill="{p.nose_base}" opacity="0.5"/>
    <ellipse cx="64" cy="40" rx="5" ry="3.5" fill="{p.nose_base}"/>
    <ellipse cx="60" cy="41" rx="2.5" ry="1.8" fill="{p.nose_dark}" opacity="0.7"/>
    <ellipse cx="68" cy="41" rx="2.5" ry="1.8" fill="{p.nose_dark}" opacity="0.7"/>
    <ellipse cx="64" cy="39" rx="2" ry="1.5" fill="#f5c880" opacity="0.5"/>

    <!-- Philtrum -->
    <path d="M61,43 Q64,45 67,43" stroke="#c09060" stroke-width="0.8" fill="none" opacity="0.6"/>

    <!-- Mouth and Lips: determined expression -->
    <path d="M54,47 Q58,44 64,46 Q70,44 74,47 L72,49 Q68,46 64,48 Q60,46 56,49 Z" fill="{p.lip_upper}"/>
    <path d="M56,49 Q60,53 64,54 Q68,53 72,49 Q68,52 64,53 Q60,52 56,49 Z" fill="{p.lip_lower}"/>
    <path d="M61,47 Q64,46 67,47" stroke="#e0a080" stroke-width="0.8" fill="none" opacity="0.6"/>
    <path d="M54,47 Q52,48 53,50" stroke="{p.lip_corner}" stroke-width="1" fill="none" opacity="0.6"/>
    <path d="M74,47 Q76,48 75,50" stroke="{p.lip_corner}" stroke-width="1" fill="none" opacity="0.6"/>

    <!-- Chin -->
    <path d="M58,54 Q64,60 70,54" stroke="#c09060" stroke-width="1" fill="none" opacity="0.4"/>

    <!-- Hair peeking under hat -->
    <path d="M40,22 Q42,16 50,14 Q56,12 64,12 Q72,12 78,14 Q86,16 88,22" fill="{p.hair_main}" opacity="0.9"/>
    <rect x="38" y="22" width="6" height="14" rx="2" fill="{p.hair_main}" opacity="0.85"/>
    <rect x="84" y="22" width="6" height="14" rx="2" fill="{p.hair_main}" opacity="0.85"/>"""


def _svg_hat_front(p: CharacterPalette) -> str:
    """Fedora brim, creased crown, ribbon band, and gold badge (front view)."""
    return f"""    <!-- Fedora Brim Shadow on Face -->
    <path d="M44,20 Q64,28 84,20 L84,17 Q64,24 44,17 Z" fill="#000000" opacity="0.25"/>

    <!-- Fedora Hat Brim -->
    <ellipse cx="64" cy="18" rx="38" ry="10" fill="{p.hat_brim_base}"/>
    <ellipse cx="64" cy="16" rx="36" ry="8.5" fill="url(#hatGrad)"/>
    <path d="M28,16 Q64,20 100,16" stroke="#5c4a3c" stroke-width="1" fill="none" opacity="0.5"/>

    <!-- Hat Crown -->
    <path d="M44,14 Q46,2 64,2 Q82,2 84,14 Z" fill="url(#hatGrad)"/>
    <path d="M44,14 Q64,10 84,14" stroke="#3d2e24" stroke-width="1.5" fill="none"/>
    <path d="M52,4 Q64,10 76,4" stroke="{p.hat_crease}" stroke-width="2.5" fill="none"/>
    <path d="M44,13 Q64,16 84,13 L84,10 Q64,13 44,10 Z" fill="{p.hat_band}"/>
    <rect x="60" y="9" width="8" height="5" rx="1" fill="{p.brass}" stroke="{p.brass_dark}" stroke-width="0.5"/>
    <circle cx="64" cy="11.5" r="1.5" fill="{p.brass_dark}"/>"""


def _generate_detective_down_svg(
    bob_y: int = 0,
    l_leg_dx: int = 0,
    l_leg_dy: int = 0,
    r_leg_dx: int = 0,
    r_leg_dy: int = 0,
    l_arm_dy: int = 0,
    r_arm_dy: int = 0,
    coat_flare: int = 0,
    palette: CharacterPalette = DETECTIVE_PALETTE,
) -> str:
    """Generates an SVG for the Detective facing Down (towards the camera)."""
    defs = _svg_character_defs(palette, view="front")
    shadow = _svg_ground_shadow(64, 152, 38, 8)
    legs = _svg_legs_front(l_leg_dx, l_leg_dy, r_leg_dx, r_leg_dy, palette)
    torso = _svg_torso_front(coat_flare, l_arm_dy, r_arm_dy, palette)
    head = _svg_head_front(palette)
    hat = _svg_hat_front(palette)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 160" width="128" height="160">
{defs}

{shadow}

{legs}

  <!-- Upper Body and Head with breathing and step bob -->
  <g transform="translate(0, {bob_y*2})">
{torso}

{head}

{hat}
  </g>
</svg>"""


# ---------------------------------------------------------------------------
# Character Sub-Components: Back View (Facing Up / Walking Away)
# ---------------------------------------------------------------------------


def _svg_legs_back(
    l_dx: int, l_dy: int, r_dx: int, r_dy: int, p: CharacterPalette
) -> str:
    """Back of trousers and shoes with heel notches (back view)."""
    return f"""  <!-- Left Leg and Shoe Heel -->
  <g transform="translate({l_dx*2}, {l_dy*2})">
    <rect x="44" y="104" width="16" height="36" rx="4" fill="{p.pants_right}"/>
    <rect x="42" y="134" width="20" height="8" rx="3" fill="{p.shoe_heel_back}"/>
    <rect x="44" y="138" width="6" height="4" rx="1" fill="#222428"/>
  </g>

  <!-- Right Leg and Shoe Heel -->
  <g transform="translate({r_dx*2}, {r_dy*2})">
    <rect x="68" y="104" width="16" height="36" rx="4" fill="{p.pants_left}"/>
    <rect x="66" y="134" width="20" height="8" rx="3" fill="{p.shoe_heel_back}"/>
    <rect x="78" y="138" width="6" height="4" rx="1" fill="#222428"/>
  </g>"""


def _svg_torso_back(
    coat_flare: int, l_arm_dy: int, r_arm_dy: int, p: CharacterPalette
) -> str:
    """Back coat flaps, vent split, back belt loops, and swinging arms (back view)."""
    return f"""    <!-- Back Coat Flap and Vent Split -->
    <path d="M38,84 L{34 - coat_flare*2},116 L{94 + coat_flare*2},116 L90,84 Z" fill="{p.coat_deep}"/>
    <path d="M41,84 L{37 - coat_flare*2},112 L{91 + coat_flare*2},112 L87,84 Z" fill="url(#coatGradUp)"/>
    <line x1="64" y1="86" x2="64" y2="112" stroke="{p.coat_crease}" stroke-width="2.5"/>
    <path d="M41,84 L52,112" stroke="{p.coat_line_shadow}" stroke-width="1" opacity="0.4"/>
    <path d="M87,84 L76,112" stroke="{p.coat_line_shadow}" stroke-width="1" opacity="0.4"/>

    <!-- Left Arm -->
    <g transform="translate(0, {l_arm_dy*2})">
      <path d="M36,58 Q26,74 30,96 Q34,100 40,96 Q36,78 42,62 Z" fill="{p.coat_deep}"/>
      <rect x="28" y="90" width="14" height="6" rx="2" fill="#6a4e24"/>
      <ellipse cx="34" cy="99" rx="7" ry="5" fill="{p.coat_shadow}"/>
    </g>

    <!-- Right Arm -->
    <g transform="translate(0, {r_arm_dy*2})">
      <path d="M92,58 Q102,74 98,96 Q94,100 88,96 Q92,78 86,62 Z" fill="{p.coat_deep}"/>
      <rect x="86" y="90" width="14" height="6" rx="2" fill="#6a4e24"/>
      <ellipse cx="94" cy="99" rx="7" ry="5" fill="{p.coat_shadow}"/>
    </g>

    <!-- Torso Back -->
    <path d="M40,56 L88,56 L90,92 L38,92 Z" fill="url(#coatGradUp)"/>
    <path d="M42,64 Q64,70 86,64" stroke="{p.coat_crease}" stroke-width="2.5" fill="none"/>
    <path d="M50,68 Q64,72 78,68" stroke="{p.coat_line_shadow}" stroke-width="1" fill="none" opacity="0.5"/>

    <!-- Back Belt -->
    <rect x="38" y="86" width="52" height="7" rx="2" fill="{p.belt}"/>
    <rect x="50" y="84" width="5" height="10" rx="1" fill="#543e1d"/>
    <rect x="73" y="84" width="5" height="10" rx="1" fill="#543e1d"/>"""


def _svg_head_back(p: CharacterPalette) -> str:
    """Back of neck, collar, and head with hair texture (back view)."""
    return f"""    <!-- Back of Neck and Collar -->
    <rect x="54" y="46" width="20" height="12" rx="4" fill="{p.skin_neck}"/>
    <rect x="54" y="46" width="4" height="12" rx="2" fill="#c09060" opacity="0.5"/>
    <rect x="70" y="46" width="4" height="12" rx="2" fill="#c09060" opacity="0.5"/>
    <path d="M50,54 Q64,50 78,54 L78,58 Q64,54 50,58 Z" fill="{p.coat_deep}"/>
    <path d="M54,48 Q64,46 74,48" stroke="#6a4e24" stroke-width="1" fill="none"/>

    <!-- Back of Head with hair visible -->
    <ellipse cx="64" cy="26" rx="26" ry="22" fill="{p.hair_main}"/>
    <ellipse cx="64" cy="22" rx="18" ry="14" fill="#4a3218" opacity="0.7"/>
    <path d="M48,20 Q56,16 64,18" stroke="{p.hair_highlight}" stroke-width="1.5" fill="none" opacity="0.6"/>
    <path d="M80,20 Q72,16 64,18" stroke="{p.hair_highlight}" stroke-width="1.5" fill="none" opacity="0.6"/>"""


def _svg_hat_back(p: CharacterPalette) -> str:
    """Back of fedora brim, crown, crease, and ribbon (back view)."""
    return f"""    <!-- Back of Fedora -->
    <ellipse cx="64" cy="18" rx="38" ry="10" fill="{p.hat_brim_base}"/>
    <ellipse cx="64" cy="16" rx="36" ry="8.5" fill="url(#hatGradUp)"/>
    <path d="M44,14 Q46,2 64,2 Q82,2 84,14 Z" fill="url(#hatGradUp)"/>
    <path d="M52,4 Q64,10 76,4" stroke="{p.hat_crease}" stroke-width="2.5" fill="none"/>
    <path d="M44,13 Q64,16 84,13 L84,10 Q64,13 44,10 Z" fill="{p.hat_band}"/>
    <line x1="62" y1="3" x2="66" y2="3" stroke="#2a1e16" stroke-width="1"/>"""


def _generate_detective_up_svg(
    bob_y: int = 0,
    l_leg_dx: int = 0,
    l_leg_dy: int = 0,
    r_leg_dx: int = 0,
    r_leg_dy: int = 0,
    l_arm_dy: int = 0,
    r_arm_dy: int = 0,
    coat_flare: int = 0,
    palette: CharacterPalette = DETECTIVE_PALETTE,
) -> str:
    """Generates an SVG for the Detective facing Up (walking away / back view)."""
    defs = _svg_character_defs(palette, view="back")
    shadow = _svg_ground_shadow(64, 152, 38, 8)
    legs = _svg_legs_back(l_leg_dx, l_leg_dy, r_leg_dx, r_leg_dy, palette)
    torso = _svg_torso_back(coat_flare, l_arm_dy, r_arm_dy, palette)
    head = _svg_head_back(palette)
    hat = _svg_hat_back(palette)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 160" width="128" height="160">
{defs}

{shadow}

{legs}

  <!-- Upper Body and Back of Head -->
  <g transform="translate(0, {bob_y*2})">
{torso}

{head}

{hat}
  </g>
</svg>"""


# ---------------------------------------------------------------------------
# Character Sub-Components: Profile View (Facing Right)
# ---------------------------------------------------------------------------


def _svg_legs_side(
    f_dx: int, f_dy: int, b_dx: int, b_dy: int, p: CharacterPalette
) -> str:
    """Front and back legs and shoes in profile stride with fuller trouser cuts."""
    return f"""  <!-- Back Leg & Shoe (Swinging / Stepping) -->
  <g transform="translate({b_dx*2}, {b_dy*2})">
    <path d="M44,104 L59,104 L{61 + b_dx},136 L{45 + b_dx},136 Z" fill="{p.pants_side_back}"/>
    <g transform="translate({b_dx}, 0)">
      <rect x="42" y="135" width="22" height="8" rx="3" fill="{p.shoe_darkest}"/>
      <path d="M40,138 Q52,133 64,137 L66,145 L39,145 Z" fill="#1e222a"/>
      <line x1="39" y1="145" x2="66" y2="145" stroke="#0e1014" stroke-width="1.5"/>
    </g>
  </g>

  <!-- Front Leg & Shoe -->
  <g transform="translate({f_dx*2}, {f_dy*2})">
    <path d="M57,104 L75,104 L{77 + f_dx},136 L{58 + f_dx},136 Z" fill="{p.pants_side_front}"/>
    <line x1="{60 + f_dx*0.5}" y1="106" x2="{60 + f_dx}" y2="135" stroke="#1c1f26" stroke-width="1"/>
    <g transform="translate({f_dx}, 0)">
      <rect x="56" y="135" width="25" height="8" rx="3" fill="#181a20"/>
      <path d="M54,138 Q68,133 81,137 L83,145 L53,145 Z" fill="{p.shoe_leather_side}"/>
      <path d="M72,136 Q79,135 82,138 L82,145 L72,145 Z" fill="{p.shoe_highlight}" opacity="0.6"/>
      <line x1="53" y1="145" x2="83" y2="145" stroke="{p.shoe_sole}" stroke-width="1.5"/>
    </g>
  </g>"""


def _svg_torso_side(coat_flare: int, f_arm_rot: int, p: CharacterPalette) -> str:
    """Substantial profile trench coat, broad shoulder, lapel overlap, shirt collar, red tie, and front swinging arm."""
    return f"""    <!-- Trench Coat Tail & Back Flare -->
    <path d="M37,84 L{28 - coat_flare*3.0},114 L76,114 L79,84 Z" fill="{p.coat_lapel_r}"/>
    <path d="M39,84 L{31 - coat_flare*3.0},112 L75,112 L78,84 Z" fill="url(#coatGradSide)"/>
    <line x1="{39 - coat_flare}" y1="92" x2="{34 - coat_flare*2.5}" y2="112" stroke="#684f2c" stroke-width="1.5"/>

    <!-- Torso Silhouette with broad tailored rounded shoulder (depth x=36 to x=79) -->
    <path d="M48,52 
             Q36,54 36,65 
             L37,88 
             L79,88 
             L78,60 
             Q78,54 67,52 
             Z" fill="url(#coatGradSide)"/>
    
    <!-- Coat Lapel Overlap & Double-breasted chest -->
    <path d="M46,54 Q38,56 38,66 L39,86 L77,86 L77,64 Q76,55 66,53 Z" fill="url(#coatGradSide)"/>
    <line x1="68" y1="58" x2="70" y2="84" stroke="#7e6034" stroke-width="1.2" stroke-dasharray="3,2"/>

    <!-- Belt & Brass Buckle -->
    <rect x="36" y="84" width="43" height="6.5" rx="1.5" fill="{p.belt_dark}"/>
    <rect x="46" y="83" width="3" height="8" rx="1" fill="{p.belt_loop}"/>
    <rect x="60" y="83" width="3" height="8" rx="1" fill="{p.belt_loop}"/>
    <!-- Belt Buckle on front hip -->
    <rect x="74" y="82" width="7" height="9" rx="2" fill="{p.brass}" stroke="{p.brass_border}" stroke-width="0.8"/>
    <rect x="75.5" y="83.5" width="4" height="6" rx="1" fill="{p.brass_side_gold}"/>
    <line x1="77.5" y1="82" x2="77.5" y2="91" stroke="#8a681a" stroke-width="1"/>

    <!-- Shirt Collar & Silk Tie (recessed under projecting jaw) -->
    <polygon points="65,50 77,51 78,60 70,56" fill="{p.shirt_white}"/>
    <polygon points="70,50 77,51 74,56" fill="{p.shirt_side_shadow}"/>
    <polygon points="72,54 78,55 77,74 73,77 71,60" fill="{p.tie_red}"/>
    <polygon points="73,55 77,56 76,73 73,75" fill="{p.tie_highlight}"/>

    <!-- Coat Lapels -->
    <polygon points="56,52 76,64 72,75 56,58" fill="{p.coat_lapel_side_base}"/>
    <polygon points="56,52 74,63 71,73 57,58" fill="{p.coat_lapel_side_light}"/>
    <!-- Double-breasted Coat buttons -->
    <circle cx="71" cy="65" r="2.2" fill="{p.brass}" stroke="{p.coat_lapel_r}" stroke-width="0.6"/>
    <circle cx="72" cy="76" r="2.2" fill="{p.brass}" stroke="{p.coat_lapel_r}" stroke-width="0.6"/>
    <circle cx="63" cy="65" r="2.2" fill="{p.brass}" stroke="{p.coat_lapel_r}" stroke-width="0.6"/>
    <circle cx="64" cy="76" r="2.2" fill="{p.brass}" stroke="{p.coat_lapel_r}" stroke-width="0.6"/>

    <!-- Front Arm (Substantial sleeve swinging in front of body) -->
    <g transform="rotate({f_arm_rot}, 58, 60)">
      <ellipse cx="57" cy="58" rx="8.5" ry="6.5" fill="{p.coat_mid}"/>
      <path d="M51,59 L62,76 L60,92 L49,92 L47,76 L49,59 Z" fill="url(#coatGradSide)"/>
      <path d="M47,74 Q54,77 59,74" stroke="{p.coat_lapel_r}" stroke-width="1.2" fill="none"/>
      <rect x="48" y="88" width="13" height="4.5" rx="1.5" fill="#6d512a"/>
      <circle cx="58" cy="90" r="1.3" fill="{p.brass}"/>
      <ellipse cx="55" cy="96" rx="6" ry="4.5" fill="#e2b484"/>
      <path d="M52,95 Q57,98 60,95" stroke="#b07d50" stroke-width="1" fill="none"/>
    </g>"""


def _svg_head_side(p: CharacterPalette) -> str:
    """Full-proportioned detective profile face, projecting jaw/chin, wedge eye, nose, lips, ear, and hair."""
    return f"""    <!-- Neck (broader and seated naturally over shoulders) -->
    <path d="M48,42 Q47,48 49,54 L68,54 Q67,48 66,42 Z" fill="url(#skinSide)"/>
    <path d="M48,42 L66,42 L65,50 L49,48 Z" fill="#b88450" opacity="0.45"/>

    <!-- Cranium / Head Base (fuller skull volume in back) -->
    <path d="M40,22 Q38,32 43,40 Q47,46 58,48 L68,48 Q70,44 70,36 L70,22 Z" fill="url(#skinSide)"/>

    <!-- Hair: Rich dark brown hair covering back of head and under hat -->
    <path d="M39,20 Q37,28 39,36 Q42,42 50,44 Q47,38 46,32 Q45,24 46,20 Z" fill="{p.hair_dark}"/>
    <path d="M41,22 Q39,30 42,38 Q46,42 51,43 L49,34 Q47,26 48,20 Z" fill="{p.hair_main}"/>
    <path d="M41,24 Q39,32 43,38" stroke="{p.hair_highlight}" stroke-width="1" fill="none" opacity="0.7"/>

    <!-- Ear -->
    <ellipse cx="50" cy="33" rx="5" ry="7.5" fill="#e0b280"/>
    <ellipse cx="49.5" cy="33" rx="3.4" ry="5.5" fill="#c69262"/>
    <path d="M48,30 Q46,33 49,36" stroke="{p.nostril_shadow}" stroke-width="1" fill="none"/>
    <ellipse cx="50" cy="37.5" rx="2.3" ry="2.3" fill="#d8a474"/>

    <!-- Natural tapered sideburn in front of ear -->
    <path d="M52,21 L55,29 Q54,31.5 52,31.5 L50.5,28 L51,21 Z" fill="{p.hair_dark}"/>

    <!-- Front Face Profile Contour (Projecting nose at x=85, forward jaw & chin at x=79.5 overhanging neck) -->
    <path d="M67,18 
             L76,22.5 
             Q76.5,24.5 73.5,26.5 
             L85,33.5 
             Q85,35.8 78,36.8 
             L78,38.8 
             L81.5,40.6 
             L77,42.2 
             L80.5,43.8 
             Q76.5,44.8 76.5,46.2 
             Q80.5,47.8 79.5,50.5 
             Q75,52.5 65,49.5 
             L54,45.5 
             Z" fill="url(#skinSide)"/>

    <!-- Under-jaw shadow to separate projecting chin from neck/collar -->
    <path d="M58,48.5 Q72,52.5 78.5,50.5 Q73,53.5 61,51 Z" fill="#a67244" opacity="0.7"/>

    <!-- Facial Contour details (Nose bridge highlight & nostril) -->
    <path d="M74,26.5 L83.8,33.5 L78,35.8" stroke="#fce4c8" stroke-width="0.9" fill="none" opacity="0.75"/>
    <ellipse cx="79.2" cy="35.5" rx="1.6" ry="1" fill="{p.nostril_shadow}" opacity="0.65"/>

    <!-- Profile Lips -->
    <path d="M78,38.8 Q80.8,40 81.5,40.6 L77.2,41.6 Z" fill="{p.lip_side_upper}"/>
    <path d="M77.2,42.2 Q80,42.8 79.8,44 L76.2,43.6 Z" fill="{p.lip_side_lower}"/>
    <path d="M76.5,45 Q78,46 77,47" stroke="#b88450" stroke-width="0.8" fill="none" opacity="0.5"/>

    <!-- Defined Forward Jawline -->
    <path d="M53,39 L62,46 L74,50.5 L79,49.5" stroke="{p.jaw_line}" stroke-width="1.3" fill="none" opacity="0.75"/>
    <ellipse cx="66.5" cy="34.5" rx="4.5" ry="3.2" fill="{p.cheek_flush_side}" opacity="0.3" transform="rotate(-10 66.5 34.5)"/>

    <!-- Profile Eye (Recessed cleanly behind nose bridge) -->
    <path d="M65,26 Q70,24 73,27 Q69,30 65,29 Z" fill="#d9a877" opacity="0.3"/>
    <path d="M67,26 L73,27.5 L68,30 Z" fill="{p.eye_side_white}"/>
    <path d="M69.5,26.8 Q72.8,27.5 72.5,29.2 Q70.5,30 69,29.2 Z" fill="url(#irisGradSide)"/>
    <ellipse cx="71" cy="28.2" rx="1.2" ry="1.6" fill="#0b1408"/>
    <circle cx="71.5" cy="27.4" r="0.7" fill="#ffffff"/>
    <path d="M65,25 Q70,23.5 73.5,26" stroke="{p.eye_side_liner}" stroke-width="1.4" fill="none" stroke-linecap="round"/>
    <path d="M66,23.5 Q70,22.5 73,24.5" stroke="#a06c3a" stroke-width="0.7" fill="none" opacity="0.6"/>
    <line x1="73" y1="26" x2="74.5" y2="25" stroke="{p.eye_side_liner}" stroke-width="1.2" stroke-linecap="round"/>

    <!-- Eyebrow: Sharp, focused detective brow -->
    <path d="M65,21 Q70,18.2 75,21" stroke="{p.brow_side}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M65,21 Q70,18.2 75,21" stroke="{p.hair_main}" stroke-width="1.5" fill="none" stroke-linecap="round"/>

    <!-- Front hair fringe peeking under fedora brim -->
    <path d="M67,18 Q71,19 73,22 Q70,21 68,20 Z" fill="{p.hair_dark}"/>
    <path d="M64,18 Q67,21 69,23 Q66,21 64,19 Z" fill="{p.hair_main}"/>"""



def _svg_hat_side(p: CharacterPalette) -> str:
    """Fedora hat in profile: wide snap brim, creased crown, ribbon band, and gold pin."""
    return f"""    <!-- Classic Noir Fedora (Full Profile View) -->
    <path d="M35,20 Q63,22 89,23 L87,25 Q63,24 35,21 Z" fill="#120e0b" opacity="0.5"/>
    <ellipse cx="63" cy="18" rx="31" ry="5.8" fill="{p.hat_crease}" transform="rotate(-3 63 18)"/>
    <ellipse cx="63" cy="17" rx="30" ry="5.0" fill="url(#hatGradSide)" transform="rotate(-3 63 17)"/>
    <path d="M42,16 
             Q44,6 59,4 
             Q65,6 74,5 
             Q78,8 79,16 
             Z" fill="url(#hatGradSide)"/>
    <path d="M50,6 Q61,9 73,6" stroke="#18120d" stroke-width="2.2" fill="none" stroke-linecap="round"/>
    <path d="M72,8 Q76,11 77,15" stroke="{p.hat_crease}" stroke-width="1.8" fill="none" opacity="0.7"/>

    <!-- Hat Ribbon Band & Badge -->
    <path d="M42,16 Q62,18 79,15.5 L79.3,13 Q62,15 42.3,13.5 Z" fill="{p.hat_band_side}"/>
    <line x1="42.1" y1="16" x2="79" y2="15.5" stroke="#0e1012" stroke-width="0.8"/>
    <circle cx="56" cy="14.5" r="2.2" fill="{p.brass}" stroke="#8a681a" stroke-width="0.6"/>
    <circle cx="56" cy="14.5" r="1.1" fill="{p.brass_dark}"/>"""


def _generate_detective_side_svg(
    bob_y: int = 0,
    f_leg_dx: int = 0,
    f_leg_dy: int = 0,
    b_leg_dx: int = 0,
    b_leg_dy: int = 0,
    f_arm_rot: int = 0,
    b_arm_rot: int = 0,
    coat_flare: int = 0,
    palette: CharacterPalette = DETECTIVE_PALETTE,
) -> str:
    """Generates an SVG for the Detective facing Right (profile view)."""
    defs = _svg_character_defs(palette, view="side")
    shadow = f'  <!-- Ground contact shadow -->\n  <ellipse cx="{62 + f_leg_dx}" cy="152" rx="{40 + abs(f_leg_dx)*2}" ry="8.5" fill="#000000" opacity="0.32"/>'
    legs = _svg_legs_side(f_leg_dx, f_leg_dy, b_dx=b_leg_dx, b_dy=b_leg_dy, p=palette)
    torso = _svg_torso_side(coat_flare, f_arm_rot, palette)
    head = _svg_head_side(palette)
    hat = _svg_hat_side(palette)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 160" width="128" height="160">
{defs}

{shadow}

{legs}

  <!-- Back Arm (Swinging behind body) -->
  <g transform="translate(0, {bob_y*2}) rotate({b_arm_rot}, 52, 62)">
    <path d="M48,58 L38,80 L46,94 L56,92 L53,76 L58,58 Z" fill="url(#coatBackGrad)"/>
    <rect x="42" y="88" width="13" height="4.5" rx="1.5" fill="{palette.belt_dark}"/>
    <circle cx="52" cy="90" r="1.3" fill="{palette.brass}"/>
    <ellipse cx="47" cy="97" rx="6" ry="4.5" fill="#cf9f6e"/>
  </g>

  <!-- Upper Body and Profile Head (bobs together) -->
  <g transform="translate(0, {bob_y*2})">
{torso}

{head}

{hat}
  </g>
</svg>"""


# ---------------------------------------------------------------------------
# Animation Pipeline
# ---------------------------------------------------------------------------


def get_character_animations(palette: CharacterPalette = DETECTIVE_PALETTE) -> dict:
    """
    Renders and returns all directional animations for the Detective:
    'down', 'up', 'right', 'left' containing 'idle' and 'walk' frame lists.
    The SVGs use a 128x160 internal viewBox for detail but are scaled to 64x80.
    """
    W, H = 64, 80  # Final sprite size in pixels

    # Down animations (Facing player)
    down_idle = [
        render_svg(_generate_detective_down_svg(bob_y=0, palette=palette), W, H),
        render_svg(_generate_detective_down_svg(bob_y=1, palette=palette), W, H),
    ]
    down_walk = [
        render_svg(
            _generate_detective_down_svg(
                bob_y=0,
                l_leg_dx=-1,
                l_leg_dy=-4,
                r_leg_dx=1,
                r_leg_dy=3,
                l_arm_dy=2,
                r_arm_dy=-2,
                coat_flare=2,
                palette=palette,
            ),
            W,
            H,
        ),
        render_svg(
            _generate_detective_down_svg(
                bob_y=1,
                l_leg_dx=0,
                l_leg_dy=0,
                r_leg_dx=0,
                r_leg_dy=0,
                l_arm_dy=0,
                r_arm_dy=0,
                coat_flare=0,
                palette=palette,
            ),
            W,
            H,
        ),
        render_svg(
            _generate_detective_down_svg(
                bob_y=0,
                l_leg_dx=1,
                l_leg_dy=3,
                r_leg_dx=-1,
                r_leg_dy=-4,
                l_arm_dy=-2,
                r_arm_dy=2,
                coat_flare=-2,
                palette=palette,
            ),
            W,
            H,
        ),
        render_svg(
            _generate_detective_down_svg(
                bob_y=1,
                l_leg_dx=0,
                l_leg_dy=0,
                r_leg_dx=0,
                r_leg_dy=0,
                l_arm_dy=0,
                r_arm_dy=0,
                coat_flare=0,
                palette=palette,
            ),
            W,
            H,
        ),
    ]

    # Up animations (Facing away)
    up_idle = [
        render_svg(_generate_detective_up_svg(bob_y=0, palette=palette), W, H),
        render_svg(_generate_detective_up_svg(bob_y=1, palette=palette), W, H),
    ]
    up_walk = [
        render_svg(
            _generate_detective_up_svg(
                bob_y=0,
                l_leg_dx=-1,
                l_leg_dy=-4,
                r_leg_dx=1,
                r_leg_dy=3,
                l_arm_dy=2,
                r_arm_dy=-2,
                coat_flare=2,
                palette=palette,
            ),
            W,
            H,
        ),
        render_svg(
            _generate_detective_up_svg(
                bob_y=1,
                l_leg_dx=0,
                l_leg_dy=0,
                r_leg_dx=0,
                r_leg_dy=0,
                l_arm_dy=0,
                r_arm_dy=0,
                coat_flare=0,
                palette=palette,
            ),
            W,
            H,
        ),
        render_svg(
            _generate_detective_up_svg(
                bob_y=0,
                l_leg_dx=1,
                l_leg_dy=3,
                r_leg_dx=-1,
                r_leg_dy=-4,
                l_arm_dy=-2,
                r_arm_dy=2,
                coat_flare=-2,
                palette=palette,
            ),
            W,
            H,
        ),
        render_svg(
            _generate_detective_up_svg(
                bob_y=1,
                l_leg_dx=0,
                l_leg_dy=0,
                r_leg_dx=0,
                r_leg_dy=0,
                l_arm_dy=0,
                r_arm_dy=0,
                coat_flare=0,
                palette=palette,
            ),
            W,
            H,
        ),
    ]

    # Right animations (Profile)
    right_idle = [
        render_svg(_generate_detective_side_svg(bob_y=0, palette=palette), W, H),
        render_svg(_generate_detective_side_svg(bob_y=1, palette=palette), W, H),
    ]
    right_walk = [
        render_svg(
            _generate_detective_side_svg(
                bob_y=0,
                f_leg_dx=4,
                f_leg_dy=-2,
                b_leg_dx=-5,
                b_leg_dy=2,
                f_arm_rot=-16,
                b_arm_rot=16,
                coat_flare=3,
                palette=palette,
            ),
            W,
            H,
        ),
        render_svg(
            _generate_detective_side_svg(
                bob_y=1,
                f_leg_dx=1,
                f_leg_dy=0,
                b_leg_dx=-1,
                b_leg_dy=0,
                f_arm_rot=-4,
                b_arm_rot=4,
                coat_flare=1,
                palette=palette,
            ),
            W,
            H,
        ),
        render_svg(
            _generate_detective_side_svg(
                bob_y=0,
                f_leg_dx=-5,
                f_leg_dy=2,
                b_leg_dx=4,
                b_leg_dy=-2,
                f_arm_rot=16,
                b_arm_rot=-16,
                coat_flare=2,
                palette=palette,
            ),
            W,
            H,
        ),
        render_svg(
            _generate_detective_side_svg(
                bob_y=1,
                f_leg_dx=-1,
                f_leg_dy=0,
                b_leg_dx=1,
                b_leg_dy=0,
                f_arm_rot=4,
                b_arm_rot=-4,
                coat_flare=1,
                palette=palette,
            ),
            W,
            H,
        ),
    ]

    # Left animations (Flipped horizontally from Right for perfect frame symmetry)
    left_idle = [pygame.transform.flip(s, True, False) for s in right_idle]
    left_walk = [pygame.transform.flip(s, True, False) for s in right_walk]

    return {
        "down": {"idle": down_idle, "walk": down_walk},
        "up": {"idle": up_idle, "walk": up_walk},
        "right": {"idle": right_idle, "walk": right_walk},
        "left": {"idle": left_idle, "walk": left_walk},
    }


def _field_detective_svg(direction: str, step: int, bob: int, walking: bool = False) -> str:
    """Draw a readable, animated noir investigator for the small in-world scale."""
    ink, outline, coat, coat_light = "#151a1d", "#20272a", "#53636a", "#839097"
    coat_shadow, scarf, skin, skin_shadow = "#344148", "#8e483b", "#c79870", "#9b7054"
    trousers, boot, brass, paper = "#273237", "#111719", "#c9a566", "#d8c9a6"
    # The idle uses a slow breath and a small hand shift; walking gets a larger,
    # deliberate stride because the coat conceals most leg movement at 64 px.
    if walking:
        stride, lift, swing = step * 10, abs(step) * 3, step * 14
    else:
        stride, lift = 0, 0
        swing = {0: -2, -1: 0, -2: 3}.get(bob, 0)
    shadow = '<ellipse cx="80" cy="181" rx="36" ry="7" fill="#080c0e" opacity=".45"/>'
    legs = f'''<g><path d="M57 128h19l-3 36-10 7-12-3z" fill="{trousers}" stroke="{outline}" stroke-width="3" transform="translate({stride} {lift})"/>
<path d="M82 128h19l4 36-10 7-13-3z" fill="{trousers}" stroke="{outline}" stroke-width="3" transform="translate({-stride} {lift})"/>
<path d="M49 164q12 3 25 0l5 8-4 6H47l-3-5z" fill="{boot}" stroke="{outline}" stroke-width="3" transform="translate({stride} {lift})"/>
<path d="M78 167q12 3 25-1l7 7-3 6H76l-3-5z" fill="{boot}" stroke="{outline}" stroke-width="3" transform="translate({-stride} {lift})"/>
<path d="M52 173h22m7 0h25" stroke="#6d7778" stroke-width="2" opacity=".75"/></g>'''
    hat_front = f'''<path d="M51 45q1-25 29-29 28 4 29 29l-8 5H59z" fill="#30393a" stroke="#101416" stroke-width="3"/>
<path d="M56 38q24 8 48 0" fill="none" stroke="#69706b" stroke-width="2" opacity=".7"/><path d="M61 20v21m19-24v25m19-22v20" stroke="#1f2728" stroke-width="2" opacity=".85"/>
<path d="M57 43q24-7 49 0l5 5q-26 6-58 0z" fill="#20292a" stroke="#101416" stroke-width="3"/><path d="M61 45q19 3 43 0" stroke="{brass}" stroke-width="1.6" opacity=".8"/>'''
    if direction == "down":
        head = f'''<path d="M55 44q1-22 25-23 25 1 25 23v22q-3 20-25 23-22-3-25-23z" fill="{skin}" stroke="{skin_shadow}" stroke-width="3"/>
<path d="M56 51q5-8 12-9m24 0q8 2 12 10" fill="none" stroke="#4a332a" stroke-width="5" stroke-linecap="round"/><path d="M58 66q8 12 22 13 15-1 23-13v8q-5 14-23 17-18-3-23-17z" fill="#966a50" opacity=".54"/>
<path d="M61 55q7-6 15-1m9 0q8-5 15 1" fill="none" stroke="#3e2a24" stroke-width="3" stroke-linecap="round"/>
<rect x="60" y="58" width="18" height="12" rx="5" fill="#d8c6a9" opacity=".35" stroke="#263337" stroke-width="2"/><rect x="82" y="58" width="18" height="12" rx="5" fill="#d8c6a9" opacity=".35" stroke="#263337" stroke-width="2"/><path d="M78 63h4" stroke="#263337" stroke-width="2"/>
<ellipse cx="70" cy="64" rx="2.8" ry="3.2" fill="#2c3e42"/><ellipse cx="91" cy="64" rx="2.8" ry="3.2" fill="#2c3e42"/><circle cx="69" cy="63" r=".8" fill="#e9e2d2"/><circle cx="90" cy="63" r=".8" fill="#e9e2d2"/>
<path d="M80 64v9l-4 3 5 2" fill="none" stroke="{skin_shadow}" stroke-width="2.4" stroke-linecap="round"/><path d="M68 80q12 5 24 0" fill="none" stroke="#52372d" stroke-width="3" stroke-linecap="round"/><path d="M72 78q8 2 16 0" stroke="#453129" stroke-width="2" stroke-linecap="round"/>
<path d="M64 51l4-6m-1 9 5-7" stroke="#754c3c" stroke-width="1.5" stroke-linecap="round"/><path d="M64 74q16 12 32 0" fill="none" stroke="#654536" stroke-width="2" opacity=".65"/>'''
        torso = f'''<path d="M51 77q28-13 57 0l12 27-5 49-19 12-16-8-17 8-19-13-5-48z" fill="{coat}" stroke="{outline}" stroke-width="4"/>
<path d="M54 80 78 101 67 132 48 101zm52 0-26 21 12 31 20-31z" fill="{coat_light}" stroke="{outline}" stroke-width="2"/>
<path d="M69 88 80 102l11-14-5 32H74z" fill="{paper}" stroke="{outline}" stroke-width="2"/><path d="M77 103h7l2 26-6 5-6-5z" fill="{scarf}"/>
<path d="M45 129q36 10 70 0" fill="none" stroke="{coat_shadow}" stroke-width="6"/><rect x="76" y="126" width="10" height="9" rx="2" fill="{brass}" stroke="#765e38" stroke-width="2"/>
<path d="M55 139h13m24 0h13M57 146h10m26 0h10" stroke="{coat_light}" stroke-width="2" opacity=".7"/>'''
        arms = f'''<g transform="rotate({swing} 51 94)"><path d="M53 81q-17 19-13 49l11 10 12-7-4-34 8-13z" fill="{coat_shadow}" stroke="{outline}" stroke-width="3"/><path d="M43 131q6-5 11 1l4 8-7 7-9-4z" fill="{skin}" stroke="{skin_shadow}" stroke-width="2"/></g>
<g transform="rotate({-swing} 108 94)"><path d="M107 81q18 19 13 49l-11 10-12-7 4-34-8-13z" fill="{coat}" stroke="{outline}" stroke-width="3"/><path d="M106 131q6-5 11 1l4 8-7 7-9-4z" fill="{skin}" stroke="{skin_shadow}" stroke-width="2"/></g>'''
        detail = '<path d="M109 105h9v19h-9z" fill="#263135" stroke="#c9a566" stroke-width="2"/><path d="M112 110h3m-3 5h3" stroke="#c9a566" stroke-width="1.5"/>'
        art = arms + torso + head + hat_front + detail
    elif direction == "up":
        head = f'''<path d="M56 43q0-21 24-22 24 1 24 22v20q-4 17-24 20-20-3-24-20z" fill="#352d29" stroke="#1b1a19" stroke-width="3"/><path d="M59 47q21 12 42 0v17q-20 13-42 0z" fill="#4a3a2f"/><path d="M65 59q15 6 30 0" fill="none" stroke="#77604b" stroke-width="2"/>'''
        torso = f'''<path d="M51 77q28-13 57 0l12 27-5 50-20 11-15-8-17 8-19-13-5-48z" fill="{coat_shadow}" stroke="{outline}" stroke-width="4"/>
<path d="M52 83q28 14 56 0l5 20q-33 14-66 0z" fill="{coat}" stroke="{outline}" stroke-width="2"/><path d="M47 105q34 12 66 0v37l-15 13-18-7-18 7-15-13z" fill="{coat}"/>
<path d="M56 104q24 9 48 0" fill="none" stroke="{coat_light}" stroke-width="2"/><path d="M67 113v37m26-37v37" stroke="{coat_light}" stroke-width="2" opacity=".7"/>
<path d="M54 88 108 153" stroke="#222b2f" stroke-width="7"/><path d="M54 88 108 153" stroke="{brass}" stroke-width="2"/><rect x="96" y="139" width="19" height="17" rx="3" fill="#263135" stroke="{outline}" stroke-width="3"/>'''
        arms = f'''<g transform="rotate({swing} 50 94)"><path d="M52 82q-18 21-12 49l11 10 12-7-4-34 7-13z" fill="{coat}" stroke="{outline}" stroke-width="3"/></g>
<g transform="rotate({-swing} 109 94)"><path d="M108 82q18 21 12 49l-11 10-12-7 4-34-7-13z" fill="{coat_light}" stroke="{outline}" stroke-width="3"/></g>'''
        art = arms + torso + head + hat_front
    else:
        head = f'''<path d="M66 39q5-22 25-20 18 4 18 24l-7 17-18 13-18-9-4-17z" fill="{skin}" stroke="{skin_shadow}" stroke-width="3"/>
<path d="M86 50q8-5 15 0" fill="none" stroke="#49342b" stroke-width="3.5" stroke-linecap="round"/><path d="M89 55q5-4 10 0v4q-5 3-10 0z" fill="#e5cfad" stroke="#69503e" stroke-width="1.5"/><circle cx="95" cy="57" r="2.2" fill="{ink}"/>
<path d="M101 57l8 3-8 4" fill="{skin}" stroke="{skin_shadow}" stroke-width="2" stroke-linejoin="round"/><path d="M87 67q9 5 16 0" fill="none" stroke="#563c31" stroke-width="2.5" stroke-linecap="round"/><path d="M81 64q12 14 24 4v6q-12 12-25 1z" fill="#9d7358" opacity=".62"/>
<path d="M84 47l4-5m-2 8 5-6" stroke="#6e4a3d" stroke-width="1.5" stroke-linecap="round"/>'''
        hat_side = f'''<path d="M61 45q4-26 30-26 23 5 20 27l-10 5-37-2z" fill="#30393a" stroke="#101416" stroke-width="3"/><path d="M66 38q17 7 37 3" fill="none" stroke="#69706b" stroke-width="2" opacity=".7"/><path d="M83 23v20m15-15v17" stroke="#1f2728" stroke-width="2"/>
<path d="M61 44q25-8 48 0l9 5q-25 7-60 1z" fill="#20292a" stroke="#101416" stroke-width="3"/><path d="M70 47q16 3 34 0" stroke="{brass}" stroke-width="1.5" opacity=".8"/>'''
        torso = f'''<path d="M53 78q20-13 44-2l20 25-4 50-19 14-15-7-17 7-16-14-2-47z" fill="{coat}" stroke="{outline}" stroke-width="4"/>
<path d="M63 80 86 102l-12 31-18-30z" fill="{coat_light}" stroke="{outline}" stroke-width="2"/><path d="M78 91 88 103l-6 25h-9z" fill="{scarf}"/>
<path d="M48 126q30 9 63-1" fill="none" stroke="{coat_shadow}" stroke-width="6"/><rect x="77" y="123" width="10" height="9" rx="2" fill="{brass}" stroke="#765e38" stroke-width="2"/>
<path d="M49 116 64 123l-10 20-12-5z" fill="{coat_shadow}" stroke="{outline}" stroke-width="2"/>'''
        arms = f'''<g transform="rotate({swing} 50 94)"><path d="M55 82q-18 17-14 47l11 11 12-7-3-34 10-11z" fill="{coat_shadow}" stroke="{outline}" stroke-width="3"/><path d="M44 130q6-5 11 1l4 8-7 7-9-4z" fill="{skin}" stroke="{skin_shadow}" stroke-width="2"/></g>
<g transform="rotate({-swing} 104 94)"><path d="M97 82q19 18 17 43l-10 14-12-6 3-32-9-12z" fill="{coat_light}" stroke="{outline}" stroke-width="3"/><path d="M104 126l17 4-5 18-17-4z" fill="{paper}" stroke="{outline}" stroke-width="2"/><path d="M107 134h9m-10 5h8" stroke="#8a7960" stroke-width="2"/></g>'''
        art = arms + torso + head + hat_side
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 200" width="160" height="200">
{shadow}<g transform="translate(0 {bob})">{legs}{art}</g></svg>'''


# Replace the highly detailed poster-scale portrait generator with this small, readable
# in-game character. Keep its public API and direction/state/frame structure unchanged.
_PAINTED_ANIMATION_CACHE: dict | None = None


def _room_style_detective_svg(direction: str, phase: int, breath: int) -> str:
    """A compact detective drawn in the same outlined SVG language as room props."""
    outline, coat, coat_light, coat_dark = "#29302e", "#4e5b58", "#66736f", "#3b4442"
    cap, cap_light, skin, skin_dark = "#343d3c", "#56615d", "#c39a70", "#9b7455"
    trouser, boot, brass, scarf = "#303a39", "#241f1a", "#dfb15b", "#934d37"
    stride, arm = phase * 6, phase * 8
    step_lift = abs(phase) * 2
    shadow = '<ellipse cx="64" cy="148" rx="28" ry="5" fill="#000000" opacity=".36"/>'

    if phase < 0:
        left_leg, right_leg = 'translate(0 0)', f'translate({stride} {-step_lift})'
    elif phase > 0:
        left_leg, right_leg = f'translate({stride} {-step_lift})', 'translate(0 0)'
    else:
        left_leg = right_leg = 'translate(0 0)'
    legs = f'''<g stroke="{outline}" stroke-width="2"><path d="M46 105h15l-1 30-6 5-10-2z" fill="{trouser}" transform="{left_leg}"/><path d="M67 105h15l2 30-6 5-11-2z" fill="{trouser}" transform="{right_leg}"/>
<path d="M42 133q10 3 18 0l4 6-3 4H41l-2-4z" fill="{boot}" transform="{left_leg}"/><path d="M65 133q11 3 19 0l4 6-3 4H64l-2-4z" fill="{boot}" transform="{right_leg}"/></g>'''
    cap_front = f'''<path d="M44 34q2-21 20-23 20 2 21 23l-6 6H51z" fill="{cap}" stroke="{outline}" stroke-width="2"/>
<path d="M49 29q15 5 31 0" fill="none" stroke="{cap_light}" stroke-width="2"/><path d="M36 35q28-8 56 0 5 3 0 7-30 5-59 0-3-4 3-7z" fill="{cap_light}" stroke="{outline}" stroke-width="2"/><path d="M49 37q15 2 31 0" stroke="{brass}" stroke-width="1"/>'''

    if direction == "down":
        head = f'''<path d="M47 39q0-17 17-18 17 1 17 18v15q-2 15-17 17-15-2-17-17z" fill="{skin}" stroke="{skin_dark}" stroke-width="2"/>
<path d="M51 48q5-4 10 0m7 0q5-4 10 0" fill="none" stroke="#49372a" stroke-width="2"/><path d="M53 53h7m9 0h7" stroke="#202625" stroke-width="2" stroke-linecap="round"/><path d="M64 53v8l-3 2 4 1m-9 3q8 3 16 0" fill="none" stroke="{skin_dark}" stroke-width="1.5"/>'''
        torso = f'''<path d="M45 67q19-10 38 0l10 20-4 38-14 10-11-6-12 6-14-10-4-38z" fill="{coat}" stroke="{outline}" stroke-width="3"/>
<path d="M48 69 64 84 55 105 42 84zm32 0L64 84l9 21 13-21z" fill="{coat_light}" stroke="{outline}" stroke-width="1.5"/><path d="M59 76 64 84l6-8-3 20h-6z" fill="#eee2c8"/><path d="M61 84h6v20h-6z" fill="{scarf}"/>
<path d="M40 106q24 8 48 0" fill="none" stroke="{coat_dark}" stroke-width="4"/><rect x="60" y="103" width="8" height="7" rx="1" fill="{brass}" stroke="#876b3d" stroke-width="1"/>'''
        arms = f'''<g transform="rotate({arm} 45 80)"><path d="M47 70q-12 14-8 32l8 8 9-6-3-24 7-8z" fill="{coat_dark}" stroke="{outline}" stroke-width="2"/><path d="M40 102q5-3 9 1l2 6-5 5-7-3z" fill="{skin}" stroke="{skin_dark}" stroke-width="1"/></g>
<g transform="rotate({-arm} 83 80)"><path d="M81 70q13 14 9 32l-8 8-9-6 3-24-7-8z" fill="{coat_light}" stroke="{outline}" stroke-width="2"/><path d="M80 102q5-3 9 1l2 6-5 5-7-3z" fill="{skin}" stroke="{skin_dark}" stroke-width="1"/></g>'''
        art = arms + torso + head + cap_front + '<rect x="84" y="83" width="6" height="15" rx="1" fill="#303a39" stroke="#dfb15b" stroke-width="1"/>'
    elif direction == "up":
        head = f'''<path d="M47 38q0-17 17-18 17 1 17 18v18q-3 13-17 16-14-3-17-16z" fill="#3b3029" stroke="#25221f" stroke-width="2"/><path d="M51 47q13 8 26 0v12q-13 9-26 0z" fill="#514035"/>'''
        torso = f'''<path d="M45 67q19-10 38 0l10 20-4 38-14 10-11-6-12 6-14-10-4-38z" fill="{coat_dark}" stroke="{outline}" stroke-width="3"/>
<path d="M43 73q21 10 42 0l4 17q-25 10-50 0z" fill="{coat}" stroke="{outline}" stroke-width="1.5"/><path d="M43 104q21 8 43 0v20l-12 8-10-5-11 5-13-8z" fill="{coat}"/><path d="M48 103q16 6 32 0" fill="none" stroke="{coat_light}" stroke-width="1.5"/>
<path d="M47 76 83 123" stroke="#251f1a" stroke-width="5"/><path d="M47 76 83 123" stroke="{brass}" stroke-width="1"/><rect x="77" y="113" width="14" height="13" rx="2" fill="#3b4442" stroke="{outline}" stroke-width="2"/>'''
        arms = f'''<path d="M47 70q-12 14-8 32l8 8 9-6-3-24 7-8z" fill="{coat}" stroke="{outline}" stroke-width="2" transform="rotate({arm} 45 80)"/><path d="M81 70q13 14 9 32l-8 8-9-6 3-24-7-8z" fill="{coat_light}" stroke="{outline}" stroke-width="2" transform="rotate({-arm} 83 80)"/>'''
        art = arms + torso + head + cap_front
    else:
        head = f'''<path d="M54 38q5-18 20-16 14 3 13 19l-6 15-14 9-13-7-2-14z" fill="{skin}" stroke="{skin_dark}" stroke-width="2"/><path d="M72 48h8m-10 9 9 1" stroke="#49372a" stroke-width="2"/><path d="M76 49h4" stroke="#202625" stroke-width="2" stroke-linecap="round"/>'''
        cap_side = f'''<path d="M52 35q5-22 22-21 18 3 16 23l-7 6-28-1z" fill="{cap}" stroke="{outline}" stroke-width="2"/><path d="M57 31q13 5 26 1" stroke="{cap_light}" stroke-width="2"/><path d="M38 36q25-9 49 0 5 3 0 7-27 5-53 0-3-4 4-7z" fill="{cap_light}" stroke="{outline}" stroke-width="2"/>'''
        torso = f'''<path d="M45 68q17-11 35-3l15 20-4 40-14 11-11-6-12 5-14-11-3-38z" fill="{coat}" stroke="{outline}" stroke-width="3"/><path d="M55 69 70 84l-9 23-16-22z" fill="{coat_light}" stroke="{outline}" stroke-width="1.5"/><path d="M66 77 73 85l-5 20h-6z" fill="{scarf}"/><path d="M40 104q23 7 48 0" fill="none" stroke="{coat_dark}" stroke-width="4"/><rect x="63" y="101" width="8" height="7" rx="1" fill="{brass}"/>'''
        arms = f'''<g transform="rotate({arm} 45 80)"><path d="M49 70q-14 15-9 33l8 8 9-6-3-25 8-8z" fill="{coat_dark}" stroke="{outline}" stroke-width="2"/><path d="M40 103q5-3 9 1l2 6-5 5-7-3z" fill="{skin}" stroke="{skin_dark}" stroke-width="1"/></g><g transform="rotate({-arm} 82 80)"><path d="M79 70q16 14 12 31l-8 10-9-6 3-24-8-9z" fill="{coat_light}" stroke="{outline}" stroke-width="2"/><path d="M83 100l12 3-4 14-12-3z" fill="#e8d3b0" stroke="{outline}" stroke-width="1"/></g>'''
        art = arms + torso + head + cap_side
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 160" width="128" height="160">{shadow}<g transform="translate(0 {breath})">{legs}{art}</g></svg>'''


def get_character_animations(palette: CharacterPalette = DETECTIVE_PALETTE) -> dict:
    """Return four-direction detective frames in the room's SVG art style."""
    del palette  # Kept only for callers using the original public API.
    global _PAINTED_ANIMATION_CACHE
    if _PAINTED_ANIMATION_CACHE is not None:
        return _PAINTED_ANIMATION_CACHE

    result = {}
    for direction in ("down", "up", "right"):
        result[direction] = {
            "idle": [render_svg(_room_style_detective_svg(direction, 0, breath), 64, 80)
                     for breath in (0, -1, -2, -1)],
            "walk": [render_svg(_room_style_detective_svg(direction, phase, breath), 64, 80)
                     for phase, breath in ((-1, 0), (0, -1), (1, 0), (0, -1))],
        }
    result["left"] = {
        state: [pygame.transform.flip(frame, True, False) for frame in frames]
        for state, frames in result["right"].items()
    }

    _PAINTED_ANIMATION_CACHE = result
    return result


# Painted character assets and their authored gait. This definition supersedes the
# SVG fallback above while preserving the public animation API used by Player.
def _read_strip(path: Path, columns: int = 4) -> list[pygame.Surface]:
    """Read an authored transparent sprite strip into gameplay-size frames."""
    strip = pygame.image.load(str(path))
    cell_width = strip.get_width() // columns
    return [pygame.transform.smoothscale(
        strip.subsurface(pygame.Rect(index * cell_width, 0, cell_width, strip.get_height())), (64, 80)
    ) for index in range(columns)]


def _breathe_frame(base: pygame.Surface, y_offset: int) -> pygame.Surface:
    """Create a quiet idle breath while preserving the painted silhouette."""
    frame = pygame.Surface(base.get_size(), pygame.SRCALPHA)
    frame.blit(base, (0, y_offset))
    return frame


def get_character_animations(palette: CharacterPalette = DETECTIVE_PALETTE) -> dict:
    """Return the painted, four-direction detective animation set."""
    del palette
    global _PAINTED_ANIMATION_CACHE
    if _PAINTED_ANIMATION_CACHE is not None:
        return _PAINTED_ANIMATION_CACHE

    sprites_dir = Path(__file__).resolve().parent / "sprites"
    sheet = pygame.image.load(str(sprites_dir / "detective_sheet_v1.png"))
    cell_width = sheet.get_width() // 4
    direction_cells = {"down": 0, "up": 1, "right": 2, "left": 3}
    result = {}
    for direction, cell in direction_cells.items():
        source = sheet.subsurface(pygame.Rect(cell * cell_width, 0, cell_width, sheet.get_height()))
        base = pygame.transform.smoothscale(source, (64, 80))
        result[direction] = {"idle": [_breathe_frame(base, offset) for offset in (0, -1, -2, -1)]}

    result["down"]["walk"] = _read_strip(sprites_dir / "detective_walk_down_v1.png")
    result["up"]["walk"] = _read_strip(sprites_dir / "detective_walk_up_v1.png")
    result["right"]["walk"] = _read_strip(sprites_dir / "detective_walk_right_v1.png")
    result["left"]["walk"] = [pygame.transform.flip(frame, True, False) for frame in result["right"]["walk"]]
    _PAINTED_ANIMATION_CACHE = result
    return result
