"""
Main Game class for Flappy Bird
"""
import pygame
import sys
import random
from settings import *
from bird import Bird
from obstacles import ObstacleManager

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.game_active = False
        self.score = 0
        self.high_score = 0
        
        # Load assets
        self.load_assets()
        
        # Initialize game objects
        self.bird = Bird(self.screen)
        self.obstacles = ObstacleManager(self.screen)
        
        # Floor
        self.floor_x = 0
        
        # Set up timers
        self.setup_timers()
        
    def load_assets(self):
        """Load all game assets"""
        # Background
        self.background = pygame.image.load(f'{ASSETS_PATH}background-night.png')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Floor
        self.floor = pygame.image.load(f'{ASSETS_PATH}floor.png')
        self.floor = pygame.transform.scale(self.floor, (SCREEN_WIDTH, FLOOR_HEIGHT))
        
        # Game over screen
        self.game_over_screen = pygame.image.load(f'{ASSETS_PATH}message.png')
        
        # Sounds
        self.flap_sound = pygame.mixer.Sound(f'{SOUNDS_PATH}sfx_wing.wav')
        self.hit_sound = pygame.mixer.Sound(f'{SOUNDS_PATH}sfx_hit.wav')
        self.score_sound = pygame.mixer.Sound(f'{SOUNDS_PATH}sfx_point.wav')
        
        # Font
        self.font = pygame.font.Font(FONT_PATH, 40)
        
    def setup_timers(self):
        """Set up pygame timers"""
        pygame.time.set_timer(BIRD_FLAP_EVENT, BIRD_FLAP_TIMER)
        pygame.time.set_timer(SPAWN_PIPE_EVENT, PIPE_SPAWN_TIMER)
        
    def draw_floor(self):
        """Draw the scrolling floor"""
        self.screen.blit(self.floor, (self.floor_x, FLOOR_Y))
        self.screen.blit(self.floor, (self.floor_x + SCREEN_WIDTH, FLOOR_Y))
        
    def update_floor(self):
        """Update floor position for scrolling effect"""
        self.floor_x -= 1
        if self.floor_x <= -SCREEN_WIDTH:
            self.floor_x = 0
            
    def check_collision(self):
        """Check all collisions"""
        # Check boundary collision
        if self.bird.check_boundaries():
            self.hit_sound.play()
            return False
            
        # Check obstacle collision
        if not self.obstacles.check_collision(self.bird.rect):
            self.hit_sound.play()
            return False
            
        return True
        
    def score_display(self, game_state):
        """Display score on screen"""
        if game_state == 'main_game':
            score_surface = self.font.render(f'Score: {int(self.score)}', True, BLACK)
            score_rect = score_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(score_surface, score_rect)
            
        elif game_state == 'game_over':
            score_surface = self.font.render(f'Score: {int(self.score)}', True, BLACK)
            score_rect = score_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(score_surface, score_rect)
            
            high_score_surface = self.font.render(f'High score: {int(self.high_score)}', True, BLACK)
            high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH//2, 950))
            self.screen.blit(high_score_surface, high_score_rect)
            
    def update_high_score(self):
        """Update high score if current score is higher"""
        if self.score > self.high_score:
            self.high_score = self.score
            
    def reset_game(self):
        """Reset game to initial state"""
        self.score = 0
        self.game_active = True
        self.obstacles.clear()
        self.bird.reset()
        
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_active:
                        self.bird.jump()
                        self.flap_sound.play()
                    else:
                        self.reset_game()
                        
            if event.type == SPAWN_PIPE_EVENT and self.game_active:
                self.obstacles.add_pipe_pair()
                
            if event.type == BIRD_FLAP_EVENT and self.game_active:
                self.bird.animate()
                
            # Uncomment to enable rocket spawning
            # if event.type == SPAWN_ROCKET_EVENT and self.game_active:
            #     self.obstacles.add_rocket()
                
    def update_game(self):
        """Update game logic"""
        if self.game_active:
            # Update bird
            self.bird.update()
            
            # Update obstacles and score
            self.score = self.obstacles.update(self.score, self.score_sound)
            
            # Check collisions
            self.game_active = self.check_collision()
            
            # Update floor
            self.update_floor()
        else:
            self.update_high_score()
            self.update_floor()
            
    def draw_game(self):
        """Draw all game elements"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        if self.game_active:
            # Draw bird (rotated)
            self.bird.draw(rotated=True)
            
            # Draw obstacles
            self.obstacles.draw()
            
            # Draw floor
            self.draw_floor()
            
            # Draw score
            self.score_display('main_game')
        else:
            # Draw bird (static)
            self.bird.draw(rotated=False)
            
            # Draw floor
            self.draw_floor()
            
            # Draw game over score
            self.score_display('game_over')
            
    def run(self):
        """Main game loop"""
        while True:
            self.handle_events()
            self.update_game()
            self.draw_game()
            
            pygame.display.update()
            self.clock.tick(FPS)
