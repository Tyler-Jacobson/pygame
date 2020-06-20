import pygame
import random
import sys
import time

WIDTH = 800
HEIGHT = 600

player_pos = [400, 300]
player_x = player_pos[0]
player_y = player_pos[1]
player_size = 20
player_health = [3]

enemy_x = 200
enemy_y = 200
enemy_size = 20
aggro_range = 200

enemy_2_x = 600
enemy_2_y = 100

PLAYER_COLOR = (0,0,255)
ENEMY_COLOR = (255,0,0)
AGGRO_RANGE_COLOR = (0,255,0)
background_color = [(0,0,0)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

clock = pygame.time.Clock()
current_time = 0
time_hit = [10]

enemy_list = [[enemy_x, enemy_y], [enemy_2_x, enemy_2_y], [600, 600]]

def in_aggro_range(player_pos, aggro_box_x, aggro_box_y, aggro_box_size):
    if player_pos[0] >= aggro_box_x and player_pos[0] <= aggro_box_x + aggro_box_size:
        if player_pos[1] >= aggro_box_y and player_pos[1] <= aggro_box_y + aggro_box_size:
            return True
    return False

def move_enemies(enemy_list, player_pos):
    for pos in enemy_list:

        aggro_box_x = pos[0] - (aggro_range / 2)
        aggro_box_y = pos[1] - (aggro_range / 2)
        aggro_box_size = enemy_size + aggro_range

        if in_aggro_range(player_pos, aggro_box_x, aggro_box_y, aggro_box_size):
            if player_pos[0] > pos[0]:
                pos[0] += 1
            if player_pos[0] < pos[0]:
                pos[0] -= 1
            if player_pos[1] > pos[1]:
                pos[1] += 1
            if player_pos[1] < pos[1]:
                pos[1] -= 1

        pygame.draw.rect(screen, (AGGRO_RANGE_COLOR), (int(aggro_box_x), int(aggro_box_y), aggro_box_size, aggro_box_size))
        pygame.draw.rect(screen, (ENEMY_COLOR), (pos[0], pos[1], enemy_size, enemy_size))

def move_player(player_pos):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] -= 3

    if keys[pygame.K_d]:
        player_pos[0] += 3

    if keys[pygame.K_w]:
        player_pos[1] -= 3
    
    if keys[pygame.K_s]:
        player_pos[1] += 3
    
    pygame.draw.rect(screen, (PLAYER_COLOR), (player_pos[0], player_pos[1], player_size, player_size))

def detect_collisions(player_pos, enemy_list, enemy_size):
    p_x = player_pos[0]
    p_y = player_pos[1]

    for enemy in enemy_list:
        e_x = enemy[0]
        e_y = enemy[1]
        if p_x >= e_x and p_x <= e_x + enemy_size or e_x >= p_x and e_x <= p_x + player_size:
            if p_y >= e_y and p_y <= e_y + enemy_size or e_y >= p_y and e_y <= p_y + player_size:
                return True
    return False

def lose_health(player_health, current_time, time_hit):
    current_time = time.time()

    if current_time > time_hit[0] + 1:
        player_health[0] -= 1
        time_hit[0] = time.time()

        background_color[0] = (255,0,0)

        if player_health[0] <= 0:
            return True

def draw_health(player_health):
    for health in range(0, player_health[0]):
        pygame.draw.circle(screen, (200,50,50), (20 + (health * 30), 20), 10)
        

    




while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_over = True
    
    screen.fill(background_color[0])
    background_color[0] = (0,0,0)

    
    move_enemies(enemy_list, player_pos)

    move_player(player_pos)

    draw_health(player_health)


    if detect_collisions(player_pos, enemy_list, enemy_size):
        if lose_health(player_health, current_time, time_hit):
            game_over = True
        
        



    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()