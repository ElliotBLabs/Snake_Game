import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class cube(object):
    global width, rows

    def __init__(self, start, dirnx=1, dirny=0, colour=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.colour = colour

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = width // rows
        i = self.pos[0]  # Row
        j = self.pos[1]  # Coluumn

        pygame.draw.rect(surface, self.colour, (i*dis+1, j*dis+1, dis-2, dis-2))  # +1/-2 is to keep cube within the grid lines
        if eyes:
            centre = dis // 2
            radius = 3   #Eye Radius
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, colour, pos):
        self.colour = colour
        self.head = cube(pos)  # Head starting position passed in by pos
        self.body.append(self.head)
        self.dirnx = 1
        self.dirny = 0 # Sets up a moving direction for the snake

    def move(self):
        global rows
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:

                if keys[pygame.K_LEFT] == 1:
                    self.dirnx = -1
                    self.dirny = 0    #Pygame requires a left turn to have a negative x as (0,0) is at the top right of the window
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]    # Records the turning point and the driection of the turn
                elif keys[pygame.K_RIGHT] == 1:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP] == 1:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN] == 1:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i,c in enumerate(self.body):  # i represents index and c represents cube object
            p = c.pos[:]    # Gets position of cube
            if p in self.turns:  # Sees if position is in turn list
                turn = self.turns[p]
                c.move(turn[0], turn[1])   # Gives cube a new direction
                if i == len(self.body)-1:
                    self.turns.pop(p) # Once last cube hits the turn, it is removed
            else:   #Handles moving off the edge of the screen/ normal movement
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], rows - 1)
                else:   #Just keep moving the cube in the correct direction
                    print('Move')
                    c.move(c.dirnx, c.dirny)


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 1
        self.dirny = 0



    def addCube(self):
        tail = self.body[-1]
        dx,dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:   # Handles knowing where to add the cube
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy # Cube moves in correct direction


    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i ==0:
                c.draw(surface,True)  # First head can be custom designed so it is diff. from the rest
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizebetween = w //rows # Figures out how big the coloumns should be

    x= 0
    y= 0
    for l in range(rows):
        x+= sizebetween
        y += sizebetween

        pygame.draw.line(surface, (255,255,255), (x,0), (x,w)) # Draw white line from top of screen to bottom
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y)) # Draw white line across a screen from right to left



def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))  # Darws a black screen
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(item):
    global rows
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:     # Checks if snack is in snake
            continue
        else:
            break

    return (x,y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)   #Window on top of it
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, height, s, snack
    width = 600
    height = 600
    rows = 60 # Columns
    pygame.init()
    pygame.display.set_caption('The Snake Game')
    win = pygame.display.set_mode((width, height))
    s = snake((255,0 ,0), (10,10))  # Relates to Snake Object of colour = Red And Pos. = 10,10
    snack = cube(randomSnack(s), colour = (0,255,0))
    flag = True

    clock = pygame.time.Clock()  # iNIT. A FPS for the game

    while flag:
        pygame.time.delay(50) # Slows game by 50ms each tick
        clock.tick(10) # Games runs at 10FPS
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(s), colour = (0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x +1:])):  # Check collision
                print('Score', len(s.body))
                message_box('You lost with a score of: '+ str(len(s.body)), 'Play again...')
                s.reset((10,10))

        redrawWindow(win)




main()