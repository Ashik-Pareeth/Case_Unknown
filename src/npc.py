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

    def _safe_directions(self):
        doorward = self._doorward_direction()
        return [direction for direction in _DIRECTIONS if direction != doorward]

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

    def draw_vision(self, surface: pygame.Surface):
        """Draw this NPC's 70-degree forward field of view."""
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
        points = [origin, *arc]
        pygame.draw.polygon(surface, (218, 174, 86, 24), points)
        pygame.draw.lines(surface, (218, 174, 86, 62), False, [origin, arc[0]], 1)
        pygame.draw.lines(surface, (218, 174, 86, 62), False, [origin, arc[-1]], 1)


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

    def draw_vision(self, surface: pygame.Surface, bounds: pygame.Rect):
        if not self.npcs:
            return
        vision_layer = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        vision_layer.set_clip(bounds)
        for npc in self.npcs:
            npc.draw_vision(vision_layer)
        surface.blit(vision_layer, (0, 0))
