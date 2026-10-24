"""
Precinct Room Configurations & Environmental Blueprints for Case Unknown.

Defines all 5 interconnected precinct sectors with unique architectural themes,
floor styles, door passages, furniture placement, clues, and treasure points.
"""

from src.settings import (
    COLOR_WALL,
    COLOR_WALL_TOP,
    COLOR_WALL_BASE,
    COLOR_FLOOR_A,
    COLOR_FLOOR_B,
    COLOR_FLOOR_SEAM,
)

ROOMS_DATA = {
    # =========================================================================
    # 1. PRECINCT DETECTIVE OFFICE (Central Command)
    # =========================================================================
    "office": {
        "id": "office",
        "name": "Detective Office — Precinct 13",
        "subtitle": "Central detective squad room and case coordination desk",
        "floor_style": "parquet",
        "colors": {
            "wall": COLOR_WALL,
            "wall_top": COLOR_WALL_TOP,
            "wall_base": COLOR_WALL_BASE,
            "floor_a": (50, 38, 30),
            "floor_b": (44, 34, 26),
            "floor_seam": (32, 24, 18),
        },
        "lighting": {
            "ambient_tint": (255, 220, 150, 18),
            "warm_lamps": [(420, 275)],
            "sconces": [(110, 55), (850, 55)],
            "moon_rays": [
                [(170, 95), (250, 95), (290, 230), (130, 230)],
                [(710, 95), (790, 95), (830, 230), (670, 230)],
            ],
        },
        "doors": [
            {
                "wall": "right",
                "target_room": "archive",
                "target_pos": (130, 350),
                "label": "East Hallway -> Evidence Archive",
            },
            {
                "wall": "bottom",
                "target_room": "lockup",
                "target_pos": (480, 175),
                "label": "South Stairwell -> Detention Lockup",
            },
        ],
        "wall_decor": [
            {"prop": "window", "pos": (170, 16)},
            {"prop": "window", "pos": (710, 16)},
            {"prop": "evidence_board", "pos": (395, 20)},
            {"prop": "sconce", "pos": (90, 35)},
            {"prop": "sconce", "pos": (830, 35)},
        ],
        "floor_decor": [
            {"prop": "rug", "pos": (370, 240)},
        ],
        "furniture": [
            {
                "prop": "bookshelf",
                "pos": (100, 105),
                "hitbox": (102, 185, 80, 48),
                "id": "bookshelf",
                "name": "Case Archive Library",
                "description": "Stacked district criminal codes and penal statute books. Tucked in the shelf is an old 1928 Precinct founding journal.",
            },
            {
                "prop": "desk",
                "pos": (390, 245),
                "hitbox": (398, 290, 164, 65),
                "id": "desk",
                "name": "Detective's Desk",
                "description": "Your workstation. A handwritten memo reads: 'Check the brass wall safe. Founding year was 1928 — code uses first 3 digits: 1-9-2'.",
            },
            {
                "prop": "filing_cabinet",
                "pos": (780, 120),
                "hitbox": (784, 170, 56, 42),
                "id": "filing_cabinet",
                "name": "Confidential Filing Cabinet",
                "description": "Steel drawers containing unsolved crime reports. Someone hastily jotted 'Archive door is unlocked to the east'.",
            },
            {
                "prop": "sofa",
                "pos": (110, 390),
                "hitbox": (118, 435, 154, 50),
                "id": "sofa",
                "name": "Chesterfield Leather Sofa",
                "description": "Worn burgundy leather couch for witness testimonies. Smells of pipe tobacco and damp raincoats.",
            },
            {
                "prop": "plant",
                "pos": (780, 440),
                "hitbox": (792, 480, 36, 32),
                "id": "plant",
                "name": "Office Monstera Plant",
                "description": "Glossy green leaves watered faithfully by the department clerk.",
            },
            {
                "prop": "safe",
                "pos": (600, 120),
                "hitbox": (604, 160, 72, 45),
                "id": "office_safe",
                "name": "Precinct Commander's Wall Safe",
                "description": "Heavy reinforced steel safe with a 3-digit brass dial lock.",
                "is_treasure": True,
            },
        ],
        "interactables": [
            {
                "id": "window_left",
                "name": "Venetian Blind Window",
                "description": "Rain trickles down the dark glass. Red neon signs flicker faintly in the foggy streets outside.",
                "trigger_rect": (160, 95, 100, 50),
                "badge_pos": (210, 110),
            },
            {
                "id": "evidence_board",
                "name": "Case Pinboard",
                "description": "Photographs connected with red twine. At the center is a recurring crimson spiral symbol discovered across the city.",
                "trigger_rect": (385, 95, 190, 50),
                "badge_pos": (480, 105),
            },
        ],
    },

    # =========================================================================
    # 2. FORENSIC EVIDENCE ARCHIVE (Central Hub)
    # =========================================================================
    "archive": {
        "id": "archive",
        "name": "Forensic Evidence Archive",
        "subtitle": "Sealed evidence vault, chain-of-custody ledgers, and forensic repository",
        "floor_style": "tiles",
        "colors": {
            "wall": (32, 42, 46),
            "wall_top": (44, 58, 64),
            "wall_base": (22, 28, 32),
            "floor_a": (30, 48, 52),
            "floor_b": (24, 38, 42),
            "floor_seam": (16, 24, 28),
        },
        "lighting": {
            "ambient_tint": (160, 225, 230, 14),
            "warm_lamps": [(480, 280)],
            "sconces": [(120, 55), (840, 55)],
            "moon_rays": [],
        },
        "doors": [
            {
                "wall": "left",
                "target_room": "office",
                "target_pos": (820, 350),
                "label": "West Hallway -> Detective Office",
            },
            {
                "wall": "top",
                "target_room": "morgue",
                "target_pos": (480, 520),
                "label": "North Corridor -> Cold Storage & Morgue",
            },
            {
                "wall": "right",
                "target_room": "interrogation",
                "target_pos": (130, 350),
                "label": "East Security Gate -> Interrogation Chamber",
            },
        ],
        "wall_decor": [
            {"prop": "evidence_board", "pos": (395, 20)},
            {"prop": "sconce", "pos": (120, 35)},
            {"prop": "sconce", "pos": (840, 35)},
        ],
        "floor_decor": [],
        "furniture": [
            {
                "prop": "filing_cabinet",
                "pos": (110, 120),
                "hitbox": (114, 170, 56, 42),
                "id": "archive_cab_1",
                "name": "Cold Case Drawer #04",
                "description": "Steel drawers labeled 'Chain of Custody'. An index card reads: 'To open Vault Box, align all 4 compass dials clockwise: North, East, South, West'.",
            },
            {
                "prop": "filing_cabinet",
                "pos": (180, 120),
                "hitbox": (184, 170, 56, 42),
                "id": "archive_cab_2",
                "name": "Ballistics Dossiers",
                "description": "Ballistic comparison slides and slug casings wrapped in sealed cotton.",
            },
            {
                "prop": "bookshelf",
                "pos": (780, 110),
                "hitbox": (782, 185, 80, 48),
                "id": "archive_shelf",
                "name": "Forensic Ledger Bookshelf",
                "description": "Heavy leather-bound ledgers dating back forty years of city investigations.",
            },
            {
                "prop": "desk",
                "pos": (390, 260),
                "hitbox": (398, 305, 164, 65),
                "id": "archive_desk",
                "name": "Archivist Examination Table",
                "description": "A metal desk with magnifying glass, tweezers, and evidence seal envelopes.",
            },
            {
                "prop": "treasure_chest",
                "pos": (750, 440),
                "hitbox": (754, 465, 66, 35),
                "id": "archive_vault",
                "name": "Archival Evidence Vault Strongbox",
                "description": "Reinforced iron strongbox locked with a 4-dial forensic compass mechanism.",
                "is_treasure": True,
            },
        ],
        "interactables": [
            {
                "id": "archive_board",
                "name": "District Crime Map",
                "description": "A blueprint schematic of the district waterfront and shipping docks marked with contraband transit routes.",
                "trigger_rect": (385, 95, 190, 50),
                "badge_pos": (480, 105),
            },
        ],
    },

    # =========================================================================
    # 3. COLD STORAGE & MORGUE (North Sector)
    # =========================================================================
    "morgue": {
        "id": "morgue",
        "name": "Cold Storage & Forensic Morgue",
        "subtitle": "Pathology laboratory, refrigerated lockers, and post-mortem examination",
        "floor_style": "tiles",
        "colors": {
            "wall": (28, 36, 42),
            "wall_top": (38, 48, 56),
            "wall_base": (18, 24, 28),
            "floor_a": (36, 46, 52),
            "floor_b": (30, 40, 46),
            "floor_seam": (20, 26, 30),
        },
        "lighting": {
            "ambient_tint": (140, 200, 235, 22),
            "warm_lamps": [],
            "sconces": [(120, 55), (840, 55)],
            "moon_rays": [
                [(440, 95), (520, 95), (560, 260), (400, 260)],
            ],
        },
        "doors": [
            {
                "wall": "bottom",
                "target_room": "archive",
                "target_pos": (480, 175),
                "label": "South Passage -> Evidence Archive",
            },
        ],
        "wall_decor": [
            {"prop": "window", "pos": (440, 16)},
            {"prop": "sconce", "pos": (120, 35)},
            {"prop": "sconce", "pos": (840, 35)},
        ],
        "floor_decor": [],
        "furniture": [
            {
                "prop": "autopsy_table",
                "pos": (390, 240),
                "hitbox": (405, 275, 140, 60),
                "id": "autopsy_table",
                "name": "Forensic Autopsy Table",
                "description": "Stainless steel examination table. A clipboard notes: 'Toxicology batch synthesized under code 8-4-1-6 for cold cryo locker.'",
            },
            {
                "prop": "specimen_cabinet",
                "pos": (110, 120),
                "hitbox": (116, 170, 62, 45),
                "id": "specimen_cabinet",
                "name": "Chemical Specimen Cabinet",
                "description": "Jars of colored chemical reagents and organ specimens suspended in formalin.",
            },
            {
                "prop": "filing_cabinet",
                "pos": (780, 120),
                "hitbox": (784, 170, 56, 42),
                "id": "morgue_cabinet",
                "name": "Pathologist Records",
                "description": "Case autopsy logs detailing chemical toxin analysis.",
            },
            {
                "prop": "safe",
                "pos": (760, 390),
                "hitbox": (764, 430, 72, 45),
                "id": "morgue_locker",
                "name": "Cryo Specimen Storage Locker",
                "description": "Deep freeze steel safe chilled with liquid coolant. Uses a 4-digit combination.",
                "is_treasure": True,
            },
        ],
        "interactables": [
            {
                "id": "chalk_outline",
                "name": "Forensic Floor Outline",
                "description": "White chalk markings on the cold tiles marking where the courier collapsed before reaching the chief's desk.",
                "trigger_rect": (220, 350, 120, 80),
                "badge_pos": (280, 390),
            },
        ],
    },

    # =========================================================================
    # 4. DETENTION LOCKUP (South Sector)
    # =========================================================================
    "lockup": {
        "id": "lockup",
        "name": "Precinct Detention Lockup",
        "subtitle": "Holding block, iron cell gates, and contraband seizure lockers",
        "floor_style": "stone",
        "colors": {
            "wall": (30, 30, 34),
            "wall_top": (42, 42, 48),
            "wall_base": (20, 20, 24),
            "floor_a": (38, 38, 42),
            "floor_b": (32, 32, 36),
            "floor_seam": (22, 22, 26),
        },
        "lighting": {
            "ambient_tint": (255, 190, 120, 16),
            "warm_lamps": [(240, 290)],
            "sconces": [(100, 55), (860, 55)],
            "moon_rays": [],
        },
        "doors": [
            {
                "wall": "top",
                "target_room": "office",
                "target_pos": (480, 520),
                "label": "North Stairs -> Detective Office",
            },
        ],
        "wall_decor": [
            {"prop": "sconce", "pos": (100, 35)},
            {"prop": "sconce", "pos": (860, 35)},
        ],
        "floor_decor": [],
        "furniture": [
            {
                "prop": "prison_bars",
                "pos": (580, 110),
                "hitbox": (580, 160, 160, 50),
                "id": "prison_bars_1",
                "name": "Cell Block Alpha",
                "description": "Heavy wrought iron cell gate. Scratched on the inner door is a cryptic cipher: 'Pins alternate Down, Up, Down, Up (180, 0, 180, 0)'.",
            },
            {
                "prop": "prison_bars",
                "pos": (740, 110),
                "hitbox": (740, 160, 160, 50),
                "id": "prison_bars_2",
                "name": "Cell Block Beta",
                "description": "A dark empty holding cell with a wooden cot bolted to the floor.",
            },
            {
                "prop": "desk",
                "pos": (160, 260),
                "hitbox": (168, 305, 164, 65),
                "id": "guard_station",
                "name": "Correctional Guard Desk",
                "description": "The precinct guard's post. A ledger logs suspect property confiscated upon booking.",
            },
            {
                "prop": "treasure_chest",
                "pos": (680, 430),
                "hitbox": (684, 455, 66, 35),
                "id": "lockup_stash",
                "name": "Smuggled Contraband Strongbox",
                "description": "A contraband box hidden beneath a loose floor tile, locked with alternating pin dials.",
                "is_treasure": True,
            },
        ],
        "interactables": [
            {
                "id": "cell_wall_clue",
                "name": "Carved Graffiti Inscription",
                "description": "'Trust no one with the key. The locket lies in the floor stash.'",
                "trigger_rect": (560, 240, 120, 60),
                "badge_pos": (620, 260),
            },
        ],
    },

    # =========================================================================
    # 5. INTERROGATION CHAMBER (East Sector)
    # =========================================================================
    "interrogation": {
        "id": "interrogation",
        "name": "Precinct Interrogation Room",
        "subtitle": "Observation booth, reel-to-reel audio wiretap, and witness chamber",
        "floor_style": "concrete",
        "colors": {
            "wall": (24, 26, 30),
            "wall_top": (36, 38, 44),
            "wall_base": (16, 18, 20),
            "floor_a": (32, 34, 38),
            "floor_b": (26, 28, 32),
            "floor_seam": (18, 20, 24),
        },
        "lighting": {
            "ambient_tint": (255, 235, 170, 25),
            "warm_lamps": [(470, 270)],  # Harsh interrogation spotlight
            "sconces": [(120, 55), (840, 55)],
            "moon_rays": [],
        },
        "doors": [
            {
                "wall": "left",
                "target_room": "archive",
                "target_pos": (820, 350),
                "label": "West Exit -> Evidence Archive",
            },
        ],
        "wall_decor": [
            {"prop": "sconce", "pos": (120, 35)},
            {"prop": "sconce", "pos": (840, 35)},
        ],
        "floor_decor": [],
        "furniture": [
            {
                "prop": "interrogation_table",
                "pos": (390, 230),
                "hitbox": (405, 270, 130, 60),
                "id": "interrogation_table",
                "name": "Interrogation Table & Audio Wiretap",
                "description": "Cold steel table with two chairs. A reel-to-reel tape machine has a stamped sticker: 'Statement recorded 03:59 AM (Code 3-5-9)'.",
            },
            {
                "prop": "filing_cabinet",
                "pos": (110, 120),
                "hitbox": (114, 170, 56, 42),
                "id": "interview_files",
                "name": "Suspect Transcripts",
                "description": "Bound interview dossiers and polygraph test ribbons.",
            },
            {
                "prop": "safe",
                "pos": (760, 240),
                "hitbox": (764, 280, 72, 45),
                "id": "interrogation_box",
                "name": "One-Way Mirror Lockbox",
                "description": "A metal lockbox set into the wall behind the one-way mirror. Uses a 3-digit combination.",
                "is_treasure": True,
            },
        ],
        "interactables": [
            {
                "id": "one_way_mirror",
                "name": "One-Way Observation Mirror",
                "description": "Looking into the dark tinted glass, you can see faint silhouettes observing from the detective gallery.",
                "trigger_rect": (380, 95, 180, 50),
                "badge_pos": (470, 105),
            },
        ],
    },
}
