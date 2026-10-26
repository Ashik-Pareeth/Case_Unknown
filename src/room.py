"""
Reusable Room Environment, Architectural Customization, Flooring, and Doorways for Case Unknown.

Provides the single customizable Room class that instantiates any precinct sector:
- Dynamic flooring: Parquet mahogany, Ceramic forensic tiles, Concrete slabs, Rough stone.
- Doorway passages: Cut-outs in perimeter walls with entry zones and room transitions.
- Furniture and prop placement with layered depth-sorting and solid collision hitboxes.
- Atmospheric lighting layers: Warm desk lamps, Wall sconces, Window moonlight rays.
- Interactive clues and treasure points with puzzle hooks.
"""

import pygame
from src.settings import (
    ROOM_X,
    ROOM_Y,
    ROOM_WIDTH,
    ROOM_HEIGHT,
    WALL_THICKNESS,
    DOOR_SIZE,
    DOOR_THICKNESS,
    DOOR_FRAME_COLOR,
    DOOR_PASSAGE_COLOR,
    COLOR_WALL,
    COLOR_WALL_TOP,
    COLOR_WALL_BASE,
    COLOR_FLOOR_A,
    COLOR_FLOOR_B,
    COLOR_FLOOR_SEAM,
)
from assets.svg_assets import get_room_objects
from src.interaction import InteractionManager
from src.rooms_data import ROOMS_DATA
from src.evidence_manager import TYPE_EXAMINABLE, TYPE_EVIDENCE, EvidenceManager


class Room:
    """
    Modular, reusable precinct room that dynamically customizes its appearance,
    doors, collision geometry, lighting, and interactables based on room definition data.
    """

    def __init__(
        self,
        interaction_mgr: InteractionManager,
        room_id: str = "office",
        room_data: dict = None,
        treasure_mgr=None,
        evidence_mgr: EvidenceManager | None = None,
    ):
        self.room_id = room_id
        self.data = room_data if room_data is not None else ROOMS_DATA.get(room_id, ROOMS_DATA["office"])
        self.name = self.data.get("name", "Precinct Room")
        self.subtitle = self.data.get("subtitle", "")
        self.treasure_mgr = treasure_mgr
        self.evidence_mgr = evidence_mgr

        # Room bounds
        self.rect = pygame.Rect(ROOM_X, ROOM_Y, ROOM_WIDTH, ROOM_HEIGHT)
        self.wall_thickness = WALL_THICKNESS
        self.top_wall_height = 80  # Top wall zone for windows/boards

        # Floor bounds inside the walls
        self.floor_rect = pygame.Rect(
            self.rect.left + self.wall_thickness,
            self.rect.top + self.top_wall_height,
            self.rect.width - 2 * self.wall_thickness,
            self.rect.height - self.top_wall_height - self.wall_thickness,
        )

        # Theme colors
        colors = self.data.get("colors", {})
        self.color_wall = colors.get("wall", COLOR_WALL)
        self.color_wall_top = colors.get("wall_top", COLOR_WALL_TOP)
        self.color_wall_base = colors.get("wall_base", COLOR_WALL_BASE)
        self.color_floor_a = colors.get("floor_a", COLOR_FLOOR_A)
        self.color_floor_b = colors.get("floor_b", COLOR_FLOOR_B)
        self.color_floor_seam = colors.get("floor_seam", COLOR_FLOOR_SEAM)
        self.floor_style = self.data.get("floor_style", "parquet")

        # Load SVG assets
        self.assets = get_room_objects()

        # Collections
        self.furniture_items = []
        self.wall_decor = []
        self.floor_decor = []
        self.solid_objects = []
        self.doorways = []

        # Build walls, doorways, furniture, and interactables
        self._setup_doorways_and_walls()
        self._setup_furniture_and_interactables(interaction_mgr)

        # Door font
        pygame.font.init()
        self.door_font = pygame.font.SysFont("segoeui", 11, bold=True)

    def _setup_doorways_and_walls(self):
        """Constructs solid walls with doorway passages leaving openings for travel."""
        doors_config = self.data.get("doors", [])
        doors_by_wall = {d["wall"]: d for d in doors_config}

        # 1. TOP WALL
        if "top" in doors_by_wall:
            door = doors_by_wall["top"]
            dw = DOOR_SIZE
            dx = self.rect.centerx - dw // 2
            # Left segment
            w_left = pygame.Rect(self.rect.left, self.rect.top, dx - self.rect.left, self.top_wall_height)
            # Right segment
            w_right = pygame.Rect(dx + dw, self.rect.top, self.rect.right - (dx + dw), self.top_wall_height)
            self.solid_objects.extend([w_left, w_right])

            # Doorway Trigger Zone
            trigger_rect = pygame.Rect(dx + 10, self.rect.top + self.top_wall_height - 18, dw - 20, 24)
            self.doorways.append({
                "wall": "top",
                "rect": pygame.Rect(dx, self.rect.top + self.top_wall_height - 12, dw, 16),
                "trigger_rect": trigger_rect,
                "target_room": door["target_room"],
                "target_pos": door["target_pos"],
                "label": door.get("label", "North Door"),
                "gate_id": door.get("gate_id", ""),
                "gate_msg": door.get("gate_msg", ""),
            })
        else:
            self.solid_objects.append(
                pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.top_wall_height)
            )

        # 2. BOTTOM WALL
        if "bottom" in doors_by_wall:
            door = doors_by_wall["bottom"]
            dw = DOOR_SIZE
            dx = self.rect.centerx - dw // 2
            by = self.rect.bottom - self.wall_thickness
            # Left segment
            w_left = pygame.Rect(self.rect.left, by, dx - self.rect.left, self.wall_thickness)
            # Right segment
            w_right = pygame.Rect(dx + dw, by, self.rect.right - (dx + dw), self.wall_thickness)
            self.solid_objects.extend([w_left, w_right])

            # Doorway Trigger Zone
            trigger_rect = pygame.Rect(dx + 10, by - 6, dw - 20, 24)
            self.doorways.append({
                "wall": "bottom",
                "rect": pygame.Rect(dx, by, dw, self.wall_thickness),
                "trigger_rect": trigger_rect,
                "target_room": door["target_room"],
                "target_pos": door["target_pos"],
                "label": door.get("label", "South Door"),
                "gate_id": door.get("gate_id", ""),
                "gate_msg": door.get("gate_msg", ""),
            })
        else:
            self.solid_objects.append(
                pygame.Rect(self.rect.left, self.rect.bottom - self.wall_thickness, self.rect.width, self.wall_thickness)
            )

        # 3. LEFT WALL
        if "left" in doors_by_wall:
            door = doors_by_wall["left"]
            dh = DOOR_SIZE
            dy = self.floor_rect.centery - dh // 2
            # Top segment
            w_top = pygame.Rect(self.rect.left, self.rect.top, self.wall_thickness, dy - self.rect.top)
            # Bottom segment
            w_bottom = pygame.Rect(self.rect.left, dy + dh, self.wall_thickness, self.rect.bottom - (dy + dh))
            self.solid_objects.extend([w_top, w_bottom])

            # Doorway Trigger Zone
            trigger_rect = pygame.Rect(self.rect.left - 4, dy + 10, 24, dh - 20)
            self.doorways.append({
                "wall": "left",
                "rect": pygame.Rect(self.rect.left, dy, self.wall_thickness, dh),
                "trigger_rect": trigger_rect,
                "target_room": door["target_room"],
                "target_pos": door["target_pos"],
                "label": door.get("label", "West Door"),
                "gate_id": door.get("gate_id", ""),
                "gate_msg": door.get("gate_msg", ""),
            })
        else:
            self.solid_objects.append(
                pygame.Rect(self.rect.left, self.rect.top, self.wall_thickness, self.rect.height)
            )

        # 4. RIGHT WALL
        if "right" in doors_by_wall:
            door = doors_by_wall["right"]
            dh = DOOR_SIZE
            dy = self.floor_rect.centery - dh // 2
            rx = self.rect.right - self.wall_thickness
            # Top segment
            w_top = pygame.Rect(rx, self.rect.top, self.wall_thickness, dy - self.rect.top)
            # Bottom segment
            w_bottom = pygame.Rect(rx, dy + dh, self.wall_thickness, self.rect.bottom - (dy + dh))
            self.solid_objects.extend([w_top, w_bottom])

            # Doorway Trigger Zone
            trigger_rect = pygame.Rect(rx - 8, dy + 10, 24, dh - 20)
            self.doorways.append({
                "wall": "right",
                "rect": pygame.Rect(rx, dy, self.wall_thickness, dh),
                "trigger_rect": trigger_rect,
                "target_room": door["target_room"],
                "target_pos": door["target_pos"],
                "label": door.get("label", "East Door"),
                "gate_id": door.get("gate_id", ""),
                "gate_msg": door.get("gate_msg", ""),
            })
        else:
            self.solid_objects.append(
                pygame.Rect(self.rect.right - self.wall_thickness, self.rect.top, self.wall_thickness, self.rect.height)
            )

    def _setup_furniture_and_interactables(self, interaction_mgr: InteractionManager):
        """Places SVG furniture items and connects them to the interaction system."""
        # Clean interaction manager for new room
        interaction_mgr.clear()
        if self.treasure_mgr is not None:
            interaction_mgr.treasure_manager = self.treasure_mgr

        # 1. Floor Decor (Rugs, etc.)
        for item in self.data.get("floor_decor", []):
            prop_key = item["prop"]
            if prop_key in self.assets:
                surf = self.assets[prop_key]
                rect = surf.get_rect(topleft=item["pos"])
                self.floor_decor.append({"surface": surf, "rect": rect})

        # 2. Wall Decor (Windows, Evidence Board, Sconces)
        for item in self.data.get("wall_decor", []):
            prop_key = item["prop"]
            if prop_key in self.assets:
                surf = self.assets[prop_key]
                rect = surf.get_rect(topleft=item["pos"])
                self.wall_decor.append({"surface": surf, "rect": rect})

        # 3. Solid Depth-Sorted Furniture
        for f in self.data.get("furniture", []):
            prop_key = f["prop"]
            if prop_key in self.assets:
                surf = self.assets[prop_key]
                rect = surf.get_rect(topleft=f["pos"])
                hitbox_tuple = f["hitbox"]
                hitbox = pygame.Rect(*hitbox_tuple)

                self.furniture_items.append({
                    "surface": surf,
                    "rect": rect,
                    "hitbox": hitbox,
                    "sort_y": hitbox.bottom,
                })
                self.solid_objects.append(hitbox)

                # Add to interactables
                is_treasure = f.get("is_treasure", False)
                treasure_id = f.get("id", "")
                interaction_mgr.add_object(
                    obj_id=f["id"],
                    name=f["name"],
                    description=f["description"],
                    trigger_rect=hitbox.inflate(45, 45),
                    badge_pos=(rect.centerx, rect.top + 20),
                    obj_type=f.get("obj_type", TYPE_EXAMINABLE),
                    evidence_id=f.get("evidence_id", ""),
                    full_text=f.get("full_text", ""),
                    is_treasure=is_treasure,
                    treasure_id=treasure_id,
                )

        # 4. Standalone Environmental Interactables
        for inter in self.data.get("interactables", []):
            interaction_mgr.add_object(
                obj_id=inter["id"],
                name=inter["name"],
                description=inter["description"],
                trigger_rect=pygame.Rect(*inter["trigger_rect"]),
                badge_pos=inter["badge_pos"],
                obj_type=inter.get("obj_type", TYPE_EXAMINABLE),
                evidence_id=inter.get("evidence_id", ""),
                full_text=inter.get("full_text", ""),
            )

    def check_door_transitions(self, player_hitbox: pygame.Rect) -> dict | None:
        """Returns the door configuration if the player has entered a doorway trigger."""
        for d in self.doorways:
            if player_hitbox.colliderect(d["trigger_rect"]):
                gate_id = d.get("gate_id")
                if gate_id and self.evidence_mgr and not self.evidence_mgr.is_gate_unlocked(gate_id):
                    return {"blocked": True, "door": d}
                return d
        return None

    def draw_background(self, surface: pygame.Surface):
        """Draws room walls, custom flooring, baseboards, and wall decor."""
        # 1. Outer room shell and top wall
        pygame.draw.rect(surface, self.color_wall, self.rect)
        pygame.draw.rect(
            surface,
            self.color_wall_top,
            (self.rect.left, self.rect.top, self.rect.width, self.top_wall_height),
        )

        # 2. Floor Generation by Style
        pygame.draw.rect(surface, self.color_floor_a, self.floor_rect)

        if self.floor_style == "parquet":
            # Hardwood parquet plank pattern
            plank_h = 24
            plank_w = 72
            row = 0
            for y in range(self.floor_rect.top, self.floor_rect.bottom, plank_h):
                row += 1
                x_offset = (row % 2) * (plank_w // 2)
                for x in range(self.floor_rect.left - x_offset, self.floor_rect.right, plank_w):
                    p_rect = pygame.Rect(x, y, plank_w, plank_h).clip(self.floor_rect)
                    if p_rect.width > 0 and p_rect.height > 0:
                        color = self.color_floor_a if (row + (x // plank_w)) % 2 == 0 else self.color_floor_b
                        pygame.draw.rect(surface, color, p_rect)
                        pygame.draw.rect(surface, self.color_floor_seam, p_rect, 1)

        elif self.floor_style == "tiles":
            # Ceramic / clinical square tile pattern
            tile_size = 36
            row = 0
            for y in range(self.floor_rect.top, self.floor_rect.bottom, tile_size):
                row += 1
                col = 0
                for x in range(self.floor_rect.left, self.floor_rect.right, tile_size):
                    col += 1
                    t_rect = pygame.Rect(x, y, tile_size, tile_size).clip(self.floor_rect)
                    if t_rect.width > 0 and t_rect.height > 0:
                        color = self.color_floor_a if (row + col) % 2 == 0 else self.color_floor_b
                        pygame.draw.rect(surface, color, t_rect)
                        pygame.draw.rect(surface, self.color_floor_seam, t_rect, 1)

        elif self.floor_style == "stone":
            # Heavy stone slab flagstones
            slab_w = 90
            slab_h = 45
            row = 0
            for y in range(self.floor_rect.top, self.floor_rect.bottom, slab_h):
                row += 1
                x_offset = (row % 2) * (slab_w // 3)
                for x in range(self.floor_rect.left - x_offset, self.floor_rect.right, slab_w):
                    s_rect = pygame.Rect(x, y, slab_w, slab_h).clip(self.floor_rect)
                    if s_rect.width > 0 and s_rect.height > 0:
                        color = self.color_floor_a if (row * 3 + x // slab_w) % 2 == 0 else self.color_floor_b
                        pygame.draw.rect(surface, color, s_rect)
                        pygame.draw.rect(surface, self.color_floor_seam, s_rect, 2)

        elif self.floor_style == "concrete":
            # Smooth dark industrial concrete with expansion lines
            pygame.draw.rect(surface, self.color_floor_a, self.floor_rect)
            for y in range(self.floor_rect.top + 90, self.floor_rect.bottom, 120):
                pygame.draw.line(surface, self.color_floor_seam, (self.floor_rect.left, y), (self.floor_rect.right, y), 2)
            for x in range(self.floor_rect.left + 140, self.floor_rect.right, 180):
                pygame.draw.line(surface, self.color_floor_seam, (x, self.floor_rect.top), (x, self.floor_rect.bottom), 2)

        # 3. Baseboard trim
        pygame.draw.rect(
            surface,
            self.color_wall_base,
            (self.floor_rect.left, self.floor_rect.top - 6, self.floor_rect.width, 6),
        )

        # 4. Wall Boundaries
        for solid in self.solid_objects:
            if solid.width == self.wall_thickness or solid.height in (self.wall_thickness, self.top_wall_height):
                pygame.draw.rect(surface, self.color_wall_base, solid, 2)

        # 5. Doorways (Open passage thresholds, brass plates, and directional arrows)
        for door in self.doorways:
            d_rect = door["rect"]
            wall = door["wall"]
            if wall in ("left", "right"):
                # Vertical Doorway
                pygame.draw.rect(surface, DOOR_PASSAGE_COLOR, d_rect)
                pygame.draw.rect(surface, DOOR_FRAME_COLOR, d_rect, 2)
                # Door runner mat extending into floor
                mat_x = d_rect.right if wall == "left" else d_rect.left - 24
                mat_rect = pygame.Rect(mat_x, d_rect.y + 12, 24, d_rect.height - 24)
                pygame.draw.rect(surface, (45, 38, 30), mat_rect)
                pygame.draw.rect(surface, (85, 70, 50), mat_rect, 1)
            else:
                # Horizontal Doorway (top / bottom)
                pygame.draw.rect(surface, DOOR_PASSAGE_COLOR, d_rect)
                pygame.draw.rect(surface, DOOR_FRAME_COLOR, d_rect, 2)
                mat_y = d_rect.bottom if wall == "top" else d_rect.top - 24
                mat_rect = pygame.Rect(d_rect.x + 12, mat_y, d_rect.width - 24, 24)
                pygame.draw.rect(surface, (45, 38, 30), mat_rect)
                pygame.draw.rect(surface, (85, 70, 50), mat_rect, 1)

        # 6. Wall Mounted Decor
        for item in self.wall_decor:
            surface.blit(item["surface"], item["rect"])

        # 7. Floor Decor
        for item in self.floor_decor:
            surface.blit(item["surface"], item["rect"])

    def draw_lighting(self, surface: pygame.Surface):
        """Draws atmospheric lighting, warm lamp spheres, sconces, and moonbeams."""
        lighting = self.data.get("lighting", {})
        light_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        # Room-wide subtle ambient tint
        ambient_tint = lighting.get("ambient_tint", (255, 220, 150, 18))
        ambient_surf = pygame.Surface(self.floor_rect.size, pygame.SRCALPHA)
        ambient_surf.fill(ambient_tint)
        light_surf.blit(ambient_surf, self.floor_rect.topleft)

        # Warm desk lamps
        for lamp_pos in lighting.get("warm_lamps", []):
            for r, alpha in [(85, 20), (55, 32), (28, 48)]:
                pygame.draw.circle(light_surf, (255, 225, 140, alpha), lamp_pos, r)

        # Wall sconces
        for sc in lighting.get("sconces", []):
            pygame.draw.circle(light_surf, (255, 210, 120, 25), sc, 60)
            pygame.draw.circle(light_surf, (255, 230, 160, 40), sc, 30)

        # Cool moonlight window rays
        for poly in lighting.get("moon_rays", []):
            pygame.draw.polygon(light_surf, (160, 200, 255, 14), poly)

        surface.blit(light_surf, (0, 0))
