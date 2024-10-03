import pygame, sys, random

def draw_floor():
    screen.blit(floor, (floor_x, 800))
    screen.blit(floor, (floor_x + 576, 800))

def create_pipe():
    random_pipe_pos = random.randint(500, 700)
    bottom_pipe = pipe.get_rect(midtop = (600, random_pipe_pos))
    top_pipe = pipe.get_rect(midtop = (600, random_pipe_pos - 700))
    return bottom_pipe, top_pipe

def create_rocket():
    random_rocket_pos = random.randint(0, 800)
    rocket_rect = rocket.get_rect(midtop = (600, random_rocket_pos))
    return rocket_rect

def move_pipes(pipes, score):
    for pipe_rect in pipes:
        pipe_rect.centerx -= 5
        if pipe_rect.centerx == 200:
            score += 0.5
            score_sound.play()
    return pipes, score

def move_rockets(rockets):
    for rocket_rect in rockets:
        rocket_rect.centerx -= 10
    return rockets

def draw_pipe(pipes):
    for pipe_element in pipes:
        if pipe_element.bottom >= 800:
            screen.blit(pipe, pipe_element)
        else:
            flip_pipe = pygame.transform.flip(pipe, False, True)
            screen.blit(flip_pipe, pipe_element)

def draw_rocket(rockets):
    for rocket_element in rockets:
        screen.blit(rocket, rocket_element)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            print('HIT')
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 800:
        hit_sound.play()
        print('HIT')
        return False
    return True

def check_collision_rocket(rockets):
    for rocket in rockets:
        if bird_rect.colliderect(rocket):
            hit_sound.play()
            print('HIT')
            return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (200, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RANDOM_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    if game_state == 'main_game':
        score_surface = my_font.render(f'Score: {str(int(score))}', True, BLACK)
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = my_font.render(f'Score: {str(int(score))}', True, BLACK)
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)      

        high_score_surface = my_font.render(f'High score: {str(int(high_score))}', True, BLACK)
        high_score_rect = high_score_surface.get_rect(center = (288, 950))
        screen.blit(high_score_surface, high_score_rect)    

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

back_ground = pygame.image.load('assets/background-night.png')
back_ground = pygame.transform.scale(back_ground, (576, 1024))

floor = pygame.image.load('assets/floor.png')
floor = pygame.transform.scale(floor, (576, 300))
floor_x = 0

bird_mid = pygame.image.load('assets/conchim.png')
bird_mid = pygame.transform.scale2x(bird_mid)
print(bird_mid.get_size())

bird_up = pygame.image.load('assets/canhlen.png')
bird_up = pygame.transform.scale2x(bird_up)

bird_down = pygame.image.load('assets/canhxuong.png')
bird_down = pygame.transform.scale2x(bird_down)

bird_list = [bird_down, bird_mid, bird_up]
bird_index = 1
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (200, 300))

pipe = pygame.image.load('assets/pipe-green.png')
pipe = pygame.transform.scale2x(pipe)

rocket = pygame.image.load('assets/latrobe.png')
rocket = pygame.transform.scale(rocket, (68/2, 48/2))

end_game = pygame.image.load('assets/message.png')

bird_flap = pygame.USEREVENT + 1
spawn_pipe = pygame.USEREVENT
spawn_rocket = pygame.USEREVENT + 2
spawn_boom = pygame.USEREVENT + 3

pygame.time.set_timer(bird_flap, 200)
pygame.time.set_timer(spawn_pipe, 1200)
pygame.time.set_timer(spawn_rocket, random.randint(1000, 3000))

pipes = []
rockets = []

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
wait_sound = pygame.mixer.Sound('sound/nhaccho.wav')

my_font = pygame.font.Font('04B_19.TTF', 40)
FPS = 120
gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score = 0
score_sound_count = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= gravity * 30
                print('Jump')
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active == False:
                score = 0
                game_active = True
                pipes.clear()
                rockets.clear()
                bird_rect.center = (200, 300)
                bird_movement = 0

        if event.type == spawn_pipe and game_active:
            pipes.extend(create_pipe())

        if event.type == bird_flap and game_active:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

        if event.type == spawn_rocket and game_active:
            rockets.append(create_rocket())

    screen.blit(back_ground, (0, 0))

    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipes) and check_collision_rocket(rockets)
        pipes, score = move_pipes(pipes, score)
        rockets = move_rockets(rockets)
        draw_rocket(rockets)
        draw_pipe(pipes)
        floor_x -= 1
        draw_floor()
        if floor_x <= -576:
            floor_x = 0
        score_display('main_game')
    else:
        high_score = update_score(score, high_score)
        screen.blit(bird_list[1], bird_rect)
        draw_floor()
        if floor_x <= -576:
            floor_x = 0
        score_display('game_over')

    pygame.display.update()
    clock.tick(FPS)