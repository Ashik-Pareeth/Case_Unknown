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
        self._background_cache = None
        self._lighting_cache = None

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
                "key_id": door.get("key_id", ""),
                "pin_code": door.get("pin_code"),
                "door_hint": door.get("door_hint", ""),
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
                "key_id": door.get("key_id", ""),
                "pin_code": door.get("pin_code"),
                "door_hint": door.get("door_hint", ""),
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
                "key_id": door.get("key_id", ""),
                "pin_code": door.get("pin_code"),
                "door_hint": door.get("door_hint", ""),
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
                "key_id": door.get("key_id", ""),
                "pin_code": door.get("pin_code"),
                "door_hint": door.get("door_hint", ""),
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
                    key_id=f.get("key_id", ""),
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
                key_id=inter.get("key_id", ""),
            )

    def check_door_transitions(self, player_hitbox: pygame.Rect) -> dict | None:
        """Returns the door configuration if the player has entered a doorway trigger."""
        for d in self.doorways:
            if player_hitbox.colliderect(d["trigger_rect"]):
                gate_id = d.get("gate_id")
                key_id = d.get("key_id")
                if key_id and self.evidence_mgr and not self.evidence_mgr.has_key(key_id):
                    return {"blocked": True, "door": d}
                if gate_id and d.get("pin_code") and self.evidence_mgr and not self.evidence_mgr.is_gate_unlocked(gate_id):
                    return {"door_code": True, "door": d}
                if gate_id and not key_id and self.evidence_mgr and not self.evidence_mgr.is_gate_unlocked(gate_id):
                    return {"blocked": True, "door": d}
                return d
        return None

    def draw_background(self, surface: pygame.Surface):
        """Draw the room's static architecture from a cached surface."""
        if self._background_cache is None or self._background_cache.get_size() != surface.get_size():
            self._background_cache = pygame.Surface(surface.get_size())
            self._background_cache.fill((12, 14, 18))
            self._render_static_background(self._background_cache)
        surface.blit(self._background_cache, (0, 0))

    def _render_static_background(self, surface: pygame.Surface):
        """Draws room walls, custom flooring, baseboards, and wall decor."""
        # 1. Deep cast shadow and architectural shell
        pygame.draw.rect(surface, (5, 7, 9), self.rect.move(0, 9).inflate(14, 14), border_radius=5)
        pygame.draw.rect(surface, self.color_wall, self.rect)
        pygame.draw.rect(
            surface,
            self.color_wall_top,
            (self.rect.left, self.rect.top, self.rect.width, self.top_wall_height),
        )
        # Wall plaster bands catch a little light at the picture rail and base.
        wall_lip = tuple(min(255, c + 12) for c in self.color_wall_top)
        wall_shade = tuple(max(0, c - 10) for c in self.color_wall_top)
        pygame.draw.line(surface, wall_lip, (self.rect.left, self.rect.top + 7),
                         (self.rect.right, self.rect.top + 7), 2)
        pygame.draw.line(surface, wall_shade,
                         (self.rect.left + 2, self.rect.top + self.top_wall_height - 14),
                         (self.rect.right - 2, self.rect.top + self.top_wall_height - 14), 2)
        pygame.draw.line(surface, tuple(min(255, c + 5) for c in self.color_wall),
                         (self.rect.left + 5, self.rect.top + self.top_wall_height + 2),
                         (self.rect.right - 5, self.rect.top + self.top_wall_height + 2), 1)

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
                        if (row + x // plank_w) % 3 == 0:
                            grain = tuple(min(255, c + 4) for c in color)
                            gy = p_rect.top + 7
                            pygame.draw.line(surface, grain, (p_rect.left + 18, gy),
                                             (p_rect.right - 24, gy), 1)

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

        # Recessed wall panels give the upper wall a finished, precinct-office feel.
        panel_top = self.rect.top + 12
        panel_bottom = self.rect.top + self.top_wall_height - 13
        panel_color = tuple(max(0, min(255, c + 7)) for c in self.color_wall_top)
        panel_line = tuple(max(0, c - 8) for c in self.color_wall_top)
        for px in range(self.rect.left + 20, self.rect.right - 14, 74):
            panel = pygame.Rect(px, panel_top, 58, panel_bottom - panel_top)
            pygame.draw.rect(surface, panel_color, panel, 1, border_radius=2)
            pygame.draw.line(surface, panel_line, (px + 5, panel_top + 5), (px + 5, panel_bottom - 5), 1)
        pygame.draw.line(surface, tuple(min(255, c + 15) for c in self.color_wall_top),
                         (self.rect.left, panel_bottom + 5), (self.rect.right, panel_bottom + 5), 2)

        # Floor border and subtle reflection line at the edge of the room.
        pygame.draw.rect(surface, tuple(min(255, c + 12) for c in self.color_floor_a), self.floor_rect, 1)

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
        """Composite the room's soft, cached light pools over its moving characters."""
        if self._lighting_cache is None or self._lighting_cache.get_size() != surface.get_size():
            self._lighting_cache = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            self._render_lighting(self._lighting_cache)
        surface.blit(self._lighting_cache, (0, 0))

    def _render_lighting(self, light_surf: pygame.Surface):
        lighting = self.data.get("lighting", {})

        # Room-wide subtle ambient tint
        ambient_tint = lighting.get("ambient_tint", (255, 220, 150, 18))
        ambient_surf = pygame.Surface(self.floor_rect.size, pygame.SRCALPHA)
        ambient_surf.fill(ambient_tint)
        light_surf.blit(ambient_surf, self.floor_rect.topleft)

        def soft_pool(center, radius, tint, peak_alpha):
            # Draw each light separately and alpha-composite it over the room tone.
            # Drawing straight onto the cache overwrites stronger ambient pixels at
            # the pool edge, which reads as an artificial dark halo.
            pool = pygame.Surface(light_surf.get_size(), pygame.SRCALPHA)
            for r in range(radius, 0, -3):
                t = 1.0 - r / radius
                alpha = int(peak_alpha * t * t)
                if alpha:
                    pygame.draw.circle(pool, (*tint, alpha), center, r)
            light_surf.blit(pool, (0, 0))

        # Feathered pools avoid the hard-edged spotlight rings of the old scene.
        for lamp_pos in lighting.get("warm_lamps", []):
            soft_pool(lamp_pos, 160, (255, 218, 155), 10)

        # Small warm spill from wall fittings
        for sc in lighting.get("sconces", []):
            soft_pool(sc, 86, (255, 215, 145), 7)

        # Cool, broad window shafts retain enough contrast for navigation.
        for poly in lighting.get("moon_rays", []):
            pygame.draw.polygon(light_surf, (160, 200, 255, 12), poly)
