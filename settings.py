"""
Game settings and constants
"""
import pygame

# Screen dimensions
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 1024

# Game settings
FPS = 120
GRAVITY = 0.25
JUMP_STRENGTH = 7.5  # gravity * 30 = 0.25 * 30 = 7.5

# Floor settings
FLOOR_Y = 800
FLOOR_HEIGHT = 300

# Pipe settings
PIPE_SPEED = 5
PIPE_GAP = 700
PIPE_MIN_HEIGHT = 500
PIPE_MAX_HEIGHT = 700
PIPE_SPAWN_X = 600

# Rocket settings
ROCKET_SPEED = 10
ROCKET_WIDTH = 34  # 68/2
ROCKET_HEIGHT = 24  # 48/2

# Bird settings
BIRD_START_X = 200
BIRD_START_Y = 300
BIRD_ROTATION_SPEED = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Events
BIRD_FLAP_EVENT = pygame.USEREVENT + 1
SPAWN_PIPE_EVENT = pygame.USEREVENT
SPAWN_ROCKET_EVENT = pygame.USEREVENT + 2

# Timers (milliseconds)
BIRD_FLAP_TIMER = 200
PIPE_SPAWN_TIMER = 1200

# Asset paths
ASSETS_PATH = "assets/"
SOUNDS_PATH = "sound/"
FONT_PATH = "04B_19.TTF"
