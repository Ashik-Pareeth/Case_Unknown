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

# Detective settings
PLAYER_SIZE = 32
PLAYER_SPEED = 240

player = pygame.Rect(
    ROOM.centerx - PLAYER_SIZE // 2,
    ROOM.centery - PLAYER_SIZE // 2,
    PLAYER_SIZE,
    PLAYER_SIZE,
)

running = True

while running:
    delta_time = clock.tick(FPS) / 1000

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read keyboard input
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

    # Move horizontally and resolve wall collisions
    old_x = player.x
    player.x += round(direction.x * PLAYER_SPEED * delta_time)

    if any(player.colliderect(wall) for wall in walls):
        player.x = old_x

    # Move vertically and resolve wall collisions
    old_y = player.y
    player.y += round(direction.y * PLAYER_SPEED * delta_time)

    if any(player.colliderect(wall) for wall in walls):
        player.y = old_y

    # Draw the background and room
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, WALL_COLOR, ROOM)
    pygame.draw.rect(screen, FLOOR_COLOR, FLOOR)

    # Draw the floor grid
    grid_size = 48

    for x in range(FLOOR.left, FLOOR.right, grid_size):
        pygame.draw.line(screen, GRID_COLOR, (x, FLOOR.top), (x, FLOOR.bottom))

    for y in range(FLOOR.top, FLOOR.bottom, grid_size):
        pygame.draw.line(screen, GRID_COLOR, (FLOOR.left, y), (FLOOR.right, y))

    # Draw the detective
    pygame.draw.rect(screen, PLAYER_COLOR, player, border_radius=6)

    pygame.display.flip()

pygame.quit()
