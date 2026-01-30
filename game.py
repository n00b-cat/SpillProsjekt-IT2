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

class Player():
    def __init__(self, speed):
        self.rect = pygame.FRect(30, 30, 20, 20)
        self.speed = speed
        self.directionVector = pygame.math.Vector2()
        self.image = pygame.image.load("player.png")
        
        self.lastMine = 0
        self.mineColldown = 1000
        self.money = 0

player = Player(1.3)

# Font
font = pygame.font.Font('Micro5-Regular.ttf', 32)

# Shop
shopOpen = False

shopText = font.render(f"Shop", True, "white", "black")
shopTextRect = shopText.get_rect(topleft =(560, 10))

upgradePrice = 15

# Gameloop
running = True
clock = pygame.time.Clock()
deltaTime = 0

def collision(tiles, axis):
    for tile in tiles:
        if player.rect.colliderect(tile.rect) and tile.type != "empty":
            currentTime = pygame.time.get_ticks()

            if currentTime - player.lastMine >= player.mineColldown:
                player.lastMine = currentTime
                if axis == "x":
                    player.rect.x -= (player.directionVector.x * player.speed) * 6
                elif axis == "y":
                    player.rect.y -= (player.directionVector.y * player.speed) * 6

                tile.type = "empty"
                player.money += tile.value
            else:
                if axis == "x":
                    player.rect.x -= player.directionVector.x * player.speed
                elif axis == "y":
                    player.rect.y -= player.directionVector.y * player.speed

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            mousePosition = pygame.mouse.get_pos()

            if (shopTextRect.collidepoint(mousePosition)) and event.button == 1:
                if shopOpen:
                    shopOpen = False
                else:
                    shopOpen = True
                
            elif (upgradeTextRect.collidepoint(mousePosition)) and event.button == 1 and player.money >= upgradePrice:
                player.money -= upgradePrice
                upgradePrice = upgradePrice * 1.05
                player.mineColldown -= 100

    keys = pygame.key.get_pressed()
    player.directionVector.x = keys[pygame.K_d] - keys[pygame.K_a]
    player.directionVector.y = keys[pygame.K_s] - keys[pygame.K_w]

    if player.directionVector:
        player.directionVector = player.directionVector.normalize()

    # Surrounding tiles
    # cordinateX = int(player.rect.x // 32)
    # cordinateY = int(player.rect.y // 32)

    # for y in range(cordinateY -1, cordinateY + 2):
    #     for x in range(cordinateX -1, cordinateX + 2):
    #         print(f"x:{x}, y:{y}")
    
    player.rect.x += player.directionVector.x * player.speed
    collision(tiles, "x")
                
    player.rect.y += player.directionVector.y * player.speed
    collision(tiles, "y")

    for tile in tiles:
        if player.rect.colliderect(tile.rect) and tile.type != "empty":
            currentTime = pygame.time.get_ticks()

            if currentTime - player.lastMine >= player.mineColldown:
                player.lastMine = currentTime
                player.rect.y -= (player.directionVector.y * player.speed) * 6
                tile.type = "empty"
                player.money += tile.value
            else:
                player.rect.y -= player.directionVector.y * player.speed
    # Draw
    window.fill("black")

    for tile in tiles:
        if (tile.type == "empty"):
            window.blit(tileMapImage, tile.rect, (160, 32, 192, 64))
        elif (tile.type == "dirt"):
            window.blit(tileMapImage, tile.rect, (32, 0, 64, 32))
        elif (tile.type == "ore"):
            window.blit(tileMapImage, tile.rect, (32, 96, 64, 128))

    window.blit(player.image, player, (0, 0, 24, 24))

    moneyCounter = font.render(f"Money: ${player.money}", True, "white", "black")
    window.blit(moneyCounter, (10, 10))
    
    window.blit(shopText, (560, 10))

    upgradeText = font.render(f"Mining Speed +1 ${upgradePrice}", True, "black", "white")
    upgradeTextRect = upgradeText.get_rect(topleft =(230, 150))
    
    if shopOpen:
        pygame.draw.rect(window, "black", (220, 100, 200, 300))
        window.blit(shopText, (300, 110))
        window.blit(upgradeText, (230, 150))

    pygame.display.update()

    deltaTime = clock.tick(60) / 1000

pygame.quit()