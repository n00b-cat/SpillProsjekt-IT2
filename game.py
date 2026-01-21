import pygame, random

pygame.init()

WindowWidth, WindowHeight = 640, 480
player_x = 10
player_y = 10
speed = 0.1

ores = [
    "red",
    "green",
    "yellow",
    "blue",
    "white",
]

tileSize = 32
tiles = []

class Tile():
    def __init__(self, x, y, type, color):
        self.x = x
        self.y = y
        self.type = type
        self.color = color

# Make map
for x in range(20):
    for y in range(15):
        orechance = random.randint(1, 100)
        
        if orechance > 90:
            color = ores[random.randint(0, len(ores) -1)]
            type = "ore"
        else:
            color = "#8C5E53"
            type = "dirt"
        
        tiles.append(Tile(x * tileSize,y * tileSize, type, color))

# Game window
window = pygame.display.set_mode([WindowWidth, WindowHeight])
pygame.display.set_caption("Epic Mining game")

for tile in tiles:
    if tile.x / 32 <= 2 and tile.y / 32 <= 2:
        tile.color = "#4A3A2D"
        tile.type = "empty"
    

running = True

# Gameloop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed
    if keys[pygame.K_UP]:
        player_y -= speed
    if keys[pygame.K_DOWN]:
        player_y += speed
    if keys[pygame.K_SPACE]:
        print(player_x // tileSize, player_y // tileSize)

    window.fill("black")

    for tile in tiles:
        pygame.draw.rect(window, tile.color, (tile.x, tile.y, tileSize, tileSize)) 
        
    pygame.draw.rect(window, (73, 119, 238), (player_x, player_y, 32, 32)) 

    pygame.display.update()

pygame.quit()