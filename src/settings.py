"""
Global configuration and game settings for Case Unknown.
"""

# Display settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60
TITLE = "Case Unknown — Detective Office"

# Room settings
ROOM_X = 60
ROOM_Y = 50
ROOM_WIDTH = 840
ROOM_HEIGHT = 540
WALL_THICKNESS = 24

# Player movement & physics
PLAYER_SPEED = 210  # Pixels per second
PLAYER_HITBOX_WIDTH = 28
PLAYER_HITBOX_HEIGHT = 16
PLAYER_SPRITE_WIDTH = 52
PLAYER_SPRITE_HEIGHT = 68

# Animation settings
WALK_ANIM_SPEED = 0.13  # Seconds per frame in walk cycle
IDLE_ANIM_SPEED = 0.50  # Seconds per frame in subtle idle cycle

# Color Palette (Atmospheric Noir)
COLOR_BG = (14, 16, 20)
COLOR_WALL = (42, 46, 54)
COLOR_WALL_TOP = (58, 64, 74)
COLOR_WALL_BASE = (30, 33, 40)
COLOR_FLOOR_A = (50, 38, 30)       # Rich mahogany parquet tone
COLOR_FLOOR_B = (44, 34, 26)       # Alternating parquet plank
COLOR_FLOOR_SEAM = (32, 24, 18)
COLOR_SHADOW = (10, 12, 16, 90)

# UI Theme (Vintage Detective / Brass Accents)
UI_PANEL_BG = (22, 25, 31, 235)
UI_PANEL_BORDER = (196, 162, 94)    # Antique brass
UI_TEXT_TITLE = (235, 205, 145)
UI_TEXT_BODY = (225, 228, 232)
UI_TEXT_MUTED = (150, 155, 165)
UI_HIGHLIGHT_RED = (215, 65, 65)
