"""
Bird class for Flappy Bird game
"""
import pygame
from settings import *

class Bird:
    def __init__(self, screen):
        self.screen = screen
        self.movement = 0
        self.index = 1
        
        # Load bird sprites
        self.load_sprites()
        
        # Bird rect
        self.rect = self.sprites[self.index].get_rect(center=(BIRD_START_X, BIRD_START_Y))
        
    def load_sprites(self):
        """Load and scale bird sprites"""
        bird_mid = pygame.image.load(f'{ASSETS_PATH}conchim.png')
        bird_mid = pygame.transform.scale2x(bird_mid)
        
        bird_up = pygame.image.load(f'{ASSETS_PATH}canhlen.png')
        bird_up = pygame.transform.scale2x(bird_up)
        
        bird_down = pygame.image.load(f'{ASSETS_PATH}canhxuong.png')
        bird_down = pygame.transform.scale2x(bird_down)
        
        self.sprites = [bird_down, bird_mid, bird_up]
        
    def jump(self):
        """Make the bird jump"""
        self.movement = 0
        self.movement -= JUMP_STRENGTH
        
    def update(self):
        """Update bird position"""
        self.movement += GRAVITY
        self.rect.centery += self.movement
        
    def animate(self):
        """Animate bird wing flapping"""
        if self.index < 2:
            self.index += 1
        else:
            self.index = 0
            
    def rotate(self):
        """Rotate bird based on movement"""
        return pygame.transform.rotozoom(self.sprites[self.index], -self.movement * BIRD_ROTATION_SPEED, 1)
        
    def draw(self, rotated=True):
        """Draw the bird on screen"""
        if rotated:
            rotated_bird = self.rotate()
            self.screen.blit(rotated_bird, self.rect)
        else:
            self.screen.blit(self.sprites[1], self.rect)
            
    def reset(self):
        """Reset bird to starting position"""
        self.rect.center = (BIRD_START_X, BIRD_START_Y)
        self.movement = 0
        self.index = 1
        
    def check_boundaries(self):
        """Check if bird hit boundaries"""
        return self.rect.top <= -50 or self.rect.bottom >= FLOOR_Y
