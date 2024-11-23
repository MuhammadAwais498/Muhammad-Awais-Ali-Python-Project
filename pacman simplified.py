# MUHAMMAD AWAIS ALI 461465
# FOP PROJECT USING PYGAME
# PACMAN SIMPLIFIED

import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
black = (0, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# Define screen size and create a window
screen_size = (400, 400)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Pacman Simplified')

# Setup the clock for frame rate control
clock = pygame.time.Clock()
clock.tick(30)

gameicon=pygame.image.load('pacman.png')
pygame.display.set_icon(gameicon)


pygame.mixer.init()
pygame.mixer.music.load('pacman.mp3')
pygame.mixer.music.play(-1, 0.0)

# Define the wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Define the player (Pacman) class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load and scale the Pacman image
        self.image = pygame.image.load("pacman.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self, x_change, y_change):
        self.rect.x += x_change
        self.rect.y += y_change

# Define the block (food) class
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([7, 7])
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Define the ghost class
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, image_file, walls):
        super().__init__()
        # Load and scale the ghost image
        self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3
        self.direction = random.choice(["up", "down", "left", "right"])
        self.walls = walls
        self.change_direction_timer = random.randint(30, 60)

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Check collision with walls
        if pygame.sprite.spritecollideany(self, self.walls):
            if self.direction == "up":
                self.rect.y += self.speed
            elif self.direction == "down":
                self.rect.y -= self.speed
            elif self.direction == "left":
                self.rect.x += self.speed
            elif self.direction == "right":
                self.rect.x -= self.speed

            self.direction = random.choice(["up", "down", "left", "right"])

        self.change_direction_timer -= 1
        if self.change_direction_timer <= 0:
            self.direction = random.choice(["up", "down", "left", "right"])
            self.change_direction_timer = random.randint(30, 60)

# Setup the walls and blocks
def setup_game():
    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    ghosts = pygame.sprite.Group()

    # Define walls
    wall_positions = [
        [0, 0, 400, 10], [0, 0, 10, 400], [390, 0, 10, 400], [0, 390, 400, 10],
        [100, 100, 10, 200], [200, 100, 10, 200], [100, 90, 110, 10], [210, 200, 100, 10]
    ]

    for pos in wall_positions:
        wall = Wall(*pos, blue)
        all_sprites.add(wall)
        walls.add(wall)

    # Add blocks (food)
    block_positions = [
        (50, 50), (100, 50), (150, 50), (200, 50), (250, 50), (300, 50), (350, 50),
        (50, 100), (250, 100), (300, 100), (350, 100),
        (50, 150), (150, 150), (250, 150), (300, 150), (350, 150),
        (50, 200), (150, 200), (350, 200),
        (50, 250), (150, 250), (250, 250), (300, 250), (350, 250),
        (150, 300), (250, 300), (300, 300), (350, 300),
        (50, 350), (100, 350), (150, 350), (200, 350), (250, 350), (300, 350), (350, 350)
    ]
    for x, y in block_positions:
        block = Block(x, y)
        all_sprites.add(block)
        blocks.add(block)

    # Add ghosts with their images
    ghost_positions = [(130, 130), (280, 280), (180, 180), (30, 30)]
    ghost_images = ["Blinky.png", "Inky.png", "Clyde.png", "Pinky.png"]

    for i, pos in enumerate(ghost_positions):
        ghost = Ghost(pos[0], pos[1], ghost_images[i], walls)
        all_sprites.add(ghost)
        ghosts.add(ghost)

    return all_sprites, blocks, walls, ghosts

def display_message(text, color, x_offset=0, y_offset=0):
    font = pygame.font.Font(None, 15)
    message = font.render(text, True, color)
    screen.blit(message, (20 + x_offset, 150 + y_offset))

def play_again():
    while True:
        screen.fill(black)
        display_message("If You want To Play Again then Press P and To Quit The Game Press Q.", white)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return True
                elif event.key == pygame.K_q:
                    return False
    
# Main game loop
def game_loop():
    while True:
        all_sprites, blocks, walls, ghosts = setup_game()

        # Create the player object (Pacman)
        pacman = Player(50, 300)
        all_sprites.add(pacman)

        # Game variables
        score = 0
        speed = pacman.speed
        x_change = 0
        y_change = 0

        running = True
        while running:
            screen.fill(black)

            # Handle events (keys pressed by the user)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -speed
                        y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x_change = speed
                        y_change = 0
                    elif event.key == pygame.K_UP:
                        y_change = -speed
                        x_change = 0
                    elif event.key == pygame.K_DOWN:
                        y_change = speed
                        x_change = 0

            # Update player position
            pacman.update(x_change, y_change)

            # Check for collisions with walls
            if pygame.sprite.spritecollide(pacman, walls, False):
                pacman.update(-x_change, -y_change)

            # Check if pacman eats a block (score point)
            blocks_hit = pygame.sprite.spritecollide(pacman, blocks, True)
            score += len(blocks_hit)

            # Update ghost positions
            for ghost in ghosts:
                ghost.update()

            # Check for collisions with ghosts (Game Over)
            if pygame.sprite.spritecollide(pacman, ghosts, False):
                font = pygame.font.Font(None, 65)
                game_over = font.render("Game Over!", True, red)
                screen.blit(game_over, (80, 100))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False

            # Draw everything
            all_sprites.draw(screen)

            # Display the score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, white)
            screen.blit(score_text, (10, 10))

            # Check if the player has collected all blocks
            if len(blocks) == 0:
                font = pygame.font.Font(None, 65)
                you_win = font.render("You Win!", True, green)
                screen.blit(you_win, (80, 100))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False

            # Update the screen
            pygame.display.flip()
            clock.tick(30)

        if not play_again():
            break

game_loop()
