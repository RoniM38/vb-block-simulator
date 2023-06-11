import pygame
import sys
import random
import time
from button import Button
pygame.init()


SCREEN_SIZE = (1100, 550)
window = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Volleyball")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = "#d30cc1"

# consts
PLAYER_SPEED = 8
JUMP_MAX = 20
BALL_SPEED = 15
BW_PROGRESS = 0.2 # ball_wait (bw) change when the score is divisible by 50
SW_PROGRESS = 0.1 # spawn_wait change (sw) when the score is divisible by 50

ball_wait = 3
spawn_wait = 3
score_list = []

score = 0

# images
menu_bg = pygame.transform.scale(pygame.image.load("Images/menu_bg.png"), SCREEN_SIZE)
net_img = pygame.transform.scale(pygame.image.load("Images/net.png"), SCREEN_SIZE)
player_img = pygame.image.load("Images/player.png")
ball_img = pygame.transform.scale(pygame.image.load("Images/ball.png"), (80, 80))


class Player:
    def __init__(self, surface, img, x, y, vel, jumpMax):
        self.surface = surface
        self.img = img
        self.x = x
        self.y = y
        self.vel = vel
        self.jumpMax = jumpMax

        self.isJumping = False
        self.jumpCount = 0
        self.health = 100

        self.width, self.height = self.img.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface.blit(self.img, (self.x, self.y))
        # drawing the hit box
        # pygame.draw.rect(self.surface, RED, self.rect, 1)

        health_font = pygame.font.SysFont("Arial", 15, "bold")
        window.blit(health_font.render(f"HEALTH: {self.health}", True, (255, 255, 255)), (980, 0))
        pygame.draw.rect(window, (255, 0, 0), (980 + self.health, 20, 100 - self.health, 20))
        pygame.draw.rect(window, (0, 255, 0), (980, 20, self.health, 20))

    def move_right(self):
        if self.x + self.width <= SCREEN_SIZE[0]:
            self.x += self.vel

    def move_left(self):
        if self.x > 0:
            self.x -= self.vel

    def jump(self):
        self.y -= self.jumpCount
        if self.jumpCount > -self.jumpMax:
            self.jumpCount -= 1
        else:
            self.isJumping = False

    def check_block(self, balls):
        for ball in balls:
            if not ball.dropped and self.rect.colliderect(ball.rect):
                balls.remove(ball)
                return True
        return False


class Ball:
    def __init__(self, surface, img, x, y, vel, wait):
        self.surface = surface
        self.img = img
        self.x = x
        self.y = y
        self.vel = vel
        self.wait = wait

        self.dropped = False
        self.create_time = time.time()

        self.width, self.height = self.img.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface.blit(self.img, (self.x, self.y))
        # drawing the hit box
        # pygame.draw.rect(self.surface, RED, self.rect, 1)

        now = time.time()
        if now - self.create_time > self.wait:
            self.drop()

    def drop(self):
        self.dropped = True
        self.y += self.vel


def display_score(player):
    global ball_wait, spawn_wait

    # displaying the score
    score_font = pygame.font.SysFont("britannic", 40, True)
    score_text = score_font.render(f"SCORE: {score}", True, BLACK)
    window.blit(score_text, (10, 10))

    # extreme mode font
    extreme_font = pygame.font.SysFont("Berlin Sans FB Demi", 60, "bold")

    if ball_wait >= 0.8:
        if score not in score_list and score % 50 == 0:
            ball_wait -= BW_PROGRESS
            spawn_wait -= SW_PROGRESS
            player.vel += 0.08
            score_list.append(score)
    elif ball_wait != 0:
        player.vel += 0.1
        window.blit(extreme_font.render("EXTREME", True, (136, 0, 21)), (400, 10))
        window.blit(extreme_font.render("MODE", True, (136, 0, 21)), (440, 60))


def game_over():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.fill(RED)
        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def main():
    global score

    middle_x, middle_y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - 310
    player = Player(window, player_img, middle_x, middle_y, PLAYER_SPEED, JUMP_MAX)
    balls = []

    clock = pygame.time.Clock()
    start_time = time.time()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if not player.isJumping and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                    player.isJumping = True
                    player.jumpCount = JUMP_MAX

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.move_right()

        if keys[pygame.K_LEFT]:
            player.move_left()

        window.fill(BLACK)
        window.blit(net_img, (0, 0))

        now = time.time()
        if len(balls) == 0 or now - start_time > spawn_wait:
            ball_x = random.randint(10, SCREEN_SIZE[0] - ball_img.get_width())
            ball = Ball(window, ball_img, ball_x, 60, BALL_SPEED, ball_wait)
            balls.append(ball)
            start_time = time.time()

        for b in balls:
            if b.y > SCREEN_SIZE[1]:
                balls.remove(b)
                player.health -= 10
                continue

            b.draw()

        player.draw()

        clock.tick(60)
        if player.isJumping:
            player.jump()

            if player.check_block(balls):
                score += 5

        display_score(player)

        if player.health <= 0:
            game_over()

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def menu():
    play_button = Button(window, "PLAY", "#69f5d1", WHITE, 330, 220, 400, 150)
    title_font = pygame.font.SysFont("Arial Rounded MT Bold", 100, True)
    title_text = title_font.render("Volley Block Simulator", True, PINK)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    main()

        window.fill(BLACK)
        window.blit(menu_bg, (0, 0))
        window.blit(title_text, (170, 20))

        play_button.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    menu()
