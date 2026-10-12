import pygame

pygame.init()

# Window settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Case Unknown")

clock = pygame.time.Clock()

# Room settings
ROOM = pygame.Rect(80, 60, 800, 520)
WALL_THICKNESS = 24
FLOOR = ROOM.inflate(-2 * WALL_THICKNESS, -2 * WALL_THICKNESS)

# Colors
BACKGROUND_COLOR = (20, 22, 26)
WALL_COLOR = (65, 69, 76)
FLOOR_COLOR = (35, 38, 43)
GRID_COLOR = (43, 46, 52)
PLAYER_COLOR = (220, 220, 220)

# Create the four solid walls
walls = [
    pygame.Rect(ROOM.left, ROOM.top, ROOM.width, WALL_THICKNESS),
    pygame.Rect(ROOM.left, ROOM.bottom - WALL_THICKNESS, ROOM.width, WALL_THICKNESS),
    pygame.Rect(
        ROOM.left,
        ROOM.top + WALL_THICKNESS,
        WALL_THICKNESS,
        ROOM.height - 2 * WALL_THICKNESS,
    ),
    pygame.Rect(
        ROOM.right - WALL_THICKNESS,
        ROOM.top + WALL_THICKNESS,
        WALL_THICKNESS,
        ROOM.height - 2 * WALL_THICKNESS,
    ),
]

# Furniture settings & images
table_image = pygame.image.load(
    "assets/images/furniture/clerk_table.png"
).convert_alpha()
sofa_image = pygame.image.load("assets/images/furniture/sofa.png").convert_alpha()

table_image = pygame.transform.smoothscale(table_image, (180, 125))
sofa_image = pygame.transform.smoothscale(sofa_image, (190, 125))

furniture = [
    {
        "image": table_image,
        "rect": table_image.get_rect(topleft=(180, 150)),
        "hitbox_insets": (12, 20, 12, 8),
    },
    {
        "image": sofa_image,
        "rect": sofa_image.get_rect(topleft=(180, 390)),
        "hitbox_insets": (10, 18, 10, 6),
    },
]

# Compute furniture hitboxes (left, top, right, bottom insets)
for item in furniture:
    left, top, right, bottom = item["hitbox_insets"]
    rect = item["rect"]
    item["hitbox"] = pygame.Rect(
        rect.left + left,
        rect.top + top,
        rect.width - left - right,
        rect.height - top - bottom,
    )

# Detective settings
PLAYER_SIZE = 32
PLAYER_SPEED = 240

player_image = pygame.image.load(
    "assets/images/characters/charcter_front.png"
).convert_alpha()
player_image = pygame.transform.scale(player_image, (48, 60))

player = pygame.Rect(
    ROOM.centerx - PLAYER_SIZE // 2,
    ROOM.centery - PLAYER_SIZE // 2,
    PLAYER_SIZE,
    PLAYER_SIZE,
)

# Solid obstacles (walls + calculated furniture hitboxes)
solid_objects = walls + [item["hitbox"] for item in furniture]

running = True

while running:
    delta_time = clock.tick(FPS) / 1000

    # 1. Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Player Input & Movement
    keys = pygame.key.get_pressed()
    direction = pygame.Vector2(0, 0)

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        direction.y -= 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        direction.y += 1
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        direction.x -= 1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        direction.x += 1

    if direction.length_squared() > 0:
        direction = direction.normalize()

    # Move X and collide
    old_x = player.x
    player.x += round(direction.x * PLAYER_SPEED * delta_time)
    if any(player.colliderect(obj) for obj in solid_objects):
        player.x = old_x

    # Move Y and collide
    old_y = player.y
    player.y += round(direction.y * PLAYER_SPEED * delta_time)
    if any(player.colliderect(obj) for obj in solid_objects):
        player.y = old_y

    # 3. Drawing / Rendering
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, WALL_COLOR, ROOM)
    pygame.draw.rect(screen, FLOOR_COLOR, FLOOR)

    # Floor grid
    grid_size = 48
    for x in range(FLOOR.left, FLOOR.right, grid_size):
        pygame.draw.line(screen, GRID_COLOR, (x, FLOOR.top), (x, FLOOR.bottom))
    for y in range(FLOOR.top, FLOOR.bottom, grid_size):
        pygame.draw.line(screen, GRID_COLOR, (FLOOR.left, y), (FLOOR.right, y))

    # Draw furniture
    for item in furniture:
        screen.blit(item["image"], item["rect"])

    # Draw detective
    sprite_x = player.centerx - player_image.get_width() // 2
    sprite_y = player.bottom - player_image.get_height()
    screen.blit(player_image, (sprite_x, sprite_y))

    # Update frame
    pygame.display.flip()

pygame.quit()
