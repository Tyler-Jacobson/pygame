import pygame
import random
import sys

WIDTH = 800
HEIGHT = 600

player_x = 400
player_y = 300
player_size = 20

enemy_x = 200
enemy_y = 200
enemy_size = 20
aggro_range = 200

enemy_2_x = 600
enemy_2_y = 100

PLAYER_COLOR = (0,0,255)
ENEMY_COLOR = (255,0,0)
AGGRO_RANGE_COLOR = (0,255,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

clock = pygame.time.Clock()

enemy_list = [[enemy_x, enemy_y], [enemy_2_x, enemy_2_y]]

def in_aggro_range(player_x, player_y, aggro_box_x, aggro_box_y, aggro_box_size):
    if player_x >= aggro_box_x and player_x <= aggro_box_x + aggro_box_size:
        if player_y >= aggro_box_y and player_y <= aggro_box_y + aggro_box_size:
            return True
    return False



while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_over = True
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_x -= 3

    if keys[pygame.K_d]:
        player_x += 3

    if keys[pygame.K_w]:
        player_y -= 3
    
    if keys[pygame.K_s]:
        player_y += 3
    
    screen.fill((0,0,0))
    for x,y in enemy_list:

        aggro_box_x = x - (aggro_range / 2)
        aggro_box_y = y - (aggro_range / 2)
        aggro_box_size = enemy_size + aggro_range

        if in_aggro_range(player_x, player_y, aggro_box_x, aggro_box_y, aggro_box_size):
            if player_x > x:
                x += 1
            if player_x < x:
                x -= 1
            if player_y > y:
                y += 1
            if player_y < y:
                y -= 1



    
        pygame.draw.rect(screen, (AGGRO_RANGE_COLOR), (aggro_box_x, aggro_box_y, aggro_box_size, aggro_box_size))
        pygame.draw.rect(screen, (ENEMY_COLOR), (x, y, enemy_size, enemy_size))

    pygame.draw.rect(screen, (PLAYER_COLOR), (player_x, player_y, player_size, player_size))
    

    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()