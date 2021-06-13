# Normal implementation (without OOPS)

import pygame
import time
import random
 
pygame.init()
move_sound = pygame.mixer.Sound("move.mp3")
eat_sound = pygame.mixer.Sound("Snack2.mp3")
pygame.mixer.music.load("back1.mp3")
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
display_width = 600
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game by Edureka')
clock = pygame.time.Clock()
rows = 20
snake_width = display_width // rows 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def draw_snake(snake_width, snake_body):
    for x in snake_body:
        pygame.draw.rect(gameDisplay, black, [x[0]*snake_width, x[1]*snake_width, snake_width-1, snake_width-1])

def my_score(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    gameDisplay.blit(value, (0, 0))
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    gameDisplay.blit(mesg, [display_width / 6, display_height / 3])
 
def game_loop():
    game_over = False
    quit_game = False
    x = 10
    y = 10
    x_change = 1
    y_change = 0
    snake_body = []
    snake_length = 1
    snack_x = round(random.randrange(0, 20)) 
    snack_y = round(random.randrange(0, 20))
    pygame.mixer.music.play(-1)

    while not game_over:
        speed = 10
        opposite_turn = False
        while quit_game == True:
            speed += 0.02
            if speed >= 17:
                speed = 17
            gameDisplay.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            my_score(snake_length - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        quit_game = False
                    if event.key == pygame.K_c:
                        game_loop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.mixer.Sound.play(move_sound)
                    if x_change == 1:
                        continue
                        opposite_turn = True
                    else:
                        x_change = -1
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    pygame.mixer.Sound.play(move_sound)
                    if x_change == -1:
                        continue
                        opposite_turn = True
                    else:
                        x_change = 1
                    y_change = 0
                elif event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(move_sound)
                    if y_change == 1:
                        continue
                        opposite_turn = True
                    else:
                        y_change = -1
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(move_sound)
                    if y_change == -1:
                        continue
                        opposite_turn = True
                    else:
                        y_change = 1
                    x_change = 0

        if x >= rows or x < 0 or y >= rows or y < 0:
            quit_game = True
        x += x_change
        y += y_change
        
        gameDisplay.fill(blue)
        pygame.draw.rect(gameDisplay, green, [snack_x*snake_width, snack_y*snake_width, snake_width, snake_width])
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_body.append(snake_head)
        if len(snake_body) > snake_length:
            del snake_body[0]
 
        for pos in snake_body[:-1]:
            if pos == snake_head and opposite_turn == False:
                quit_game = True
 
        draw_snake(snake_width, snake_body)
        my_score(snake_length - 1)
 
        pygame.display.update()
 
        if x == snack_x and y == snack_y:
            pygame.mixer.Sound.play(eat_sound)
            snack_x = round(random.randrange(0, 20))
            snack_y = round(random.randrange(0, 20))
            snake_length += 1
 
        clock.tick(speed)
 
    pygame.quit()
    quit()
 
game_loop()
