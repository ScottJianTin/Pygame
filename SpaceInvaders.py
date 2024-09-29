# Pre-requisites: install library below
import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((800, 600))

# Insert background pic
background = pygame.image.load('space.jpg')

# Insert background music
mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption('Space Invaders')
icon_img = pygame.image.load('ufo.png')
pygame.display.set_icon(icon_img)

# Player
player_img = pygame.image.load('spaceship.png')
pygame.display.set_icon(player_img)
playerX = 370
playerY = 480
playerX_change = 0


def Player(x, y):
    screen.blit(player_img, (x, y))


# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemy = 6

for i in range(num_enemy):
    enemy_img.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)


def Enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# Bullet
bullet_img = pygame.image.load('bullet.png')
pygame.display.set_icon(bullet_img)
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.5
bullet_state = 'ready'


def Bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Score
score_value = 0
font = pygame.font.SysFont('comicsans', 36)
textX = 10
textY = 10


# print(pygame.font.get_fonts())

def showScore(x, y):
    score = font.render("Score: " + str(score_value) + "  (Target Score: 10)", True, (0, 255, 0))
    screen.blit(score, (x, y))


# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 300)


def game_over_text():
    over_text = font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (325, 250))

# Congratulations
congratz_font = pygame.font.Font('freesansbold.ttf', 300)


def congratz_text():
    congrat_text = font.render('CONGRATULATIONS', True, (255, 255, 255))
    screen.blit(congrat_text, (325, 250))


running = True
while running:
    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 1
            elif event.key == pygame.K_RIGHT:
                playerX_change += 1
            elif event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    Bullet(bulletX, bulletY)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    playerX += playerX_change

    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0

    enemyX[i] += enemyX_change[i]

    # when enemy touches border, it moves in opposite direction and down automatically
    if enemyX[i] >= 736:
        enemyX[i] = 736
    elif enemyX[i] <= 0:
        enemyX[i] = 0

    for i in range(num_enemy):

        # Congratulations
        if score_value == 10:
            congratz_text()
            break

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = .3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        Enemy(enemyX[i], enemyY[i], i)


    # movement of bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        Bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    Player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()
