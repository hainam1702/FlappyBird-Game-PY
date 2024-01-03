import pygame
import sys
import random

# Tạo hàm cho trò chơi


# fore bg auto chạy
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

# tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos + 50))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 700))
    return bottom_pipe, top_pipe

def create_pipe_advanced():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos + 50))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 750))
    if random_pipe_pos == 300:
        xbottom_pipe = pipe_surface.get_rect(midtop=(590, random_pipe_pos + 50))
        ybottom_pipe = pipe_surface.get_rect(midtop=(680, random_pipe_pos + 100))
        xtop_pipe = pipe_surface.get_rect(midtop=(590, random_pipe_pos - 650))
        ytop_pipe = pipe_surface.get_rect(midtop=(680, random_pipe_pos - 600))
    if random_pipe_pos == 400:
        xbottom_pipe = pipe_surface.get_rect(midtop=(590, random_pipe_pos + 50))
        ybottom_pipe = pipe_surface.get_rect(midtop=(680, random_pipe_pos + 100))
        xtop_pipe = pipe_surface.get_rect(midtop=(590, random_pipe_pos - 650))
        ytop_pipe = pipe_surface.get_rect(midtop=(680, random_pipe_pos - 600))
    if random_pipe_pos == 500:
        xbottom_pipe = pipe_surface.get_rect(midtop=(590, random_pipe_pos - 100))
        ybottom_pipe = pipe_surface.get_rect(midtop=(680, random_pipe_pos - 50))
        xtop_pipe = pipe_surface.get_rect(midtop=(590, random_pipe_pos - 750))
        ytop_pipe = pipe_surface.get_rect(midtop=(680, random_pipe_pos - 800))

    return bottom_pipe, top_pipe, xbottom_pipe, xtop_pipe, ybottom_pipe, ytop_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes    


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        die_sound.play()
        return False
    return True


def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird

def bird_animaton():
    new_bird = bird_list[bird_index]
    return new_bird

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(26, 50))
        screen.blit(score_surface, score_rect)

    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 50))
        screen.blit(score_surface, score_rect)
        bird2_rect = bird.get_rect(center=(216, 550))
        screen.blit(bird, bird2_rect)

        high_score_surface = game_font.render(
            f"High Score: {int(high_score)}", True, (255, 255, 255)
        )
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.ttf", 35)

# Tạo các biến cho trò chơi
gravity = 0.20  # giả lập trọng lực
bird_movement = 0
game_active = False
score = 0
high_score = 0

# chèn background
bg_night = pygame.image.load("assets/background-night.png").convert()
bg_night = pygame.transform.scale2x(bg_night)
bg_day = pygame.image.load("assets/bg.png").convert()
bg_day = pygame.transform.scale2x(bg_day)

# chèn sàn
floor = pygame.image.load("assets/floor.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# tạo chim
birdImg1 = pygame.image.load("assets/bird.png").convert_alpha()
birdImg1 = pygame.transform.scale2x(birdImg1)
birdImg2 = pygame.image.load("assets/bird2.png").convert_alpha()
birdImg2 = pygame.transform.scale2x(birdImg2)
birdImg3 = pygame.image.load("assets/bird3.png").convert_alpha()
birdImg3 = pygame.transform.scale2x(birdImg3)
birdImg4 = pygame.image.load("assets/bird4.png").convert_alpha()
birdImg4 = pygame.transform.scale2x(birdImg4)
bird_list = [birdImg1, birdImg2, birdImg3, birdImg4]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

# tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)
# tạo ống
pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# time tạo cột
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1900)

pipe_height = [300, 400, 500]

# Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(
    pygame.image.load("assets/message2.png").convert_alpha()
)
game_over_rect = game_over_surface.get_rect(center=(216, 280))
# Chèn âm thanh
flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
die_sound = pygame.mixer.Sound("sound/sfx_die.wav")
swooshing_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")
hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100

# while loop của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -5
                flap_sound.play()  # nhạc game
            if event.key == pygame.K_SPACE and game_active == False:
                swooshing_sound.play()
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
            if event.key == pygame.K_UP and game_active == False:
                bird_index += 1
                if bird_index > 3:
                    bird_index = 0
            if event.key == pygame.K_DOWN and game_active == False:
                bird_index -= 1
                if bird_index < 0:
                    bird_index = 2
            bird = bird_animaton()
        if event.type == spawnpipe:
            if 10 <= score <= 20 or 30 <= score <= 40:
                pipe_list.extend(create_pipe_advanced())
            else:
                pipe_list.extend(create_pipe())
    if game_active:
        if 10 < score <= 20:
            screen.blit(bg_night, (0, 0))
        else:
            screen.blit(bg_day, (0, 0))

        # chim
        bird_movement += gravity  # tăng trọng lực khi chim di chuyển
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(bg_night, (0, 0))
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")
    # sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
