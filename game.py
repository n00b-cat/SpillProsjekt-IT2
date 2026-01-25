import pygame, random

pygame.init()

windowWidth, windowHeight = 640, 480

tileSize = 32
tiles = []

class Tile():
    def __init__(self, x, y, type, color):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.type = type
        self.color = color

# Make map

ores = [
    "red",
    "green",
    "yellow",
    "blue",
    "white",
]

for x in range(20):
    for y in range(15):
        oreChance = random.randint(1, 100)
        
        if oreChance > 90:
            color = ores[random.randint(0, len(ores) -1)]
            type = "ore"
        else:
            color = "#8C5E53"
            type = "dirt"
        
        tiles.append(Tile(x * 32, y * 32, type, color))


# Game window
window = pygame.display.set_mode([windowWidth, windowHeight])
pygame.display.set_caption("Mining game")

for tile in tiles:
    if tile.rect.x <= 64 and tile.rect.y <= 64:
        tile.color = "#4A3A2D"
        tile.type = "empty"
    
running = True
clock = pygame.time.Clock()
deltaTime = 0

player = pygame.FRect(30, 30, 28, 28)
speed = 1
directionVector = pygame.math.Vector2()

# Gameloop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    directionVector.x = keys[pygame.K_d] - keys[pygame.K_a]
    directionVector.y = keys[pygame.K_s] - keys[pygame.K_w]

    if directionVector:
        directionVector = directionVector.normalize()
    
    player.x += directionVector.x * speed

    for tile in tiles:
        if player.colliderect(tile.rect) and tile.type != "empty":
            player.x -= directionVector.x * speed

    player.y += directionVector.y * speed

    for tile in tiles:
        if player.colliderect(tile.rect) and tile.type != "empty":
            player.y -= directionVector.y * speed

    window.fill("black")

    for tile in tiles:
        pygame.draw.rect(window, tile.color, tile.rect) 
        
    pygame.draw.rect(window, "blue", player) 

    pygame.display.update()

    deltaTime = clock.tick(60) / 1000

pygame.quit()