#NOTE:This creation of this game is focused on object oriented programming.'''

'''We are working in a grid system with a total of 20 rows and 20 columns.So, if position is (10, 10) 
means we are in 11th column and the 11th row (because position count starts from 0)'''

import random
import math
import pygame
import time
import tkinter as tk
from tkinter import messagebox

pygame.init()
move_sound = pygame.mixer.Sound("move.mp3")
eat_sound = pygame.mixer.Sound("Snack2.mp3")
pygame.mixer.music.load("back1.mp3")

pygame.font.init()
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 25)

def draw_text_middle(surface, text, size, color):  
    global width
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)

    surface.blit(label, (width/5, width/2))

class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0,color=(255, 0, 0)): #'dirnx=1' -> snake starts moving(right) automatically when game starts
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color        
    
    def move(self, dirnx, dirny): #here,(dirnx, dirny): change-in-position(made in 'snake'class) but in '__init__()' it's the starting-position
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) #changes position so that snake appears to move

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows #'dis' is the width(lenght=width) of one grid 
        i = self.pos[0] #column number
        j = self.pos[1] #row number
        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2)) #pygame.draw.pygame.draw.line(Surface, color, start_pos, end_pos, thickness)
        #Drawing the eyes
        if eyes:
            centre = dis // 2 #'//' is regular division with result as an integer
            radius = 3
            circleMiddle = (i*dis + centre - radius, j*dis + 8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius) #pygame.draw.circle(Surface, color, pos, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

#contains a bunch of cube objects
class snake(object):
    body = [] #contains the address of cube-objects present at different position
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) #head of snake(first cube) is equal to cube at given position
        self.body.append(self.head) #adding cubes(position) to make the body 
        self.dirnx = 0
        self.dirny = 0

    def move(self):
        global opposite_dirn
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #keys = pygame.key.get_pressed() ->gets a dictionary of all keyboard-keys and if they were pressed(value = 1) or not(value = 0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.mixer.Sound.play(move_sound)
                    if self.dirnx == 1:
                        continue
                        opposite_dirn = True
                    else:
                        self.dirnx = -1
                    self.dirny = 0
                    '''Now we should store the position where the snake(head) turns so that whole body also turns. 
                    Thus we add a key(by copying([:]) current position-of-head('self.head.pos') as key) and set its 
                    value = '[self.dirnx, self.dirny]' to the 'turns' dictionary'''
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] #'[:]' copies the tuple to a variable(to key-of-dictionary)
                elif event.key == pygame.K_RIGHT:
                    pygame.mixer.Sound.play(move_sound)
                    if self.dirnx == -1:
                        continue
                        opposite_dirn = True
                    else:
                        self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(move_sound)
                    if self.dirny == 1:
                        continue
                        opposite_dirn = True
                    else:
                        self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                    #print(self.dirnx, self.dirny) //prints 0 -1 in console
                elif event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(move_sound)
                    if self.dirny == -1:
                        continue
                        opposite_dirn = True
                    else:
                        self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): #'c' points to the cubes; one cube at a time; present in the list 'body'
            p = c.pos[:] #copying([:]) the position-of-current-cube(c.pos) to new variable 'p' 
            ''' we may have written just 'p = c.pos' but it may cause problems when 'c.position' changes its value. But '[:]' copies the 
            value of'c.pos' to the new variable 'p' thus 'p' won't change even if 'c.pos' changes'''            
            #If we have pressed any of the four arrow keys
            if p in self.turns:  #if the cube position present in 'turns' as a 'key-of-the-dictionary'
                turn = self.turns[p] #storing the position(x, y; where we want to turn); in a tuple(here: 'turn')
                c.move(turn[0], turn[1]) #turns[0] -> x and turns[1] -> y; here we actually move
                if i == len(self.body) - 1:
                    self.turns.pop(p) #dict.'pop(k, d=None)'-> removes specified key and return the corresponding value
                    '''once we are on the last cube we'll remove 'p' to avoid this -> Whenever the snake reachs position 'p' on screen,
                    it will turn regardless of pressing any key because 'p' is still present in the 'turns' dictionary'''       

            #When snake reaches the end of screen, it emerges from the other side
            else:
                '''[dirnx = -1] -> left direction but [dirny = -1] -> upward direction
                [c.row - 1] -> last row or column'''
                if c.dirnx == -1 and c.pos[0] <= 0: #while moving left and crosses the left end(x = 0)
                    c.pos = (c.rows-1, c.pos[1]) #'rows' represent columns
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: #while moving right and crosses the right end(x is max)
                    c.pos = (0, c.pos[1])#'rows' represent columns
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: #while moving down crosses the bottom(y is max)
                    c.pos = (c.pos[0], 0)#'rows' represent rows
                elif c.dirny == -1 and c.pos[1] <= 0: #while moving up crosses the top (y = 0)
                    c.pos = (c.pos[0], c.rows-1)#'rows' represent rows
                else: #if a key is pressed to change the direction and thus snake does'nt reach any end
                    c.move(c.dirnx, c.dirny) #then keep on moving in the changed direction 

    def reset(self, pos):
        self.head = cube(pos) #head of snake(first cube) is equal to cube at given position
        self.body = []
        self.body.append(self.head) #adding cubes(position) to make the body 
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny 

        if dx == 1 and dy == 0: #when going right, add cube to the left of tail
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        #added cube should move in directoion of tail    
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0: #if it's the first cube
                c.draw(surface, True) #draws both (cube and eyes)         
            else:
                c.draw(surface) #draws the cube only

def drawGrid(w, rows, surface):
    spaceBtw = w // rows
    x = 0
    y = 0
    for i in range(rows):
        x += spaceBtw
        y += spaceBtw
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w)) #vertical lines
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y)) #horizontal lines

def redrawWindow(surface, score):
    global width, rows, s, snack
    surface.fill((0, 0 , 0))
    my_score(score)
    s.draw(surface)
    snack.draw(surface)
    #drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(row, item): #'item' is snake object
    global rows
    positions = item.body #'positions' is a list of different cubes('cube-objects') present in the current-snake-length(the list 'body') 

    while True:
        x = random.randrange(rows) #random column-number between 0 and 20
        y = random.randrange(rows) #random row-number between 0 and 20

        #filter(function, sequence) -> 'function' checks the sequence and filters out the items according to 'function'
        #lambda arguments:expression -> can take any number of arguments, but only one expression(executed and the result is returned)

        #Ensuring that snack never appears on snake

        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
            '''NOTE: Here 'z' switches b/w different cube-objects present in the list 'body'(of 'snake' class).If object-position('z.pos') is equal
            to snack-position(x,y),then we'll store 'z.pos' in a list; this makes list-length > 0.Hence,list-length tells us 
            if the snack is present on the snake or not; and if it is, then another value for (x, y) gets chosen.'''
        else:
            break
    
    return (x, y)

def my_score(score):
    win = pygame.display.set_mode((width, width))
    value = score_font.render("Score: " + str(score), True, (255, 255, 255))
    win.blit(value, [0, 0])

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack, opposite_dirn
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10)) #snake(color, pos)
    snack = cube(randomSnack(rows, s), color = (0, 255, 0))
    clock = pygame.time.Clock()
    play = True
    score = 0
    pygame.mixer.music.play(-1)
    speed = 10

    while play:
        opposite_dirn = False
        #pygame.time.delay(50)
        clock.tick(speed)
        speed += 0.03
        if speed >= 17:
            speed = 17
        s.move()
        if s.body[0].pos == snack.pos:
            pygame.mixer.Sound.play(eat_sound)
            score += 1
            s.addCube()
            snack = cube(randomSnack(rows, s), color = (0, 255, 0))
        for x in range(len(s.body)):
            #map(function, iterable) -> every iterable is passed to function and result is returned
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])) and opposite_dirn == False: 
                draw_text_middle(win, "GAME OVER!", 50, (255, 255, 255))
                pygame.display.update()
                pygame.time.delay(3000)
                s.reset((10, 10))
                score = 0
                break
                
        redrawWindow(win, score)

main()
