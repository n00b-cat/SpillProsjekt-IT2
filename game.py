import pygame, random

pygame.init()

# Game window
windowWidth, windowHeight = 640, 480
window = pygame.display.set_mode([windowWidth, windowHeight])
pygame.display.set_caption("Mining game")

# Make map
tileSize = 32
tiles = []

image = pygame.image.load("tilemap.png")

class Tile():
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.type = type

for x in range(20):
    for y in range(15):
        oreChance = random.randint(1, 100)
        
        if oreChance > 90:
            type = "ore"
        else:
            type = "dirt"
        
        tiles.append(Tile(x * 32, y * 32, type))


for tile in tiles:
    if tile.rect.x <= 64 and tile.rect.y <= 64:
        tile.type = "empty"
    
player = pygame.FRect(30, 30, 20, 20)
speed = 1.3
directionVector = pygame.math.Vector2()
lastMine = 0
mineColldown = 500

# Gameloop
running = True
clock = pygame.time.Clock()
deltaTime = 0

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
            currentTime = pygame.time.get_ticks()

            if currentTime - lastMine >= mineColldown:
                lastMine = currentTime
                player.x -= (directionVector.x * speed) * 6
                tile.type = "empty"
            else:
                player.x -= directionVector.x * speed
                

    player.y += directionVector.y * speed

    for tile in tiles:
        if player.colliderect(tile.rect) and tile.type != "empty":
            currentTime = pygame.time.get_ticks()

            if currentTime - lastMine >= mineColldown:
                lastMine = currentTime
                player.y -= (directionVector.y * speed) * 6
                tile.type = "empty"
            else:
                player.y -= directionVector.y * speed
    # Draw
    window.fill("black")

    for tile in tiles:
        if (tile.type == "empty"):
            window.blit(image, tile.rect, (0, 0, 32, 32))
        elif (tile.type == "dirt"):
            window.blit(image, tile.rect, (32, 0, 64, 32))
        elif (tile.type == "ore"):
            window.blit(image, tile.rect, (64, 0, 96, 32))

    pygame.draw.rect(window, "blue", player) 

    pygame.display.update()

    deltaTime = clock.tick(60) / 1000

pygame.quit()