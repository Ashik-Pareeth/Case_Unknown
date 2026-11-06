"""Autonomous room patrols, independent of player input and movement."""

from __future__ import annotations

import math
import random
import pygame

from assets.npcs import get_npc_animations
from src.rooms_data import ROOMS_DATA


NPC_PATROLS = {
    # The opening crime scene intentionally stays empty.
    "office": (340, 455),
    "archive": (300, 455),
    "morgue": (300, 455),
    "lockup": (335, 455),
    "interrogation": (300, 455),
    "records_room": (330, 455),
    "recording_room": (310, 455),
    "restricted_office": (330, 455),
}

# Predetermined, invisible multi-point looping patrol routes for each room.
# Each room features up to 3 distinct non-trivial circuits winding around furniture.
NPC_PATROL_PATHS: dict[str, list[list[tuple[int, int]]]] = {
    "office": [
        [(240, 160), (340, 160), (340, 270), (220, 270), (310, 360), (310, 520), (360, 520), (360, 450), (320, 380), (240, 320), (240, 220)],
        [(720, 240), (750, 240), (750, 340), (750, 440), (640, 470), (600, 410), (600, 250), (700, 250)],
        [(350, 240), (480, 230), (580, 240), (590, 380), (480, 390), (360, 380), (350, 310)],
    ],
    "archive": [
        [(290, 170), (350, 220), (260, 240), (170, 250), (260, 320), (340, 280), (340, 430), (260, 450), (180, 410), (290, 370), (290, 240)],
        [(720, 200), (740, 270), (700, 380), (700, 440), (620, 480), (610, 400), (610, 260), (700, 240)],
        [(360, 250), (480, 240), (590, 250), (600, 410), (480, 410), (360, 410), (350, 330)],
    ],
    "morgue": [
        [(230, 180), (340, 180), (350, 280), (250, 310), (220, 440), (330, 460), (350, 370), (240, 360), (210, 260)],
        [(710, 180), (740, 270), (710, 380), (690, 480), (600, 480), (590, 380), (600, 250), (680, 210)],
        [(360, 230), (470, 220), (580, 230), (590, 370), (480, 380), (360, 370), (350, 300)],
    ],
    "lockup": [
        [(140, 220), (260, 220), (370, 250), (370, 390), (270, 430), (130, 430), (120, 300)],
        [(520, 250), (660, 250), (790, 250), (800, 380), (780, 440), (780, 515), (630, 515), (630, 410), (530, 390), (500, 310)],
        [(390, 260), (480, 280), (550, 310), (480, 390), (390, 450), (480, 470), (550, 420), (450, 340)],
    ],
    "interrogation": [
        [(220, 180), (340, 180), (340, 260), (220, 270), (180, 380), (270, 460), (340, 410), (310, 320), (210, 280)],
        [(700, 190), (740, 230), (710, 370), (750, 420), (680, 470), (600, 450), (590, 340), (600, 220), (690, 210)],
        [(360, 220), (470, 210), (570, 220), (580, 370), (470, 380), (360, 370), (350, 290)],
    ],
    "records_room": [
        [(310, 170), (350, 250), (280, 270), (180, 270), (150, 380), (240, 460), (330, 450), (340, 340), (280, 300)],
        [(530, 250), (650, 240), (780, 240), (800, 390), (780, 480), (660, 480), (540, 440), (530, 330)],
        [(380, 230), (470, 240), (540, 280), (520, 400), (460, 460), (380, 420), (420, 320)],
    ],
    "recording_room": [
        [(180, 200), (310, 200), (330, 290), (250, 320), (180, 390), (260, 470), (340, 450), (330, 370), (220, 320)],
        [(680, 190), (730, 240), (710, 340), (750, 420), (720, 480), (620, 470), (600, 380), (610, 250)],
        [(360, 240), (480, 230), (590, 240), (600, 410), (460, 420), (360, 410), (350, 310)],
    ],
    "restricted_office": [
        [(220, 200), (340, 200), (340, 290), (250, 310), (320, 370), (320, 520), (360, 520), (360, 440), (330, 380), (240, 320)],
        [(690, 180), (730, 230), (740, 350), (750, 470), (640, 480), (610, 400), (610, 250), (680, 210)],
        [(360, 230), (480, 220), (580, 230), (590, 410), (460, 410), (360, 400), (350, 300)],
    ],
}

_DIRECTIONS = ("down", "left", "up", "right")
NPC_COUNT_PER_ROOM = 3


class AutonomousNPC:
    """A patrolling NPC that moves in a predetermined, invisible loop.
    
    Guarantees non-extended doorward facing: never stays pointed at any doorway for
    longer than a brief fraction of a second (<0.30s) while actively traversing, and
    never points towards doorways while paused or idling.
    """

    def __init__(self, start_pos: tuple[int, int] | list[tuple[int, int]], palette_index: int = 0,
                 seed: int | None = None, door_targets: tuple[tuple[int, int], ...] = (),
                 path: list[tuple[int, int]] | None = None):
        self.animations = get_npc_animations(palette_index)
        self.scaled_animations = {
            direction: {
                state: [pygame.transform.smoothscale(frame, (60, 76)) for frame in frames]
                for state, frames in states.items()
            }
            for direction, states in self.animations.items()
        }

        if path is not None:
            self.path = [tuple(p) for p in path]
        elif isinstance(start_pos, (list, tuple)) and start_pos and isinstance(start_pos[0], (list, tuple)):
            self.path = [tuple(p) for p in start_pos]
        else:
            self.path = [tuple(start_pos)]

        self.waypoint_index = 0
        self.pos = pygame.Vector2(self.path[0])
        self.hitbox = pygame.Rect(0, 0, 24, 14)
        self.sprite_size = (60, 76)
        self.door_targets = door_targets
        self.rng = random.Random(seed)
        self.frame_index = 0
        self.anim_timer = 0.0
        self.speed = 58.0
        self.arrival_dist = 6.0
        self.vision_range = 190
        self.vision_half_angle = 35
        self.door_facing_timer = 0.0
        self.gaze_override: str | None = None

        self.phase = "walk"
        self.phase_timer = 0.0
        self.state = "walk"
        self.direction = self._choose_pause_direction()
        self.image = None
        self._update_rects()
        self._set_image()

    @property
    def sort_y(self):
        return self.hitbox.bottom

    def _update_rects(self):
        self.hitbox.center = (round(self.pos.x), round(self.pos.y))
        self.sprite_rect = pygame.Rect(0, 0, *self.sprite_size)
        self.sprite_rect.midbottom = (self.hitbox.centerx, self.hitbox.bottom + 4)

    def _set_image(self):
        frames = self.scaled_animations[self.direction][self.state]
        self.frame_index %= len(frames)
        self.image = frames[self.frame_index]

    def is_pointing_at_door(self, direction: str | None = None, cone_angle: float = 38.0) -> bool:
        """Returns True if the given (or current) facing direction points towards any doorway."""
        if not self.door_targets:
            return False
        d = direction or self.direction
        facing_angles = {"right": 0, "down": 90, "left": 180, "up": 270}
        fa = facing_angles.get(d, 0)
        for dx, dy in self.door_targets:
            dist = math.hypot(dx - self.pos.x, dy - self.pos.y)
            ang = math.degrees(math.atan2(dy - self.pos.y, dx - self.pos.x)) % 360
            diff = abs((ang - fa + 180) % 360 - 180)
            # Within vision reach and cone angle
            if dist <= self.vision_range + 35 and diff <= cone_angle:
                return True
            # Direct corridor / hallway alignment
            if dist > self.vision_range + 35:
                # Top / Bottom door corridor
                if abs(dx - 480) < 15 and abs(self.pos.x - dx) <= 55:
                    if (dy < self.pos.y and d == "up") or (dy > self.pos.y and d == "down"):
                        return True
                # Left / Right door corridor
                if abs(dy - 348) < 15 and abs(self.pos.y - dy) <= 55:
                    if (dx < self.pos.x and d == "left") or (dx > self.pos.x and d == "right"):
                        return True
        return False

    def _doorward_direction(self) -> str | None:
        """Returns the single cardinal direction most directly pointing to the nearest doorway."""
        if not self.door_targets:
            return None
        target_x, target_y = min(
            self.door_targets,
            key=lambda target: (target[0] - self.pos.x) ** 2 + (target[1] - self.pos.y) ** 2,
        )
        dx, dy = target_x - self.pos.x, target_y - self.pos.y
        if abs(dx) > abs(dy):
            return "right" if dx > 0 else "left"
        if dy:
            return "down" if dy > 0 else "up"
        return None

    def _safe_directions(self) -> list[str]:
        """Cardinal directions that do not point toward any doorway."""
        safe = [d for d in _DIRECTIONS if not self.is_pointing_at_door(d)]
        if not safe:
            doorward = self._doorward_direction()
            safe = [d for d in _DIRECTIONS if d != doorward]
        return safe if safe else list(_DIRECTIONS)

    def _choose_pause_direction(self) -> str:
        """Select a direction safe from pointing at any door when stopped."""
        safe = self._safe_directions()
        return self.rng.choice(safe)

    def _safe_gaze_direction(self, current_dir: str) -> str:
        """Find a perpendicular safe direction to look away from a doorway."""
        safe = self._safe_directions()
        perp = {
            "up": ["left", "right"],
            "down": ["left", "right"],
            "left": ["up", "down"],
            "right": ["up", "down"],
        }.get(current_dir, ["left", "right"])
        for p in perp:
            if p in safe:
                return p
        return safe[0] if safe else current_dir

    def update(self, delta_time: float, bounds: pygame.Rect, solid_objects: list[pygame.Rect], other_npcs=()):
        if len(self.path) > 1:
            target = self.path[(self.waypoint_index + 1) % len(self.path)]
            if self.phase == "wait":
                self.phase_timer -= delta_time
                # Strictly enforce never pointing to any door during pauses
                if self.is_pointing_at_door(self.direction):
                    self.direction = self._choose_pause_direction()
                if self.phase_timer <= 0:
                    self.phase = "walk"
                    self.state = "walk"
                    self.gaze_override = None
                    self.door_facing_timer = 0.0
            else:
                dx = target[0] - self.pos.x
                dy = target[1] - self.pos.y
                dist = math.hypot(dx, dy)
                if dist <= max(self.arrival_dist, self.speed * delta_time):
                    # Arrived at waypoint
                    self.pos.x = target[0]
                    self.pos.y = target[1]
                    self.waypoint_index = (self.waypoint_index + 1) % len(self.path)
                    self.door_facing_timer = 0.0
                    self.gaze_override = None
                    # Periodic brief pause to inspect room (only looking in safe directions)
                    if self.rng.random() < 0.40:
                        self.phase = "wait"
                        self.phase_timer = self.rng.uniform(0.8, 1.4)
                        self.state = "idle"
                        self.direction = self._choose_pause_direction()
                        self.frame_index = 0
                else:
                    self.state = "walk"
                    if abs(dx) >= abs(dy):
                        move_dir = "right" if dx > 0 else "left"
                    else:
                        move_dir = "down" if dy > 0 else "up"

                    current_facing = self.gaze_override or move_dir
                    if self.is_pointing_at_door(current_facing):
                        self.door_facing_timer += delta_time
                        if self.door_facing_timer >= 0.30:
                            # Break door line-of-sight: divert gaze to a safe direction
                            self.gaze_override = self._safe_gaze_direction(move_dir)
                            current_facing = self.gaze_override
                            self.door_facing_timer = 0.0
                    else:
                        self.door_facing_timer = 0.0
                        if self.gaze_override and not self.is_pointing_at_door(move_dir):
                            self.gaze_override = None
                            current_facing = move_dir
                        elif not self.gaze_override:
                            current_facing = move_dir

                    self.direction = current_facing

                    step = min(dist, self.speed * delta_time)
                    old_pos = self.pos.copy()
                    self.pos.x += (dx / dist) * step
                    self.pos.y += (dy / dist) * step
                    self._update_rects()

                    # Yield if encountering another NPC
                    if any(self.hitbox.colliderect(obj) for obj in other_npcs):
                        self.pos = old_pos
                        self._update_rects()
                        self.phase = "wait"
                        self.phase_timer = 0.5
                        self.state = "idle"
                        self.direction = self._choose_pause_direction()
        else:
            # Single-point path fallback
            self.phase_timer -= delta_time
            if self.is_pointing_at_door(self.direction):
                self.direction = self._choose_pause_direction()

        self.anim_timer += delta_time
        frame_time = 0.18 if self.state == "walk" else 0.5
        if self.anim_timer >= frame_time:
            self.anim_timer %= frame_time
            self.frame_index += 1
        self._set_image()

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.sprite_rect)

    def get_vision_points(self) -> list[tuple[int, int]]:
        """Compute the polygon vertices defining this NPC's viewpoint."""
        facing_angle = {
            "right": 0,
            "down": 90,
            "left": 180,
            "up": 270,
        }[self.direction]
        origin = (round(self.pos.x), round(self.pos.y - 48))
        angles = range(-self.vision_half_angle, self.vision_half_angle + 1, 5)
        arc = [
            (
                round(origin[0] + math.cos(math.radians(facing_angle + offset)) * self.vision_range),
                round(origin[1] + math.sin(math.radians(facing_angle + offset)) * self.vision_range),
            )
            for offset in angles
        ]
        return [origin, *arc]

    def draw_vision(self, surface: pygame.Surface):
        """Draw this NPC's 70-degree forward field of view."""
        points = self.get_vision_points()
        origin = points[0]
        arc = points[1:]
        pygame.draw.polygon(surface, (218, 174, 86, 24), points)
        pygame.draw.lines(surface, (218, 174, 86, 62), False, [origin, arc[0]], 1)
        pygame.draw.lines(surface, (218, 174, 86, 62), False, [origin, arc[-1]], 1)

    def collides_with_vision(self, target, bounds: pygame.Rect | None = None) -> bool:
        """Check if target (Player, Rect, or point) collides with this viewpoint."""
        target_hitbox = getattr(target, "hitbox", target if isinstance(target, pygame.Rect) else None)
        if bounds is not None and target_hitbox is not None:
            if not bounds.colliderect(target_hitbox):
                return False

        poly = self.get_vision_points()

        # Point / coordinates
        if isinstance(target, (tuple, list, pygame.Vector2)):
            return point_in_polygon(target[0], target[1], poly)

        # Player entity with hitbox and body_rect
        if hasattr(target, "hitbox") and polygon_collides_with_rect(poly, target.hitbox):
            return True
        if hasattr(target, "body_rect") and polygon_collides_with_rect(poly, target.body_rect):
            return True

        if isinstance(target, pygame.Rect):
            return polygon_collides_with_rect(poly, target)

        return False


class RoomNPCController:
    """Owns independent NPCs for one room and updates their patrols."""

    def __init__(self, room_id: str, bounds: pygame.Rect, solid_objects: list[pygame.Rect]):
        self.npcs = []
        self._seed = sum(map(ord, room_id))

        door_walls = [door["wall"] for door in ROOMS_DATA.get(room_id, {}).get("doors", [])]
        door_targets = tuple({
            "left": (bounds.left, bounds.centery),
            "right": (bounds.right, bounds.centery),
            "top": (bounds.centerx, bounds.top),
            "bottom": (bounds.centerx, bounds.bottom),
        }[wall] for wall in door_walls)

        room_paths = NPC_PATROL_PATHS.get(room_id)
        if room_paths:
            for idx in range(min(NPC_COUNT_PER_ROOM, len(room_paths))):
                path = room_paths[idx]
                self.npcs.append(AutonomousNPC(
                    start_pos=path,
                    palette_index=idx % 2,
                    seed=self._seed + idx * 7919,
                    door_targets=door_targets,
                ))
        elif room_id in NPC_PATROLS:
            start_pos = NPC_PATROLS[room_id]
            self.npcs.append(AutonomousNPC(
                start_pos=start_pos,
                palette_index=0,
                seed=self._seed,
                door_targets=door_targets,
            ))

    def update(self, delta_time: float, bounds: pygame.Rect, solid_objects: list[pygame.Rect]):
        for index, npc in enumerate(self.npcs):
            other_hitboxes = [other.hitbox for other in self.npcs if other is not npc]
            npc.update(delta_time, bounds, solid_objects, other_hitboxes)

    def draw_queue(self, surface: pygame.Surface):
        return [
            {"sort_y": npc.sort_y, "draw": lambda actor=npc: actor.draw(surface)}
            for npc in self.npcs
        ]

    def draw_vision(self, surface: pygame.Surface, bounds: pygame.Rect):
        if not self.npcs:
            return
        vision_layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        vision_layer.set_clip(bounds)
        for npc in self.npcs:
            npc.draw_vision(vision_layer)
        surface.blit(vision_layer, (0, 0))

    def check_player_spotted(self, target, bounds: pygame.Rect | None = None) -> bool:
        """Returns True if the target collides with any NPC's viewpoint points."""
        for npc in self.npcs:
            if npc.collides_with_vision(target, bounds=bounds):
                return True
        return False


def point_in_polygon(x: float, y: float, poly: list[tuple[float, float]]) -> bool:
    """Ray casting algorithm to determine if point (x, y) is inside polygon."""
    n = len(poly)
    if n < 3:
        return False
    inside = False
    p1x, p1y = poly[0]
    for i in range(1, n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def segments_intersect(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> bool:
    """Returns True if line segment p1-p2 intersects line segment p3-p4."""
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    if d == 0:
        return False
    u = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    v = ((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / d
    return (0.0 <= u <= 1.0) and (0.0 <= v <= 1.0)


def polygon_collides_with_rect(poly: list[tuple[float, float]], rect: pygame.Rect) -> bool:
    """Checks collision between an arbitrary 2D polygon and a pygame.Rect."""
    min_x = min(p[0] for p in poly)
    max_x = max(p[0] for p in poly)
    min_y = min(p[1] for p in poly)
    max_y = max(p[1] for p in poly)
    poly_bbox = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    if not rect.colliderect(poly_bbox):
        return False

    # Check if any polygon vertex is inside rect
    for p in poly:
        if rect.collidepoint(p):
            return True

    # Check if key rect sample points are inside polygon
    rect_points = [
        (rect.left, rect.top),
        (rect.right, rect.top),
        (rect.right, rect.bottom),
        (rect.left, rect.bottom),
        (rect.centerx, rect.centery),
        (rect.centerx, rect.top),
        (rect.centerx, rect.bottom),
        (rect.left, rect.centery),
        (rect.right, rect.centery),
    ]
    for px, py in rect_points:
        if point_in_polygon(px, py, poly):
            return True

    # Check if any rect edge intersects any polygon edge
    rect_edges = [
        ((rect.left, rect.top), (rect.right, rect.top)),
        ((rect.right, rect.top), (rect.right, rect.bottom)),
        ((rect.right, rect.bottom), (rect.left, rect.bottom)),
        ((rect.left, rect.bottom), (rect.left, rect.top)),
    ]
    n = len(poly)
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i + 1) % n]
        for r1, r2 in rect_edges:
            if segments_intersect(p1, p2, r1, r2):
                return True

    return False
