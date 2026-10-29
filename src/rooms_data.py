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
        "floor_decor": [
            {"prop": "wastebasket", "pos": (760, 386)},
        ],
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

    # =========================================================================
    # LEVEL 1 — THE SILENT WITNESS (directives.txt §4)
    # =========================================================================

    # Room 1: The Crime Scene
    "crime_scene": {
        "id": "crime_scene",
        "name": "The Crime Scene — Study of Martin Hale",
        "subtitle": "Level 1 • Where Martin Hale was discovered deceased at his desk",
        "floor_style": "parquet",
        "colors": {
            "wall": COLOR_WALL,
            "wall_top": COLOR_WALL_TOP,
            "wall_base": COLOR_WALL_BASE,
            "floor_a": (48, 36, 28),
            "floor_b": (40, 30, 22),
            "floor_seam": (28, 20, 14),
        },
        "lighting": {
            "ambient_tint": (255, 210, 140, 16),
            "warm_lamps": [(460, 275)],
            "sconces": [(110, 55), (850, 55)],
            "moon_rays": [
                [(170, 95), (250, 95), (290, 230), (130, 230)],
            ],
        },
        "doors": [
            {
                "wall": "right",
                "target_room": "records_room",
                "target_pos": (140, 350),
                "label": "East Hallway -> Records Archive",
                "gate_id": "door_crime_scene_to_records",
                "key_id": "records_room_key",
                "gate_msg": "This door needs a key. Search the crime scene carefully.",
            },
        ],
        "wall_decor": [
            {"prop": "keyhole_door", "pos": (872, 300)},
            {"prop": "window", "pos": (170, 16)},
            {"prop": "evidence_board", "pos": (395, 20)},
            {"prop": "sconce", "pos": (90, 35)},
            {"prop": "sconce", "pos": (830, 35)},
        ],
        "floor_decor": [
            {"prop": "rug", "pos": (370, 240)},
            {"prop": "evidence_marker", "pos": (312, 362)},
            {"prop": "wastebasket", "pos": (798, 450), "hitbox": (807, 485, 36, 20)},
        ],
        "furniture": [
            {
                "prop": "crime_desk",
                "pos": (390, 245),
                "hitbox": (398, 290, 164, 65),
                "id": "hale_desk",
                "name": "Martin Hale's Study Desk",
                "description": "Martin Hale was found seated here. An official Preliminary Incident Log is pinned under the paperweight.",
                "obj_type": "evidence",
                "evidence_id": "hale_autopsy_report",
                "full_text": (
                    "INCIDENT REPORT #4092\n"
                    "Subject: Martin Hale, Senior Archivist.\n"
                    "Found: Seated upright at study desk, sharp trauma to upper torso.\n"
                    "Status: Time of death estimated at 21:40. Office window latched from inside.\n"
                    "Note: Hale's personal diary is missing, but desk drawers remain locked."
                ),
            },
            {
                "prop": "chair",
                "pos": (468, 316),
                "hitbox": (486, 369, 48, 22),
                "id": "pulled_back_chair",
                "name": "Hale's Desk Chair",
                "description": "The chair sits several inches out from the desk, its angle inconsistent with someone who simply stood up.",
                "obj_type": "examinable",
            },
            {
                "prop": "bookshelf",
                "pos": (100, 105),
                "hitbox": (102, 185, 80, 48),
                "id": "hale_bookshelf",
                "name": "Archival Reference Bookshelf",
                "description": "Dusty municipal census records and regional water distribution surveys from 1950 through 1975.",
                "obj_type": "examinable",
            },
            {
                "prop": "filing_cabinet",
                "pos": (780, 120),
                "hitbox": (784, 170, 56, 42),
                "id": "hale_cabinet",
                "name": "Private Filing Cabinet",
                "description": "Personal research correspondence. A folder labelled 'Project Echo (Classified)' has been emptied.",
                "obj_type": "examinable",
            },
            {
                "prop": "sofa",
                "pos": (110, 390),
                "hitbox": (118, 435, 154, 50),
                "id": "hale_sofa",
                "name": "Study Chesterfield Sofa",
                "description": "Worn leather settee with scattered drafts and reference notes.",
                "obj_type": "environmental",
            },
        ],
        "interactables": [
            {
                "id": "hidden_records_key",
                "name": "Brass Passage Key",
                "description": "You find a brass key tucked beneath a loose floorboard near the study desk. It may fit the east passage door.",
                "trigger_rect": (610, 390, 64, 45),
                "badge_pos": (642, 404),
                "obj_type": "examinable",
                "key_id": "records_room_key",
                "full_text": "A small brass key, hidden beneath a loose floorboard. The tag reads: EAST RECORDS PASSAGE.",
            },
            {
                "id": "shattered_watch",
                "name": "Shattered Pocket Chronometer",
                "description": "A heavy gold pocket watch dropped beneath the desk edge. Hands are stopped abruptly at 22:15.",
                "trigger_rect": (330, 285, 60, 50),
                "badge_pos": (360, 310),
                "obj_type": "evidence",
                "evidence_id": "shattered_chronometer",
                "full_text": (
                    "ARTIFACT EXAMINATION:\n"
                    "Heavy brass pocket watch found beneath the desk edge.\n"
                    "The casing was cracked by sudden blunt impact.\n"
                    "Hands are frozen at 22:15. Contradicts the 21:40 time of death in the initial dispatch."
                ),
            },
            {
                "id": "latched_window",
                "name": "Latched Study Window",
                "description": "Heavy wooden casement latched tightly from inside. Rain lashes the glass.",
                "trigger_rect": (170, 95, 100, 50),
                "badge_pos": (220, 110),
                "obj_type": "environmental",
            },
        ],
    },

    # Room 2: The Records Room
    "records_room": {
        "id": "records_room",
        "name": "The Records Room — Directorate Archive",
        "subtitle": "Level 1 • Official dispatch ledgers and municipal registries",
        "floor_style": "concrete",
        "colors": {
            "wall": (38, 42, 50),
            "wall_top": (52, 58, 68),
            "wall_base": (28, 30, 38),
            "floor_a": (36, 38, 44),
            "floor_b": (30, 32, 38),
            "floor_seam": (22, 24, 28),
        },
        "lighting": {
            "ambient_tint": (220, 230, 255, 14),
            "warm_lamps": [(640, 290)],
            "sconces": [(480, 55)],
            "moon_rays": [],
        },
        "doors": [
            {
                "wall": "left",
                "target_room": "crime_scene",
                "target_pos": (820, 350),
                "label": "West Passage -> The Crime Scene",
            },
            {
                "wall": "right",
                "target_room": "recording_room",
                "target_pos": (140, 350),
                "label": "East Hallway -> Audio Recording Room",
                "gate_id": "door_records_to_recording_keypad",
                "pin_code": [4, 1, 7],
                "gate_msg": "The keypad needs a three-digit code.",
                "door_hint": "Look at the railway painting on the wall. Read the three mile markers from left to right.",
            },
        ],
        "wall_decor": [
            {"prop": "keypad_door", "pos": (856, 300)},
            {"prop": "painting", "pos": (610, 18)},
            {"prop": "sconce", "pos": (470, 35)},
            {"prop": "evidence_board", "pos": (395, 20)},
        ],
        "floor_decor": [
            {"prop": "wastebasket", "pos": (760, 386)},
        ],
        "furniture": [
            {
                "prop": "filing_cabinet",
                "pos": (200, 115),
                "hitbox": (204, 165, 56, 42),
                "id": "ledger_cabinet",
                "name": "Dispatch Log Cabinet",
                "description": "Directorate Dispatch Log 1988-B has chemical solvent erasures across October dates.",
                "obj_type": "evidence",
                "evidence_id": "altered_archive_ledger",
                "full_text": (
                    "DIRECTORATE DISPATCH LOG 1988-B:\n"
                    "Entries for October 12-14 show evident chemical erasure.\n"
                    "A faint carbon impression underneath reads: 'Requisition - Dossier Echo 4 - Voss, A.'\n"
                    "Someone altered official records prior to the detective squad arriving."
                ),
            },
            {
                "prop": "records_table",
                "pos": (580, 260),
                "hitbox": (588, 305, 164, 65),
                "id": "clerk_table",
                "name": "Records Inspection Table",
                "description": "Examination desk with ink blotters, chemical solvent bottles, and magnifying glasses.",
                "obj_type": "examinable",
            },
            {
                "prop": "bookshelf",
                "pos": (100, 105),
                "hitbox": (102, 185, 80, 48),
                "id": "county_archives",
                "name": "Municipal County Ledgers",
                "description": "Volumes detailing district budget allocations and historical town council resolutions.",
                "obj_type": "examinable",
            },
        ],
        "interactables": [
            {
                "id": "railway_painting",
                "name": "Railway Painting",
                "description": "A faded railway landscape hangs over the records cabinets. Three mile markers are painted along the track.",
                "trigger_rect": (606, 88, 128, 76),
                "badge_pos": (670, 102),
                "obj_type": "examinable",
                "full_text": "The railway markers read 4, 1, 7 from left to right. The records room keypad likely uses these numbers.",
            },
        ],
    },

    # Room 3: The Recording Room
    "recording_room": {
        "id": "recording_room",
        "name": "The Recording Room — Audio Archive",
        "subtitle": "Level 1 • Sound playback devices and confidential recorded memos",
        "floor_style": "parquet",
        "colors": {
            "wall": (44, 46, 52),
            "wall_top": (60, 64, 72),
            "wall_base": (32, 34, 40),
            "floor_a": (42, 34, 28),
            "floor_b": (36, 28, 22),
            "floor_seam": (24, 18, 14),
        },
        "lighting": {
            "ambient_tint": (255, 215, 140, 18),
            "warm_lamps": [(420, 280)],
            "sconces": [(110, 55), (850, 55)],
            "moon_rays": [],
        },
        "doors": [
            {
                "wall": "left",
                "target_room": "records_room",
                "target_pos": (820, 350),
                "label": "West Passage -> Records Room",
            },
            {
                "wall": "right",
                "target_room": "restricted_office",
                "target_pos": (140, 350),
                "label": "East Passage -> Restricted Office",
            },
        ],
        "wall_decor": [
            {"prop": "sconce", "pos": (90, 35)},
            {"prop": "sconce", "pos": (830, 35)},
            {"prop": "acoustic_panel", "pos": (130, 68)},
            {"prop": "acoustic_panel", "pos": (735, 68)},
        ],
        "floor_decor": [
            {"prop": "rug", "pos": (360, 240)},
            {"prop": "wastebasket", "pos": (594, 369)},
        ],
        "furniture": [
            {
                "prop": "audio_console",
                "pos": (390, 245),
                "hitbox": (398, 290, 164, 65),
                "id": "audio_console",
                "name": "Dictaphone Audio Playback Console",
                "description": "A heavy magnetic reel recorder loaded with Martin Hale's final memo reel.",
                "obj_type": "evidence",
                "evidence_id": "hale_magnetic_tape",
                "full_text": (
                    "AUDIO TRANSCRIPT [REEL EXCERPT]:\n"
                    "HALE (audio raspy): '...if they seal the west archive, it's not to protect the data.\n"
                    "They are burying the personnel rosters. Adrian Voss signed the transfer order himself...\n"
                    "Nora tried to warn them. The town... they never even knew what was tested...'"
                ),
            },
            {
                "prop": "chair",
                "pos": (468, 316),
                "hitbox": (486, 369, 48, 22),
                "id": "recorder_chair",
                "name": "Playback Chair",
                "description": "A chair with one arm polished smooth from repeated use at the reel recorder.",
                "obj_type": "examinable",
            },
            {
                "prop": "bookshelf",
                "pos": (760, 105),
                "hitbox": (762, 185, 80, 48),
                "id": "spool_shelves",
                "name": "Magnetic Reel Vault",
                "description": "Carefully labelled reels containing archived police dispatches and committee testimony.",
                "obj_type": "examinable",
            },
        ],
        "interactables": [],
    },

    # Room 4: The Restricted Office
    "restricted_office": {
        "id": "restricted_office",
        "name": "The Restricted Office — Adrian Voss",
        "subtitle": "Level 1 • Directorate Executive Office & Authorization Vault",
        "floor_style": "parquet",
        "colors": {
            "wall": (35, 38, 45),
            "wall_top": (43, 50, 57),
            "wall_base": (25, 28, 34),
            "floor_a": (34, 36, 38),
            "floor_b": (29, 31, 33),
            "floor_seam": (19, 21, 23),
        },
        "lighting": {
            "ambient_tint": (218, 230, 242, 10),
            "warm_lamps": [(460, 260)],
            "sconces": [(110, 55), (850, 55)],
            "moon_rays": [
                [(710, 95), (790, 95), (830, 230), (670, 230)],
            ],
        },
        "doors": [
            {
                "wall": "left",
                "target_room": "recording_room",
                "target_pos": (820, 350),
                "label": "West Passage -> Recording Room",
            },
        ],
        "wall_decor": [
            {"prop": "window", "pos": (710, 16)},
            {"prop": "directorate_seal", "pos": (392, 24)},
            {"prop": "sconce", "pos": (90, 35)},
            {"prop": "sconce", "pos": (830, 35)},
        ],
        "floor_decor": [],
        "furniture": [
            {
                "prop": "executive_desk",
                "pos": (390, 235),
                "hitbox": (398, 280, 164, 65),
                "id": "voss_desk",
                "name": "Director Voss's Executive Desk",
                "description": "Heavy mahogany desk. Pinned to the leather blotter is Executive Authorization #88-C.",
                "obj_type": "evidence",
                "evidence_id": "voss_authorization_slip",
                "full_text": (
                    "DIRECTORATE EXECUTIVE DIRECTIVE:\n"
                    "Authorized by: Adrian Voss, Operations Directorate.\n"
                    "Action: Immediate relocation of all Project Echo field journals to deep vault.\n"
                    "Mandate: No personnel outside Class-4 clearance may review Hale's historical files.\n"
                    "Signature verified: Adrian Voss."
                ),
            },
            {
                "prop": "chair",
                "pos": (468, 306),
                "hitbox": (486, 359, 48, 22),
                "id": "voss_chair",
                "name": "Director's Chair",
                "description": "A high-backed chair kept square to the desk, with no personal effects left on it.",
                "obj_type": "examinable",
            },
            {
                "prop": "safe",
                "pos": (760, 120),
                "hitbox": (764, 160, 72, 45),
                "id": "directorate_vault",
                "name": "Executive Directorate Safe",
                "description": "Reinforced steel safe bearing the Directorate seal and marked: 'DOSSIER ECHO - LEVEL 2 DIRECTIVE'.",
                "obj_type": "examinable",
            },
            {
                "prop": "sofa",
                "pos": (110, 390),
                "hitbox": (118, 435, 154, 50),
                "id": "executive_sofa",
                "name": "Formal Leather Settee",
                "description": "Pristine black leather sofa reserved for high-ranking Directorate officials.",
                "obj_type": "environmental",
            },
        ],
        "interactables": [],
    },
}
