from map_generator import MapGenerator
from breadth_first import breadthFirst
import numpy as np
import pygame
import random

pygame.init()

mapWidth = int(input("Enter map width: "))
mapHeight = int(input("Enter map height: "))
points = int(input("Enter number of points: "))
sizeScaler = 20
running = True

screen = pygame.display.set_mode((mapWidth * sizeScaler, mapHeight * sizeScaler))
pygame.display.set_caption("Breadth First")

map_generator = MapGenerator(mapWidth, mapHeight, points)
bfs = breadthFirst(map_generator.generateMap(), [0, 0], [mapWidth - 1, mapHeight - 1])

def draw_map():
    screen.fill((0, 0, 0))
    for x in range(mapWidth):
        for y in range(mapHeight):
            if map_generator.map[x][y] == 255:
                pygame.draw.rect(screen, (255, 255, 255), (x * sizeScaler, y * sizeScaler, sizeScaler, sizeScaler))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (x * sizeScaler, y * sizeScaler, sizeScaler, sizeScaler))
    pygame.draw.rect(screen, (0, 255, 0), (bfs.start[0] * sizeScaler, bfs.start[1] * sizeScaler, sizeScaler, sizeScaler))
    pygame.draw.rect(screen, (255, 0, 0), (bfs.end[0] * sizeScaler, bfs.end[1] * sizeScaler, sizeScaler, sizeScaler))

def draw_path(path):
    for node in path:
        pygame.draw.rect(screen, (0, 0, 255), (node[0] * sizeScaler, node[1] * sizeScaler, sizeScaler, sizeScaler))
    pygame.display.update()

draw_map()
pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bfs = breadthFirst(map_generator.generateMap(), [0, 0], [mapWidth - 1, mapHeight - 1])
            draw_map()
            pygame.display.update()

    if not bfs.found:
        bfs.findPath()
        draw_path(bfs.path)

pygame.quit()
