"""
Obstacles (Pipes and Rockets) for Flappy Bird game
"""
import pygame
import random
from settings import *

class Pipe:
    def __init__(self, screen):
        self.screen = screen
        self.sprite = pygame.image.load(f'{ASSETS_PATH}pipe-green.png')
        self.sprite = pygame.transform.scale2x(self.sprite)
        
    def create_pipe_pair(self):
        """Create a pair of pipes (top and bottom)"""
        random_pipe_pos = random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT)
        bottom_pipe = self.sprite.get_rect(midtop=(PIPE_SPAWN_X, random_pipe_pos))
        top_pipe = self.sprite.get_rect(midtop=(PIPE_SPAWN_X, random_pipe_pos - PIPE_GAP))
        return bottom_pipe, top_pipe
        
    def move_pipes(self, pipes, score, score_sound):
        """Move pipes and update score"""
        for pipe_rect in pipes:
            pipe_rect.centerx -= PIPE_SPEED
            if pipe_rect.centerx == 200:
                score += 0.5
                score_sound.play()
        return pipes, score
        
    def draw_pipes(self, pipes):
        """Draw all pipes on screen"""
        for pipe_element in pipes:
            if pipe_element.bottom >= FLOOR_Y:
                self.screen.blit(self.sprite, pipe_element)
            else:
                flip_pipe = pygame.transform.flip(self.sprite, False, True)
                self.screen.blit(flip_pipe, pipe_element)

class Rocket:
    def __init__(self, screen):
        self.screen = screen
        self.sprite = pygame.image.load(f'{ASSETS_PATH}latrobe.png')
        self.sprite = pygame.transform.scale(self.sprite, (ROCKET_WIDTH, ROCKET_HEIGHT))
        
    def create_rocket(self):
        """Create a rocket at random height"""
        random_rocket_pos = random.randint(0, FLOOR_Y)
        rocket_rect = self.sprite.get_rect(midtop=(PIPE_SPAWN_X, random_rocket_pos))
        return rocket_rect
        
    def move_rockets(self, rockets):
        """Move rockets across screen"""
        for rocket_rect in rockets:
            rocket_rect.centerx -= ROCKET_SPEED
        return rockets
        
    def draw_rockets(self, rockets):
        """Draw all rockets on screen"""
        for rocket_element in rockets:
            self.screen.blit(self.sprite, rocket_element)

class ObstacleManager:
    def __init__(self, screen):
        self.screen = screen
        self.pipe = Pipe(screen)
        self.rocket = Rocket(screen)
        self.pipes = []
        self.rockets = []
        
    def create_pipe_pair(self):
        """Create a new pipe pair"""
        return self.pipe.create_pipe_pair()
        
    def create_rocket(self):
        """Create a new rocket"""
        return self.rocket.create_rocket()
        
    def update(self, score, score_sound):
        """Update all obstacles"""
        self.pipes, score = self.pipe.move_pipes(self.pipes, score, score_sound)
        self.rockets = self.rocket.move_rockets(self.rockets)
        
        # Remove off-screen obstacles
        self.pipes = [pipe for pipe in self.pipes if pipe.centerx > -100]
        self.rockets = [rocket for rocket in self.rockets if rocket.centerx > -100]
        
        return score
        
    def draw(self):
        """Draw all obstacles"""
        self.pipe.draw_pipes(self.pipes)
        self.rocket.draw_rockets(self.rockets)
        
    def check_collision(self, bird_rect):
        """Check collision with bird"""
        # Check pipe collision
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe):
                return False
                
        # Check rocket collision
        for rocket in self.rockets:
            if bird_rect.colliderect(rocket):
                return False
                
        return True
        
    def clear(self):
        """Clear all obstacles"""
        self.pipes.clear()
        self.rockets.clear()
        
    def add_pipe_pair(self):
        """Add a new pipe pair"""
        self.pipes.extend(self.create_pipe_pair())
        
    def add_rocket(self):
        """Add a new rocket"""
        self.rockets.append(self.create_rocket())
