import pygame
import random

# Initialize pygame
pygame.init()

# Initialize music
pygame.mixer.init()
pygame.mixer.music.load("monkey_background.mp3")
pygame.mixer.music.play(-1)
game_over_sound = pygame.mixer.Sound("gameover_music.mp3")
eating_banana = pygame.mixer.Sound("eat.mp3")
crash_wall = pygame.mixer.Sound("crash_wall.mp3")
coin_crash = pygame.mixer.Sound("coin.mp3")
stone_crash = pygame.mixer.Sound("stone.mp3")
love_crash = pygame.mixer.Sound("love.mp3")

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BananaRun")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load images
monkey_img = pygame.image.load("monkey_1.png")
monkey_img = pygame.transform.scale(monkey_img, (60, 60))
banana_img = pygame.image.load("banana_6.png")
banana_img = pygame.transform.scale(banana_img, (50, 50))
coin_img = pygame.image.load("coin_2.png")
coin_img = pygame.transform.scale(coin_img, (50, 50))
wall_img = pygame.image.load("wall.png")
wall_img = pygame.transform.scale(wall_img, (50, 50))
stone_img = pygame.image.load("stone_3.png")
stone_img = pygame.transform.scale(stone_img, (50, 50))
love_img = pygame.image.load("love_1.png")
love_img = pygame.transform.scale(love_img, (50, 50))
forest_background = pygame.image.load("forest_background.png")
forest_background = pygame.transform.scale(forest_background, (WIDTH, HEIGHT))

# number of the falling objects
NUM_BANANAS = 10
NUM_COINS = 5
NUM_WALLS = 5
NUM_STONES = 5
NUM_LOVES = 5
BANANA_SPEED = 5
COIN_SPEED = 5
WALL_SPEED = 5
STONE_SPEED = 5
LOVE_SPEED = 5


bananas = []
coins = []
walls = []
stones = []
loves = []

# Function to generate non-colliding objects
def generate_non_colliding_positions(num_objects):
    positions = []
    while len(positions) < num_objects:
        new_pos = [random.randint(0, WIDTH - 50), random.randint(-500, -50)]
        if all(abs(new_pos[0] - pos[0]) > 50 for pos in positions):  # Ensure no horizontal overlap
            positions.append(new_pos)
    return positions

# Generate objects
bananas = generate_non_colliding_positions(NUM_BANANAS)
coins = generate_non_colliding_positions(NUM_COINS)
walls = generate_non_colliding_positions(NUM_WALLS)
stones = generate_non_colliding_positions(NUM_STONES)
loves = generate_non_colliding_positions(NUM_LOVES)

# Monkey
monkey_x, monkey_y = WIDTH // 2, HEIGHT - 100
monkey_speed = 5

# Score money lives
score = 0
money = 0
lives = 3
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.blit(forest_background, (0, 0))
    if score > 10 : # level 2
        BANANA_SPEED = 7
        STONE_SPEED = 7
        LOVE_SPEED = 7
        WALL_SPEED = 7
        COIN_SPEED = 7
    if score > 15 : # level 3
        BANANA_SPEED = 9
        STONE_SPEED = 9
        LOVE_SPEED = 9
        WALL_SPEED = 9
        COIN_SPEED = 9


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen.blit(forest_background, (0, 0))
    # the monkey moves
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and monkey_x > 0:
        monkey_x -= monkey_speed
    if keys[pygame.K_RIGHT] and monkey_x < WIDTH - 60:
        monkey_x += monkey_speed
    if keys[pygame.K_UP] and monkey_y > 0:
        monkey_y -= monkey_speed
    if keys[pygame.K_DOWN] and monkey_y < HEIGHT - 60:
        monkey_y += monkey_speed

    # Update positions and check for collisions
    for obj_list, speed in zip([bananas, coins, walls, stones, loves],
                               [BANANA_SPEED, COIN_SPEED, WALL_SPEED, STONE_SPEED, LOVE_SPEED]):
        for obj in obj_list:
            obj[1] += speed
            if obj[1] > HEIGHT:
                obj[0] = random.randint(0, WIDTH - 50)
                obj[1] = random.randint(-500, -50)

    # Create Rect objects for collision detection
    monkey_rect = pygame.Rect(monkey_x, monkey_y, 60, 60)

    for obj_list, img in zip([bananas, coins, walls, stones, loves],
                             [banana_img, coin_img, wall_img, stone_img, love_img]):
        for obj in obj_list:
            obj_rect = pygame.Rect(obj[0], obj[1], 50, 50)
            if monkey_rect.colliderect(obj_rect):
                obj[0] = random.randint(0, WIDTH - 50)
                obj[1] = random.randint(-500, -50)

                if obj_list == bananas:
                    score += 1
                    pygame.mixer.Sound.play(eating_banana)

                elif obj_list == coins:
                    money += 1
                    pygame.mixer.Sound.play(coin_crash)

                elif obj_list == walls:
                    lives -= 1
                    pygame.mixer.Sound.play(crash_wall)
                    if lives == 0:
                        pygame.mixer.music.stop()  # Stop music on game over
                        game_over_sound.play()
                        game_over_font = pygame.font.Font(None, 60)
                        game_over_text = game_over_font.render("GAME OVER", True, RED)
                        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
                        pygame.display.update()

                        pygame.time.wait(4000)
                        running = False
                elif obj_list == stones:
                    score -= 1
                    pygame.mixer.Sound.play(stone_crash)
                    if score < 0:
                        score = 0
                        pygame.mixer.music.stop()
                        game_over_sound.play()
                        game_over_font = pygame.font.Font(None, 60)
                        game_over_text = game_over_font.render("GAME OVER", True, RED)
                        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
                        pygame.display.update()
                        pygame.time.wait(3000)
                        running = False
                elif obj_list == loves:
                    pygame.mixer.Sound.play(love_crash)
                    if lives < 3:
                        lives += 1


    # Draw objects
    for obj_list, img in zip([bananas, coins, walls, stones, loves],
                             [banana_img, coin_img, wall_img, stone_img, love_img]):
        for obj in obj_list:
            screen.blit(img, (obj[0], obj[1]))

    screen.blit(monkey_img, (monkey_x, monkey_y))

    # Display score, money, lives
    score_text = font.render(f"Score: {score}", True, RED)
    screen.blit(score_text, (10, 10))
    money_text = font.render(f"Money: {money}", True, RED)
    screen.blit(money_text, (10, 60))
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(lives_text, (10, 110))
    pygame.display.update()
    clock.tick(30)

pygame.quit()
