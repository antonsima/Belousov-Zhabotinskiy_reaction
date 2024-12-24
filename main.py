from copy import deepcopy
from random import randint

import numpy as np
import pygame
from numba import njit

RES = WIDTH, HEIGHT = 1280, 720
TILE = 4
W, H = WIDTH // TILE, HEIGHT // TILE
FPS = 60

pygame.init()
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

current_field = np.array([[randint(0, 2) for i in range(W)] for j in range(H)])
next_field = np.array([[0 for i in range(W)] for j in range(H)])


@njit(fastmath=True)
def check_cells(current_field, next_field):
    res_r = []
    res_g = []
    res_b = []

    for x in range(W):
        for y in range(H):
            count = 0
            if current_field[y][x] == 0:
                for j in range(y - 1, y + 2):
                    for i in range(x - 1, x + 2):
                        if current_field[j % H][i % W] == 1:
                            count += 1
                if count in [3, 4, 5, 6, 7, 8]:
                    next_field[y][x] = 1
                    res_g.append((x, y))
                else:
                    next_field[y][x] = 0
                    res_r.append((x, y))
            if current_field[y][x] == 1:
                for j in range(y - 1, y + 2):
                    for i in range(x - 1, x + 2):
                        if current_field[j % H][i % W] == 2:
                            count += 1
                if count in [3, 4, 5, 6, 7, 8]:
                    next_field[y][x] = 2
                    res_b.append((x, y))
                else:
                    next_field[y][x] = 1
                    res_g.append((x, y))
            if current_field[y][x] == 2:
                for j in range(y - 1, y + 2):
                    for i in range(x - 1, x + 2):
                        if current_field[j % H][i % W] == 0:
                            count += 1
                if count in [3, 4, 5, 6, 7, 8]:
                    next_field[y][x] = 0
                    res_r.append((x, y))
                else:
                    next_field[y][x] = 2
                    res_b.append((x, y))

    return next_field, res_r, res_g, res_b


while True:
    screen.fill(pygame.Color('red'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    next_field, res_r, res_g, res_b = check_cells(current_field, next_field)

    [pygame.draw.rect(screen, pygame.Color(246, 211, 210),
                      (x * TILE + 1, y * TILE + 1, TILE, TILE)) for x, y in res_r]
    [pygame.draw.rect(screen, pygame.Color(205, 233, 144),
                      (x * TILE + 1, y * TILE + 1, TILE, TILE)) for x, y in res_g]
    [pygame.draw.rect(screen, pygame.Color(255, 255, 231),
                      (x * TILE + 1, y * TILE + 1, TILE, TILE)) for x, y in res_b]

    current_field = deepcopy(next_field)

    print(clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)
