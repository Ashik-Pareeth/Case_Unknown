"""NPC character designs for Case Unknown.

Three NPC types accessible via get_npc_animations(palette_index):

  0 – Mob Grunt        : user-designed mob silhouette (charcoal coat tint)
  1 – The Fixer        : inner-room schemer, detective rig, navy suit + cigar
  2 – Mob Grunt Alt    : same mob design, blue-black coat tint

The Mob Grunt is drawn from scratch using custom SVGs that match the
reference artwork supplied by the user:  tall top-hat, wide brim, huge body,
full balaclava with diamond-shaped eye openings, dark coat + waistcoat,
gloves, and boots. All four walk directions are generated; left is a
horizontal flip of the right (profile) frames.
"""

from dataclasses import replace
from functools import lru_cache

import pygame

from assets.characters import DETECTIVE_PALETTE, get_character_animations
from assets.renderer import render_svg


# =============================================================================
# THE FIXER  (palette_index = 1) – detective rig, navy suit, moustache, cigar
# =============================================================================

FIXER_PALETTE = replace(
    DETECTIVE_PALETTE,
    coat_light="#2a3550", coat_mid="#1e2840", coat_dark="#162030",
    coat_deep="#101828", coat_shadow="#0c1220", coat_line_shadow="#0c1220",
    coat_crease="#080e18", coat_lapel_l="#162030", coat_lapel_r="#101828",
    coat_up_mid="#222e48", coat_side_arm="#182438", coat_side_light="#2a3550",
    coat_side_dark="#101828", coat_side_back_dark="#0c1220",
    coat_lapel_side_base="#162030", coat_lapel_side_light="#2a3550",
    belt="#1a1430", belt_dark="#120e22", belt_loop="#0c0a1a",
    tie_red="#b8c0cc", tie_highlight="#d0d8e4",
    skin_light="#f0d8c0", skin_mid="#dcc0a0", skin_dark="#c8a880",
    skin_shadow="#b89060", skin_neck="#d0b080", skin_side_base="#c8a870",
    skin_side_mid="#dcc0a0", skin_side_light="#ecd8b8",
    cheek_flush="#dca888", cheek_flush_side="#d4a080",
    nose_base="#c09060", nose_dark="#9e7040", nostril_shadow="#8a5e30",
    lip_upper="#a05848", lip_lower="#b86858",
    lip_side_upper="#905040", lip_side_lower="#a86050", lip_corner="#784038",
    jaw_line="#b88858",
    iris_mid="#4a6080", iris_deep="#283848", iris_dark="#182030",
    iris_side_light="#586880", iris_side_mid="#304050", iris_side_dark="#1a2838",
    eye_white="#e8ecf0", eye_side_white="#ecf0f4", eye_pupil="#0a0e12",
    eye_liner="#1a1008", eye_shadow="#c0a878", eye_side_liner="#140c06",
    hair_dark="#060604", hair_main="#100e0c", hair_highlight="#1c1a18",
    hair_brow_front="#0a0806", brow_front="#100c08", brow_side="#0e0b04",
    pants_left="#182030", pants_right="#141c28",
    pants_side_back="#101820", pants_side_front="#161e2a",
    brass="#e0b840", brass_dark="#c09828", brass_gold="#d4aa30",
    brass_side_gold="#cca028", brass_border="#a88018",
    shirt_white="#eef2f6", shirt_shadow="#e0e6ec", shirt_side_shadow="#d4dce4",
    shoe_black="#0e1014", shoe_leather="#181c22", shoe_leather_side="#181c24",
    shoe_darkest="#0a0c10", shoe_highlight="#222630", shoe_sole="#080a0e",
    shoe_heel_back="#181a1f",
)


def _fixer_face_overlay(frame: pygame.Surface, direction: str) -> pygame.Surface:
    """Add The Fixer's thin moustache and cigar to a detective-rig frame."""
    out = frame.copy()
    if direction == "down":
        pygame.draw.line(out, (20, 14, 8), (57, 44), (62, 43), 2)
        pygame.draw.line(out, (20, 14, 8), (67, 43), (72, 44), 2)
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


def _get_fixer_animations() -> dict:
    """Render The Fixer using the detective rig with a navy palette + overlays."""
    base = get_character_animations(FIXER_PALETTE)
    return {
        direction: {
            state: [_fixer_face_overlay(f, direction) for f in frames]
            for state, frames in states.items()
        }
        for direction, states in base.items()
    }


# =============================================================================
# MOB GRUNT  (palette_index = 0 or 2)
# Custom SVGs: viewBox="0 0 320 480" → rendered to 64×80 px.
#
# Design matches the user-supplied reference artwork:
#   tall top-hat · wide brim · full balaclava with diamond eye holes
#   long dark overcoat · waistcoat · cuffs · gloves · trousers · boots
# =============================================================================

# Slight coat-colour variation between the two grunt variants
_GRUNT_COAT_BASE = ["#1c1d21", "#191a20"]   # idx-0 charcoal, idx-1 blue-black
_GRUNT_COAT_DARK = ["#111215", "#0f1016"]


def _mob_defs(grunt_idx: int) -> str:
    base = _GRUNT_COAT_BASE[grunt_idx % 2]
    dark = _GRUNT_COAT_DARK[grunt_idx % 2]
    return f"""  <defs>
    <linearGradient id="coat" x2="1" y2="0">
      <stop stop-color="{dark}"/>
      <stop offset=".5" stop-color="{base}"/>
      <stop offset="1"  stop-color="{dark}"/>
    </linearGradient>
    <linearGradient id="hat" x2="0" y2="1">
      <stop stop-color="#292a2e"/>
      <stop offset="1" stop-color="#101114"/>
    </linearGradient>
    <linearGradient id="mask" x2="0" y2="1">
      <stop stop-color="#25262a"/>
      <stop offset="1" stop-color="#101114"/>
    </linearGradient>
  </defs>"""


# ---------------------------------------------------------------------------
# Shared SVG fragment builders (reused across front / back / side)
# ---------------------------------------------------------------------------

def _hat_crown_front() -> str:
    """Tall top-hat crown, front/back view."""
    return """
    <!-- Tall top hat crown -->
    <path d="M77 100 L83 14 Q160 -4 237 14 L243 100Z"
          fill="url(#hat)" stroke="#090a0c" stroke-width="4"/>
    <path d="M83 18 Q160 1 237 18" fill="none" stroke="#44454a" stroke-width="2"/>
    <!-- Hat band -->
    <path d="M79 76 L241 76 L243 98 L77 98Z" fill="#3b2025"/>
    <path d="M79 76 L241 76" stroke="#5b393e" stroke-width="2"/>"""


def _hat_brim_front() -> str:
    """Wide hat brim, front/back view."""
    return """
    <!-- Wide brim -->
    <path d="M36 108 Q160 79 284 108 Q299 114 284 127 Q160 153 36 127 Q21 114 36 108Z"
          fill="url(#hat)" stroke="#090a0c" stroke-width="4"/>
    <path d="M36 113 Q160 87 284 113" fill="none" stroke="#45464b" stroke-width="2"/>"""


def _head_and_mask_front() -> str:
    """Head, full balaclava, diamond eye-holes and mask detailing (front)."""
    return """
    <!-- Head -->
    <path d="M105 116 Q160 99 215 116 L208 153 Q202 181 160 197 Q118 181 112 153Z"
          fill="#18191c" stroke="#08090b" stroke-width="3"/>
    <!-- Full face mask -->
    <path d="M111 116 Q160 102 209 116 L203 154 Q197 177 160 190 Q123 177 117 154Z"
          fill="url(#mask)" stroke="#08090b" stroke-width="2.5"/>
    <!-- Left eye opening (diamond) -->
    <path d="M122 128 Q138 119 151 128 L149 139 Q137 146 124 138Z"
          fill="#050608" stroke="#55565a" stroke-width="1.5"/>
    <!-- Right eye opening (diamond) -->
    <path d="M169 128 Q182 119 198 128 L196 138 Q183 146 171 139Z"
          fill="#050608" stroke="#55565a" stroke-width="1.5"/>
    <!-- Mask nose bridge + chin detailing -->
    <path d="M160 126 L151 155 L160 161 L169 155Z"
          fill="#151619" stroke="#515257" stroke-width="1.5"/>
    <path d="M132 151 Q145 145 150 158
             M188 151 Q175 145 170 158
             M136 166 Q160 176 184 166"
          fill="none" stroke="#55565a" stroke-width="1.5"/>"""


# ---------------------------------------------------------------------------
# FRONT (down) view
# ---------------------------------------------------------------------------

def _grunt_svg_front(
    bob_y: int = 0,
    l_leg_dx: int = 0, l_leg_dy: int = 0,
    r_leg_dx: int = 0, r_leg_dy: int = 0,
    l_arm_dy: int = 0, r_arm_dy: int = 0,
    grunt_idx: int = 0,
) -> str:
    defs = _mob_defs(grunt_idx)
    lx, ly = l_leg_dx * 8, l_leg_dy * 10
    rx, ry = r_leg_dx * 8, r_leg_dy * 10
    la = l_arm_dy * 8
    ra = r_arm_dy * 8
    b  = bob_y * 5

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 480">
{defs}

  <!-- Ground shadow -->
  <ellipse cx="163" cy="476" rx="106" ry="11" fill="#000" opacity="0.42"/>

  <!-- ── LEFT LEG + BOOT ── -->
  <g transform="translate({lx},{ly})">
    <path d="M100 366 L158 385 L154 466 L101 466Z"
          fill="#18191c" stroke="#090a0c" stroke-width="2"/>
    <path d="M119 390 L116 457 M139 395 L137 457"
          fill="none" stroke="#34353a" stroke-width="1.5"/>
    <path d="M101 457 L154 457 L151 475 L88 475 Q87 465 101 457Z"
          fill="#090a0c" stroke="#050506" stroke-width="2"/>
    <path d="M98 466 L145 466" stroke="#45464a" stroke-width="2"/>
  </g>

  <!-- ── RIGHT LEG + BOOT ── -->
  <g transform="translate({rx},{ry})">
    <path d="M162 385 L220 366 L219 466 L166 466Z"
          fill="#18191c" stroke="#090a0c" stroke-width="2"/>
    <path d="M181 395 L183 457 M201 390 L204 457"
          fill="none" stroke="#34353a" stroke-width="1.5"/>
    <path d="M166 457 L219 457 L232 475 L169 475Z"
          fill="#090a0c" stroke="#050506" stroke-width="2"/>
    <path d="M174 466 L222 466" stroke="#45464a" stroke-width="2"/>
  </g>

  <!-- ── BOB GROUP (upper body + head breathe together) ── -->
  <g transform="translate(0,{b})">

    <!-- Coat body (behind arms) -->
    <path d="M133 204 L99 216 L73 240 L43 438
             L85 449 L100 303 L91 466
             L229 466 L220 303 L235 449 L277 438
             L247 240 L221 216 L187 204
             L175 225 L160 236 L145 225Z"
          fill="url(#coat)" stroke="#090a0c" stroke-width="3"/>

    <!-- ── LEFT ARM ── -->
    <g transform="translate(0,{la})">
      <path d="M100 219 L76 241 L57 343 L82 350 L109 263Z"
            fill="url(#coat)" stroke="#0b0b0c" stroke-width="3"/>
      <!-- Sleeve folds (matches back view) -->
      <path d="M83 242 Q89 246 95 245
               M76 270 Q83 274 88 272
               M69 302 Q77 306 84 303"
            fill="none" stroke="#444246" stroke-width="2" opacity=".6"/>
      <!-- Cuff -->
      <path d="M57 337 L83 344 L80 361 L54 354Z"
            fill="#17181b" stroke="#55565a" stroke-width="2"/>
      <!-- Glove -->
      <path d="M54 354 Q47 368 55 382 L68 390 L81 361Z"
            fill="#111113" stroke="#080809" stroke-width="2" stroke-linejoin="round"/>
    </g>

    <!-- ── RIGHT ARM ── -->
    <g transform="translate(0,{ra})">
      <path d="M220 219 L244 241 L263 343 L238 350 L211 263Z"
            fill="url(#coat)" stroke="#0b0b0c" stroke-width="3"/>
      <!-- Sleeve folds (matches back view) -->
      <path d="M225 245 Q231 246 237 242
               M232 272 Q237 274 244 270
               M236 303 Q243 306 251 302"
            fill="none" stroke="#444246" stroke-width="2" opacity=".6"/>
      <!-- Cuff -->
      <path d="M237 344 L263 337 L266 354 L240 361Z"
            fill="#17181b" stroke="#55565a" stroke-width="2"/>
      <!-- Glove -->
      <path d="M266 354 Q273 368 265 382 L252 390 L239 361Z"
            fill="#111113" stroke="#080809" stroke-width="2" stroke-linejoin="round"/>
    </g>

    <!-- Waistcoat (over coat center) -->
    <path d="M145 225 L160 236 L175 225 L195 361 L160 385 L125 361Z"
          fill="#402329" stroke="#151114" stroke-width="2.5"/>
    <path d="M145 225 L160 236 L175 225 L195 361 L160 385 L125 361Z"
          fill="none" stroke="#654148" stroke-width="1.5"/>

    <!-- Coat lapels -->
    <path d="M133 204 L103 220 L145 274 L160 236 L145 225Z"
          fill="#303136" stroke="#55565a" stroke-width="2"/>
    <path d="M187 204 L217 220 L175 274 L160 236 L175 225Z"
          fill="#303136" stroke="#55565a" stroke-width="2"/>

    <!-- Tailoring seams -->
    <path d="M104 221 L76 438 M216 221 L244 438"
          fill="none" stroke="#45464a" stroke-width="1.5"/>
    <path d="M91 466 L229 466" stroke="#45464a" stroke-width="2"/>

    <!-- Buttons -->
    <g fill="#55565a" stroke="#17181b" stroke-width="1.5">
      <circle cx="160" cy="260" r="3.5"/>
      <circle cx="160" cy="284" r="3.5"/>
      <circle cx="160" cy="308" r="3.5"/>
      <circle cx="160" cy="332" r="3.5"/>
      <circle cx="160" cy="356" r="3.5"/>
    </g>

    <!-- Neck + shirt collar + cravat -->
    <path d="M140 184 L180 184 L185 210 L135 210Z" fill="#16171a"/>
    <!-- Shirt visible in lapel V — darkened to match raised collar tone -->
    <path d="M139 188 L160 207 L181 188 L176 184 L160 197 L144 184Z" fill="#343236"/>
    <path d="M146 198 L160 207 L174 198 L170 224 L160 232 L150 224Z"
          fill="#45252a" stroke="#171114" stroke-width="2"/>

    <!-- Hat crown + band -->
{_hat_crown_front()}

    <!-- Hat brim -->
{_hat_brim_front()}

    <!-- Head + balaclava + eyes -->
{_head_and_mask_front()}

  </g>
</svg>"""


# ---------------------------------------------------------------------------
# BACK (up) view
# ---------------------------------------------------------------------------

def _grunt_svg_back(
    bob_y: int = 0,
    l_leg_dx: int = 0, l_leg_dy: int = 0,
    r_leg_dx: int = 0, r_leg_dy: int = 0,
    l_arm_dy: int = 0, r_arm_dy: int = 0,
    grunt_idx: int = 0,
) -> str:
    """Back view based on user-supplied artwork.

    Modifications applied to the reference SVG:
      - Defs replaced with shared _mob_defs() (same gradient IDs, slight
        coat-colour variation per grunt_idx).
      - Hat-band colour normalised to #3b2025 to match front view.
      - Arms (+ sleeve folds + gloves) wrapped in per-side translate groups
        so they swing during the walk cycle.
      - Trousers + boots moved outside the bob group so they stay grounded.
      - Bob group wraps hat / head / collar / coat body / vent / hem.
      - Ground-contact shadow ellipse added.
    """
    defs = _mob_defs(grunt_idx)
    lx, ly = l_leg_dx * 8, l_leg_dy * 10
    rx, ry = r_leg_dx * 8, r_leg_dy * 10
    la = l_arm_dy * 8
    ra = r_arm_dy * 8
    b  = bob_y * 5

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 480">
{defs}

  <!-- Ground shadow -->
  <ellipse cx="160" cy="474" rx="102" ry="11" fill="#000" opacity="0.42"/>

  <!-- ── LEFT TROUSER + BOOT ── -->
  <g transform="translate({lx},{ly})">
    <path d="M91 389 L153 396 L148 449 L111 449 L103 418 L83 418 Z"
          fill="#171719"/>
    <path d="M108 441 L149 441 L151 463 Q130 470 101 463 Z"
          fill="#0d0d0e"/>
    <path d="M108 450 L149 450" stroke="#38373a" stroke-width="2" fill="none"/>
  </g>

  <!-- ── RIGHT TROUSER + BOOT ── -->
  <g transform="translate({rx},{ry})">
    <path d="M167 396 L229 389 L237 418 L217 418 L209 449 L172 449 Z"
          fill="#171719"/>
    <path d="M171 441 L212 441 L219 463 Q190 470 169 463 Z"
          fill="#0d0d0e"/>
    <path d="M171 450 L212 450" stroke="#38373a" stroke-width="2" fill="none"/>
  </g>

  <!-- ── BOB GROUP (hat / head / collar / coat / arms breathe together) ── -->
  <g transform="translate(0,{b})">

    <!-- ╔══ HAT (drawn first — behind head) ══╗ -->
    <!-- Tall crown (back) -->
    <path d="M92 74 L99 15 Q160 4 221 15 L228 74 Z"
          fill="url(#hat)" stroke="#080809" stroke-width="3"/>
    <!-- Crown highlight line -->
    <path d="M100 25 Q160 17 220 25"
          fill="none" stroke="#444246" stroke-width="2" opacity=".5"/>
    <!-- Hat-band ribbon (burgundy, matches front) -->
    <path d="M91 54 Q160 62 229 54 L231 69 Q160 78 89 69 Z"
          fill="#3b2025"/>
    <!-- Wide brim (back) -->
    <path d="M65 77 Q160 62 255 77 L265 91 Q160 106 55 91 Z"
          fill="#171719" stroke="#080809" stroke-width="3"/>

    <!-- ╔══ HEAD + COLLAR (in front of hat) ══╗ -->
    <!-- Back of skull (dark block behind collar) -->
    <path d="M124 91 L196 91 L200 123 L120 123 Z" fill="#171719"/>
    <!-- Raised coat collar (dark grey, slightly lighter for depth) -->
    <path d="M108 108 L133 91 L160 112 L187 91 L212 108
             L194 145 L126 145 Z"
          fill="#343236" stroke="#111113" stroke-width="3"/>
    <!-- Inner collar facing -->
    <path d="M133 93 L160 112 L187 93 L180 126 L140 126 Z"
          fill="#242326"/>

    <!-- ╔══ ARMS (behind coat body, swing per step) ══╗ -->
    <!-- Left sleeve -->
    <g transform="translate(0,{la})">
      <path d="M112 137
               Q100 143 94 157
               L77 214
               Q73 231 76 249
               L82 264
               Q87 270 94 266
               L104 259
               Q99 247 103 231
               L120 180
               Q127 162 136 154 Z"
            fill="url(#coat)" stroke="#0b0b0c" stroke-width="3"
            stroke-linejoin="round"/>
      <!-- Sleeve folds -->
      <path d="M99 177 Q105 181 111 181
               M91 204 Q98 208 104 207
               M83 235 Q90 239 99 236"
            fill="none" stroke="#444246" stroke-width="2" opacity=".6"/>
      <!-- Left glove -->
      <path d="M82 258
               Q78 266 83 273
               Q89 280 96 273
               L105 263
               L101 254
               Q96 251 92 257
               L88 252
               Q83 251 82 258 Z"
            fill="#111113" stroke="#080809" stroke-width="2"
            stroke-linejoin="round"/>
    </g>

    <!-- Right sleeve -->
    <g transform="translate(0,{ra})">
      <path d="M208 137
               Q220 143 226 157
               L243 214
               Q247 231 244 249
               L238 264
               Q233 270 226 266
               L216 259
               Q221 247 217 231
               L200 180
               Q193 162 184 154 Z"
            fill="url(#coat)" stroke="#0b0b0c" stroke-width="3"
            stroke-linejoin="round"/>
      <!-- Sleeve folds -->
      <path d="M202 181 Q208 181 214 177
               M209 207 Q215 208 222 204
               M221 236 Q230 239 237 235"
            fill="none" stroke="#444246" stroke-width="2" opacity=".6"/>
      <!-- Right glove -->
      <path d="M238 258
               Q242 266 237 273
               Q231 280 224 273
               L215 263
               L219 254
               Q224 251 228 257
               L232 252
               Q237 251 238 258 Z"
            fill="#111113" stroke="#080809" stroke-width="2"
            stroke-linejoin="round"/>
    </g>

    <!-- ╔══ OVERCOAT BODY (rear silhouette, covers arm tops) ══╗ -->
    <path d="M112 132
             Q160 116 208 132
             L229 183
             L219 293
             L238 392
             Q160 414 82 392
             L101 293
             L91 183 Z"
          fill="url(#coat)" stroke="#0b0b0c" stroke-width="4"
          stroke-linejoin="round"/>

    <!-- Shoulder seams -->
    <path d="M112 136 Q133 151 160 153 Q187 151 208 136"
          fill="none" stroke="#444246" stroke-width="2" opacity=".75"/>
    <path d="M112 139 L130 171 M208 139 L190 171"
          fill="none" stroke="#111113" stroke-width="2"/>

    <!-- Center back seam + fabric folds -->
    <path d="M160 153 L160 390"
          fill="none" stroke="#0d0d0e" stroke-width="2.5"/>
    <path d="M133 172 Q145 205 139 242 L127 313"
          fill="none" stroke="#3b393d" stroke-width="2" opacity=".6"/>
    <path d="M187 172 Q175 205 181 242 L193 313"
          fill="none" stroke="#3b393d" stroke-width="2" opacity=".6"/>
    <path d="M103 290 Q119 302 132 304 M217 290 Q201 302 188 304"
          fill="none" stroke="#444246" stroke-width="2" opacity=".5"/>

    <!-- Rear coat vent -->
    <path d="M145 345 L160 390 L175 345 L175 398 Q160 402 145 398 Z"
          fill="#111113" stroke="#080809" stroke-width="2"/>
    <path d="M160 390 L160 400" fill="none" stroke="#4a171e" stroke-width="3"/>

    <!-- Coat hem -->
    <path d="M82 392 Q160 414 238 392"
          fill="none" stroke="#454347" stroke-width="2"/>

  </g>
</svg>"""


# ---------------------------------------------------------------------------
# SIDE (right-facing) view
# ---------------------------------------------------------------------------

def _grunt_svg_side(
    bob_y: int = 0,
    f_leg_dx: int = 0, f_leg_dy: int = 0,
    b_leg_dx: int = 0, b_leg_dy: int = 0,
    f_arm_rot: int = 0,
    grunt_idx: int = 0,
) -> str:
    defs = _mob_defs(grunt_idx)
    flx, fly = f_leg_dx * 8, f_leg_dy * 10
    blx, bly = b_leg_dx * 8, b_leg_dy * 10
    b = bob_y * 5
    # Front arm rotation applied around shoulder pivot
    arm_rot = f_arm_rot

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 480">
{defs}

  <!-- Ground shadow -->
  <ellipse cx="165" cy="476" rx="92" ry="10" fill="#000" opacity="0.40"/>

  <!-- ── BACK LEG + BOOT ── -->
  <g transform="translate({blx},{bly})">
    <path d="M118 370 L160 386 L158 466 L116 466Z"
          fill="#14151a" stroke="#090a0c" stroke-width="2"/>
    <path d="M115 457 L162 457 L160 476 L113 476 Q111 466 115 457Z"
          fill="#08090c" stroke="#050506" stroke-width="2"/>
    <path d="M115 466 L160 466" stroke="#3a3b40" stroke-width="2"/>
  </g>

  <!-- ── FRONT LEG + BOOT ── -->
  <g transform="translate({flx},{fly})">
    <path d="M158 386 L208 368 L210 466 L158 466Z"
          fill="#18191d" stroke="#090a0c" stroke-width="2"/>
    <path d="M174 395 L176 458 M193 390 L196 458"
          fill="none" stroke="#34353a" stroke-width="1.5"/>
    <path d="M156 457 L212 457 L218 476 L154 476 Q152 466 156 457Z"
          fill="#090a0c" stroke="#050506" stroke-width="2"/>
    <path d="M156 466 L214 466" stroke="#45464a" stroke-width="2"/>
  </g>

  <!-- ── BOB GROUP ── -->
  <g transform="translate(0,{b})">

    <!-- Back arm (behind coat, left/back side) -->
    <path d="M112 222 L88 248 L76 348 L100 354 L122 268Z"
          fill="url(#coat)" stroke="#0b0b0c" stroke-width="3"/>
    <!-- Back sleeve folds -->
    <path d="M94 249 Q100 253 106 252
             M86 276 Q93 280 98 278
             M79 307 Q87 311 94 308"
          fill="none" stroke="#444246" stroke-width="2" opacity=".6"/>
    <path d="M76 342 L102 348 L100 364 L74 358Z"
          fill="#17181b" stroke="#55565a" stroke-width="2"/>
    <path d="M74 358 Q67 372 75 385 L87 392 L100 364Z"
          fill="#111113" stroke="#080809" stroke-width="2" stroke-linejoin="round"/>
          fill="#101114" stroke="#08090b" stroke-width="2"/>

    <!-- Coat body (side – slightly narrower depth) -->
    <path d="M112 208 Q100 218 86 244 L62 440
             L100 450 L112 310 L108 466
             L220 466 L218 310 L228 450 L258 440
             L238 244 Q226 218 216 208
             L200 228 L165 238 L140 228Z"
          fill="url(#coat)" stroke="#090a0c" stroke-width="3"/>
    <!-- Side coat front edge highlight -->
    <path d="M216 210 Q224 230 232 440"
          fill="none" stroke="#303136" stroke-width="2"/>

    <!-- Front arm (swinging, right side of body) -->
    <g transform="rotate({arm_rot}, 216, 228)">
      <path d="M208 222 L232 248 L246 348 L222 354 L204 268Z"
            fill="url(#coat)" stroke="#0b0b0c" stroke-width="3"/>
      <!-- Front sleeve folds -->
      <path d="M214 249 Q220 253 226 249
               M221 278 Q227 282 233 278
               M228 309 Q234 313 240 309"
            fill="none" stroke="#444246" stroke-width="2" opacity=".6"/>
      <!-- Cuff -->
      <path d="M222 342 L248 337 L250 354 L224 360Z"
            fill="#17181b" stroke="#55565a" stroke-width="2"/>
      <!-- Glove -->
      <path d="M250 354 Q258 368 250 382 L236 390 L222 360Z"
            fill="#111113" stroke="#080809" stroke-width="2" stroke-linejoin="round"/>
    </g>

    <!-- Waistcoat (side strip) -->
    <path d="M144 230 L165 240 L178 230 L192 362 L165 384 L140 362Z"
          fill="#402329" stroke="#151114" stroke-width="2.5"/>
    <path d="M144 230 L165 240 L178 230 L192 362 L165 384 L140 362Z"
          fill="none" stroke="#654148" stroke-width="1.5"/>

    <!-- Side coat lapel (one visible) -->
    <path d="M216 208 L196 226 L178 272 L165 240 L178 230Z"
          fill="#303136" stroke="#55565a" stroke-width="2"/>

    <!-- Tailoring seam (front edge) -->
    <path d="M216 212 L238 440" fill="none" stroke="#45464a" stroke-width="1.5"/>
    <path d="M108 466 L220 466" stroke="#45464a" stroke-width="2"/>

    <!-- Buttons (one column visible) -->
    <g fill="#55565a" stroke="#17181b" stroke-width="1.5">
      <circle cx="185" cy="260" r="3.5"/>
      <circle cx="187" cy="284" r="3.5"/>
      <circle cx="189" cy="308" r="3.5"/>
      <circle cx="191" cy="332" r="3.5"/>
      <circle cx="193" cy="356" r="3.5"/>
    </g>

    <!-- Neck + collar side — dark to match raised collar in back view -->
    <path d="M150 186 L182 186 L185 210 L148 210Z" fill="#16171a"/>
    <!-- Shirt visible at lapel V — same dark tone as raised collar facing -->
    <path d="M160 190 L165 207 L178 190 L182 186 L165 198 L160 186Z" fill="#343236"/>
    <path d="M162 200 L165 207 L174 200 L172 224 L165 232 L158 224Z"
          fill="#45252a" stroke="#171114" stroke-width="2"/>
    <!-- Hat crown (side profile – narrower) -->
    <path d="M118 100 L124 14 Q165 -4 210 14 L216 100Z"
          fill="url(#hat)" stroke="#090a0c" stroke-width="4"/>
    <path d="M126 18 Q165 1 208 18" fill="none" stroke="#44454a" stroke-width="2"/>
    <path d="M120 76 L214 76 L216 98 L118 98Z" fill="#3b2025"/>
    <path d="M120 76 L214 76" stroke="#5b393e" stroke-width="2"/>

    <!-- Hat brim (side – wider right, slightly narrower left) -->
    <path d="M62 108 Q165 80 272 108 Q288 115 272 128 Q165 154 62 128 Q46 115 62 108Z"
          fill="url(#hat)" stroke="#090a0c" stroke-width="4"/>
    <path d="M62 113 Q165 88 272 113" fill="none" stroke="#45464b" stroke-width="2"/>

    <!-- Head (side – oval slightly forward-jutting face) -->
    <path d="M114 116 Q165 100 218 116 L212 154 Q206 182 165 197 Q124 182 118 154Z"
          fill="#18191c" stroke="#08090b" stroke-width="3"/>
    <!-- Balaclava (side) -->
    <path d="M120 116 Q165 103 212 116 L206 154 Q200 177 165 190 Q130 177 126 154Z"
          fill="url(#mask)" stroke="#08090b" stroke-width="2.5"/>

    <!-- Face profile protrusion (right/front side of head) -->
    <path d="M196 120 Q218 132 220 152 Q218 172 204 182 L200 118Z"
          fill="url(#mask)" stroke="#08090b" stroke-width="2"/>

    <!-- Single eye slit (right side only, diamond shape) -->
    <path d="M196 130 Q208 122 218 130 L216 140 Q206 148 197 142Z"
          fill="#050608" stroke="#55565a" stroke-width="1.5"/>

    <!-- Mask nose-bridge detail (side) -->
    <path d="M200 152 Q208 148 212 156" fill="none" stroke="#55565a" stroke-width="1.5"/>
    <path d="M190 166 Q200 174 210 168"
          fill="none" stroke="#55565a" stroke-width="1.5"/>

  </g>
</svg>"""


# ---------------------------------------------------------------------------
# Animation builder
# ---------------------------------------------------------------------------

def _get_grunt_animations(grunt_idx: int) -> dict:
    """Render all four-direction idle + walk frames for a mob grunt."""
    W, H = 64, 80

    def fr(fn, **kw):
        return render_svg(fn(grunt_idx=grunt_idx, **kw), W, H)

    # Down
    down_idle = [
        fr(_grunt_svg_front, bob_y=0),
        fr(_grunt_svg_front, bob_y=1),
    ]
    down_walk = [
        fr(_grunt_svg_front, bob_y=0, l_leg_dx=-1, l_leg_dy=-3, r_leg_dx=1,  r_leg_dy=2,  l_arm_dy=2,  r_arm_dy=-2),
        fr(_grunt_svg_front, bob_y=1),
        fr(_grunt_svg_front, bob_y=0, l_leg_dx=1,  l_leg_dy=2,  r_leg_dx=-1, r_leg_dy=-3, l_arm_dy=-2, r_arm_dy=2),
        fr(_grunt_svg_front, bob_y=1),
    ]

    # Up
    up_idle = [
        fr(_grunt_svg_back, bob_y=0),
        fr(_grunt_svg_back, bob_y=1),
    ]
    up_walk = [
        fr(_grunt_svg_back, bob_y=0, l_leg_dx=-1, l_leg_dy=-3, r_leg_dx=1,  r_leg_dy=2,  l_arm_dy=2,  r_arm_dy=-2),
        fr(_grunt_svg_back, bob_y=1),
        fr(_grunt_svg_back, bob_y=0, l_leg_dx=1,  l_leg_dy=2,  r_leg_dx=-1, r_leg_dy=-3, l_arm_dy=-2, r_arm_dy=2),
        fr(_grunt_svg_back, bob_y=1),
    ]

    # Right (side)
    right_idle = [
        fr(_grunt_svg_side, bob_y=0),
        fr(_grunt_svg_side, bob_y=1),
    ]
    right_walk = [
        fr(_grunt_svg_side, bob_y=0, f_leg_dx=4,  f_leg_dy=-2, b_leg_dx=-4, b_leg_dy=2,  f_arm_rot=-14),
        fr(_grunt_svg_side, bob_y=1, f_leg_dx=1,  f_leg_dy=0,  b_leg_dx=-1, b_leg_dy=0,  f_arm_rot=-4),
        fr(_grunt_svg_side, bob_y=0, f_leg_dx=-4, f_leg_dy=2,  b_leg_dx=4,  b_leg_dy=-2, f_arm_rot=14),
        fr(_grunt_svg_side, bob_y=1, f_leg_dx=-1, f_leg_dy=0,  b_leg_dx=1,  b_leg_dy=0,  f_arm_rot=4),
    ]

    # Left = horizontal flip of right
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

NPC_PALETTES = (None, FIXER_PALETTE, None)  # None = custom SVG renderer
NPC_NAMES    = ("The Mob Grunt", "The Fixer", "The Mob Grunt (Alt)")


@lru_cache(maxsize=3)
def get_npc_animations(palette_index: int = 0) -> dict:
    """Return cached four-direction animation dict for the given NPC type.

    palette_index:
      0 – Mob Grunt      (charcoal coat)
      1 – The Fixer      (navy suit, detective rig)
      2 – Mob Grunt Alt  (blue-black coat)
    """
    if palette_index == 1:
        return _get_fixer_animations()
    grunt_idx = 0 if palette_index == 0 else 1
    return _get_grunt_animations(grunt_idx)
