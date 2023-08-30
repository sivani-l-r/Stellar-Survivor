import pygame
import random
import sys
from pygame import mixer

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)
ENEMY_SPEED = 1.3
PLAYER_SPEED = 3
POINT_SPEED = 3
NUM_ENEMIES = 4
NUM_POINTS = 6

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Stellar Survivor')
icon = pygame.image.load('Images/icon.png')
pygame.display.set_icon(icon)

# Load assets
bg_img = pygame.image.load('Images/bg.png')
start_img = pygame.image.load('Images/start.png')
play_button_rect = pygame.Rect(300, 400, 200, 50)
player_img = pygame.image.load('Images/player.png')
point_img = [pygame.image.load('Images/point.png') for _ in range(NUM_POINTS)]
enemy_img = [pygame.image.load('Images/enemy.png') for _ in range(NUM_ENEMIES)]
font = pygame.font.Font('game_over.ttf', 50)
font_2 = pygame.font.Font('game_over.ttf', 150)

# Load sounds
mixer.music.load('Sound/bg.mp3')
collision_sound = mixer.Sound('Sound/collision.wav')
point_sound = mixer.Sound('Sound/point.mp3')

# Initialize player
playerX = 375
playerY = 520
playerX_change = 0

# Initialize enemies
enemyX = [random.randint(0, SCREEN_WIDTH - 32) for _ in range(NUM_ENEMIES)]
enemyY = [random.randint(0, 45) for _ in range(NUM_ENEMIES)]

# Initialize points
pointX = [random.randint(0, SCREEN_WIDTH - 32) for _ in range(NUM_POINTS)]
pointY = [random.randint(0, 45) for _ in range(NUM_POINTS)]

# Initialize game variables
hits = 5
score = 0

def show_stats():
    score_obj = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_obj, (10, 10))
    hits_obj = font.render("Hits : " + str(hits), True, (255, 255, 255))
    screen.blit(hits_obj, (10, 30))

def player(x, y):
    screen.blit(player_img, (x, y))

def point(x, y, i):
    screen.blit(point_img[i], (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def isCollision(enemyX, enemyY, playerX, playerY, i):
    player_rect = player_img.get_rect(topleft=(playerX, playerY))
    enemy_rect = enemy_img[i].get_rect(topleft=(enemyX[i], enemyY[i]))
    return player_rect.colliderect(enemy_rect)

def isPoint(pointX, pointY, playerX, playerY, i):
    player_rect = player_img.get_rect(topleft=(playerX, playerY))
    point_rect = point_img[i].get_rect(topleft=(pointX[i], pointY[i]))
    return player_rect.colliderect(point_rect)

def game_over():
    over_txt = font_2.render("Game Over!", True, (255, 0, 0))
    screen.blit(over_txt, (200, 250))

def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    return

        screen.blit(start_img, (0, 0))
        pygame.draw.rect(screen, (82, 45, 128), play_button_rect)
        play_text = font.render("Play", True, (255, 255, 255))
        screen.blit(play_text, (play_button_rect.x + 70, play_button_rect.y + 10))
        pygame.display.flip()

def main():
    global playerX, playerX_change, score, hits

    # Start screen
    start_screen()

    # Play the background music
    mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -PLAYER_SPEED
                if event.key == pygame.K_RIGHT:
                    playerX_change = PLAYER_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Update player position
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= SCREEN_WIDTH - 64:
            playerX = SCREEN_WIDTH - 64

        screen.blit(bg_img, (0, 0))

        # Update enemies
        for i in range(NUM_ENEMIES):
            if isCollision(enemyX, enemyY, playerX, playerY, i):
                collision_sound.play()
                hits -= 1
                enemyX[i] = random.randint(0, SCREEN_WIDTH - 32)
                enemyY[i] = random.randint(0, 45)
            elif enemyY[i] >= SCREEN_HEIGHT:
                enemyX[i] = random.randint(0, SCREEN_WIDTH - 32)
                enemyY[i] = random.randint(0, 45)
            else:
                enemyY[i] += ENEMY_SPEED
            if hits <= 0:
                enemyY[i] = 2000
                game_over()

            enemy(enemyX[i], enemyY[i], i)

        # Update points
        for i in range(NUM_POINTS):
            if isPoint(pointX, pointY, playerX, playerY, i):
                point_sound.play()
                score += 1
                pointX[i] = random.randint(0, SCREEN_WIDTH - 32)
                pointY[i] = random.randint(0, 45)
            elif pointY[i] >= SCREEN_HEIGHT:
                pointX[i] = random.randint(0, SCREEN_WIDTH - 32)
                pointY[i] = random.randint(0, 45)
            else:
                pointY[i] += POINT_SPEED

            if hits <= 0:
                pointY[i] = 2000
                game_over()
            point(pointX[i], pointY[i], i)

        # Update player
        player(playerX, playerY)
        show_stats()



        pygame.display.update()

if __name__ == "__main__":
    main()
