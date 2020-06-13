import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

BLUE = (0,0,255)
BLACK = (0,0,0)

player_pos = [400, 300]
player_size = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

while not game_over:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_a:

                x -= player_size

            elif event.key == pygame.K_d:

                x += player_size
            
            player_pos = [x, y]
    
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    pygame.display.update()



