import pygame
import random
import math

#Initializing the game
pygame.init()

#Creating the main window
screen = pygame.display.set_mode((600, 400))

#Changing the caption of the game window
pygame.display.set_caption("Space Invaders")

#To set the icon
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#Background
background = pygame.image.load("background.png")

#Player
playerImg = pygame.image.load('player.png')
playerX = 300-(64/2)
playerY = 350
playerChangeX = 0

enemyImg = []
enemyX = []
enemyY = []
enemyChangeX = []
enemyChangeY = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 536))
    enemyY.append(random.randint(0, 40))
    enemyChangeX.append(2)
    enemyChangeY.append(10)

#Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 350
bulletChangeX= 0
bulletChangeY= 5
bullet_state = "ready"

#Initialization functions
def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False

#Score

score_value = 0
textX = 10
textY = 10

font = pygame.font.Font("freesansbold.ttf", 30)

def show_score(x, y):
    score = font.render(str(score_value), True,  (255, 255, 255))
    screen.blit(score, (x, y))

#Game loop
running = True
while running:

    #Changing the background color of the gaming window and setting the background image
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                playerChangeX = -2
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                playerChangeX = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            playerChangeX = 0

#Player staying within the boarder
    playerX += playerChangeX

    if playerX <= 0:
        playerX = 0
    elif playerX >= 536:
        playerX = 536


    for i in range(num_of_enemies):
        #Enemy staying within the boundary
        enemyX[i] += enemyChangeX[i]
        
        if enemyX[i] <= 0:
            enemyChangeX[i] = 1
            enemyY[i] += enemyChangeY[i]
        elif enemyX[i] >= 536:
            enemyChangeX[i] = -1
            enemyY[i] += enemyChangeY[i]

        #Collision physics
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 350
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 536)
            enemyY[i] = random.randint(0, 40)

        enemy(enemyX[i], enemyY[i], i)

    #Bullet Movement
    if bulletY <=0:
        bulletY = 350
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletChangeY

    player(playerX, playerY)
    show_score(textX, textY)
    #To update the game window
    pygame.display.update()