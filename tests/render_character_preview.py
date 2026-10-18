"""
Generates a side-by-side preview sheet of all directional character animations.
"""

import os
import sys

os.environ["SDL_VIDEODRIVER"] = "dummy"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from assets.svg_assets import get_character_animations

pygame.init()
pygame.font.init()

anims = get_character_animations()
font = pygame.font.SysFont("georgia", 14, bold=True)
label_font = pygame.font.SysFont("segoeui", 11)

sheet = pygame.Surface((620, 430))
sheet.fill((22, 25, 31))

# Headers
title = font.render(
    "CASE UNKNOWN — DETECTIVE SPRITE ANIMATION SHEET", True, (215, 185, 125)
)
sheet.blit(title, (20, 15))

sheet.blit(label_font.render("IDLE (2 Frames)", True, (150, 160, 175)), (120, 42))
sheet.blit(label_font.render("WALK CYCLE (4 Frames)", True, (150, 160, 175)), (280, 42))

y = 65
for direction in ["down", "up", "right", "left"]:
    dir_label = font.render(direction.upper(), True, (196, 162, 94))
    sheet.blit(dir_label, (20, y + 25))

    x = 110
    for frame in anims[direction]["idle"]:
        sheet.blit(frame, (x, y))
        x += 70

    x = 270
    for frame in anims[direction]["walk"]:
        sheet.blit(frame, (x, y))
        x += 70

    # Separator
    pygame.draw.line(sheet, (35, 40, 50), (20, y + 84), (600, y + 84), 1)
    y += 90

out_path = r"C:/Users/Ashik/MyProjects/mypython/Case_Unknown/tests/output/character_preview.png"
pygame.image.save(sheet, out_path)
print("Saved preview to:", out_path)
