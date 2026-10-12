"""
Detective office room environment, parquet flooring, furniture placement, and collision structures.
"""

import pygame
from src.settings import (
    ROOM_X,
    ROOM_Y,
    ROOM_WIDTH,
    ROOM_HEIGHT,
    WALL_THICKNESS,
    COLOR_BG,
    COLOR_WALL,
    COLOR_WALL_TOP,
    COLOR_WALL_BASE,
    COLOR_FLOOR_A,
    COLOR_FLOOR_B,
    COLOR_FLOOR_SEAM,
)
from assets.svg_assets import get_room_objects
from src.interaction import InteractionManager


class Room:
    def __init__(self, interaction_mgr: InteractionManager):
        self.rect = pygame.Rect(ROOM_X, ROOM_Y, ROOM_WIDTH, ROOM_HEIGHT)
        self.wall_thickness = WALL_THICKNESS
        self.top_wall_height = 80  # Wall area for windows and board

        # Floor boundaries
        self.floor_rect = pygame.Rect(
            self.rect.left + self.wall_thickness,
            self.rect.top + self.top_wall_height,
            self.rect.width - 2 * self.wall_thickness,
            self.rect.height - self.top_wall_height - self.wall_thickness,
        )

        # 4 Solid Boundary Walls
        self.walls = [
            # Top wall
            pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.top_wall_height),
            # Bottom wall
            pygame.Rect(self.rect.left, self.rect.bottom - self.wall_thickness, self.rect.width, self.wall_thickness),
            # Left wall
            pygame.Rect(self.rect.left, self.rect.top, self.wall_thickness, self.rect.height),
            # Right wall
            pygame.Rect(self.rect.right - self.wall_thickness, self.rect.top, self.wall_thickness, self.rect.height),
        ]

        # Load SVG room props
        self.assets = get_room_objects()

        # Build furniture, wall decor, and interactables
        self.furniture_items = []
        self.wall_decor = []
        self.floor_decor = []
        self.solid_objects = list(self.walls)

        self._setup_room(interaction_mgr)

    def _setup_room(self, interaction_mgr: InteractionManager):
        # 1. Floor Rug (Centered under executive office zone)
        rug_surf = self.assets["rug"]
        rug_rect = rug_surf.get_rect(topleft=(370, 240))
        self.floor_decor.append({"surface": rug_surf, "rect": rug_rect})

        # 2. Wall Mounted Decor (Rendered on top wall)
        # Windows with Venetian blinds
        win_surf = self.assets["window"]
        win_l_rect = win_surf.get_rect(topleft=(170, 16))
        win_r_rect = win_surf.get_rect(topleft=(710, 16))
        self.wall_decor.append({"surface": win_surf, "rect": win_l_rect})
        self.wall_decor.append({"surface": win_surf, "rect": win_r_rect})

        interaction_mgr.add_object(
            obj_id="window_left",
            name="Venetian Blind Window",
            description="Cold rain trickles down the dark window glass. The streetlamps outside cast long, wet shadows across the alley below.",
            trigger_rect=pygame.Rect(160, 95, 100, 50),
            badge_pos=(210, 110),
        )

        # Evidence Pinboard (Centered against top wall)
        board_surf = self.assets["evidence_board"]
        board_rect = board_surf.get_rect(topleft=(395, 20))
        self.wall_decor.append({"surface": board_surf, "rect": board_rect})

        interaction_mgr.add_object(
            obj_id="evidence_board",
            name="Evidence Pinboard",
            description="Crime scene photographs linked together by taut red twine. At the center is a recurring symbol—a peculiar crimson spiral discovered at seemingly unrelated crime scenes across the district.",
            trigger_rect=pygame.Rect(385, 95, 190, 50),
            badge_pos=(480, 105),
        )

        # Wall Sconces
        sconce_surf = self.assets["sconce"]
        sconce_1 = sconce_surf.get_rect(topleft=(90, 35))
        sconce_2 = sconce_surf.get_rect(topleft=(830, 35))
        self.wall_decor.append({"surface": sconce_surf, "rect": sconce_1})
        self.wall_decor.append({"surface": sconce_surf, "rect": sconce_2})

        # 3. Solid Depth-Sorted Furniture
        # Bookshelf (Upper left corner)
        shelf_surf = self.assets["bookshelf"]
        shelf_rect = shelf_surf.get_rect(topleft=(100, 105))
        shelf_hitbox = pygame.Rect(102, 185, 80, 48)
        self.furniture_items.append({
            "surface": shelf_surf,
            "rect": shelf_rect,
            "hitbox": shelf_hitbox,
            "sort_y": shelf_hitbox.bottom,
        })
        self.solid_objects.append(shelf_hitbox)

        interaction_mgr.add_object(
            obj_id="bookshelf",
            name="Case Archive Library",
            description="Towering shelves stacked with forensic reference manuals and district penal codes. A confidential binder on 'Internal Audit Protocol' has been pulled forward and hastily closed.",
            trigger_rect=shelf_hitbox.inflate(40, 40),
            badge_pos=(shelf_rect.centerx, shelf_rect.top + 20),
        )

        # Detective Executive Mahogany Desk
        desk_surf = self.assets["desk"]
        desk_rect = desk_surf.get_rect(topleft=(390, 245))
        # Hitbox covering the pedestal legs & desk depth
        desk_hitbox = pygame.Rect(398, 290, 164, 65)
        self.furniture_items.append({
            "surface": desk_surf,
            "rect": desk_rect,
            "hitbox": desk_hitbox,
            "sort_y": desk_hitbox.bottom,
        })
        self.solid_objects.append(desk_hitbox)

        interaction_mgr.add_object(
            obj_id="desk",
            name="Detective's Desk",
            description="Your assigned workstation. Case Dossier #001 lies open under the green banker's lamp. Recent evidence notes describe missing evidence from the precinct lockup.",
            trigger_rect=desk_hitbox.inflate(50, 50),
            badge_pos=(desk_rect.centerx, desk_rect.top + 25),
        )

        # Filing Cabinet (Upper right)
        cab_surf = self.assets["filing_cabinet"]
        cab_rect = cab_surf.get_rect(topleft=(780, 120))
        cab_hitbox = pygame.Rect(784, 170, 56, 42)
        self.furniture_items.append({
            "surface": cab_surf,
            "rect": cab_rect,
            "hitbox": cab_hitbox,
            "sort_y": cab_hitbox.bottom,
        })
        self.solid_objects.append(cab_hitbox)

        interaction_mgr.add_object(
            obj_id="filing_cabinet",
            name="Confidential Filing Cabinet",
            description="Steel drawers containing sealed case records. The lock on the upper drawer displays subtle scratch marks—someone picked the lock without leaving a key entry log.",
            trigger_rect=cab_hitbox.inflate(45, 45),
            badge_pos=(cab_rect.centerx, cab_rect.top + 20),
        )

        # Chesterfield Leather Sofa (Lower left)
        sofa_surf = self.assets["sofa"]
        sofa_rect = sofa_surf.get_rect(topleft=(110, 390))
        sofa_hitbox = pygame.Rect(118, 435, 154, 50)
        self.furniture_items.append({
            "surface": sofa_surf,
            "rect": sofa_rect,
            "hitbox": sofa_hitbox,
            "sort_y": sofa_hitbox.bottom,
        })
        self.solid_objects.append(sofa_hitbox)

        interaction_mgr.add_object(
            obj_id="sofa",
            name="Chesterfield Leather Sofa",
            description="A vintage deep-burgundy leather sofa for witness interviews. A faint scent of old pipe tobacco and cold damp coat wool still clings to the leather.",
            trigger_rect=sofa_hitbox.inflate(40, 40),
            badge_pos=(sofa_rect.centerx, sofa_rect.top + 25),
        )

        # Potted Office Plant (Lower right)
        plant_surf = self.assets["plant"]
        plant_rect = plant_surf.get_rect(topleft=(780, 440))
        plant_hitbox = pygame.Rect(792, 480, 36, 32)
        self.furniture_items.append({
            "surface": plant_surf,
            "rect": plant_rect,
            "hitbox": plant_hitbox,
            "sort_y": plant_hitbox.bottom,
        })
        self.solid_objects.append(plant_hitbox)

        interaction_mgr.add_object(
            obj_id="plant",
            name="Office Plant",
            description="A potted monstera. Its glossy green leaves look carefully watered, bringing a rare touch of life to an otherwise austere room.",
            trigger_rect=plant_hitbox.inflate(35, 35),
            badge_pos=(plant_rect.centerx, plant_rect.top + 15),
        )

    def draw_background(self, surface: pygame.Surface):
        """Draws the room walls and parquet wooden floorboards."""
        # 1. Outer room shell and top wall
        pygame.draw.rect(surface, COLOR_WALL, self.rect)
        pygame.draw.rect(surface, COLOR_WALL_TOP, (self.rect.left, self.rect.top, self.rect.width, self.top_wall_height))

        # 2. Hardwood parquet plank floor
        pygame.draw.rect(surface, COLOR_FLOOR_A, self.floor_rect)

        plank_h = 24
        plank_w = 72
        row = 0
        for y in range(self.floor_rect.top, self.floor_rect.bottom, plank_h):
            row += 1
            x_offset = (row % 2) * (plank_w // 2)
            for x in range(self.floor_rect.left - x_offset, self.floor_rect.right, plank_w):
                p_rect = pygame.Rect(x, y, plank_w, plank_h).clip(self.floor_rect)
                if p_rect.width > 0 and p_rect.height > 0:
                    color = COLOR_FLOOR_A if (row + (x // plank_w)) % 2 == 0 else COLOR_FLOOR_B
                    pygame.draw.rect(surface, color, p_rect)
                    pygame.draw.rect(surface, COLOR_FLOOR_SEAM, p_rect, 1)

        # 3. Baseboard trim
        pygame.draw.rect(surface, COLOR_WALL_BASE, (self.floor_rect.left, self.floor_rect.top - 6, self.floor_rect.width, 6))

        # 4. Outer Wall Borders
        for w in self.walls:
            pygame.draw.rect(surface, COLOR_WALL_BASE, w, 2)

        # 5. Wall Mounted Decor (Windows, Pinboard, Sconces)
        for item in self.wall_decor:
            surface.blit(item["surface"], item["rect"])

        # 6. Floor Decor (Rug)
        for item in self.floor_decor:
            surface.blit(item["surface"], item["rect"])

    def draw_lighting(self, surface: pygame.Surface):
        """Draws atmospheric ambient darkness and soft lighting beams."""
        # Subtle ambient vignette / lighting overlay
        light_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        # Soft warm lamp glow around desk
        desk_lamp_center = (420, 275)
        for r, alpha in [(80, 20), (50, 30), (25, 45)]:
            pygame.draw.circle(light_surf, (255, 225, 140, alpha), desk_lamp_center, r)

        # Soft sconce glows
        for sc in [(110, 55), (850, 55)]:
            pygame.draw.circle(light_surf, (255, 210, 120, 25), sc, 60)
            pygame.draw.circle(light_surf, (255, 230, 160, 40), sc, 30)

        # Soft cool moonlight rays from windows
        win_rays = [
            [(170, 95), (250, 95), (290, 230), (130, 230)],
            [(710, 95), (790, 95), (830, 230), (670, 230)],
        ]
        for poly in win_rays:
            pygame.draw.polygon(light_surf, (160, 200, 255, 14), poly)

        surface.blit(light_surf, (0, 0))
