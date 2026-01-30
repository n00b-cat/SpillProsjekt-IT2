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
    def __init__(self, x, y, type, value, health):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.type = type
        self.value = value
        self.health = health
        self.hidden = True

for x in range(20):
    for y in range(15):
        oreChance = random.randint(1, 100)
        
        if oreChance > 90:
            type = "ore"
            value = 20
            health = 4
        else:
            type = "dirt"
            value = 1
            health = 2
        
        tiles.append(Tile(x * 32, y * 32, type, value, health))

for tile in tiles:
    if tile.rect.x // tileSize <= 3 and tile.rect.y // tileSize <= 3:
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
        self.mineDamage = 1
        self.money = 0

player = Player(1.3)

# Font
font = pygame.font.Font('Micro5-Regular.ttf', 32)

# Shop
shopOpen = False

class UpgradeButton(pygame.sprite.Sprite):
    def __init__(self, x, y, text, price, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.text = text
        self.price = price
        self.displayText = font.render("LOADING", True, "white", "Blue")
    
    def update(self):
        self.displayText = font.render(f"{self.text} ${round(self.price, 2)}", True, "white", "Blue")
        self.rect = self.displayText.get_rect(topleft =(self.x, self.y))
    
    def checkBuy(self, mousePos):
        if (self.rect.collidepoint(mousePos)) and player.money >= self.price and shopOpen:
            player.money -= self.price
            self.price = self.price * 1.05
            player.mineColldown -= 100

    def draw(self, surface):
        surface.blit(self.displayText, (self.x, self.y))

upgrades = pygame.sprite.Group()

miningColldown = UpgradeButton(230, 150, "-100ms Colldown", 15, upgrades)
miningDamage = UpgradeButton(230, 230, "+1 Damage", 20, upgrades)

shopText = font.render(f"Shop", True, "white", "black")
shopTextRect = shopText.get_rect(topleft =(560, 10))

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
                
                tile.health -= 1

                if tile.health <= 0:
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
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mousePosition = pygame.mouse.get_pos()

            if (shopTextRect.collidepoint(mousePosition)):
                if shopOpen:
                    shopOpen = False
                else:
                    shopOpen = True
            else:
                for upgrade in upgrades:
                    upgrade.checkBuy(mousePosition)

    keys = pygame.key.get_pressed()
    player.directionVector.x = keys[pygame.K_d] - keys[pygame.K_a]
    player.directionVector.y = keys[pygame.K_s] - keys[pygame.K_w]

    if player.directionVector:
        player.directionVector = player.directionVector.normalize()

    # Surrounding tiles
    # cordinateX = int(player.rect.x // tileSize)
    # cordinateY = int(player.rect.y // tileSize)

    # for y in range(cordinateY -1, cordinateY + 2):
    #     for x in range(cordinateX -1, cordinateX + 2):
    #         print(f"x:{x}, y:{y}")
    
    player.rect.x += player.directionVector.x * player.speed
    collision(tiles, "x")
                
    player.rect.y += player.directionVector.y * player.speed
    collision(tiles, "y")
                                                              
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

    moneyCounter = font.render(f"Money: ${round(player.money)}", True, "white", "black")
    window.blit(moneyCounter, (10, 10))
    
    upgrades.update()

    window.blit(shopText, (560, 10))
    
    if shopOpen:
        pygame.draw.rect(window, "black", (220, 100, 200, 300))
        window.blit(shopText, (300, 110))

        for upgrade in upgrades:
            upgrade.draw(window)

    pygame.display.update()

    deltaTime = clock.tick(60) / 1000

pygame.quit()