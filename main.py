import pygame
import random
import math


# self created distance formula
def distance(x1, y1, x2, y2):
    dist = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    return dist


# initialize PYGAME
pygame.init()

windowSize = 800, 600  # set window size
# create a window/screen
screen = pygame.display.set_mode(windowSize)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# RGB Color for the Screen using Sccrreen.fill
screen_color = 0, 0, 0
white = (255, 255, 255)
green = (255, 255, 255)
blue = (0, 0, 128)

# Score
score = 0

# create rectangle object from spaceship image
# Player
playerImg = pygame.image.load('spaceship1.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# create a Background
background_image = pygame.image.load('backgroundImage.png').convert()

# Enemies
no_of_enemies = 6
enemy_image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

# enemy
for i in range(no_of_enemies):
    enemy_image.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 50))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 0
bulletY_change = -1.5
bullet_state = "ready"


# Bullet Function
def firebullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))


# Collide function
def collide(x1, x2, y1, y2):
    if distance(x1, y1, x2, y2) <= 25:
        return True
    return False


# gameOver
def g_over(x1, x2, y1, y2):
    if distance(x1, y1, x2, y2) <= 32 or y1 >= 526:
        return True
    return False


# enemy function
def enemy(x, y):
    screen.blit(enemy_image[i], (x, y))


# player function
def player(x, y):
    # draw on window use screen.blit
    screen.blit(playerImg, (x, y))


def displayScore(blue, green):
    # Display Score
    font = pygame.font.Font('TanglewoodTales.ttf', 32)
    text = font.render("Score:" + str(score), 1, green, blue)
    textRect = text.get_rect()
    textRect.center = 50, 20
    screen.blit(text, textRect)


def displayGameOver(blue, green):
    font = pygame.font.Font('TanglewoodTales.ttf', 32)
    text = font.render("Game Over", 1, green, blue)
    textRect = text.get_rect()
    textRect.center = 800 // 2, 600 // 2
    screen.blit(text, textRect)


# Infinite loop for the screen to work
running = True
while running:

    # RGb background color
    screen.fill(screen_color)

    # background music and Music
    # pygame.mixer.music.load('background.wav')
    # pygame.mixer.music.play()
    # pygame.mixer.music.set_volume(1)
    # pygame.mixer.set_num_channels(3)

    for event in pygame.event.get():  # check every event
        if event.type == pygame.QUIT:  # if event is equals to close button or quit
            running = False  # it sets the running variable to False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change -= 1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change += 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                playerY_change += 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                playerY_change -= 1
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = pygame.mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX
                    bulletY = playerY
                    firebullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            playerX_change = 0
            playerY_change = 0
            # bulletY_change = -0.3

    # setting background
    screen.blit(background_image, [0, 0])
    displayScore(blue, green)
    playerX += playerX_change
    playerY += playerY_change

    # Setting boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    elif playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # bullet movement
    bulletY += bulletY_change

    for i in range(no_of_enemies):
        # movement of enemy
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # check if it collides with the enemy
        if collide(enemyX[i], bulletX, enemyY[i], bulletY):
            deathSound = pygame.mixer.Sound('explosion.wav')
            deathSound.play()
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 50)
            score += 1

        if g_over(enemyX[i], playerX, enemyY[i], playerY):
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            displayGameOver(blue, green)



        # draw player movement and enemy movement
        player(playerX, playerY)
        enemy(enemyX[i], enemyY[i])

    # bullet state
    if bullet_state is "fire":
        firebullet(bulletX, bulletY)

    if bulletY <= 0:
        bullet_state = "ready"

    pygame.display.update()
