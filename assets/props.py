"""
Room Props, Furniture & Environment SVG Assets for Case Unknown.

This module defines all room objects (furniture, decorations, lighting) and UI badges
as vector graphics, along with rendering and assembly functions.
"""

from assets.renderer import render_svg

# ---------------------------------------------------------------------------
# Room Furniture & Environment SVGs (DRY Helpers)
# ---------------------------------------------------------------------------

def _svg_cabinet_drawer(y: int) -> str:
    """Generates a single metal filing cabinet drawer with brass label card slot and handle."""
    return f"""  <rect x="9" y="{y}" width="46" height="17" rx="1.5" fill="url(#drawerFace)" stroke="#29302e" stroke-width="1"/>
  <rect x="24" y="{y + 3}" width="16" height="5" fill="#dfb15b" rx="0.5"/>
  <rect x="26" y="{y + 4}" width="12" height="3" fill="#f4ebd9"/>
  <rect x="25" y="{y + 11}" width="14" height="3" fill="#202524" rx="1"/>"""


def _svg_desk_pedestal_drawers(base_x: int) -> str:
    """Generates 3 stacked drawers with brass pull handles for a desk pedestal."""
    drawers = []
    for y_offset, height in [(0, 13), (16, 13), (32, 14)]:
        y = 56 + y_offset
        handle_y = y + 5
        drawers.append(
            f'  <rect x="{base_x}" y="{y}" width="36" height="{height}" rx="1" fill="#4a2515" stroke="#2c1409" stroke-width="1"/>\n'
            f'  <rect x="{base_x + 13}" y="{handle_y}" width="10" height="3" rx="1" fill="#dfb15b"/>'
        )
    return "\n".join(drawers)


SVG_DETECTIVE_DESK = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 120" width="180" height="120">
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
{_svg_desk_pedestal_drawers(18)}

  <!-- Right Drawers & Brass Handles -->
{_svg_desk_pedestal_drawers(126)}

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
      <stop offset="0%" stop-color="#596052"/>
      <stop offset="50%" stop-color="#3f463c"/>
      <stop offset="100%" stop-color="#292e29"/>
    </linearGradient>
    <linearGradient id="sofaCushion" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4a5245"/>
      <stop offset="100%" stop-color="#30362f"/>
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
  <g fill="#202620" opacity="0.8">
    <circle cx="36" cy="30" r="2.2"/><circle cx="58" cy="30" r="2.2"/>
    <circle cx="85" cy="30" r="2.2"/><circle cx="112" cy="30" r="2.2"/><circle cx="134" cy="30" r="2.2"/>
    <circle cx="47" cy="42" r="2.2"/><circle cx="71" cy="42" r="2.2"/>
    <circle cx="99" cy="42" r="2.2"/><circle cx="123" cy="42" r="2.2"/>
  </g>
  <path d="M36,30 L47,42 L58,30 L71,42 L85,30 L99,42 L112,30 L123,42 L134,30" 
        stroke="#202620" stroke-width="1.2" fill="none" opacity="0.6"/>

  <!-- Main Seat Base & Brass Tack Line -->
  <rect x="14" y="60" width="142" height="18" rx="4" fill="#30362f"/>
  <!-- Brass nailhead trim -->
  <line x1="20" y1="74" x2="150" y2="74" stroke="#a58d62" stroke-width="1.2" stroke-dasharray="2,3"/>

  <!-- Left Rolled Armrest -->
  <ellipse cx="20" cy="52" rx="12" ry="18" fill="url(#sofaLeather)"/>
  <ellipse cx="20" cy="52" rx="9" ry="14" fill="#596052"/>
  <circle cx="20" cy="52" r="3" fill="#a58d62"/>

  <!-- Right Rolled Armrest -->
  <ellipse cx="150" cy="52" rx="12" ry="18" fill="url(#sofaLeather)"/>
  <ellipse cx="150" cy="52" rx="9" ry="14" fill="#596052"/>
  <circle cx="150" cy="52" r="3" fill="#a58d62"/>

  <!-- Plump Seat Cushions (3 cushions) -->
  <rect x="30" y="48" width="34" height="20" rx="4" fill="url(#sofaCushion)" stroke="#2b0d0f" stroke-width="1.2"/>
  <rect x="68" y="48" width="34" height="20" rx="4" fill="url(#sofaCushion)" stroke="#2b0d0f" stroke-width="1.2"/>
  <rect x="106" y="48" width="34" height="20" rx="4" fill="url(#sofaCushion)" stroke="#2b0d0f" stroke-width="1.2"/>
</svg>"""


SVG_FILING_CABINET = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 96" width="64" height="96">
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

  <!-- 4 Modular Drawers -->
{chr(10).join(_svg_cabinet_drawer(y) for y in (10, 29, 48, 67))}

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
      <stop offset="0%" stop-color="#41423b"/>
      <stop offset="100%" stop-color="#2d302c"/>
    </linearGradient>
  </defs>

  <!-- Fringe Tassels (Left & Right) -->
  <line x1="4" y1="12" x2="4" y2="118" stroke="#e6d5b8" stroke-width="2" stroke-dasharray="2,2"/>
  <line x1="216" y1="12" x2="216" y2="118" stroke="#e6d5b8" stroke-width="2" stroke-dasharray="2,2"/>

  <!-- Rug Main Body -->
  <rect x="6" y="10" width="208" height="110" rx="3" fill="url(#rugBase)"/>

  <!-- Outer Navy Border -->
  <rect x="12" y="16" width="196" height="98" rx="2" fill="none" stroke="#293136" stroke-width="7"/>
  <!-- Gold Accent Trim -->
  <rect x="16" y="20" width="188" height="90" fill="none" stroke="#a58d62" stroke-width="1.5"/>

  <!-- Inner Field Background -->
  <rect x="22" y="26" width="176" height="78" fill="#323630"/>

  <!-- Central Persian Medallion -->
  <polygon points="110,32 150,65 110,98 70,65" fill="#293136" stroke="#a58d62" stroke-width="2"/>
  <circle cx="110" cy="65" r="16" fill="#454a40" stroke="#a58d62" stroke-width="1.5"/>
  <circle cx="110" cy="65" r="7" fill="#a58d62"/>

  <!-- Corner Quarter-Medallions -->
  <polygon points="22,26 44,26 22,48" fill="#293136" stroke="#a58d62" stroke-width="1"/>
  <polygon points="198,26 176,26 198,48" fill="#293136" stroke="#a58d62" stroke-width="1"/>
  <polygon points="22,104 44,104 22,82" fill="#293136" stroke="#a58d62" stroke-width="1"/>
  <polygon points="198,104 176,104 198,82" fill="#293136" stroke="#a58d62" stroke-width="1"/>
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



SVG_WALL_SAFE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 90" width="80" height="90">
  <defs>
    <linearGradient id="safeOuter" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3d434d"/>
      <stop offset="50%" stop-color="#252a32"/>
      <stop offset="100%" stop-color="#14171d"/>
    </linearGradient>
    <linearGradient id="safeDoor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4a525f"/>
      <stop offset="100%" stop-color="#2a303a"/>
    </linearGradient>
    <radialGradient id="safeDial" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffe8a1"/>
      <stop offset="70%" stop-color="#c69a3b"/>
      <stop offset="100%" stop-color="#694d12"/>
    </radialGradient>
  </defs>
  <rect x="4" y="68" width="72" height="20" rx="4" fill="#000000" opacity="0.45"/>
  <rect x="6" y="8" width="68" height="74" rx="4" fill="url(#safeOuter)" stroke="#1a1c22" stroke-width="2"/>
  <circle cx="12" cy="14" r="2.5" fill="#c69a3b"/>
  <circle cx="68" cy="14" r="2.5" fill="#c69a3b"/>
  <circle cx="12" cy="76" r="2.5" fill="#c69a3b"/>
  <circle cx="68" cy="76" r="2.5" fill="#c69a3b"/>
  <rect x="14" y="16" width="52" height="58" rx="2" fill="url(#safeDoor)" stroke="#15181e" stroke-width="1.5"/>
  <rect x="10" y="24" width="6" height="12" rx="1.5" fill="#c69a3b"/>
  <rect x="10" y="52" width="6" height="12" rx="1.5" fill="#c69a3b"/>
  <circle cx="40" cy="45" r="14" fill="#1b1e24" stroke="#c69a3b" stroke-width="2"/>
  <circle cx="40" cy="45" r="10" fill="url(#safeDial)"/>
  <circle cx="40" cy="45" r="4" fill="#1b1e24"/>
  <line x1="40" y1="33" x2="40" y2="37" stroke="#dfb15b" stroke-width="2"/>
  <rect x="48" y="43" width="12" height="4" rx="1.5" fill="#c69a3b"/>
  <circle cx="60" cy="45" r="3.5" fill="#ffe8a1"/>
</svg>"""

SVG_AUTOPSY_TABLE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 100" width="170" height="100">
  <defs>
    <linearGradient id="metalTableTop" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#b4c2ce"/>
      <stop offset="40%" stop-color="#8ba0b2"/>
      <stop offset="100%" stop-color="#5a6e7e"/>
    </linearGradient>
    <linearGradient id="metalLegs" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#465460"/>
      <stop offset="50%" stop-color="#728594"/>
      <stop offset="100%" stop-color="#36424c"/>
    </linearGradient>
  </defs>
  <ellipse cx="85" cy="88" rx="74" ry="10" fill="#000000" opacity="0.45"/>
  <rect x="22" y="44" width="10" height="44" rx="2" fill="url(#metalLegs)"/>
  <rect x="138" y="44" width="10" height="44" rx="2" fill="url(#metalLegs)"/>
  <rect x="24" y="66" width="122" height="6" fill="#36424c"/>
  <polygon points="12,44 158,44 150,16 20,16" fill="url(#metalTableTop)" stroke="#3e4c57" stroke-width="1.5"/>
  <line x1="12" y1="44" x2="158" y2="44" stroke="#cdd9e3" stroke-width="2"/>
  <ellipse cx="85" cy="30" rx="55" ry="7" fill="none" stroke="#485764" stroke-width="1.5"/>
  <circle cx="132" cy="30" r="3" fill="#20262c"/>
  <rect x="6" y="24" width="18" height="12" rx="1.5" fill="#9db0bf" stroke="#36424c" stroke-width="1"/>
  <line x1="9" y1="27" x2="13" y2="27" stroke="#e0e8f0" stroke-width="1"/>
  <line x1="9" y1="30" x2="17" y2="30" stroke="#e0e8f0" stroke-width="1"/>
  <path d="M 40,24 Q 85,20 130,24 Q 132,32 126,34 Q 85,38 44,34 Z" fill="#cfd8dc" opacity="0.85"/>
</svg>"""

SVG_PRISON_BARS = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 120" width="160" height="120">
  <defs>
    <linearGradient id="barSteel" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2a2e33"/>
      <stop offset="50%" stop-color="#555d66"/>
      <stop offset="100%" stop-color="#1e2226"/>
    </linearGradient>
  </defs>
  <rect x="0" y="4" width="160" height="10" fill="#202428" stroke="#121518" stroke-width="1"/>
  <rect x="0" y="106" width="160" height="10" fill="#202428" stroke="#121518" stroke-width="1"/>
  <rect x="0" y="55" width="160" height="8" fill="#272c32" stroke="#121518" stroke-width="1"/>
  <rect x="14" y="4" width="8" height="112" rx="1" fill="url(#barSteel)"/>
  <rect x="36" y="4" width="8" height="112" rx="1" fill="url(#barSteel)"/>
  <rect x="58" y="4" width="8" height="112" rx="1" fill="url(#barSteel)"/>
  <rect x="80" y="4" width="8" height="112" rx="1" fill="url(#barSteel)"/>
  <rect x="102" y="4" width="8" height="112" rx="1" fill="url(#barSteel)"/>
  <rect x="124" y="4" width="8" height="112" rx="1" fill="url(#barSteel)"/>
  <rect x="144" y="4" width="8" height="112" rx="1" fill="url(#barSteel)"/>
  <rect x="74" y="52" width="20" height="20" rx="3" fill="#997a2e" stroke="#524013" stroke-width="1.5"/>
  <circle cx="84" cy="46" r="6" fill="none" stroke="#6b7782" stroke-width="3"/>
  <circle cx="84" cy="60" r="2" fill="#201806"/>
</svg>"""

SVG_INTERROGATION_TABLE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 110" width="160" height="110">
  <defs>
    <linearGradient id="intTableTop" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4d535e"/>
      <stop offset="100%" stop-color="#2a2e35"/>
    </linearGradient>
  </defs>
  <ellipse cx="80" cy="94" rx="70" ry="12" fill="#000000" opacity="0.45"/>
  <rect x="12" y="48" width="16" height="38" rx="2" fill="#242830"/>
  <polygon points="8,48 32,48 28,38 12,38" fill="#3b424d"/>
  <rect x="132" y="48" width="16" height="38" rx="2" fill="#242830"/>
  <polygon points="128,48 152,48 148,38 132,38" fill="#3b424d"/>
  <rect x="42" y="52" width="8" height="42" fill="#262b32"/>
  <rect x="110" y="52" width="8" height="42" fill="#262b32"/>
  <polygon points="32,52 128,52 120,24 40,24" fill="url(#intTableTop)" stroke="#1a1d22" stroke-width="1.5"/>
  <rect x="64" y="28" width="32" height="18" rx="2" fill="#1b1d20" stroke="#dfb15b" stroke-width="0.8"/>
  <circle cx="72" cy="37" r="4" fill="#88929b"/>
  <circle cx="88" cy="37" r="4" fill="#88929b"/>
  <circle cx="72" cy="37" r="1.5" fill="#1a1c1e"/>
  <circle cx="88" cy="37" r="1.5" fill="#1a1c1e"/>
  <circle cx="92" cy="31" r="1.5" fill="#e53935"/>
</svg>"""

SVG_TREASURE_CHEST = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 74 64" width="74" height="64">
  <defs>
    <linearGradient id="chestWood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5e341a"/>
      <stop offset="100%" stop-color="#301809"/>
    </linearGradient>
    <linearGradient id="chestGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffe699"/>
      <stop offset="50%" stop-color="#dfb15b"/>
      <stop offset="100%" stop-color="#8a6519"/>
    </linearGradient>
  </defs>
  <ellipse cx="37" cy="56" rx="32" ry="7" fill="#000000" opacity="0.45"/>
  <rect x="8" y="24" width="58" height="32" rx="3" fill="url(#chestWood)" stroke="#1f1006" stroke-width="1.5"/>
  <path d="M 8,24 Q 37,8 66,24 Z" fill="#6d3d20" stroke="#1f1006" stroke-width="1.5"/>
  <rect x="18" y="16" width="6" height="40" fill="url(#chestGold)"/>
  <rect x="50" y="16" width="6" height="40" fill="url(#chestGold)"/>
  <rect x="8" y="23" width="58" height="4" fill="url(#chestGold)"/>
  <rect x="32" y="24" width="10" height="12" rx="2" fill="url(#chestGold)" stroke="#3e2b05" stroke-width="1"/>
  <circle cx="37" cy="21" r="3.5" fill="none" stroke="#dfb15b" stroke-width="2"/>
  <circle cx="37" cy="29" r="1.5" fill="#201503"/>
  <line x1="37" y1="29" x2="37" y2="33" stroke="#201503" stroke-width="1"/>
</svg>"""

SVG_SPECIMEN_CABINET = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 74 110" width="74" height="110">
  <defs>
    <linearGradient id="specFrame" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4a5560"/>
      <stop offset="100%" stop-color="#222830"/>
    </linearGradient>
  </defs>
  <ellipse cx="37" cy="104" rx="32" ry="6" fill="#000000" opacity="0.4"/>
  <rect x="6" y="8" width="62" height="96" rx="3" fill="url(#specFrame)" stroke="#15191e" stroke-width="1.5"/>
  <rect x="12" y="14" width="50" height="38" rx="2" fill="#182c35" stroke="#354955" stroke-width="1"/>
  <rect x="12" y="56" width="50" height="38" rx="2" fill="#182c35" stroke="#354955" stroke-width="1"/>
  <polygon points="14,16 38,16 26,50 14,50" fill="#ffffff" opacity="0.12"/>
  <polygon points="14,58 38,58 26,92 14,92" fill="#ffffff" opacity="0.12"/>
  <rect x="18" y="28" width="10" height="18" rx="2" fill="#4db6ac" opacity="0.8"/>
  <rect x="32" y="24" width="11" height="22" rx="2" fill="#ffb74d" opacity="0.8"/>
  <rect x="47" y="30" width="9" height="16" rx="2" fill="#81c784" opacity="0.8"/>
  <rect x="20" y="72" width="12" height="16" rx="2" fill="#e57373" opacity="0.8"/>
  <rect x="36" y="68" width="10" height="20" rx="2" fill="#64b5f6" opacity="0.8"/>
  <rect x="56" y="50" width="3" height="12" rx="1" fill="#dfb15b"/>
</svg>"""

# ---------------------------------------------------------------------------
# Case-specific environmental storytelling props
# ---------------------------------------------------------------------------

SVG_CRIME_DESK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 190 130" width="190" height="130">
<defs>
  <linearGradient id="cdwood" x2="0" y2="1"><stop stop-color="#62432f"/><stop offset="1" stop-color="#30231d"/></linearGradient>
  <linearGradient id="cdtop" x2="0" y2="1"><stop stop-color="#77563c"/><stop offset="1" stop-color="#493224"/></linearGradient>
</defs>
<ellipse cx="95" cy="116" rx="82" ry="9" fill="#07090b" opacity=".48"/>
<path d="M22 69h146v40H22z" fill="url(#cdwood)" stroke="#201712" stroke-width="2"/>
<path d="M31 78h42v27H31zm86 0h42v27h-42z" fill="#38261d" stroke="#876447" stroke-width="1"/>
<path d="M36 86h31m-31 9h31m55-9h31m-31 9h31" stroke="#241b17" stroke-width="2"/>
<path d="M12 66 23 27h144l11 39-9 8H20z" fill="url(#cdtop)" stroke="#211712" stroke-width="2"/>
<path d="m23 29 144 0M17 66h156" stroke="#a47a51" stroke-width="2" opacity=".78"/>
<path d="m47 55 34-3-4-21-34 4z" fill="#d9c9a6" stroke="#796d5a"/>
<path d="m51 40 20-2m-19 7 19-2m-18 7 12-1" stroke="#95866e" stroke-width="1"/>
<path d="m72 51 30-2-2-24-31 2z" fill="#d1bd91" stroke="#74654d"/>
<path d="m77 34 18-1m-17 6 17-1m-16 6 11-1" stroke="#9a8767" stroke-width="1"/>
<path d="m104 24 11 0 5 27-11 2z" fill="#282522" stroke="#aaa08c" stroke-width="1"/>
<circle cx="110" cy="36" r="4" fill="#baab8f"/><circle cx="110" cy="36" r="1.2" fill="#201e1b"/>
<path d="M145 43q8 0 8 6v7h-17v-7q0-6 9-6z" fill="#34302c" stroke="#a99172"/>
<path d="M140 44v-2a5 5 0 0 1 10 0v2" fill="none" stroke="#c0a77c" stroke-width="1.5"/>
<path d="m81 66 6-5 6 5" fill="none" stroke="#ad7557" stroke-width="2" opacity=".9"/>
</svg>"""

SVG_RECORDS_TABLE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 116" width="180" height="116">
<defs><linearGradient id="rtsteel" x2="0" y2="1"><stop stop-color="#686964"/><stop offset="1" stop-color="#363936"/></linearGradient></defs>
<ellipse cx="90" cy="105" rx="77" ry="8" fill="#090b0d" opacity=".42"/>
<path d="M25 56h12v45H25zm118 0h12v45h-12z" fill="#303432"/><path d="m19 55 8-25h126l8 25-8 8H27z" fill="url(#rtsteel)" stroke="#232725" stroke-width="2"/>
<path d="m37 48 44-4-2-22-43 4z" fill="#d5c9aa" stroke="#7f7562"/><path d="m45 33 24-2m-23 8 29-2" stroke="#988c76"/>
<path d="m89 45 37-3-3-28-38 3z" fill="#b89c70" stroke="#695843"/><path d="m96 25 21-2m-20 8 19-2" stroke="#766449"/>
<circle cx="139" cy="38" r="9" fill="#555a55" stroke="#b19a70"/><circle cx="139" cy="38" r="5" fill="#252b2a"/><path d="M139 38 142 33" stroke="#ddd0ae"/>
<path d="M49 62h81v5H49z" fill="#afb3ab" opacity=".45"/>
</svg>"""

SVG_AUDIO_CONSOLE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 190 132" width="190" height="132">
<defs><linearGradient id="acwood" x2="0" y2="1"><stop stop-color="#51463b"/><stop offset="1" stop-color="#292725"/></linearGradient><linearGradient id="acmetal" x2="0" y2="1"><stop stop-color="#aaa99b"/><stop offset="1" stop-color="#555a59"/></linearGradient></defs>
<ellipse cx="95" cy="119" rx="82" ry="9" fill="#06080a" opacity=".48"/>
<path d="M26 66h138v43H26z" fill="url(#acwood)" stroke="#211e1b" stroke-width="2"/><path d="M34 74h122v29H34z" fill="#292522" stroke="#70604b"/>
<path d="m14 65 12-40h138l12 40-10 8H24z" fill="#49443d" stroke="#1e1c19" stroke-width="2"/><path d="m24 63 142 0" stroke="#b09c77" stroke-width="2"/>
<rect x="45" y="29" width="100" height="30" rx="3" fill="#252a29" stroke="#aaa28f" stroke-width="2"/>
<circle cx="70" cy="43" r="12" fill="url(#acmetal)" stroke="#201f1c" stroke-width="2"/><circle cx="70" cy="43" r="7" fill="#252a2a"/><circle cx="70" cy="43" r="2" fill="#b8b9af"/>
<circle cx="119" cy="43" r="12" fill="url(#acmetal)" stroke="#201f1c" stroke-width="2"/><circle cx="119" cy="43" r="7" fill="#252a2a"/><circle cx="119" cy="43" r="2" fill="#b8b9af"/>
<path d="M82 38h25v10H82z" fill="#111614" stroke="#65716c"/><path d="m86 43 16-2" stroke="#c3ab73" stroke-width="1.5"/>
<circle cx="53" cy="58" r="2" fill="#d77b62"/><circle cx="61" cy="58" r="2" fill="#c7b67e"/><path d="M77 66q18 12 36 0" fill="none" stroke="#b4a17e" stroke-width="1.4"/>
<path d="M45 83h38m-38 5h30" stroke="#9a8a70" stroke-width="1" opacity=".65"/>
<path d="M140 80v14m-4-7h8" stroke="#a78955" stroke-width="2"/>
</svg>"""

SVG_EXECUTIVE_DESK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 190 128" width="190" height="128">
<defs><linearGradient id="edwood" x2="0" y2="1"><stop stop-color="#443b34"/><stop offset="1" stop-color="#211f1d"/></linearGradient><linearGradient id="edtop" x2="0" y2="1"><stop stop-color="#675746"/><stop offset="1" stop-color="#3b332c"/></linearGradient></defs>
<ellipse cx="95" cy="115" rx="84" ry="9" fill="#050607" opacity=".5"/><path d="M22 66h146v43H22z" fill="url(#edwood)" stroke="#191817" stroke-width="2"/>
<path d="M30 76h37v27H30zm91 0h37v27h-37z" fill="#302a25" stroke="#85725b"/><path d="M36 84h25m-25 8h25m66-8h25m-25 8h25" stroke="#181716" stroke-width="2"/>
<path d="m12 63 11-38h144l11 38-10 8H22z" fill="url(#edtop)" stroke="#201d19" stroke-width="2"/><path d="M21 62h148" stroke="#b59a70" stroke-width="2"/>
<rect x="47" y="30" width="68" height="25" rx="2" fill="#d8d1bf" stroke="#8f8879"/><path d="m54 37 46-1m-46 6h41m-40 6h31" stroke="#928b7c"/>
<rect x="122" y="32" width="23" height="21" rx="2" fill="#282b2a" stroke="#a28d68"/><path d="M126 37h15m-15 4h15m-15 4h10" stroke="#72807a"/>
<path d="M35 52q12-8 21 0" fill="none" stroke="#1c211d" stroke-width="3"/><circle cx="43" cy="45" r="4" fill="#d2bd8b"/>
<path d="M151 29v-7m-5 7h11l-3 7h-5z" fill="#344334" stroke="#bea36d" stroke-width="1.4"/><path d="M151 36 146 50" stroke="#bea36d" stroke-width="2"/>
</svg>"""

SVG_TASK_CHAIR = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 84 88" width="84" height="88">
<defs><linearGradient id="chleather" x2="0" y2="1"><stop stop-color="#684b38"/><stop offset="1" stop-color="#302720"/></linearGradient></defs>
<ellipse cx="42" cy="80" rx="34" ry="6" fill="#070809" opacity=".44"/>
<path d="M20 18q0-8 9-8h26q9 0 9 8v31H20z" fill="url(#chleather)" stroke="#201914" stroke-width="2"/>
<path d="M27 16v27m15-30v32m15-29v27" stroke="#a17b58" stroke-width="1" opacity=".65"/><path d="M17 47h50l-4 18H21z" fill="#463328" stroke="#1f1a16" stroke-width="2"/>
<path d="M25 64 22 77m37-13 3 13M23 76h-5m47 0h-5" stroke="#282a29" stroke-width="4" stroke-linecap="round"/><path d="M26 52h33" stroke="#b19470" opacity=".55"/>
</svg>"""

SVG_WASTEBASKET = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 62" width="52" height="62">
<ellipse cx="26" cy="56" rx="20" ry="5" fill="#050607" opacity=".4"/><path d="m9 16 34 0-5 37H14z" fill="#35383a" stroke="#17191a" stroke-width="2"/>
<path d="M15 23v23m8-24v25m8-25v25m8-24v23" stroke="#606569" stroke-width="2"/><path d="M7 15h38v6H7z" fill="#777266" stroke="#242625"/>
<path d="m15 12 12-7 10 6-5 5-14-1z" fill="#c1b69f" stroke="#716c62"/><path d="m27 6 4 7" stroke="#877e6f"/>
</svg>"""

SVG_ACOUSTIC_PANEL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 62" width="100" height="62">
<rect x="5" y="5" width="90" height="52" rx="3" fill="#292d30" stroke="#121619" stroke-width="3"/><rect x="10" y="10" width="80" height="42" fill="#34383a" stroke="#66635a"/>
<path d="M10 13h80m-80 8h80m-80 8h80m-80 8h80m-80 8h80" stroke="#202629" stroke-width="4"/><path d="m13 12 74 38m0-38L13 50" stroke="#4d5150" stroke-width="1" opacity=".45"/>
</svg>"""

SVG_DIRECTORATE_SEAL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 82" width="96" height="82">
<ellipse cx="48" cy="75" rx="38" ry="4" fill="#080a0c" opacity=".35"/>
<rect x="7" y="5" width="82" height="67" rx="3" fill="#292f33" stroke="#151a1d" stroke-width="3"/>
<rect x="12" y="10" width="72" height="57" fill="#373f42" stroke="#7d7867"/>
<circle cx="48" cy="37" r="21" fill="#252b2d" stroke="#a89262" stroke-width="2"/><circle cx="48" cy="37" r="16" fill="none" stroke="#65706d"/>
<path d="M42 48V26h9q8 0 8 6 0 4-4 5 6 1 6 5 0 6-9 6zm5-13h4q3 0 3-3t-3-3h-4zm0 9h5q4 0 4-3t-4-3h-5z" fill="#bca879"/>
<path d="m21 16 3 2m48-2-3 2M21 58l3-2m48 2-3-2" stroke="#bca879" stroke-width="2"/>
</svg>"""

SVG_EVIDENCE_MARKER = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 48" width="44" height="48">
<path d="m22 3 20 39H2z" fill="#d4b05b" stroke="#3d3425" stroke-width="2"/><path d="m22 12 12 24H10z" fill="#ead38e"/>
<path d="m20 21 4-3v14m-5 0h10" fill="none" stroke="#30291e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
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
        'safe': render_svg(SVG_WALL_SAFE, 80, 90),
        'autopsy_table': render_svg(SVG_AUTOPSY_TABLE, 170, 100),
        'prison_bars': render_svg(SVG_PRISON_BARS, 160, 120),
        'interrogation_table': render_svg(SVG_INTERROGATION_TABLE, 160, 110),
        'treasure_chest': render_svg(SVG_TREASURE_CHEST, 74, 64),
        'specimen_cabinet': render_svg(SVG_SPECIMEN_CABINET, 74, 110),
        'crime_desk': render_svg(SVG_CRIME_DESK, 190, 130),
        'records_table': render_svg(SVG_RECORDS_TABLE, 180, 116),
        'audio_console': render_svg(SVG_AUDIO_CONSOLE, 190, 132),
        'executive_desk': render_svg(SVG_EXECUTIVE_DESK, 190, 128),
        'chair': render_svg(SVG_TASK_CHAIR, 84, 88),
        'wastebasket': render_svg(SVG_WASTEBASKET, 52, 62),
        'acoustic_panel': render_svg(SVG_ACOUSTIC_PANEL, 100, 62),
        'directorate_seal': render_svg(SVG_DIRECTORATE_SEAL, 96, 82),
        'evidence_marker': render_svg(SVG_EVIDENCE_MARKER, 44, 48),
    }

