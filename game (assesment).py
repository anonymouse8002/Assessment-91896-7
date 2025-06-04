import pygame 
pygame.init()                 #initialising pygame

WIDTH,HEIGHT = 1900,1000     
screen = pygame.display.set_mode((WIDTH,HEIGHT))                  #setting the height and width
pygame.display.set_caption("game name here")                      #setting the caption 
clock = pygame.time.Clock()

#defining the movemnt of the character 

import sys
import os

#function to load images
def load_image(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")    
    return pygame.image.load(path).convert_alpha()             


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = {
            "idle": load_image("images/idle.png"),
            "walk": [
                load_image("images/walk1.png"),
                load_image("images/walk2.png")
            ]
        }
        self.image = self.images["idle"]
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 5
        self.walk_index = 0
        self.vel_y = 0
        self.gravity = 1
        self.jump_speed = -15
        self.on_ground = False
        self.facing_right = True

    def update(self, keys, platforms):
        dx, dy = 0, 0
        moving = False

        # Horizontal input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            moving = True
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            moving = True
            self.facing_right = True

        # Jump input
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_speed
            self.on_ground = False

        # Apply gravity
        self.vel_y += self.gravity
        dy += self.vel_y

        # Update animation
        if moving:
            self.walk_index += 0.1
            if self.walk_index >= len(self.images["walk"]):
                self.walk_index = 0
            self.image = self.images["walk"][int(self.walk_index)]
        else:
            self.image = self.images["idle"]

        # Flip image based on direction
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        # Horizontal movement and collision
        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:  # Moving right
                    self.rect.right = platform.rect.left
                elif dx < 0:  # Moving left
                    self.rect.left = platform.rect.right

        # Vertical movement and collision
        self.rect.y += dy
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0


# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))


# Create player and platforms
player = Player(400 , 300)
ground = Platform(0, HEIGHT - 50, WIDTH, 50)
platforms = pygame.sprite.Group(ground)
all_sprites = pygame.sprite.Group(player, ground)

# Game loop
running = True
while running:
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys, platforms)

    # Drawing
    screen.fill((30, 30, 30))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()

