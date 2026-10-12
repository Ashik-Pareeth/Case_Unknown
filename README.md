# Case Unknown: A 2D Detective Mystery Game

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=flat)](https://www.pygame.org/)
[![Graphics](https://img.shields.io/badge/Graphics-Pure%20SVG%20Vector-orange?style=flat)](https://github.com/Ashik-Pareeth/Case_Unknown)

A 2D top-down detective mystery and investigation adventure developed in **Python** and **Pygame**. 

Players assume the role of a detective trainee investigating interconnected cases, uncovering hidden evidence, and discovering a recurring mysterious symbol that hints at a conspiracy reaching inside the detective unit itself.

---

## Key Features

- **Pure SVG Vector Graphics Pipeline**:
  - All character animations, furniture, and environmental objects are coded directly in Python as standalone SVGs in `assets/svg_assets.py`.
  - Zero external raster sprite sheets or PNG files are used.
  - Native runtime SVG compilation and per-pixel alpha caching via Pygame NanoSVG at 60 FPS.

- **High-Quality Detective Sprite Animations**:
  - Full 4-directional movement (`Down`, `Up`, `Right`, `Left`).
  - **Walk Cycles**: Smooth 4-frame stride cycles with foot plants, arm swings, coat flair, and fedora bobbing.
  - **Idle States**: Subtle 2-frame breathing and coat adjustments.

- **Atmospheric Detective Office Room**:
  - Hardwood parquet flooring with staggered plank seams and baseboard trims.
  - Solid collision boundaries and 2.5D depth/Z-sorting so the character moves realistically in front of and behind furniture.
  - Atmospheric ambient lighting: warm banker's desk lamp glow, wall sconces, and slatted window moonlight beams.

- **Interactive Investigation System**:
  - Distance-based interaction with animated floating `[E] Inspect` badges.
  - Clue examination modals displaying detailed observations for:
    - **Detective's Desk** (Workstation dossiers & notes)
    - **Evidence Pinboard** (Crime scene photos, red strings & the mysterious spiral glyph)
    - **Confidential Filing Cabinet** (Tampered lock & archived records)
    - **Forensic Bookshelf** (Case laws & internal audit protocols)
    - **Venetian Blind Windows** (Rainy streetlamp backdrop)
    - **Chesterfield Leather Sofa** & **Office Plant**

---

## Project Structure

```text
Case_Unknown/
├── assets/
│   ├── __init__.py
│   └── svg_assets.py          # Pure SVG vector assets, animation frames & surface cache
├── src/
│   ├── __init__.py
│   ├── settings.py            # Screen resolution, framerate, palette, physics constants
│   ├── player.py              # Animated player entity, state machine & collision
│   ├── room.py                # Office room environment, parquet floor & furniture layout
│   ├── interaction.py         # Proximity detection, inspect prompt & dialogue modals
│   └── main.py                # 60 FPS main game loop with depth-sorting (Z-ordering)
├── tests/
│   ├── test_game.py           # Automated headless test suite
│   └── render_character_preview.py  # Character sprite animation preview generator
├── .gitignore                 # Git ignore rules (virtual environment, notes, cache)
└── README.md                  # Project documentation
```

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ashik-Pareeth/Case_Unknown.git
   cd Case_Unknown
   ```

2. **Activate the virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     .\.venv\Scripts\activate.bat
     ```
   - **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install pygame==2.6.1
   ```

---

## Running the Game

Launch the application using Python:
```powershell
python src/main.py
```

### Controls

| Action | Keybinding |
| :--- | :--- |
| **Move Detective** | `W` `A` `S` `D` or `Arrow Keys` |
| **Inspect Clue / Object** | `E` or `Space` (when near interactive items) |
| **Close Dialog Modal** | `E`, `Space`, or `ESC` |
| **Exit Game** | `ESC` or Window Close (`X`) |

---

## Running Automated Tests

Run the headless verification suite:
```powershell
python tests/test_game.py
```
This verifies:
- SVG compilation of all directional frames and furniture surfaces.
- Animation cycle integrity and dimensions.
- Collision resolution and physics bounding boxes.
- Proximity detection and dialog opening/closing.
- Zero references to legacy external images.
