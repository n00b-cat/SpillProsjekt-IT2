import pygame, random

pygame.init()

# Game window
windowWidth, windowHeight = 640, 480
window = pygame.display.set_mode([windowWidth, windowHeight])
pygame.display.set_caption("Mining game")

# Surrounding tiles
def showTiles(cordinateX, cordinateY):
    for y in range(cordinateY -1, cordinateY + 2):
        for x in range(cordinateX -1, cordinateX + 2):
            for tile in tiles:
                if tile.rect.x // tileSize == x and tile.rect.y // tileSize == y:
                    tile.hidden = False
                    continue

# Make map
tileSize = 32
tiles = []

tileMapImage = pygame.image.load("tilemap.png")

class Tile():
    def __init__(self, x, y, type, value, health):
        self.rect = pygame.Rect(x, y, tileSize, tileSize)
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
        
        tiles.append(Tile(x * tileSize, y * tileSize, type, value, health))

for tile in tiles:
    if tile.rect.x // tileSize <= 3 and tile.rect.y // tileSize <= 3:
        tile.type = "empty"
        tile.hidden = False
        showTiles(tile.rect.x // tileSize, tile.rect.y // tileSize)

# Player stats 

class Player():
    def __init__(self):
        self.image = pygame.image.load("player.png")
        self.rect = pygame.FRect(30, 30, 20, 20)
        self.speed = 1.3
        self.directionVector = pygame.math.Vector2()
        
        self.lastMine = 0
        self.mineColldown = 1000
        self.mineDamage = 1
        self.money = 0

player = Player()

# Font
font = pygame.font.Font('Micro5-Regular.ttf', 32)

# Shop

shopOpen = False

class Button():
    def __init__(self, x, y , text, action):
        self.x = x
        self.y = y
        self.text = text
        self.action = action
        self.displayText = font.render("LOADING", True, "white", "Blue")
    
    def draw(self, surface):
        self.displayText = font.render(self.text, True, "white", "Blue")
        surface.blit(self.displayText, (self.x, self.y))
    
    def onClick(self, mousePos):
        self.rect = self.displayText.get_rect(topleft =(self.x, self.y))
        if self.rect.collidepoint(mousePos):
            self.action()

    def updateText(self, newText):
        self.text = newText

class Upgrade():
    def __init__(self, text, price):
        self.text = text
        self.price = price

upgradeList = [
    Upgrade("Damage", 15),
    Upgrade("Speed", 10),
    Upgrade("Cooldown", 15)
]

def buyDamageUpgrade():
    upgrade = upgradeList[0]
    if upgrade.price <= player.money:
        player.money -= upgrade.price
        player.mineDamage += 1
        upgrade.price = round(upgrade.price * 1.05, 2)
        upgrades[0].updateText(f"+1 Damage ${upgrade.price}")

def buySpeedUpgrade():
    upgrade = upgradeList[1]
    if upgrade.price <= player.money:
        player.money -= upgrade.price
        player.speed += 0.1
        upgrade.price = round(upgrade.price * 1.05, 2)
        upgrades[1].updateText(f"+0.1 speed ${upgrade.price}")

def buyMiningSpeedUpgrade():
    upgrade = upgradeList[2]
    if upgrade.price <= player.money:
        player.money -= upgrade.price
        player.mineColldown -= 50
        upgrade.price = round(upgrade.price * 1.05, 2)
        upgrades[2].updateText(f"-50ms Colldown ${upgrade.price}")

def openShop():
    global shopOpen
    shopOpen = not shopOpen

upgrades = []
upgrades.append(Button(230, 140, "+1 Damage $15", buyDamageUpgrade))
upgrades.append(Button(230, 190, "+0.1 speed $10", buySpeedUpgrade))
upgrades.append(Button(230, 240, "-50ms Colldown $15", buyMiningSpeedUpgrade))

shopButton = Button(560, 40, "Shop", openShop)

# Collisions

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
                
                tile.health -= player.mineDamage

                if tile.health <= 0:
                    tile.type = "empty"
                    player.money += tile.value
                    showTiles(tile.rect.x // tileSize, tile.rect.y // tileSize)
            else:
                if axis == "x":
                    player.rect.x -= player.directionVector.x * player.speed
                elif axis == "y":
                    player.rect.y -= player.directionVector.y * player.speed

# Gameloop
running = True
clock = pygame.time.Clock()
deltaTime = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mousePosition = pygame.mouse.get_pos()

            shopButton.onClick(mousePosition)

            if shopOpen:
                for upgrade in upgrades:
                    upgrade.onClick(mousePosition)

    keys = pygame.key.get_pressed()
    player.directionVector.x = keys[pygame.K_d] - keys[pygame.K_a]
    player.directionVector.y = keys[pygame.K_s] - keys[pygame.K_w]

    if player.directionVector:
        player.directionVector = player.directionVector.normalize()
    
    player.rect.x += player.directionVector.x * player.speed
    collision(tiles, "x")
                
    player.rect.y += player.directionVector.y * player.speed
    collision(tiles, "y")
                                                              
    # Draw
    window.fill("black")

    for tile in tiles:
        if (tile.type == "empty"):
            window.blit(tileMapImage, tile.rect, (tileSize* 5, tileSize, tileSize * 6, tileSize * 2))
        elif (tile.hidden):
            window.blit(tileMapImage, tile.rect, (tileSize, 0, tileSize * 2, tileSize))
        elif (tile.type == "dirt"):
            window.blit(tileMapImage, tile.rect, (0, 0, tileSize, tileSize))
        elif (tile.type == "ore"):
            window.blit(tileMapImage, tile.rect, (tileSize, tileSize * 3, tileSize * 2, tileSize * 4))

    window.blit(player.image, player, (0, 0, 24, 24))

    moneyCounter = font.render(f"Money: ${round(player.money, 2)}", True, "white", "black")
    window.blit(moneyCounter, (10, 10))
    
    shopButton.draw(window)
    
    if shopOpen:
        pygame.draw.rect(window, "black", (195, 100, 250, 300))

        for upgrade in upgrades:
            upgrade.draw(window)

    pygame.display.update()

    deltaTime = clock.tick(60) / 1000

pygame.quit()