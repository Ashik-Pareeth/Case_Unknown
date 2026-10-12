"""
Player character entity with 4-directional SVG sprite animation and collision physics.
"""

import pygame
from src.settings import (
    PLAYER_SPEED,
    PLAYER_HITBOX_WIDTH,
    PLAYER_HITBOX_HEIGHT,
    WALK_ANIM_SPEED,
    IDLE_ANIM_SPEED,
)
from assets.svg_assets import get_character_animations


class Player:
    def __init__(self, start_x: float, start_y: float):
        # Load all directional animations from SVG module
        self.animations = get_character_animations()

        # State & Direction
        self.direction = "down"   # "down", "up", "left", "right"
        self.state = "idle"       # "idle", "walk"
        self.frame_index = 0
        self.anim_timer = 0.0

        # Position (center of the foot collision box)
        self.pos = pygame.Vector2(start_x, start_y)
        self.velocity = pygame.Vector2(0, 0)

        # Hitbox dimensions (ground collision at feet)
        self.hitbox_w = PLAYER_HITBOX_WIDTH
        self.hitbox_h = PLAYER_HITBOX_HEIGHT

        # Initialize current surface & bounding rect
        self.image = self.animations[self.direction][self.state][0]
        self.sprite_w = self.image.get_width()
        self.sprite_h = self.image.get_height()

        # Cached hitboxes
        self.hitbox = pygame.Rect(0, 0, self.hitbox_w, self.hitbox_h)
        self.update_rects()

    def update_rects(self):
        """Synchronizes collision hitbox and sprite drawing rect with current pos."""
        self.hitbox.center = (round(self.pos.x), round(self.pos.y))
        # Foot anchor: sprite bottom aligns with bottom of hitbox
        self.sprite_x = self.hitbox.centerx - self.sprite_w // 2
        self.sprite_y = self.hitbox.bottom - self.sprite_h + 4

    def handle_input(self):
        """Reads keyboard inputs and determines movement vector and facing direction."""
        keys = pygame.key.get_pressed()
        move_vec = pygame.Vector2(0, 0)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move_vec.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move_vec.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_vec.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_vec.x += 1

        # Determine facing direction (prioritizing primary movement axis)
        if move_vec.length_squared() > 0:
            move_vec = move_vec.normalize()
            self.state = "walk"
            if abs(move_vec.x) > abs(move_vec.y):
                self.direction = "right" if move_vec.x > 0 else "left"
            else:
                self.direction = "down" if move_vec.y > 0 else "up"
        else:
            self.state = "idle"

        self.velocity = move_vec * PLAYER_SPEED

    def update(self, delta_time: float, solid_objects: list[pygame.Rect]):
        """Updates animation frames and performs collision-resolved movement."""
        # 1. Update Animation
        frames = self.animations[self.direction][self.state]
        speed = WALK_ANIM_SPEED if self.state == "walk" else IDLE_ANIM_SPEED
        self.anim_timer += delta_time

        if self.anim_timer >= speed:
            self.anim_timer -= speed
            self.frame_index = (self.frame_index + 1) % len(frames)

        # Clamping frame index if state changed
        if self.frame_index >= len(frames):
            self.frame_index = 0

        self.image = frames[self.frame_index]

        # 2. X-Axis Movement & Collision
        if self.velocity.x != 0:
            self.pos.x += self.velocity.x * delta_time
            self.update_rects()
            for obj in solid_objects:
                if self.hitbox.colliderect(obj):
                    if self.velocity.x > 0:
                        self.hitbox.right = obj.left
                    elif self.velocity.x < 0:
                        self.hitbox.left = obj.right
                    self.pos.x = self.hitbox.centerx
                    self.update_rects()

        # 3. Y-Axis Movement & Collision
        if self.velocity.y != 0:
            self.pos.y += self.velocity.y * delta_time
            self.update_rects()
            for obj in solid_objects:
                if self.hitbox.colliderect(obj):
                    if self.velocity.y > 0:
                        self.hitbox.bottom = obj.top
                    elif self.velocity.y < 0:
                        self.hitbox.top = obj.bottom
                    self.pos.y = self.hitbox.centery
                    self.update_rects()

    def get_interaction_reach(self) -> pygame.Rect:
        """Returns an interaction bounding area slightly extended forward from facing direction."""
        reach = self.hitbox.inflate(36, 36)
        if self.direction == "down":
            reach.y += 12
        elif self.direction == "up":
            reach.y -= 12
        elif self.direction == "left":
            reach.x -= 12
        elif self.direction == "right":
            reach.x += 12
        return reach

    def draw(self, surface: pygame.Surface):
        """Renders the player sprite."""
        surface.blit(self.image, (self.sprite_x, self.sprite_y))
