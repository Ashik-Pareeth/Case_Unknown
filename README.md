# Case Unknown: A 2D Detective Mystery Game

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=flat)](https://www.pygame.org/)
[![Graphics](https://img.shields.io/badge/Graphics-SVG%20Vector%20%2B%20Noir%20Art-orange?style=flat)](https://github.com/Ashik-Pareeth/Case_Unknown)

A 2D top-down noir detective mystery, puzzle, and stealth investigation adventure developed in Python and Pygame.

Players take on the role of an investigator exploring an interconnected, restricted police precinct. Uncover hidden evidence dossiers, decrypt combination safes and security keypads, navigate an interactive blueprint map, and evade vigilant patrolling mob guards who monitor the corridors.

---

## Key Features

- **Multi-Sector Precinct Investigation**:
  - Nine fully realized, interconnected precinct sectors:
    - **Crime Scene**: The initial investigation incident room.
    - **Detective Office**: Precinct 13 central coordination squad room and command desk.
    - **Evidence Archive**: Classified evidence lockers, case statute shelves, and secure vault.
    - **Morgue**: Autopsy suite, specimen cabinets, and forensic storage lockers.
    - **Detention Lockup**: High-security cell block, iron bars, and guard station.
    - **Interrogation Room**: Soundproofed interview chamber and one-way observation mirror.
    - **Records Room**: Historic county ledgers, archive cabinets, and clerk workstations.
    - **Recording Room**: Reel-to-reel audio consoles, surveillance tape spools, and wiretap station.
    - **Restricted Office**: Directorate executive office, lounge suite, and confidential vault.
  - Room-to-room transitions with door clearance requirements, PIN keypad gates, and brass key locks.

- **Stealth AI & Patrolling Mob Guards**:
  - Distinctive mob guard vector sprites styled with wide top hats, dark overcoats, and full-face masks, alongside an inner-room Fixer variant.
  - **Predetermined Invisible Looping Patrols**: Guards follow complex, multi-point routes winding naturally around desks, shelves, and room obstacles without colliding.
  - **Dynamic Vision Cones**: Forward-projecting 70-degree viewpoint fields with line-of-sight obstruction detection. Solid furniture and walls realistically block guard sightlines.
  - **Doorway Stare Prevention**: Guards actively avoid aiming their vision cones directly at doors for extended periods (capped below 0.30 seconds) and automatically look away during idle pauses to keep passageways accessible for stealth navigation.
  - **Detection & Permadeath**: Entering an alert guard's line of sight triggers immediate apprehension and an interactive Game Over screen with save file clearance.

- **Evidence Dossier & Case Progression**:
  - Narrative progression model tracking each clue through four states: `Undiscovered -> Discovered -> Recorded -> Connected`.
  - **Interactive Observation Popups**: Evidence examination cards displaying high-resolution noir illustrations and vintage documents with fallback paper rendering.
  - **3-Tab Detective Case Journal** (`J` key):
    - **Discovered Evidence**: Review collected dossiers, transcripts, and photographic evidence.
    - **Clue Connections**: Trace links between suspects, symbols, and murder weapons.
    - **Active Leads**: Track real-time objectives and precinct directives.

- **Security Puzzles & Cryptography**:
  - Interactive mini-game puzzle interfaces including 3-digit combination safes, keypad PIN locks, and tile alignment systems.
  - Clues and combinations embedded in environmental notes, desk memos, and archived reports.

- **Blueprint Precinct Map** (`M` or `Tab` key):
  - Real-time architectural blueprint showing discovered sectors, interconnected doorways, locked access gates, and player position.

- **Hybrid Graphics & Lighting Pipeline**:
  - Procedural SVG vector graphics for all character walk cycles, mob guard animations, furniture, and room architecture with native surface caching.
  - 2.5D depth-sorting (Z-ordering) allowing characters to walk realistically in front of and behind desks, sofas, and partitions.
  - Atmosphere-driven ambient tinting, warm desk lamps, wall sconces, and slatted window moonlight rays.

- **Local State Persistence**:
  - Robust JSON-based save manager (`save_game.json`) automatically persisting player position, current sector, visited rooms, collected evidence, and unlocked gates.

---

## Project Structure

```text
Case_Unknown/
├── assets/
│   ├── characters.py              # Detective vector animation frames (4 directions)
│   ├── props.py                   # Vector furniture, architectural props, and lighting
│   ├── renderer.py                # Vector compilation and per-pixel alpha surface cache
│   ├── svg_assets.py              # Centralized vector asset catalog
│   ├── assets/                    # High-resolution noir clue cards and popup artwork
│   └── npcs/
│       ├── __init__.py
│       └── characters.py          # Mob guard vector sprite definitions and variants
├── src/
│   ├── __init__.py
│   ├── settings.py                # Display dimensions, framerate, theme palettes, physics
│   ├── main.py                    # Main game loop, state machine, and event dispatcher
│   ├── player.py                  # Detective controller, animation states, collision
│   ├── npc.py                     # Autonomous NPC patrols, vision cones, loop routes
│   ├── room.py                    # Sector environment renderer, doors, collision walls
│   ├── rooms_data.py              # Complete data definitions for all 9 precinct sectors
│   ├── interaction.py             # Proximity detection, inspect prompts, observation cards
│   ├── evidence_manager.py        # Evidence states, directives, and connection tracking
│   ├── evidence_reveal.py         # Evidence discovery and examination presentation modal
│   ├── journal_view.py            # 3-tab Detective Case Journal modal (J key)
│   ├── map_view.py                # Precinct blueprint map overlay (M / Tab key)
│   ├── menu.py                    # Main start, pause, and options menu system
│   ├── puzzles.py                 # Number lock dials, keypads, and puzzle mechanics
│   ├── game_over.py               # Game Over screen on guard capture with save reset
│   ├── save_manager.py            # Local JSON save/load persistence (save_game.json)
│   ├── treasure.py                # Hidden evidence nodes and locked cache points
│   └── ui/
│       ├── __init__.py
│       ├── primitives.py          # UI drawing utilities, panels, and borders
│       ├── evidence_reader.py     # Dossier transcript reader widgets
│       ├── interaction_prompt.py  # Floating proximity interaction badges
│       └── puzzle.py              # Interactive puzzle UI components
├── tests/
│   ├── test_game.py               # Core mechanics, vector compilation, collision tests
│   ├── test_game_over_and_viewpoint.py # Vision raycasting, obstruction, game over tests
│   ├── test_predetermined_loop_patrol.py # Multi-point looping routes and door safety tests
│   ├── test_directives_progression.py   # Narrative directives and progression tests
│   ├── render_character_preview.py      # Character sprite preview generator
│   └── render_game_previews.py          # Environmental sector preview renderer
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Project Python dependencies
└── README.md                      # Comprehensive project documentation
```

---

## Installation & Setup

### Prerequisites

- **Python**: Version 3.10 or higher (Python 3.13 recommended)
- **Pip**: Standard Python package installer

### 1. Clone the Repository

```bash
git clone https://github.com/Ashik-Pareeth/Case_Unknown.git
cd Case_Unknown
```

### 2. Create and Activate a Virtual Environment

- **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```

- **Windows (Command Prompt)**:
  ```cmd
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  ```

- **Linux / macOS**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies

Install the required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## Running the Game

Launch the application directly from the repository root:
```bash
python src/main.py
```

### Controls

| Action | Keybinding |
| :--- | :--- |
| **Move Detective** | `W` `A` `S` `D` or `Arrow Keys` |
| **Inspect / Interact** | `E` or `Space` (near interactive items, doors, safes) |
| **Open Detective Journal** | `J` |
| **Open Blueprint Map** | `M` or `Tab` |
| **Pause / Main Menu** | `ESC` |
| **Toggle Fullscreen** | `F11` or `F` |
| **Close Modal / Dialogue** | `E`, `Space`, or `ESC` |
| **Navigate UI / Dials** | `Arrow Keys`, `Mouse Click`, or `0`-`9` number keys |
| **Exit Application** | `ESC` (from main menu) or Window Close button |

---

## Running Automated Tests

Run the complete headless test suite using Python's built-in `unittest` runner:
```bash
python -m unittest discover tests
```

### Test Coverage Highlights

- **`test_game.py`**: Validates vector compilation, animation frame dimensions, player physics, collision boundaries, and interaction prompts.
- **`test_game_over_and_viewpoint.py`**: Tests vision polygon calculation, player ground-contact detection, solid wall and furniture line-of-sight obstruction, and permadeath save clearing.
- **`test_predetermined_loop_patrol.py`**: Validates all 24 predetermined looping patrol circuits across all precinct rooms, confirming collision-free paths and verifying that guard vision cones never linger on doors for extended periods.
- **`test_directives_progression.py`**: Verifies evidence state transitions, gate unlocking, clue connections, and narrative progression.
