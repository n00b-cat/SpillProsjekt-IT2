import pygame, random

pygame.init()

# Game window
windowWidth, windowHeight = 640, 480
window = pygame.display.set_mode([windowWidth, windowHeight])
pygame.display.set_caption("Mining game")

# Make map
tileSize = 32
tiles = []

tileMapImage = pygame.image.load("tilemap.png")

class Tile():
    def __init__(self, x, y, type, value):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.type = type
        self.value = value

for x in range(20):
    for y in range(15):
        oreChance = random.randint(1, 100)
        
        if oreChance > 90:
            type = "ore"
            value = 20
        else:
            type = "dirt"
            value = 1
        
        tiles.append(Tile(x * 32, y * 32, type, value))


for tile in tiles:
    if tile.rect.x <= 64 and tile.rect.y <= 64:
        tile.type = "empty"

# Player stats 
player = pygame.FRect(30, 30, 20, 20)
playerSpeed = 1.3
directionVector = pygame.math.Vector2()
playerImage = pygame.image.load("player.png")

lastMine = 0
mineColldown = 500
money = 0

# Font
font = pygame.font.Font('Micro5-Regular.ttf', 32)

# Shop
shopText = font.render(f"Shop", True, "white", "black")
shopTextRect = shopText.get_rect(topleft =(560, 10))
shopOpen = False

# Gameloop
running = True
clock = pygame.time.Clock()
deltaTime = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            mousePosition = pygame.mouse.get_pos()

            if (shopTextRect.collidepoint(mousePosition)) and event.button == 1:
                if shopOpen:
                    shopOpen = False
                    print("close")
                else:
                    shopOpen = True
                    print("open")

    keys = pygame.key.get_pressed()
    directionVector.x = keys[pygame.K_d] - keys[pygame.K_a]
    directionVector.y = keys[pygame.K_s] - keys[pygame.K_w]

    if directionVector:
        directionVector = directionVector.normalize()
    
    player.x += directionVector.x * playerSpeed

    for tile in tiles:
        if player.colliderect(tile.rect) and tile.type != "empty":
            currentTime = pygame.time.get_ticks()

            if currentTime - lastMine >= mineColldown:
                lastMine = currentTime
                player.x -= (directionVector.x * playerSpeed) * 6
                tile.type = "empty"
                money += tile.value
            else:
                player.x -= directionVector.x * playerSpeed
                

    player.y += directionVector.y * playerSpeed

    for tile in tiles:
        if player.colliderect(tile.rect) and tile.type != "empty":
            currentTime = pygame.time.get_ticks()

            if currentTime - lastMine >= mineColldown:
                lastMine = currentTime
                player.y -= (directionVector.y * playerSpeed) * 6
                tile.type = "empty"
                money += tile.value
            else:
                player.y -= directionVector.y * playerSpeed
    # Draw
    window.fill("black")

    for tile in tiles:
        if (tile.type == "empty"):
            window.blit(tileMapImage, tile.rect, (0, 0, 32, 32))
        elif (tile.type == "dirt"):
            window.blit(tileMapImage, tile.rect, (32, 0, 64, 32))
        elif (tile.type == "ore"):
            window.blit(tileMapImage, tile.rect, (64, 0, 96, 32))

    window.blit(playerImage, player, (0, 0, 24, 24))

    moneyCounter = font.render(f"Money: {money}", True, "white", "black")
    window.blit(moneyCounter, (10, 10))
    
    window.blit(shopText, (560, 10))
    
    if shopOpen:
        pygame.draw.rect(window, "black", (220, 100, 200, 300))
        window.blit(shopText, (300, 110))

    pygame.display.update()

    deltaTime = clock.tick(60) / 1000

pygame.quit()