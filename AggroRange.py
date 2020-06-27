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
PLAYER_SPEED = 3

enemy_x = 200
enemy_y = 200
enemy_size = 20
enemy_speed = 1.5
aggro_range = 200
ENEMY_SPAWN_DISTANCE = 200
enemy_spacing = 30

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

enemy_list = []

# Checks if the player's location (player_pos[0] + (player_size / 2)) is greater than the far left edge of the aggro box, and less than 
# the far right edge. If this is the case for the x coordinate, the same is then checked for the y coordinate. If both are true, the player 
# must be inside of the enemy's aggro box, and True is returned
def in_aggro_range(player_pos, aggro_box_x, aggro_box_y, aggro_box_size):
    if player_pos[0] + (player_size / 2) >= aggro_box_x and player_pos[0] + (player_size / 2) <= aggro_box_x + aggro_box_size:
        if player_pos[1] + (player_size / 2) >= aggro_box_y and player_pos[1] + (player_size / 2) <= aggro_box_y + aggro_box_size:
            return True
    return False


def move_enemies(enemy_list, player_pos, enemy_speed, enemy_spacing):
    
    # For each enemy in the list of enemies, an aggro box is created. 
    for index,enemy_pos in enumerate(enemy_list):
        aggro_box_x = enemy_pos[0] - (aggro_range / 2)
        aggro_box_y = enemy_pos[1] - (aggro_range / 2)
        aggro_box_size = enemy_size + aggro_range

        print(enemy_list)

        try:
            if enemy_pos[2] == 'group':
                distance_check = []
                for index,enemy in enumerate(enemy_list):
                    location = enemy[0] + enemy[1]
                    distance = abs((enemy_pos[0] + enemy_pos[1]) - location)

                    if enemy[2] == 'idle':
                        distance_check.append([distance, index])
                    distance_check.sort()

                
                
            
                target_index = distance_check[0][1]

                # print(distance_check)
                # print(distance_check[0][1])
                # print(enemy_list[target_index][2])

                target_enemy_x = enemy_list[target_index][0]
                target_enemy_y = enemy_list[target_index][1]
                if target_enemy_x > enemy_pos[0] + enemy_spacing: enemy_pos[0] += enemy_speed
                if target_enemy_x < enemy_pos[0] - enemy_spacing: enemy_pos[0] -= enemy_speed
                if target_enemy_y > enemy_pos[1] + enemy_spacing: enemy_pos[1] += enemy_speed
                if target_enemy_y < enemy_pos[1] - enemy_spacing: enemy_pos[1] -= enemy_speed

                if target_enemy_x > enemy_pos[0] - enemy_spacing * 2 and target_enemy_x < enemy_pos[0] + enemy_spacing * 2:
                    if target_enemy_y > enemy_pos[1] - enemy_spacing * 2 and target_enemy_y < enemy_pos[1] + enemy_spacing * 2:
                        enemy_list[target_index][2] = 'group'
        except:
            pass
            
        grouped_enemies = 0
        for enemy_state in enemy_list:
            if enemy_state[2] == 'group':
                grouped_enemies += 1
        
        if grouped_enemies >= 5:
            for grouped_enemy in enemy_list:
                grouped_enemy[2] = 'attack'
            
                

        # The aggro box is checked for a player, using the in_aggro_range function.
        if in_aggro_range(player_pos, aggro_box_x, aggro_box_y, aggro_box_size):

            if enemy_pos[2] == 'idle':
                enemy_pos[2] = 'group'


            # If a player is detected, a relative location is determined by comparing 
            # the player and enemy x and y locations (player_pos[0], player_pos[1]).
            # The enemy is then moved to minimize the relative distance. For example:
            # If the player X location is greater than the enemy X location, the enemy
            # X will be increased by enemy_speed every tick until the distance is zero.

        if enemy_pos[2] == 'attack':
            state_attack(player_pos, enemy_pos, enemy_speed)



        pygame.draw.rect(screen, (AGGRO_RANGE_COLOR), (int(aggro_box_x), int(aggro_box_y), aggro_box_size, aggro_box_size))

    # A seperate loop here prevents aggro boxes from being drawn over adjacent enemies
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, (ENEMY_COLOR), (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def move_player(player_pos, PLAYER_SPEED):

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]: player_pos[0] -= PLAYER_SPEED
    if keys[pygame.K_d]: player_pos[0] += PLAYER_SPEED
    if keys[pygame.K_w]: player_pos[1] -= PLAYER_SPEED
    if keys[pygame.K_s]: player_pos[1] += PLAYER_SPEED
    
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
        pygame.draw.circle(screen, (250,50,50), (20 + (health * 30), 20), 10)

def spawn_enemies(enemy_list, player_pos, ENEMY_SPAWN_DISTANCE):
    if len(enemy_list) < 5:
        if random.random() < 0.05:
            new_enemy_x = random.randint(0, WIDTH)
            new_enemy_y = random.randint(0, HEIGHT)
            if new_enemy_x < (player_pos[0] + ENEMY_SPAWN_DISTANCE) and new_enemy_x > (player_pos[0] - ENEMY_SPAWN_DISTANCE):
                if new_enemy_y < (player_pos[1] + ENEMY_SPAWN_DISTANCE) and new_enemy_y > (player_pos[1] - ENEMY_SPAWN_DISTANCE):
                    pass
            else:
                enemy_list.append([new_enemy_x, new_enemy_y, 'idle'])
                
    return enemy_list

# States: Idle, Attack, Group
def change_states():
    pass

def state_attack(player_pos, enemy_pos, enemy_speed):
    if player_pos[0] > enemy_pos[0]: enemy_pos[0] += enemy_speed
    if player_pos[0] < enemy_pos[0]: enemy_pos[0] -= enemy_speed
    if player_pos[1] > enemy_pos[1]: enemy_pos[1] += enemy_speed
    if player_pos[1] < enemy_pos[1]: enemy_pos[1] -= enemy_speed
    # print(enemy_list)




while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_over = True
    
    screen.fill(background_color[0])
    background_color[0] = (0,0,0)

    spawn_enemies(enemy_list, player_pos, ENEMY_SPAWN_DISTANCE)
    move_enemies(enemy_list, player_pos, enemy_speed, enemy_spacing)
    move_player(player_pos, PLAYER_SPEED)
    draw_health(player_health)

    if detect_collisions(player_pos, enemy_list, enemy_size):
        if lose_health(player_health, current_time, time_hit):
            game_over = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()