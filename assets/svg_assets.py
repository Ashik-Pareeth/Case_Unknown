"""
SVG Vector Assets Module for Case Unknown.

This module defines all characters, furniture, and environmental objects
as standalone SVG vector graphics and provides rendering and caching utilities
to produce high-quality Pygame surfaces without external raster images.
"""

import io
import pygame

# ---------------------------------------------------------------------------
# SVG Rendering & Caching Pipeline
# ---------------------------------------------------------------------------

_SURFACE_CACHE = {}


def render_svg(svg_code: str, width: int = None, height: int = None) -> pygame.Surface:
    """
    Renders an SVG string into a Pygame Surface with per-pixel alpha transparency.
    Caches the resulting surface for optimal 60 FPS performance.
    """
    cache_key = (svg_code, width, height)
    if cache_key in _SURFACE_CACHE:
        return _SURFACE_CACHE[cache_key]

    # If width and height are specified, ensure the root SVG tag reflects them
    processed_svg = svg_code
    if width is not None and height is not None:
        if '<svg' in processed_svg:
            # Replace or inject width and height in the <svg tag
            header_end = processed_svg.find('>')
            header = processed_svg[:header_end]
            # Strip existing width and height if any
            import re
            header = re.sub(r'\bwidth="[^"]*"', '', header)
            header = re.sub(r'\bheight="[^"]*"', '', header)
            new_header = f'{header} width="{width}" height="{height}"'
            processed_svg = new_header + processed_svg[header_end:]

    svg_bytes = processed_svg.encode('utf-8')
    bytes_io = io.BytesIO(svg_bytes)
    surface = pygame.image.load(bytes_io, "asset.svg")
    if pygame.display.get_surface() is not None:
        surface = surface.convert_alpha()

    # If dimensions requested differ from rendered surface size, smoothscale it
    if width is not None and height is not None:
        if surface.get_size() != (width, height):
            surface = pygame.transform.smoothscale(surface, (width, height))

    _SURFACE_CACHE[cache_key] = surface
    return surface


# ---------------------------------------------------------------------------
# Character SVG Assets: Detective Trainee
# ---------------------------------------------------------------------------

def _generate_detective_down_svg(bob_y: int = 0, l_leg_dx: int = 0, l_leg_dy: int = 0,
                                 r_leg_dx: int = 0, r_leg_dy: int = 0,
                                 l_arm_dy: int = 0, r_arm_dy: int = 0,
                                 coat_flare: int = 0) -> str:
    """Generates an SVG for the Detective facing Down (towards the camera)."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 80" width="64" height="80">
  <defs>
    <!-- Coat gradient -->
    <linearGradient id="coatGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#b08b58"/>
      <stop offset="50%" stop-color="#c9a470"/>
      <stop offset="100%" stop-color="#9e7b48"/>
    </linearGradient>
    <!-- Hat gradient -->
    <linearGradient id="hatGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4a3e35"/>
      <stop offset="100%" stop-color="#2d241d"/>
    </linearGradient>
  </defs>

  <!-- Ground contact shadow -->
  <ellipse cx="32" cy="74" rx="19" ry="5" fill="#000000" opacity="0.35"/>

  <!-- Left Leg & Shoe -->
  <g transform="translate({l_leg_dx}, {l_leg_dy})">
    <rect x="23" y="52" width="7" height="18" rx="2" fill="#2a2e36"/>
    <ellipse cx="26" cy="71" rx="5" ry="3" fill="#181a1f"/>
    <path d="M22,70 Q26,68 30,70 L30,73 L22,73 Z" fill="#2d3039"/>
  </g>

  <!-- Right Leg & Shoe -->
  <g transform="translate({r_leg_dx}, {r_leg_dy})">
    <rect x="34" y="52" width="7" height="18" rx="2" fill="#262930"/>
    <ellipse cx="38" cy="71" rx="5" ry="3" fill="#181a1f"/>
    <path d="M34,70 Q38,68 42,70 L42,73 L34,73 Z" fill="#2d3039"/>
  </g>

  <!-- Upper Body & Head (with breathing / step bob) -->
  <g transform="translate(0, {bob_y})">
    <!-- Trench Coat Tail & Flare -->
    <path d="M19,42 L{17 - coat_flare},58 L{47 + coat_flare},58 L45,42 Z" fill="#9e7b48"/>
    <path d="M21,42 L{19 - coat_flare},56 L{45 + coat_flare},56 L43,42 Z" fill="url(#coatGrad)"/>

    <!-- Left Arm -->
    <g transform="translate(0, {l_arm_dy})">
      <path d="M18,30 Q14,38 16,48 Q18,50 20,48 Q18,40 21,32 Z" fill="#967544"/>
      <!-- Glove / hand -->
      <circle cx="18" cy="49" r="3" fill="#d2ab82"/>
    </g>

    <!-- Right Arm -->
    <g transform="translate(0, {r_arm_dy})">
      <path d="M46,30 Q50,38 48,48 Q46,50 44,48 Q46,40 43,32 Z" fill="#967544"/>
      <!-- Glove / hand -->
      <circle cx="46" cy="49" r="3" fill="#d2ab82"/>
    </g>

    <!-- Main Coat Torso -->
    <path d="M20,28 L44,28 L45,46 L19,46 Z" fill="url(#coatGrad)"/>
    
    <!-- Coat Lapels -->
    <polygon points="26,28 32,38 23,38" fill="#88683a"/>
    <polygon points="38,28 32,38 41,38" fill="#7a5d34"/>

    <!-- Shirt Collar & Crimson Detective Tie -->
    <polygon points="28,27 32,32 30,27" fill="#e8edf2"/>
    <polygon points="36,27 32,32 34,27" fill="#e8edf2"/>
    <polygon points="31,30 33,30 34,39 32,41 30,39" fill="#a82323"/>

    <!-- Double-breasted Brass Buttons -->
    <circle cx="28" cy="41" r="1.5" fill="#dfb15b"/>
    <circle cx="36" cy="41" r="1.5" fill="#dfb15b"/>
    <circle cx="28" cy="46" r="1.5" fill="#dfb15b"/>
    <circle cx="36" cy="46" r="1.5" fill="#dfb15b"/>

    <!-- Coat Belt -->
    <rect x="20" y="43" width="24" height="3" fill="#6d532a"/>
    <rect x="30" y="42" width="4" height="5" fill="#dfb15b" rx="1"/>

    <!-- Head & Face -->
    <ellipse cx="32" cy="22" rx="9" ry="9" fill="#f0ca9c"/>
    <!-- Cheeks & ears -->
    <circle cx="22" cy="22" r="2.5" fill="#deb485"/>
    <circle cx="42" cy="22" r="2.5" fill="#deb485"/>
    <!-- Detective Eyes -->
    <ellipse cx="28" cy="23" rx="1.5" ry="2" fill="#24211d"/>
    <ellipse cx="36" cy="23" rx="1.5" ry="2" fill="#24211d"/>
    <circle cx="28.5" cy="22.5" r="0.6" fill="#ffffff"/>
    <circle cx="36.5" cy="22.5" r="0.6" fill="#ffffff"/>
    
    <!-- Fedora Brim Shadow on Face -->
    <path d="M23,19 Q32,24 41,19 L41,17 Q32,21 23,17 Z" fill="#000000" opacity="0.3"/>

    <!-- Fedora Hat Brim -->
    <ellipse cx="32" cy="18" rx="19" ry="6" fill="#2a221b"/>
    <ellipse cx="32" cy="17" rx="18" ry="5" fill="url(#hatGrad)"/>

    <!-- Hat Crown -->
    <path d="M22,17 Q23,6 32,7 Q41,6 42,17 Z" fill="url(#hatGrad)"/>
    <!-- Crown Dent / Crease -->
    <path d="M28,8 Q32,11 36,8" stroke="#1d1611" stroke-width="1.8" fill="none"/>
    <!-- Hat Band (Dark Charcoal/Crimson) -->
    <path d="M22,16 Q32,18 42,16 L42,14 Q32,16 22,14 Z" fill="#15171a"/>
    <rect x="30" y="14" width="4" height="3" fill="#dfb15b" rx="0.5"/>
  </g>
</svg>"""


def _generate_detective_up_svg(bob_y: int = 0, l_leg_dx: int = 0, l_leg_dy: int = 0,
                               r_leg_dx: int = 0, r_leg_dy: int = 0,
                               l_arm_dy: int = 0, r_arm_dy: int = 0,
                               coat_flare: int = 0) -> str:
    """Generates an SVG for the Detective facing Up (walking away / back view)."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 80" width="64" height="80">
  <defs>
    <linearGradient id="coatGradUp" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#9e7b48"/>
      <stop offset="50%" stop-color="#b8935e"/>
      <stop offset="100%" stop-color="#8c6a3b"/>
    </linearGradient>
    <linearGradient id="hatGradUp" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4a3e35"/>
      <stop offset="100%" stop-color="#2d241d"/>
    </linearGradient>
  </defs>

  <!-- Ground contact shadow -->
  <ellipse cx="32" cy="74" rx="19" ry="5" fill="#000000" opacity="0.35"/>

  <!-- Left Leg & Shoe Heel -->
  <g transform="translate({l_leg_dx}, {l_leg_dy})">
    <rect x="23" y="52" width="7" height="18" rx="2" fill="#262930"/>
    <ellipse cx="26" cy="71" rx="5" ry="3" fill="#181a1f"/>
  </g>

  <!-- Right Leg & Shoe Heel -->
  <g transform="translate({r_leg_dx}, {r_leg_dy})">
    <rect x="34" y="52" width="7" height="18" rx="2" fill="#2a2e36"/>
    <ellipse cx="38" cy="71" rx="5" ry="3" fill="#181a1f"/>
  </g>

  <!-- Upper Body & Back of Head -->
  <g transform="translate(0, {bob_y})">
    <!-- Back Coat Flap & Vent Split -->
    <path d="M19,42 L{17 - coat_flare},58 L{47 + coat_flare},58 L45,42 Z" fill="#8c6a3b"/>
    <path d="M21,42 L{19 - coat_flare},56 L{45 + coat_flare},56 L43,42 Z" fill="url(#coatGradUp)"/>
    <!-- Center coat vent crease -->
    <line x1="32" y1="44" x2="32" y2="56" stroke="#684e27" stroke-width="2"/>

    <!-- Left Arm -->
    <g transform="translate(0, {l_arm_dy})">
      <path d="M18,30 Q14,38 16,48 Q18,50 20,48 Q18,40 21,32 Z" fill="#8c6a3b"/>
      <circle cx="18" cy="49" r="3" fill="#7a5c32"/>
    </g>

    <!-- Right Arm -->
    <g transform="translate(0, {r_arm_dy})">
      <path d="M46,30 Q50,38 48,48 Q46,50 44,48 Q46,40 43,32 Z" fill="#8c6a3b"/>
      <circle cx="46" cy="49" r="3" fill="#7a5c32"/>
    </g>

    <!-- Torso Back -->
    <path d="M20,28 L44,28 L45,46 L19,46 Z" fill="url(#coatGradUp)"/>
    <!-- Back Shoulder Yoke & Seams -->
    <path d="M21,33 Q32,36 43,33" stroke="#684e27" stroke-width="2" fill="none"/>

    <!-- Back Belt with loops -->
    <rect x="20" y="43" width="24" height="3" fill="#6d532a"/>
    <rect x="27" y="42" width="2" height="5" fill="#543e1d"/>
    <rect x="35" y="42" width="2" height="5" fill="#543e1d"/>

    <!-- Back of Neck & Collar -->
    <rect x="27" y="24" width="10" height="6" fill="#f0ca9c" rx="2"/>
    <path d="M25,27 Q32,25 39,27 L39,30 Q32,28 25,30 Z" fill="#8c6a3b"/>

    <!-- Back of Fedora -->
    <ellipse cx="32" cy="18" rx="19" ry="6" fill="#2a221b"/>
    <ellipse cx="32" cy="17" rx="18" ry="5" fill="url(#hatGradUp)"/>
    <path d="M22,17 Q23,6 32,7 Q41,6 42,17 Z" fill="url(#hatGradUp)"/>
    <path d="M28,8 Q32,11 36,8" stroke="#1d1611" stroke-width="1.8" fill="none"/>
    <path d="M22,16 Q32,17 42,16 L42,14 Q32,15 22,14 Z" fill="#15171a"/>
  </g>
</svg>"""


def _generate_detective_side_svg(bob_y: int = 0, f_leg_dx: int = 0, f_leg_dy: int = 0,
                                 b_leg_dx: int = 0, b_leg_dy: int = 0,
                                 f_arm_rot: int = 0, b_arm_rot: int = 0,
                                 coat_flare: int = 0) -> str:
    """Generates an SVG for the Detective facing Right (profile view)."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 80" width="64" height="80">
  <defs>
    <linearGradient id="coatGradSide" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8c6a3b"/>
      <stop offset="70%" stop-color="#c9a470"/>
      <stop offset="100%" stop-color="#a88450"/>
    </linearGradient>
    <linearGradient id="hatGradSide" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4a3e35"/>
      <stop offset="100%" stop-color="#2d241d"/>
    </linearGradient>
  </defs>

  <!-- Ground contact shadow -->
  <ellipse cx="33" cy="74" rx="18" ry="5" fill="#000000" opacity="0.35"/>

  <!-- Back Leg (Left Leg from viewer) -->
  <g transform="translate({b_leg_dx}, {b_leg_dy})">
    <rect x="25" y="52" width="7" height="18" rx="2" fill="#20232a"/>
    <ellipse cx="29" cy="71" rx="6" ry="3" fill="#14161a"/>
  </g>

  <!-- Front Leg (Right Leg from viewer) -->
  <g transform="translate({f_leg_dx}, {f_leg_dy})">
    <rect x="31" y="52" width="7" height="18" rx="2" fill="#2c3039"/>
    <ellipse cx="36" cy="71" rx="6" ry="3" fill="#1a1c22"/>
  </g>

  <!-- Back Arm (Swinging) -->
  <g transform="translate(0, {bob_y}) rotate({b_arm_rot}, 28, 32)">
    <path d="M26,30 Q22,40 24,47 Q26,49 28,47 Q28,40 30,32 Z" fill="#826235"/>
    <circle cx="25" cy="48" r="3" fill="#c0966a"/>
  </g>

  <!-- Upper Body & Profile Head -->
  <g transform="translate(0, {bob_y})">
    <!-- Trench Coat Silhouette & Back Tail Sway -->
    <path d="M22,42 L{18 - coat_flare},58 L39,58 L42,42 Z" fill="#8c6a3b"/>
    <path d="M24,42 L{20 - coat_flare},56 L38,56 L41,42 Z" fill="url(#coatGradSide)"/>

    <!-- Torso Profile -->
    <path d="M24,28 L40,28 L42,46 L24,46 Z" fill="url(#coatGradSide)"/>

    <!-- Belt & Holster/Pocket -->
    <rect x="23" y="43" width="19" height="3" fill="#6d532a"/>
    <rect x="38" y="42" width="3" height="5" fill="#dfb15b" rx="0.5"/>

    <!-- Collar & Profile Tie -->
    <polygon points="36,28 41,33 39,28" fill="#e8edf2"/>
    <polygon points="39,30 42,35 40,38 38,33" fill="#a82323"/>

    <!-- Front Arm (Swinging) -->
    <g transform="rotate({f_arm_rot}, 34, 32)">
      <path d="M31,30 Q36,38 38,47 Q40,49 42,47 Q40,38 36,31 Z" fill="url(#coatGradSide)"/>
      <circle cx="40" cy="48" r="3" fill="#d2ab82"/>
    </g>

    <!-- Profile Neck & Face -->
    <ellipse cx="33" cy="22" rx="8" ry="8" fill="#f0ca9c"/>
    <!-- Detective Nose & Chin in profile -->
    <path d="M38,20 L43,23 L39,26 L38,28" stroke="#deb485" stroke-width="1.5" fill="#f0ca9c"/>
    <!-- Eye in profile -->
    <ellipse cx="37" cy="22" rx="1.5" ry="2" fill="#24211d"/>
    <circle cx="37.5" cy="21.5" r="0.6" fill="#ffffff"/>

    <!-- Profile Fedora -->
    <!-- Fedora Brim (Angled forward) -->
    <ellipse cx="34" cy="18" rx="18" ry="5.5" fill="#2a221b" transform="rotate(-4, 34, 18)"/>
    <ellipse cx="34" cy="17" rx="17" ry="4.5" fill="url(#hatGradSide)" transform="rotate(-4, 34, 17)"/>
    <!-- Crown -->
    <path d="M24,16 Q27,6 35,7 Q41,7 42,16 Z" fill="url(#hatGradSide)"/>
    <path d="M29,8 Q34,11 38,8" stroke="#1d1611" stroke-width="1.8" fill="none"/>
    <!-- Hat band -->
    <path d="M24,16 Q33,17 42,15 L42,13 Q33,15 24,14 Z" fill="#15171a"/>
  </g>
</svg>"""


def get_character_animations() -> dict:
    """
    Renders and returns all directional animations for the Detective:
    'down', 'up', 'right', 'left' containing 'idle' and 'walk' frame lists.
    """
    # Down animations (Facing player)
    down_idle = [
        render_svg(_generate_detective_down_svg(bob_y=0)),
        render_svg(_generate_detective_down_svg(bob_y=1)),
    ]
    down_walk = [
        render_svg(_generate_detective_down_svg(bob_y=0, l_leg_dx=-1, l_leg_dy=-4, r_leg_dx=1, r_leg_dy=3, l_arm_dy=2, r_arm_dy=-2, coat_flare=2)),
        render_svg(_generate_detective_down_svg(bob_y=1, l_leg_dx=0, l_leg_dy=0, r_leg_dx=0, r_leg_dy=0, l_arm_dy=0, r_arm_dy=0, coat_flare=0)),
        render_svg(_generate_detective_down_svg(bob_y=0, l_leg_dx=1, l_leg_dy=3, r_leg_dx=-1, r_leg_dy=-4, l_arm_dy=-2, r_arm_dy=2, coat_flare=-2)),
        render_svg(_generate_detective_down_svg(bob_y=1, l_leg_dx=0, l_leg_dy=0, r_leg_dx=0, r_leg_dy=0, l_arm_dy=0, r_arm_dy=0, coat_flare=0)),
    ]

    # Up animations (Facing away)
    up_idle = [
        render_svg(_generate_detective_up_svg(bob_y=0)),
        render_svg(_generate_detective_up_svg(bob_y=1)),
    ]
    up_walk = [
        render_svg(_generate_detective_up_svg(bob_y=0, l_leg_dx=-1, l_leg_dy=-4, r_leg_dx=1, r_leg_dy=3, l_arm_dy=2, r_arm_dy=-2, coat_flare=2)),
        render_svg(_generate_detective_up_svg(bob_y=1, l_leg_dx=0, l_leg_dy=0, r_leg_dx=0, r_leg_dy=0, l_arm_dy=0, r_arm_dy=0, coat_flare=0)),
        render_svg(_generate_detective_up_svg(bob_y=0, l_leg_dx=1, l_leg_dy=3, r_leg_dx=-1, r_leg_dy=-4, l_arm_dy=-2, r_arm_dy=2, coat_flare=-2)),
        render_svg(_generate_detective_up_svg(bob_y=1, l_leg_dx=0, l_leg_dy=0, r_leg_dx=0, r_leg_dy=0, l_arm_dy=0, r_arm_dy=0, coat_flare=0)),
    ]

    # Right animations (Profile)
    right_idle = [
        render_svg(_generate_detective_side_svg(bob_y=0)),
        render_svg(_generate_detective_side_svg(bob_y=1)),
    ]
    right_walk = [
        render_svg(_generate_detective_side_svg(bob_y=0, f_leg_dx=4, f_leg_dy=-3, b_leg_dx=-4, b_leg_dy=3, f_arm_rot=-14, b_arm_rot=14, coat_flare=3)),
        render_svg(_generate_detective_side_svg(bob_y=1, f_leg_dx=0, f_leg_dy=0, b_leg_dx=0, b_leg_dy=0, f_arm_rot=0, b_arm_rot=0, coat_flare=0)),
        render_svg(_generate_detective_side_svg(bob_y=0, f_leg_dx=-4, f_leg_dy=3, b_leg_dx=4, b_leg_dy=-3, f_arm_rot=14, b_arm_rot=-14, coat_flare=1)),
        render_svg(_generate_detective_side_svg(bob_y=1, f_leg_dx=0, f_leg_dy=0, b_leg_dx=0, b_leg_dy=0, f_arm_rot=0, b_arm_rot=0, coat_flare=0)),
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


# ---------------------------------------------------------------------------
# Room Furniture & Environment SVGs
# ---------------------------------------------------------------------------

SVG_DETECTIVE_DESK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 120" width="180" height="120">
  <defs>
    <!-- Desk Wood Gradients -->
    <linearGradient id="deskTop" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6e3e26"/>
      <stop offset="40%" stop-color="#552c1a"/>
      <stop offset="100%" stop-color="#412113"/>
    </linearGradient>
    <linearGradient id="deskFront" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3c1e11"/>
      <stop offset="100%" stop-color="#24120a"/>
    </linearGradient>
    <linearGradient id="lampShade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0f5228"/>
      <stop offset="50%" stop-color="#1f8745"/>
      <stop offset="100%" stop-color="#0c4320"/>
    </linearGradient>
    <radialGradient id="lampGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffe699" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#ffe699" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Floor drop shadow under desk -->
  <rect x="6" y="86" width="168" height="28" rx="6" fill="#000000" opacity="0.4"/>

  <!-- Left & Right Pedestal Cabinets -->
  <rect x="14" y="52" width="44" height="54" rx="2" fill="url(#deskFront)"/>
  <rect x="122" y="52" width="44" height="54" rx="2" fill="url(#deskFront)"/>
  <!-- Middle Kneehole Backboard -->
  <rect x="58" y="54" width="64" height="38" fill="#1f1009"/>

  <!-- Left Drawers & Brass Handles -->
  <rect x="18" y="56" width="36" height="13" rx="1" fill="#4a2515" stroke="#2c1409" stroke-width="1"/>
  <rect x="31" y="61" width="10" height="3" rx="1" fill="#dfb15b"/>
  <rect x="18" y="72" width="36" height="13" rx="1" fill="#4a2515" stroke="#2c1409" stroke-width="1"/>
  <rect x="31" y="77" width="10" height="3" rx="1" fill="#dfb15b"/>
  <rect x="18" y="88" width="36" height="14" rx="1" fill="#4a2515" stroke="#2c1409" stroke-width="1"/>
  <rect x="31" y="93" width="10" height="3" rx="1" fill="#dfb15b"/>

  <!-- Right Drawers & Brass Handles -->
  <rect x="126" y="56" width="36" height="13" rx="1" fill="#4a2515" stroke="#2c1409" stroke-width="1"/>
  <rect x="139" y="61" width="10" height="3" rx="1" fill="#dfb15b"/>
  <rect x="126" y="72" width="36" height="13" rx="1" fill="#4a2515" stroke="#2c1409" stroke-width="1"/>
  <rect x="139" y="77" width="10" height="3" rx="1" fill="#dfb15b"/>
  <rect x="126" y="88" width="36" height="14" rx="1" fill="#4a2515" stroke="#2c1409" stroke-width="1"/>
  <rect x="139" y="93" width="10" height="3" rx="1" fill="#dfb15b"/>

  <!-- Main Polished Desk Top -->
  <polygon points="10,50 170,50 162,18 18,18" fill="url(#deskTop)"/>
  <!-- Polished Top Edge Rim -->
  <line x1="10" y1="50" x2="170" y2="50" stroke="#844e31" stroke-width="3"/>
  <line x1="18" y1="18" x2="162" y2="18" stroke="#482515" stroke-width="1.5"/>

  <!-- Desk Inlay Blotter (Dark green leather mat) -->
  <polygon points="46,47 134,47 130,24 50,24" fill="#1b2e23" stroke="#dfb15b" stroke-width="0.8"/>

  <!-- Open Case File & Manila Folder -->
  <polygon points="56,43 88,41 85,27 53,29" fill="#d9be8b"/>
  <polygon points="58,41 86,39 84,29 56,31" fill="#f0e2c8"/>
  <!-- Paper text lines -->
  <line x1="60" y1="33" x2="80" y2="32" stroke="#524a3c" stroke-width="1"/>
  <line x1="60" y1="36" x2="78" y2="35" stroke="#524a3c" stroke-width="1"/>
  <line x1="60" y1="39" x2="74" y2="38" stroke="#a33636" stroke-width="1"/>

  <!-- Coffee Mug & Coaster -->
  <ellipse cx="140" cy="40" rx="6" ry="3.5" fill="#e0e0e0"/>
  <ellipse cx="140" cy="38" rx="5" ry="2.5" fill="#3c2214"/>

  <!-- Antique Banker's Lamp (Emerald Glass & Brass) -->
  <!-- Ambient glow circle -->
  <circle cx="28" cy="28" r="28" fill="url(#lampGlow)"/>
  <!-- Brass base & neck -->
  <ellipse cx="28" cy="38" rx="6" ry="3" fill="#dfb15b"/>
  <path d="M28,38 L28,26 Q28,21 32,21" stroke="#dfb15b" stroke-width="2.5" fill="none"/>
  <!-- Emerald green curved glass shade -->
  <rect x="20" y="16" width="22" height="9" rx="4" fill="url(#lampShade)"/>
  <ellipse cx="31" cy="25" rx="9" ry="2.5" fill="#6fe398" opacity="0.6"/>
</svg>"""


SVG_LEATHER_SOFA = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 100" width="170" height="100">
  <defs>
    <linearGradient id="sofaLeather" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6e282c"/>
      <stop offset="50%" stop-color="#4f1b1e"/>
      <stop offset="100%" stop-color="#351114"/>
    </linearGradient>
    <linearGradient id="sofaCushion" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5c2024"/>
      <stop offset="100%" stop-color="#3d1416"/>
    </linearGradient>
  </defs>

  <!-- Floor drop shadow -->
  <rect x="8" y="70" width="154" height="22" rx="8" fill="#000000" opacity="0.4"/>

  <!-- Wooden Turned Bun Feet -->
  <ellipse cx="18" cy="84" rx="6" ry="4" fill="#24140b"/>
  <ellipse cx="152" cy="84" rx="6" ry="4" fill="#24140b"/>
  <ellipse cx="46" cy="82" rx="5" ry="3" fill="#1c0f08"/>
  <ellipse cx="124" cy="82" rx="5" ry="3" fill="#1c0f08"/>

  <!-- Sofa Backrest (Tufted Chesterfield) -->
  <rect x="16" y="18" width="138" height="42" rx="10" fill="url(#sofaLeather)"/>
  
  <!-- Diamond Tufting Buttons & Creases -->
  <g fill="#240c0e" opacity="0.8">
    <circle cx="36" cy="30" r="2.2"/><circle cx="58" cy="30" r="2.2"/>
    <circle cx="85" cy="30" r="2.2"/><circle cx="112" cy="30" r="2.2"/><circle cx="134" cy="30" r="2.2"/>
    <circle cx="47" cy="42" r="2.2"/><circle cx="71" cy="42" r="2.2"/>
    <circle cx="99" cy="42" r="2.2"/><circle cx="123" cy="42" r="2.2"/>
  </g>
  <path d="M36,30 L47,42 L58,30 L71,42 L85,30 L99,42 L112,30 L123,42 L134,30" 
        stroke="#240c0e" stroke-width="1.2" fill="none" opacity="0.6"/>

  <!-- Main Seat Base & Brass Tack Line -->
  <rect x="14" y="60" width="142" height="18" rx="4" fill="#3d1416"/>
  <!-- Brass nailhead trim -->
  <line x1="20" y1="74" x2="150" y2="74" stroke="#dfb15b" stroke-width="1.5" stroke-dasharray="2,3"/>

  <!-- Left Rolled Armrest -->
  <ellipse cx="20" cy="52" rx="12" ry="18" fill="url(#sofaLeather)"/>
  <ellipse cx="20" cy="52" rx="9" ry="14" fill="#6e282c"/>
  <circle cx="20" cy="52" r="3" fill="#dfb15b"/>

  <!-- Right Rolled Armrest -->
  <ellipse cx="150" cy="52" rx="12" ry="18" fill="url(#sofaLeather)"/>
  <ellipse cx="150" cy="52" rx="9" ry="14" fill="#6e282c"/>
  <circle cx="150" cy="52" r="3" fill="#dfb15b"/>

  <!-- Plump Seat Cushions (3 cushions) -->
  <rect x="30" y="48" width="34" height="20" rx="4" fill="url(#sofaCushion)" stroke="#2b0d0f" stroke-width="1.2"/>
  <rect x="68" y="48" width="34" height="20" rx="4" fill="url(#sofaCushion)" stroke="#2b0d0f" stroke-width="1.2"/>
  <rect x="106" y="48" width="34" height="20" rx="4" fill="url(#sofaCushion)" stroke="#2b0d0f" stroke-width="1.2"/>
</svg>"""


SVG_FILING_CABINET = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 96" width="64" height="96">
  <defs>
    <linearGradient id="metalCab" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#3b4442"/>
      <stop offset="50%" stop-color="#4e5b58"/>
      <stop offset="100%" stop-color="#323a38"/>
    </linearGradient>
    <linearGradient id="drawerFace" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#52605d"/>
      <stop offset="100%" stop-color="#3b4543"/>
    </linearGradient>
  </defs>

  <!-- Ground drop shadow -->
  <rect x="4" y="86" width="56" height="8" rx="3" fill="#000000" opacity="0.4"/>

  <!-- Cabinet Shell -->
  <rect x="6" y="6" width="52" height="84" rx="2" fill="url(#metalCab)" stroke="#222826" stroke-width="1.5"/>

  <!-- Drawer 1 (Top) -->
  <rect x="9" y="10" width="46" height="17" rx="1.5" fill="url(#drawerFace)" stroke="#29302e" stroke-width="1"/>
  <!-- Brass Label Card Slot & Handle -->
  <rect x="24" y="13" width="16" height="5" fill="#dfb15b" rx="0.5"/>
  <rect x="26" y="14" width="12" height="3" fill="#f4ebd9"/>
  <rect x="25" y="21" width="14" height="3" fill="#202524" rx="1"/>

  <!-- Drawer 2 -->
  <rect x="9" y="29" width="46" height="17" rx="1.5" fill="url(#drawerFace)" stroke="#29302e" stroke-width="1"/>
  <rect x="24" y="32" width="16" height="5" fill="#dfb15b" rx="0.5"/>
  <rect x="26" y="33" width="12" height="3" fill="#f4ebd9"/>
  <rect x="25" y="40" width="14" height="3" fill="#202524" rx="1"/>

  <!-- Drawer 3 -->
  <rect x="9" y="48" width="46" height="17" rx="1.5" fill="url(#drawerFace)" stroke="#29302e" stroke-width="1"/>
  <rect x="24" y="51" width="16" height="5" fill="#dfb15b" rx="0.5"/>
  <rect x="26" y="52" width="12" height="3" fill="#f4ebd9"/>
  <rect x="25" y="59" width="14" height="3" fill="#202524" rx="1"/>

  <!-- Drawer 4 (Bottom) -->
  <rect x="9" y="67" width="46" height="17" rx="1.5" fill="url(#drawerFace)" stroke="#29302e" stroke-width="1"/>
  <rect x="24" y="70" width="16" height="5" fill="#dfb15b" rx="0.5"/>
  <rect x="26" y="71" width="12" height="3" fill="#f4ebd9"/>
  <rect x="25" y="78" width="14" height="3" fill="#202524" rx="1"/>

  <!-- Placed file folder on top -->
  <polygon points="12,5 34,4 32,1 16,1" fill="#c4a572"/>
  <polygon points="13,5 33,5 31,3 17,3" fill="#e8d3b0"/>
</svg>"""


SVG_EVIDENCE_BOARD = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 95" width="170" height="95">
  <defs>
    <linearGradient id="corkGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#b68b59"/>
      <stop offset="100%" stop-color="#9a6e3e"/>
    </linearGradient>
  </defs>

  <!-- Wooden Frame Outer -->
  <rect x="2" y="2" width="166" height="91" rx="3" fill="#432814" stroke="#251408" stroke-width="2"/>
  <rect x="7" y="7" width="156" height="81" fill="#5c381c"/>
  <!-- Cork Board Interior -->
  <rect x="10" y="10" width="150" height="75" fill="url(#corkGrad)"/>

  <!-- Pinned Evidence Items -->
  <!-- Photo 1: Crime Scene Warehouse (Left) -->
  <g transform="rotate(-5, 30, 32)">
    <rect x="18" y="18" width="28" height="30" fill="#f4ebd9" stroke="#b0a28f" stroke-width="0.8"/>
    <rect x="20" y="21" width="24" height="20" fill="#2b313a"/>
    <path d="M22,37 L29,29 L35,36 L39,32 L42,38 Z" fill="#636e7b"/>
    <!-- Red Pin -->
    <circle cx="32" cy="19" r="2.2" fill="#d62828"/>
  </g>

  <!-- Photo 2: Suspect Silhouette (Right) -->
  <g transform="rotate(4, 135, 30)">
    <rect x="122" y="16" width="28" height="30" fill="#f4ebd9" stroke="#b0a28f" stroke-width="0.8"/>
    <rect x="124" y="19" width="24" height="20" fill="#22252a"/>
    <circle cx="136" cy="27" r="4.5" fill="#757d88"/>
    <path d="M128,39 Q136,33 144,39 Z" fill="#757d88"/>
    <!-- Yellow Pin -->
    <circle cx="136" cy="17" r="2.2" fill="#dfb15b"/>
  </g>

  <!-- Central Evidence: The Mysterious Recurring Symbol! -->
  <g transform="translate(68, 22)">
    <rect x="0" y="0" width="34" height="36" fill="#fdfbf7" stroke="#9e3a3a" stroke-width="1"/>
    <!-- Ancient Spiral Symbol in Crimson Ink -->
    <circle cx="17" cy="18" r="11" stroke="#b71c1c" stroke-width="1.8" fill="none"/>
    <path d="M17,11 Q24,11 24,18 Q24,24 17,24 Q12,24 12,18 Q12,14 17,14" 
          stroke="#b71c1c" stroke-width="2" fill="none"/>
    <circle cx="17" cy="18" r="2" fill="#b71c1c"/>
    <!-- Red Pin -->
    <circle cx="17" cy="3" r="2.5" fill="#d62828"/>
  </g>

  <!-- Sticky Notes (Yellow & Blue) -->
  <rect x="22" y="56" width="24" height="20" fill="#ffeb3b" stroke="#fbc02d" stroke-width="0.6"/>
  <line x1="25" y1="62" x2="42" y2="62" stroke="#5d4037" stroke-width="1"/>
  <line x1="25" y1="67" x2="38" y2="67" stroke="#5d4037" stroke-width="1"/>
  <circle cx="34" cy="57" r="1.8" fill="#1565c0"/>

  <rect x="115" y="54" width="26" height="22" fill="#80d8ff" stroke="#40c4ff" stroke-width="0.6"/>
  <line x1="118" y1="60" x2="137" y2="60" stroke="#004d40" stroke-width="1"/>
  <line x1="118" y1="65" x2="132" y2="65" stroke="#004d40" stroke-width="1"/>
  <circle cx="128" cy="55" r="1.8" fill="#d62828"/>

  <!-- Newspaper Clipping -->
  <rect x="64" y="62" width="42" height="19" fill="#eceff1" stroke="#cfd8dc" stroke-width="0.6"/>
  <rect x="67" y="65" width="36" height="3" fill="#263238"/>
  <line x1="67" y1="71" x2="103" y2="71" stroke="#546e7a" stroke-width="0.8"/>
  <line x1="67" y1="74" x2="98" y2="74" stroke="#546e7a" stroke-width="0.8"/>
  <circle cx="85" cy="63" r="1.8" fill="#d62828"/>

  <!-- Red String Yarn Connecting Evidence (Tension lines) -->
  <line x1="32" y1="19" x2="85" y2="25" stroke="#d62828" stroke-width="1.8" opacity="0.9"/>
  <line x1="85" y1="25" x2="136" y2="17" stroke="#d62828" stroke-width="1.8" opacity="0.9"/>
  <line x1="85" y1="25" x2="34" y2="57" stroke="#d62828" stroke-width="1.5" opacity="0.85"/>
  <line x1="85" y1="25" x2="128" y2="55" stroke="#d62828" stroke-width="1.5" opacity="0.85"/>
  <line x1="85" y1="25" x2="85" y2="63" stroke="#d62828" stroke-width="1.5" opacity="0.85"/>
</svg>"""


SVG_BOOKSHELF = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 84 130" width="84" height="130">
  <defs>
    <linearGradient id="shelfWood" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#462412"/>
      <stop offset="50%" stop-color="#5a301a"/>
      <stop offset="100%" stop-color="#3c1d0d"/>
    </linearGradient>
  </defs>

  <!-- Floor shadow -->
  <rect x="4" y="122" width="76" height="8" rx="3" fill="#000000" opacity="0.4"/>

  <!-- Bookcase Frame -->
  <rect x="6" y="6" width="72" height="118" rx="2" fill="url(#shelfWood)" stroke="#221107" stroke-width="1.5"/>
  <rect x="10" y="10" width="64" height="110" fill="#261207"/>

  <!-- Shelves -->
  <rect x="10" y="44" width="64" height="5" fill="#4d2814"/>
  <rect x="10" y="80" width="64" height="5" fill="#4d2814"/>
  <rect x="10" y="116" width="64" height="5" fill="#4d2814"/>

  <!-- Shelf 1 (Top Shelf Books) -->
  <rect x="14" y="16" width="8" height="28" rx="1" fill="#8c2323"/>
  <rect x="23" y="18" width="7" height="26" rx="1" fill="#1e3a5f"/>
  <rect x="31" y="14" width="10" height="30" rx="1" fill="#2d5234"/>
  <line x1="33" y1="18" x2="39" y2="18" stroke="#dfb15b" stroke-width="1"/>
  <rect x="42" y="20" width="8" height="24" rx="1" fill="#6d4c2b"/>
  <rect x="51" y="17" width="9" height="27" rx="1" fill="#a47535"/>
  <rect x="61" y="19" width="8" height="25" rx="1" fill="#3a3845"/>

  <!-- Shelf 2 (Middle Shelf Books & Dossiers) -->
  <rect x="14" y="52" width="11" height="28" rx="1" fill="#1b2a4a"/>
  <line x1="16" y1="56" x2="23" y2="56" stroke="#dfb15b" stroke-width="1"/>
  <rect x="26" y="55" width="8" height="25" rx="1" fill="#6b2b2b"/>
  <rect x="35" y="50" width="9" height="30" rx="1" fill="#846543"/>
  <!-- Slanted book -->
  <g transform="rotate(12, 50, 78)">
    <rect x="45" y="52" width="8" height="27" rx="1" fill="#2f4839"/>
  </g>
  <rect x="59" y="54" width="11" height="26" rx="1" fill="#40394f"/>

  <!-- Shelf 3 (Heavy Archive Ledger Binders) -->
  <rect x="14" y="88" width="12" height="28" rx="1" fill="#362215"/>
  <circle cx="20" cy="98" r="2" fill="#dfb15b"/>
  <rect x="27" y="88" width="12" height="28" rx="1" fill="#1e2d24"/>
  <circle cx="33" cy="98" r="2" fill="#dfb15b"/>
  <rect x="40" y="88" width="12" height="28" rx="1" fill="#471d23"/>
  <circle cx="46" cy="98" r="2" fill="#dfb15b"/>
  <!-- Box files stacked horizontally -->
  <rect x="53" y="104" width="18" height="6" rx="1" fill="#c4a572"/>
  <rect x="54" y="97" width="17" height="6" rx="1" fill="#b09260"/>
</svg>"""


SVG_NOIR_WINDOW = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 110" width="80" height="110">
  <defs>
    <!-- Night Sky Gradient with Moon Hue -->
    <linearGradient id="nightSky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0c1322"/>
      <stop offset="60%" stop-color="#14213d"/>
      <stop offset="100%" stop-color="#1f3152"/>
    </linearGradient>
  </defs>

  <!-- Arched Window Frame Outer -->
  <path d="M6,36 Q6,6 40,6 Q74,6 74,36 L74,106 L6,106 Z" fill="#222830" stroke="#121519" stroke-width="2"/>
  <!-- Window Glass Pane -->
  <path d="M10,38 Q10,10 40,10 Q70,10 70,38 L70,102 L10,102 Z" fill="url(#nightSky)"/>

  <!-- Distant crescent moon & stars -->
  <circle cx="54" cy="24" r="5" fill="#f4ebd9" opacity="0.8"/>
  <circle cx="56" cy="22" r="4.5" fill="#14213d"/>
  <circle cx="24" cy="26" r="0.8" fill="#ffffff" opacity="0.7"/>
  <circle cx="36" cy="18" r="0.8" fill="#ffffff" opacity="0.6"/>

  <!-- Window Muntin Mullions -->
  <line x1="40" y1="10" x2="40" y2="102" stroke="#2a323c" stroke-width="3"/>
  <line x1="10" y1="56" x2="70" y2="56" stroke="#2a323c" stroke-width="3"/>

  <!-- Venetian Wooden Blinds (Noir Slats) -->
  <g stroke="#3a2f26" stroke-width="2.5" opacity="0.85">
    <line x1="11" y1="42" x2="69" y2="42"/>
    <line x1="11" y1="48" x2="69" y2="48"/>
    <line x1="11" y1="64" x2="69" y2="64"/>
    <line x1="11" y1="70" x2="69" y2="70"/>
    <line x1="11" y1="76" x2="69" y2="76"/>
    <line x1="11" y1="82" x2="69" y2="82"/>
    <line x1="11" y1="88" x2="69" y2="88"/>
    <line x1="11" y1="94" x2="69" y2="94"/>
  </g>
  <!-- Blind pull cords -->
  <line x1="22" y1="36" x2="22" y2="98" stroke="#dfb15b" stroke-width="1"/>
  <line x1="58" y1="36" x2="58" y2="98" stroke="#dfb15b" stroke-width="1"/>
  <circle cx="22" cy="99" r="1.5" fill="#dfb15b"/>
  <circle cx="58" cy="99" r="1.5" fill="#dfb15b"/>
</svg>"""


SVG_VINTAGE_RUG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 130" width="220" height="130">
  <defs>
    <linearGradient id="rugBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5c1920"/>
      <stop offset="100%" stop-color="#421217"/>
    </linearGradient>
  </defs>

  <!-- Fringe Tassels (Left & Right) -->
  <line x1="4" y1="12" x2="4" y2="118" stroke="#e6d5b8" stroke-width="2" stroke-dasharray="2,2"/>
  <line x1="216" y1="12" x2="216" y2="118" stroke="#e6d5b8" stroke-width="2" stroke-dasharray="2,2"/>

  <!-- Rug Main Body -->
  <rect x="6" y="10" width="208" height="110" rx="3" fill="url(#rugBase)"/>

  <!-- Outer Navy Border -->
  <rect x="12" y="16" width="196" height="98" rx="2" fill="none" stroke="#1c2838" stroke-width="7"/>
  <!-- Gold Accent Trim -->
  <rect x="16" y="20" width="188" height="90" fill="none" stroke="#cca458" stroke-width="1.5"/>

  <!-- Inner Field Background -->
  <rect x="22" y="26" width="176" height="78" fill="#50161c"/>

  <!-- Central Persian Medallion -->
  <polygon points="110,32 150,65 110,98 70,65" fill="#1c2838" stroke="#cca458" stroke-width="2"/>
  <circle cx="110" cy="65" r="16" fill="#751f28" stroke="#cca458" stroke-width="1.5"/>
  <circle cx="110" cy="65" r="7" fill="#cca458"/>

  <!-- Corner Quarter-Medallions -->
  <polygon points="22,26 44,26 22,48" fill="#1c2838" stroke="#cca458" stroke-width="1"/>
  <polygon points="198,26 176,26 198,48" fill="#1c2838" stroke="#cca458" stroke-width="1"/>
  <polygon points="22,104 44,104 22,82" fill="#1c2838" stroke="#cca458" stroke-width="1"/>
  <polygon points="198,104 176,104 198,82" fill="#1c2838" stroke="#cca458" stroke-width="1"/>
</svg>"""


SVG_POTTED_PLANT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 75" width="60" height="75">
  <defs>
    <linearGradient id="potGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#994c30"/>
      <stop offset="50%" stop-color="#bd6646"/>
      <stop offset="100%" stop-color="#7e3b23"/>
    </linearGradient>
  </defs>

  <!-- Drop Shadow -->
  <ellipse cx="30" cy="71" rx="16" ry="4" fill="#000000" opacity="0.35"/>

  <!-- Terracotta Clay Pot -->
  <polygon points="18,46 42,46 38,69 22,69" fill="url(#potGrad)"/>
  <rect x="16" y="42" width="28" height="6" rx="2" fill="#bd6646" stroke="#7e3b23" stroke-width="1"/>
  <ellipse cx="30" cy="45" rx="12" ry="2.5" fill="#32221b"/>

  <!-- Lush Monstera / Plant Leaves -->
  <!-- Leaf 1 (Left low) -->
  <path d="M28,43 Q12,40 10,28 Q18,22 28,36" fill="#1e5c2e"/>
  <!-- Leaf 2 (Right low) -->
  <path d="M32,43 Q48,40 50,28 Q42,22 32,36" fill="#256b37"/>
  <!-- Leaf 3 (Center High) -->
  <path d="M30,38 Q30,12 24,6 Q36,8 32,32" fill="#2d7e42"/>
  <!-- Leaf 4 (Upper Left) -->
  <path d="M29,35 Q14,20 16,10 Q28,14 30,30" fill="#38944f"/>
  <!-- Leaf 5 (Upper Right) -->
  <path d="M31,35 Q46,20 44,10 Q32,14 30,30" fill="#2c8041"/>

  <!-- Leaf Vein Highlights -->
  <path d="M24,6 Q30,22 30,38" stroke="#48ad63" stroke-width="1" fill="none"/>
  <path d="M16,10 Q22,22 29,35" stroke="#48ad63" stroke-width="0.8" fill="none"/>
  <path d="M44,10 Q38,22 31,35" stroke="#3fa15a" stroke-width="0.8" fill="none"/>
</svg>"""


SVG_WALL_SCONCE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 50" width="40" height="50">
  <defs>
    <radialGradient id="lampGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffe49e" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="#ffb74d" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#ff9800" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Ambient Light Halo -->
  <circle cx="20" cy="22" r="18" fill="url(#lampGlow)"/>

  <!-- Wall Brass Plate -->
  <rect x="17" y="14" width="6" height="20" rx="1.5" fill="#caa455" stroke="#7a5f25" stroke-width="1"/>
  <!-- Curved Arm -->
  <path d="M20,28 Q20,36 12,32" stroke="#caa455" stroke-width="2.5" fill="none"/>

  <!-- Frosted Amber Glass Shade -->
  <polygon points="12,14 28,14 25,28 15,28" fill="#ffe082" stroke="#ffb300" stroke-width="1"/>
  <ellipse cx="20" cy="14" rx="8" ry="3" fill="#fff9c4"/>
  <ellipse cx="20" cy="28" rx="5" ry="2" fill="#ffca28"/>
</svg>"""


SVG_INTERACTION_BADGE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 54 28" width="54" height="28">
  <defs>
    <linearGradient id="badgeBg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2a2e38"/>
      <stop offset="100%" stop-color="#14171d"/>
    </linearGradient>
  </defs>

  <!-- Glow Drop Shadow -->
  <rect x="2" y="2" width="50" height="24" rx="6" fill="#dfb15b" opacity="0.3"/>
  <!-- Badge Base -->
  <rect x="3" y="3" width="48" height="22" rx="5" fill="url(#badgeBg)" stroke="#dfb15b" stroke-width="1.5"/>

  <!-- Magnifying Glass Icon -->
  <circle cx="15" cy="13" r="5" stroke="#dfb15b" stroke-width="1.8" fill="none"/>
  <line x1="19" y1="17" x2="23" y2="21" stroke="#dfb15b" stroke-width="2.2" stroke-linecap="round"/>

  <!-- Keycap [E] Graphic Shapes (avoiding unsupported text tags in nanosvg) -->
  <rect x="27" y="7" width="18" height="14" rx="3" fill="#dfb15b"/>
  <rect x="28" y="8" width="16" height="12" rx="2" fill="#1b1e24"/>
  <!-- Letter 'E' formed by vector paths -->
  <path d="M33,11 L39,11 L39,13 L35,13 L35,14 L38.5,14 L38.5,16 L35,16 L35,17 L39,17 L39,19 L33,19 Z" fill="#dfb15b"/>
</svg>"""


def get_room_objects() -> dict:
    """Renders and returns all cached Pygame surfaces for the room furniture."""
    return {
        'desk': render_svg(SVG_DETECTIVE_DESK, 180, 120),
        'sofa': render_svg(SVG_LEATHER_SOFA, 170, 100),
        'filing_cabinet': render_svg(SVG_FILING_CABINET, 64, 96),
        'evidence_board': render_svg(SVG_EVIDENCE_BOARD, 170, 95),
        'bookshelf': render_svg(SVG_BOOKSHELF, 84, 130),
        'window': render_svg(SVG_NOIR_WINDOW, 80, 110),
        'rug': render_svg(SVG_VINTAGE_RUG, 220, 130),
        'plant': render_svg(SVG_POTTED_PLANT, 60, 75),
        'sconce': render_svg(SVG_WALL_SCONCE, 40, 50),
        'inspect_badge': render_svg(SVG_INTERACTION_BADGE, 54, 28),
    }
