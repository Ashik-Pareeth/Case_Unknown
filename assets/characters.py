"""
Character Vector Graphics & Animation Engine for Case Unknown.

This module provides modular, parameterized SVG generation for the Trainee Detective
and future NPCs, along with 4-directional idle and walk animation frame generators.
"""

from dataclasses import dataclass
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


def _svg_legs_front(l_dx: int, l_dy: int, r_dx: int, r_dy: int, p: CharacterPalette) -> str:
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


def _svg_torso_front(coat_flare: int, l_arm_dy: int, r_arm_dy: int, p: CharacterPalette) -> str:
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


def _generate_detective_down_svg(bob_y: int = 0, l_leg_dx: int = 0, l_leg_dy: int = 0,
                                 r_leg_dx: int = 0, r_leg_dy: int = 0,
                                 l_arm_dy: int = 0, r_arm_dy: int = 0,
                                 coat_flare: int = 0,
                                 palette: CharacterPalette = DETECTIVE_PALETTE) -> str:
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

def _svg_legs_back(l_dx: int, l_dy: int, r_dx: int, r_dy: int, p: CharacterPalette) -> str:
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


def _svg_torso_back(coat_flare: int, l_arm_dy: int, r_arm_dy: int, p: CharacterPalette) -> str:
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


def _generate_detective_up_svg(bob_y: int = 0, l_leg_dx: int = 0, l_leg_dy: int = 0,
                               r_leg_dx: int = 0, r_leg_dy: int = 0,
                               l_arm_dy: int = 0, r_arm_dy: int = 0,
                               coat_flare: int = 0,
                               palette: CharacterPalette = DETECTIVE_PALETTE) -> str:
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

def _svg_legs_side(f_dx: int, f_dy: int, b_dx: int, b_dy: int, p: CharacterPalette) -> str:
    """Front and back legs and shoes in profile stride."""
    return f"""  <!-- Back Leg & Shoe (Swinging / Stepping) -->
  <g transform="translate({b_dx*2}, {b_dy*2})">
    <path d="M52,104 L63,104 L{65 + b_dx},136 L{52 + b_dx},136 Z" fill="{p.pants_side_back}"/>
    <g transform="translate({b_dx}, 0)">
      <rect x="49" y="135" width="18" height="8" rx="3" fill="{p.shoe_darkest}"/>
      <path d="M47,138 Q57,134 67,137 L69,145 L46,145 Z" fill="#1e222a"/>
      <line x1="46" y1="145" x2="69" y2="145" stroke="#0e1014" stroke-width="1.5"/>
    </g>
  </g>

  <!-- Front Leg & Shoe -->
  <g transform="translate({f_dx*2}, {f_dy*2})">
    <path d="M61,104 L74,104 L{76 + f_dx},136 L{61 + f_dx},136 Z" fill="{p.pants_side_front}"/>
    <line x1="{62 + f_dx*0.5}" y1="106" x2="{62 + f_dx}" y2="135" stroke="#1c1f26" stroke-width="1"/>
    <g transform="translate({f_dx}, 0)">
      <rect x="59" y="135" width="20" height="8" rx="3" fill="#181a20"/>
      <path d="M57,138 Q69,133 80,137 L82,145 L56,145 Z" fill="{p.shoe_leather_side}"/>
      <path d="M72,136 Q78,135 81,138 L81,145 L72,145 Z" fill="{p.shoe_highlight}" opacity="0.6"/>
      <line x1="56" y1="145" x2="82" y2="145" stroke="{p.shoe_sole}" stroke-width="1.5"/>
    </g>
  </g>"""


def _svg_torso_side(coat_flare: int, f_arm_rot: int, p: CharacterPalette) -> str:
    """Tailored profile trench coat, lapel overlap, shirt collar, red tie, and front swinging arm."""
    return f"""    <!-- Trench Coat Tail & Back Flare -->
    <path d="M46,84 L{37 - coat_flare*2.5},114 L75,114 L78,84 Z" fill="{p.coat_lapel_r}"/>
    <path d="M48,84 L{40 - coat_flare*2.5},112 L74,112 L77,84 Z" fill="url(#coatGradSide)"/>
    <line x1="{48 - coat_flare}" y1="92" x2="{45 - coat_flare*2}" y2="112" stroke="#684f2c" stroke-width="1.5"/>

    <!-- Torso Silhouette with tailored rounded shoulder -->
    <path d="M54,52 
             Q45,54 45,64 
             L46,88 
             L79,88 
             L78,60 
             Q78,54 70,52 
             Z" fill="url(#coatGradSide)"/>
    
    <!-- Coat Lapel Overlap & Double-breasted chest -->
    <path d="M52,54 Q47,56 47,66 L48,86 L77,86 L77,64 Q76,55 69,53 Z" fill="url(#coatGradSide)"/>
    <line x1="68" y1="58" x2="70" y2="84" stroke="#7e6034" stroke-width="1.2" stroke-dasharray="3,2"/>

    <!-- Belt & Brass Buckle -->
    <rect x="45" y="84" width="35" height="6" rx="1.5" fill="{p.belt_dark}"/>
    <rect x="55" y="83" width="3" height="8" rx="1" fill="{p.belt_loop}"/>
    <!-- Belt Buckle on front hip -->
    <rect x="74" y="82" width="7" height="9" rx="2" fill="{p.brass}" stroke="{p.brass_border}" stroke-width="0.8"/>
    <rect x="75.5" y="83.5" width="4" height="6" rx="1" fill="{p.brass_side_gold}"/>
    <line x1="77.5" y1="82" x2="77.5" y2="91" stroke="#8a681a" stroke-width="1"/>

    <!-- Shirt Collar & Silk Tie -->
    <polygon points="67,50 78,51 79,60 72,56" fill="{p.shirt_white}"/>
    <polygon points="72,50 78,51 76,56" fill="{p.shirt_side_shadow}"/>
    <polygon points="74,54 79,55 78,73 74,76 73,60" fill="{p.tie_red}"/>
    <polygon points="75,55 78,56 77,72 75,74" fill="{p.tie_highlight}"/>

    <!-- Coat Lapels -->
    <polygon points="61,52 77,64 72,74 61,58" fill="{p.coat_lapel_side_base}"/>
    <polygon points="61,52 75,63 71,72 62,58" fill="{p.coat_lapel_side_light}"/>
    <!-- Coat buttons -->
    <circle cx="71" cy="65" r="2" fill="{p.brass}" stroke="{p.coat_lapel_r}" stroke-width="0.6"/>
    <circle cx="72" cy="76" r="2" fill="{p.brass}" stroke="{p.coat_lapel_r}" stroke-width="0.6"/>

    <!-- Front Arm (Swinging in front of body) -->
    <g transform="rotate({f_arm_rot}, 63, 60)">
      <ellipse cx="62" cy="58" rx="7" ry="5.5" fill="{p.coat_mid}"/>
      <path d="M57,59 L66,76 L64,92 L56,92 L54,76 L55,59 Z" fill="url(#coatGradSide)"/>
      <path d="M54,74 Q59,77 63,74" stroke="{p.coat_lapel_r}" stroke-width="1.2" fill="none"/>
      <rect x="55" y="88" width="11" height="4" rx="1.5" fill="#6d512a"/>
      <circle cx="63" cy="90" r="1.2" fill="{p.brass}"/>
      <ellipse cx="60" cy="96" rx="5" ry="4" fill="#e2b484"/>
      <path d="M58,95 Q62,98 64,95" stroke="#b07d50" stroke-width="1" fill="none"/>
    </g>"""


def _svg_head_side(p: CharacterPalette) -> str:
    """Sharp youthful detective profile face, jaw, wedge eye, nose, lips, ear, and hair."""
    return f"""    <!-- Neck (natural angled transition from shoulders) -->
    <path d="M54,42 Q53,48 55,54 L69,54 Q68,48 67,42 Z" fill="url(#skinSide)"/>
    <path d="M54,42 L66,42 L63,48 L55,47 Z" fill="#b88450" opacity="0.4"/>

    <!-- Cranium / Head Base -->
    <path d="M48,22 Q46,32 50,40 Q54,46 62,48 L68,48 Q74,44 76,38 Q78,30 76,22 Z" fill="url(#skinSide)"/>

    <!-- Hair: Rich dark brown hair covering back of head and under hat -->
    <path d="M46,20 Q44,28 46,36 Q48,42 54,44 Q52,38 51,32 Q50,24 51,20 Z" fill="{p.hair_dark}"/>
    <path d="M48,22 Q46,30 48,38 Q51,42 55,43 L54,34 Q52,26 53,20 Z" fill="{p.hair_main}"/>
    <path d="M48,24 Q46,32 49,38" stroke="{p.hair_highlight}" stroke-width="1" fill="none" opacity="0.7"/>

    <!-- Ear -->
    <ellipse cx="56" cy="33" rx="5" ry="7.5" fill="#e0b280"/>
    <ellipse cx="55.5" cy="33" rx="3.5" ry="5.5" fill="#c69262"/>
    <path d="M54,30 Q52,33 55,36" stroke="{p.nostril_shadow}" stroke-width="1" fill="none"/>
    <ellipse cx="56" cy="38" rx="2.5" ry="2.5" fill="#d8a474"/>

    <!-- Sideburn in front of ear -->
    <path d="M58,22 L59,34 Q58,37 57,38 L55,34 L56,22 Z" fill="{p.hair_dark}"/>

    <!-- Front Face Profile Contour (Forehead, Nose, Lips, Chin, Jawline) -->
    <path d="M68,18 
             L73,23 
             L72,25 
             L78,34 
             L74,36 
             L75,39 
             L77,41 
             L74,42 
             L76,44 
             L73,45 
             L75,48 
             L70,51 
             L60,47 
             Z" fill="url(#skinSide)"/>

    <!-- Facial Contour details -->
    <path d="M72,26 L77.5,34 L74,35.5" stroke="#fce4c8" stroke-width="0.8" fill="none" opacity="0.7"/>
    <ellipse cx="74.5" cy="35.5" rx="1.5" ry="1" fill="{p.nostril_shadow}" opacity="0.6"/>

    <!-- Profile Lips -->
    <path d="M74,39 Q76.5,40.5 77,41 L74.5,41.5 Z" fill="{p.lip_side_upper}"/>
    <path d="M74,42 Q76,42.5 75.8,44 L73.5,43.5 Z" fill="{p.lip_side_lower}"/>
    <path d="M73,45 Q74.5,46 73.5,47" stroke="#b88450" stroke-width="0.8" fill="none" opacity="0.5"/>

    <!-- Defined Jawline -->
    <path d="M58,38 L64,45 L71,49 L74,48" stroke="{p.jaw_line}" stroke-width="1.2" fill="none" opacity="0.6"/>
    <ellipse cx="67" cy="34" rx="5" ry="3.5" fill="{p.cheek_flush_side}" opacity="0.3" transform="rotate(-10 67 34)"/>

    <!-- Profile Eye (True anatomical wedge profile) -->
    <path d="M66,26 Q71,24 74,27 Q70,30 66,29 Z" fill="#d9a877" opacity="0.3"/>
    <path d="M68,26 L74,27.5 L69,30 Z" fill="{p.eye_side_white}"/>
    <path d="M70.5,26.8 Q73.8,27.5 73.5,29.2 Q71.5,30 70,29.2 Z" fill="url(#irisGradSide)"/>
    <ellipse cx="72" cy="28.2" rx="1.2" ry="1.6" fill="#0b1408"/>
    <circle cx="72.5" cy="27.4" r="0.7" fill="#ffffff"/>
    <path d="M66,25 Q71,23.5 74.5,26" stroke="{p.eye_side_liner}" stroke-width="1.4" fill="none" stroke-linecap="round"/>
    <path d="M67,23.5 Q71,22.5 74,24.5" stroke="#a06c3a" stroke-width="0.7" fill="none" opacity="0.6"/>
    <line x1="74" y1="26" x2="75.5" y2="25" stroke="{p.eye_side_liner}" stroke-width="1.2" stroke-linecap="round"/>

    <!-- Eyebrow: Sharp, focused detective brow -->
    <path d="M66,21 Q71,18 76,21" stroke="{p.brow_side}" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M66,21 Q71,18 76,21" stroke="{p.hair_main}" stroke-width="1.5" fill="none" stroke-linecap="round"/>

    <!-- Front hair fringe peeking under fedora brim -->
    <path d="M67,18 Q71,19 73,22 Q70,21 68,20 Z" fill="{p.hair_dark}"/>
    <path d="M64,18 Q67,21 69,23 Q66,21 64,19 Z" fill="{p.hair_main}"/>"""


def _svg_hat_side(p: CharacterPalette) -> str:
    """Fedora hat in profile: snap brim, creased crown, ribbon band, and gold pin."""
    return f"""    <!-- Classic Noir Fedora (Profile View) -->
    <path d="M42,20 Q62,22 84,23 L82,25 Q62,24 42,21 Z" fill="#120e0b" opacity="0.5"/>
    <ellipse cx="63" cy="18" rx="27" ry="5.5" fill="{p.hat_crease}" transform="rotate(-3 63 18)"/>
    <ellipse cx="63" cy="17" rx="26" ry="4.8" fill="url(#hatGradSide)" transform="rotate(-3 63 17)"/>
    <path d="M48,16 
             Q49,6 61,4 
             Q66,6 72,5 
             Q76,8 77,16 
             Z" fill="url(#hatGradSide)"/>
    <path d="M54,6 Q63,9 71,6" stroke="#18120d" stroke-width="2.2" fill="none" stroke-linecap="round"/>
    <path d="M70,8 Q74,11 75,15" stroke="{p.hat_crease}" stroke-width="1.8" fill="none" opacity="0.7"/>

    <!-- Hat Ribbon Band & Badge -->
    <path d="M47.5,16 Q63,18 77.2,15.5 L77.5,13 Q63,15 47.8,13.5 Z" fill="{p.hat_band_side}"/>
    <line x1="47.6" y1="16" x2="77.2" y2="15.5" stroke="#0e1012" stroke-width="0.8"/>
    <circle cx="58" cy="14.5" r="2.2" fill="{p.brass}" stroke="#8a681a" stroke-width="0.6"/>
    <circle cx="58" cy="14.5" r="1.1" fill="{p.brass_dark}"/>"""


def _generate_detective_side_svg(bob_y: int = 0, f_leg_dx: int = 0, f_leg_dy: int = 0,
                                 b_leg_dx: int = 0, b_leg_dy: int = 0,
                                 f_arm_rot: int = 0, b_arm_rot: int = 0,
                                 coat_flare: int = 0,
                                 palette: CharacterPalette = DETECTIVE_PALETTE) -> str:
    """Generates an SVG for the Detective facing Right (profile view)."""
    defs = _svg_character_defs(palette, view="side")
    shadow = f'  <!-- Ground contact shadow -->\n  <ellipse cx="{64 + f_leg_dx}" cy="152" rx="{34 + abs(f_leg_dx)*2}" ry="7" fill="#000000" opacity="0.3"/>'
    legs = _svg_legs_side(f_leg_dx, f_leg_dy, b_leg_dx, b_leg_dy, palette)
    torso = _svg_torso_side(coat_flare, f_arm_rot, palette)
    head = _svg_head_side(palette)
    hat = _svg_hat_side(palette)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 160" width="128" height="160">
{defs}

{shadow}

{legs}

  <!-- Back Arm (Swinging behind body) -->
  <g transform="translate(0, {bob_y*2}) rotate({b_arm_rot}, 58, 62)">
    <path d="M54,58 L46,80 L52,94 L60,92 L58,76 L62,58 Z" fill="url(#coatBackGrad)"/>
    <rect x="49" y="88" width="11" height="4" rx="1.5" fill="{palette.belt_dark}"/>
    <circle cx="58" cy="90" r="1.2" fill="{palette.brass}"/>
    <ellipse cx="53" cy="97" rx="5" ry="4" fill="#cf9f6e"/>
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
        render_svg(_generate_detective_down_svg(bob_y=0, l_leg_dx=-1, l_leg_dy=-4, r_leg_dx=1, r_leg_dy=3, l_arm_dy=2, r_arm_dy=-2, coat_flare=2, palette=palette), W, H),
        render_svg(_generate_detective_down_svg(bob_y=1, l_leg_dx=0, l_leg_dy=0, r_leg_dx=0, r_leg_dy=0, l_arm_dy=0, r_arm_dy=0, coat_flare=0, palette=palette), W, H),
        render_svg(_generate_detective_down_svg(bob_y=0, l_leg_dx=1, l_leg_dy=3, r_leg_dx=-1, r_leg_dy=-4, l_arm_dy=-2, r_arm_dy=2, coat_flare=-2, palette=palette), W, H),
        render_svg(_generate_detective_down_svg(bob_y=1, l_leg_dx=0, l_leg_dy=0, r_leg_dx=0, r_leg_dy=0, l_arm_dy=0, r_arm_dy=0, coat_flare=0, palette=palette), W, H),
    ]

    # Up animations (Facing away)
    up_idle = [
        render_svg(_generate_detective_up_svg(bob_y=0, palette=palette), W, H),
        render_svg(_generate_detective_up_svg(bob_y=1, palette=palette), W, H),
    ]
    up_walk = [
        render_svg(_generate_detective_up_svg(bob_y=0, l_leg_dx=-1, l_leg_dy=-4, r_leg_dx=1, r_leg_dy=3, l_arm_dy=2, r_arm_dy=-2, coat_flare=2, palette=palette), W, H),
        render_svg(_generate_detective_up_svg(bob_y=1, l_leg_dx=0, l_leg_dy=0, r_leg_dx=0, r_leg_dy=0, l_arm_dy=0, r_arm_dy=0, coat_flare=0, palette=palette), W, H),
        render_svg(_generate_detective_up_svg(bob_y=0, l_leg_dx=1, l_leg_dy=3, r_leg_dx=-1, r_leg_dy=-4, l_arm_dy=-2, r_arm_dy=2, coat_flare=-2, palette=palette), W, H),
        render_svg(_generate_detective_up_svg(bob_y=1, l_leg_dx=0, l_leg_dy=0, r_leg_dx=0, r_leg_dy=0, l_arm_dy=0, r_arm_dy=0, coat_flare=0, palette=palette), W, H),
    ]

    # Right animations (Profile)
    right_idle = [
        render_svg(_generate_detective_side_svg(bob_y=0, palette=palette), W, H),
        render_svg(_generate_detective_side_svg(bob_y=1, palette=palette), W, H),
    ]
    right_walk = [
        render_svg(_generate_detective_side_svg(bob_y=0, f_leg_dx=4, f_leg_dy=-2, b_leg_dx=-5, b_leg_dy=2, f_arm_rot=-16, b_arm_rot=16, coat_flare=3, palette=palette), W, H),
        render_svg(_generate_detective_side_svg(bob_y=1, f_leg_dx=1, f_leg_dy=0, b_leg_dx=-1, b_leg_dy=0, f_arm_rot=-4, b_arm_rot=4, coat_flare=1, palette=palette), W, H),
        render_svg(_generate_detective_side_svg(bob_y=0, f_leg_dx=-5, f_leg_dy=2, b_leg_dx=4, b_leg_dy=-2, f_arm_rot=16, b_arm_rot=-16, coat_flare=2, palette=palette), W, H),
        render_svg(_generate_detective_side_svg(bob_y=1, f_leg_dx=-1, f_leg_dy=0, b_leg_dx=1, b_leg_dy=0, f_arm_rot=4, b_arm_rot=-4, coat_flare=1, palette=palette), W, H),
    ]

    # Left animations (Flipped horizontally from Right for perfect frame symmetry)
    left_idle = [pygame.transform.flip(s, True, False) for s in right_idle]
    left_walk = [pygame.transform.flip(s, True, False) for s in right_walk]

    return {
        'down': {'idle': down_idle, 'walk': down_walk},
        'up': {'idle': up_idle, 'walk': up_walk},
        'right': {'idle': right_idle, 'walk': right_walk},
        'left': {'idle': left_idle, 'walk': left_walk},
    }
