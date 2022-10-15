import random
import pygame
import math


class Enemies:
    def __init__(self, surface, x_enem, y_enem):
        self.x_enem = x_enem
        self.y_enem = y_enem
        self.surface = surface

    def draw(self):
        surface.blit(spike, (self.x_enem, self.y_enem))

    def draw_top(self):
        surface.blit(spike_top, (self.x_enem, self.y_enem))


# Pygame Variables
pygame.init()
pygame.font.init()
Width, Height = 500, 700
clock = pygame.time.Clock()
surface = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Ice Dodger")


# Character List
L1 = pygame.image.load("left/L1.png")
L2 = pygame.image.load("left/L2.png")
L3 = pygame.image.load("left/L3.png")
L4 = pygame.image.load("left/L4.png")
L5 = pygame.image.load("left/L5.png")
L6 = pygame.image.load("left/L6.png")

R1 = pygame.image.load("right/R1.png")
R2 = pygame.image.load("right/R2.png")
R3 = pygame.image.load("right/R3.png")
R4 = pygame.image.load("right/R4.png")
R5 = pygame.image.load("right/R5.png")
R6 = pygame.image.load("right/R6.png")

S1 = pygame.image.load("standing/frame-1.png")
S2 = pygame.image.load("standing/frame-2.png")

J2 = pygame.image.load("jump/R2_jump.png")


# Character Variables
x_pos = 100
y_pos = 500
width = 50
height = 70

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

vel = 5
move_left = False
move_right = False
step = 0
stand = 2
isjumping = False
jump_count = 0
vel_y = 15

# scoring
count = 0
score_value = 0
num_of_spike = 3
font = pygame.font.Font('freesansbold.ttf', 32)


# List  of enemies
enem_w = 38
enem_h = 75
enem_vel = 3
num_of_enem = 10
enem = []


top_x = 0
top_y = 0
num_of_top = 11
enem_top = []

# Paused variables
game_ends = False

# Spike
spike1 = pygame.image.load("spike.png")
spike = pygame.transform.scale(spike1, (enem_w, enem_h))

spike2 = pygame.image.load("spike1.png")
spike_top = pygame.transform.scale(spike2, (45, 35))

for i in range(num_of_top):
    enem_top.append(Enemies(surface, top_x, top_y))
    top_x += 45

for x in range(num_of_enem):
    l1 = [0, 45, 90, 135, 180, 225, 270, 315, 360, 405, 450]
    l2 = [-50, -40, -30, -20, -10, 0]
    x_enem = random.choice(l1)
    y_enem = random.choice(l2)

    enem.append(Enemies(surface, x_enem, y_enem))


def show_score(x, y):
    global score_value
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    surface.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    surface.blit(over_text, (50, 300))


def draw_game():
    global step, stand
    bg1 = pygame.image.load("bg5.jpg")
    bg = pygame.transform.scale(bg1, (Width, Height))
    surface.blit(bg, (0, 0))

    standing = [
        pygame.transform.scale(S1, (width, height)),
        pygame.transform.scale(S2, (width, height))]

    jumping = [
        pygame.transform.scale(J2, (width, height)), ]

    left = [
        pygame.transform.scale(L1, (width, height)),
        pygame.transform.scale(L2, (width, height)),
        pygame.transform.scale(L3, (width, height)),
        pygame.transform.scale(L4, (width, height)),
        pygame.transform.scale(L5, (width, height)),
        pygame.transform.scale(L6, (width, height)), ]

    right = [
        pygame.transform.scale(R1, (width, height)),
        pygame.transform.scale(R2, (width, height)),
        pygame.transform.scale(R3, (width, height)),
        pygame.transform.scale(R4, (width, height)),
        pygame.transform.scale(R5, (width, height)),
        pygame.transform.scale(R6, (width, height)), ]

    if step >= 18:
        step = 0

    if stand == 2:
        stand = 0

    if move_left:
        surface.blit(left[step // 4], (x_pos, y_pos))
        step += 1
    elif move_right:
        surface.blit(right[step // 4], (x_pos, y_pos))
        step += 1
    elif isjumping:
        surface.blit(jumping[0], (x_pos, y_pos))
    else:
        surface.blit(standing[stand], (x_pos, y_pos))
        stand += 1


def isCollision(x_pos, y_pos, x_enem, y_enem):
    distance = math.sqrt((math.pow(x_enem - x_pos, 2)) +
                         (math.pow(y_enem - y_pos, 2)))
    if distance < 27:
        return True
    else:
        return False


def enemies():
    global x_enem, y_enem, enem, count, l1, score_value, num_of_spike, enem_vel, x_pos, y_pos, game_ends
    global top_x, top_y

    if score_value == 4:
        enem_vel = 5
        num_of_spike = 6
    elif score_value == 9:
        enem_vel = 7
        num_of_spike = 8
    elif score_value == 20:
        enem_vel = 9
        num_of_spike = 10

    for i in range(num_of_spike):
        collision = isCollision(x_pos, y_pos,  enem[i].x_enem, enem[i].y_enem)
        if collision:
            game_ends = True
            count = 0
            score_value = 0
            num_of_spike = 0
            enem_vel = 3
            enem[i].x_enem = random.choice(l1)
            enem[i].y_enem = random.choice(l2)
            break
        else:
            if game_ends is False:
                enem[i].draw()
                if enem[i].y_enem < Height - height:
                    enem[i].y_enem += enem_vel
                if enem[i].y_enem >= Height - height:
                    enem[i].y_enem = 0
                    enem[i].x_enem = random.choice(l1)
                    count += 1
                    if count % 6 == 0:
                        score_value += 1

                for x in range(len(enem_top)):
                    enem_top[x].draw_top()


run = True
while run:
    clock.tick(60)

    if game_ends:
        draw_game()
        game_over_text()
    else:
        draw_game()
        enemies()
        show_score(10, 30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_ends:
                    game_ends = False
                    num_of_spike = 3

    # WALKING
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and x_pos > 0:
        x_pos -= vel
        move_left = True
        move_right = False
    elif keys[pygame.K_d] and x_pos < Width - width:
        x_pos += vel
        move_left = False
        move_right = True
    else:
        move_left = False
        move_right = False
        step = 0

    # JUMPING
    if isjumping is False and keys[pygame.K_SPACE]:
        isjumping = True
    if isjumping:
        y_pos -= vel_y
        vel_y -= 1
        if vel_y < -15:
            isjumping = False
            vel_y = 15

    pygame.display.update()

pygame.quit()
