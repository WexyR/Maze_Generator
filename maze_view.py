#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from maze import Maze


ROWS = 50
COLS = 70

CELL_SIZE = 12

pygame.init()

screen = pygame.display.set_mode((COLS*CELL_SIZE, ROWS*CELL_SIZE))

running = True

maze = Maze(COLS, ROWS)
maze.generate()

solution = []
clicks = 0

while running:
    
    for evt in pygame.event.get():
        if evt.type == QUIT:
            running = False
        if evt.type == KEYDOWN:
            maze = Maze(ROWS, COLS)
            maze.generate()

    if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
        pos_x, pos_y = pygame.mouse.get_pos()
        x, y = pos_x//CELL_SIZE, pos_y//CELL_SIZE
        
        if pygame.mouse.get_pressed()[0]:
            x1, y1 = x, y
        elif pygame.mouse.get_pressed()[2]:
            x2, y2 = x, y
        try:
            solution = maze.resolve(maze[x1,y1], maze[x2, y2])
        except NameError:
            pass



    screen.fill((60, 60, 60))

    for line in maze:
        for cell in line:
            cx, cy = cell.coords
            if cell in solution:
                if cell == solution[0] or cell == solution[-1]:
                    color = (200, 50, 50)
                else:
                    color = (100,50,120)
                pygame.draw.rect(screen, color, 
                    pygame.Rect(cx*CELL_SIZE, cy*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if not cell.edges['N']:
                # pygame.draw.rect(screen, (0,0,0), 
                #     pygame.Rect(cx*CELL_SIZE-2, cy*CELL_SIZE, CELL_SIZE+4, 2))
                pygame.draw.line(screen, (0, 0, 0), (cx*CELL_SIZE, cy*CELL_SIZE), ((cx+1)*CELL_SIZE, cy*CELL_SIZE))
            if not cell.edges['S']:
                # pygame.draw.rect(screen, (0,0,0), 
                #     pygame.Rect(cx*CELL_SIZE-2, cy*CELL_SIZE+CELL_SIZE-2, CELL_SIZE+4, 2))
                pygame.draw.line(screen, (0, 0, 0), (cx*CELL_SIZE, (cy+1)*CELL_SIZE), ((cx+1)*CELL_SIZE, (cy+1)*CELL_SIZE))

            if not cell.edges['W']:
                # pygame.draw.rect(screen, (0,0,0), 
                #     pygame.Rect(cx*CELL_SIZE, cy*CELL_SIZE-2, 2, CELL_SIZE+4))
                pygame.draw.line(screen, (0, 0, 0), (cx*CELL_SIZE, cy*CELL_SIZE), (cx*CELL_SIZE, (cy+1)*CELL_SIZE))
            if not cell.edges['E']:
                # pygame.draw.rect(screen, (0,0,0), 
                #     pygame.Rect(cx*CELL_SIZE+CELL_SIZE-2, cy*CELL_SIZE-2, 2, CELL_SIZE+4))
                pygame.draw.line(screen, (0, 0, 0), ((cx+1)*CELL_SIZE, cy*CELL_SIZE), ((cx+1)*CELL_SIZE, (cy+1)*CELL_SIZE))


    pygame.display.flip()


pygame.quit()
