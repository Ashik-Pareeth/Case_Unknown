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

_DIRECTIONS = ("down", "left", "up", "right")
NPC_COUNT_PER_ROOM = 3


class AutonomousNPC:
    """A patrolling NPC that walks, pauses for two seconds, then turns."""

    def __init__(self, start_pos: tuple[int, int], palette_index: int = 0, seed: int | None = None,
                 door_targets: tuple[tuple[int, int], ...] = ()):
        self.animations = get_npc_animations(palette_index)
        self.scaled_animations = {
            direction: {
                state: [pygame.transform.smoothscale(frame, (60, 76)) for frame in frames]
                for state, frames in states.items()
            }
            for direction, states in self.animations.items()
        }
        self.pos = pygame.Vector2(start_pos)
        self.hitbox = pygame.Rect(0, 0, 24, 14)
        self.sprite_size = (60, 76)
        self.door_targets = door_targets
        self.rng = random.Random(seed)
        self.state = "idle"
        self.frame_index = 0
        self.anim_timer = 0.0
        self.phase = "walk"
        self.phase_timer = self.rng.uniform(1.0, 2.4)
        self.speed = 58.0
        self.vision_range = 190
        self.vision_half_angle = 35
        self.direction = self.rng.choice(self._safe_directions())
        self.state = "walk"
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

    def _doorward_direction(self):
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

    def _is_facing_door(self, direction: str) -> bool:
        """Check if facing in direction points directly towards any doorway landing spot."""
        if not self.door_targets:
            return False
        origin = (round(self.pos.x), round(self.pos.y - 48))
        facing_angles = {"right": 0, "down": 90, "left": 180, "up": 270}
        facing = facing_angles[direction]
        for target in self.door_targets:
            dx = target[0] - origin[0]
            dy = target[1] - origin[1]
            dist = math.hypot(dx, dy)
            if dist <= self.vision_range + 30:
                angle_to_target = math.degrees(math.atan2(dy, dx)) % 360
                diff = (angle_to_target - facing + 180) % 360 - 180
                if abs(diff) <= self.vision_half_angle + 10:
                    return True
        return False

    def _safe_directions(self):
        safe = [d for d in _DIRECTIONS if not self._is_facing_door(d)]
        if not safe:
            doorward = self._doorward_direction()
            safe = [d for d in _DIRECTIONS if d != doorward]
        return safe if safe else list(_DIRECTIONS)

    def _turn(self, bounds: pygame.Rect):
        choices = [direction for direction in self._safe_directions() if direction != self.direction]
        if not choices:
            choices = self._safe_directions()
        self.direction = self.rng.choice(choices)
        self.state = "idle"
        self.phase = "wait"
        self.phase_timer = 2.0
        self.frame_index = 0

    def update(self, delta_time: float, bounds: pygame.Rect, solid_objects: list[pygame.Rect], other_npcs=()):
        self.phase_timer -= delta_time
        if self.phase == "wait":
            if self.phase_timer <= 0:
                self.phase = "walk"
                self.phase_timer = self.rng.uniform(1.2, 2.8)
                if self.direction not in self._safe_directions():
                    self.direction = self.rng.choice(self._safe_directions())
                self.state = "walk"
        else:
            if self.direction not in self._safe_directions():
                self._turn(bounds)
                self._set_image()
                return
            movement = {
                "down": (0, 1), "up": (0, -1),
                "left": (-1, 0), "right": (1, 0),
            }[self.direction]
            old_pos = self.pos.copy()
            self.pos.x += movement[0] * self.speed * delta_time
            self.pos.y += movement[1] * self.speed * delta_time
            self._update_rects()
            if (not bounds.contains(self.hitbox)
                    or any(self.hitbox.colliderect(obj) for obj in solid_objects)
                    or any(self.hitbox.colliderect(obj) for obj in other_npcs)):
                self.pos = old_pos
                self._update_rects()
                self._turn(bounds)
            elif self.phase_timer <= 0:
                self._turn(bounds)

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

    def draw_vision(self, surface: pygame.Surface, is_alert: bool = False):
        """Draw this NPC's 70-degree forward field of view."""
        points = self.get_vision_points()
        origin = points[0]
        arc = points[1:]
        poly_color = (235, 65, 65, 48) if is_alert else (218, 174, 86, 24)
        line_color = (245, 80, 80, 110) if is_alert else (218, 174, 86, 62)
        pygame.draw.polygon(surface, poly_color, points)
        pygame.draw.lines(surface, line_color, False, [origin, arc[0]], 1)
        pygame.draw.lines(surface, line_color, False, [origin, arc[-1]], 1)

    def collides_with_vision(
        self,
        target,
        bounds: pygame.Rect | None = None,
        solid_objects: list[pygame.Rect] | None = None,
    ) -> bool:
        """Check if target (Player, Rect, or point) collides with this viewpoint."""
        poly = self.get_vision_points()
        origin = poly[0]

        # 1. Point / coordinates
        if isinstance(target, (tuple, list, pygame.Vector2)):
            pt = (round(target[0]), round(target[1]))
            if bounds is not None and not bounds.collidepoint(pt):
                return False
            if not point_in_polygon(pt[0], pt[1], poly):
                return False
            if solid_objects:
                for obj in solid_objects:
                    if obj.clipline(origin, pt):
                        return False
            return True

        # 2. Player entity: evaluate ground contact point and core footprint
        hitbox = getattr(target, "hitbox", target if isinstance(target, pygame.Rect) else None)
        if hitbox is None:
            return False

        if bounds is not None and not bounds.colliderect(hitbox):
            return False

        target_pos = (
            (round(target.pos.x), round(target.pos.y))
            if hasattr(target, "pos")
            else hitbox.center
        )

        # Detective has only entered the viewpoint if their ground position (feet)
        # or core ground contact area is physically inside the viewpoint polygon.
        is_inside = point_in_polygon(target_pos[0], target_pos[1], poly) or (
            polygon_collides_with_rect(poly, hitbox.inflate(-8, -4))
        )
        if not is_inside:
            return False

        # Line of sight check: ensure solid walls/furniture block detection
        if solid_objects:
            for obj in solid_objects:
                if obj.clipline(origin, target_pos):
                    return False

        return True



class RoomNPCController:
    """Owns independent NPCs for one room and updates their patrols."""

    def __init__(self, room_id: str, bounds: pygame.Rect, solid_objects: list[pygame.Rect]):
        patrol = NPC_PATROLS.get(room_id)
        self.npcs = []
        self._seed = sum(map(ord, room_id))
        if patrol is None:
            return

        start_pos = patrol
        door_walls = [door["wall"] for door in ROOMS_DATA[room_id].get("doors", [])]
        door_targets = tuple({
            "left": (bounds.left, bounds.centery),
            "right": (bounds.right, bounds.centery),
            "top": (bounds.centerx, bounds.top),
            "bottom": (bounds.centerx, bounds.bottom),
        }[wall] for wall in door_walls)

        candidates = [(x, y)
            for y in range(bounds.top + 48, bounds.bottom - 45, 46)
            for x in range(bounds.left + 48, bounds.right - 45, 52)]
        random.Random(self._seed).shuffle(candidates)
        candidates.insert(0, start_pos)
        occupied = []
        for candidate in candidates:
            spawn_hitbox = pygame.Rect(0, 0, 24, 14)
            spawn_hitbox.center = candidate
            near_door = any(pygame.Vector2(candidate).distance_to(target) < 62 for target in door_targets)
            too_close = any(pygame.Vector2(candidate).distance_to(pos) < 68 for pos in occupied)
            if (not bounds.contains(spawn_hitbox) or near_door or too_close
                    or any(spawn_hitbox.colliderect(obj) for obj in solid_objects)):
                continue
            index = len(self.npcs)
            self.npcs.append(AutonomousNPC(
                candidate, index % 2,
                seed=self._seed + index * 7919 + random.randrange(1_000_000),
                door_targets=door_targets,
            ))
            occupied.append(candidate)
            if len(self.npcs) >= NPC_COUNT_PER_ROOM:
                break

    def update(self, delta_time: float, bounds: pygame.Rect, solid_objects: list[pygame.Rect]):
        for index, npc in enumerate(self.npcs):
            other_hitboxes = [other.hitbox for other in self.npcs if other is not npc]
            npc.update(delta_time, bounds, solid_objects, other_hitboxes)

    def draw_queue(self, surface: pygame.Surface):
        return [
            {"sort_y": npc.sort_y, "draw": lambda actor=npc: actor.draw(surface)}
            for npc in self.npcs
        ]

    def draw_vision(self, surface: pygame.Surface, bounds: pygame.Rect, alerted_npcs: set[AutonomousNPC] | None = None):
        if not self.npcs:
            return
        vision_layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        vision_layer.set_clip(bounds)
        for npc in self.npcs:
            is_alert = bool(alerted_npcs and npc in alerted_npcs)
            npc.draw_vision(vision_layer, is_alert=is_alert)
        surface.blit(vision_layer, (0, 0))

    def check_player_spotted(
        self,
        target,
        bounds: pygame.Rect | None = None,
        solid_objects: list[pygame.Rect] | None = None,
    ) -> bool:
        """Returns True if the target collides with any NPC's viewpoint points."""
        for npc in self.npcs:
            if npc.collides_with_vision(target, bounds=bounds, solid_objects=solid_objects):
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

