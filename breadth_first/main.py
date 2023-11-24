from map_generator import MapGenerator
# from breadth_first import breadthFirst
import numpy as np
import pygame
import random

pygame.init()

mapWidth = int(input("Enter map width: "))
mapHeight = int(input("Enter map height: "))
points = int(input("Enter number of points: "))
sizeScaler = 5
running = True

screen = pygame.display.set_mode((mapWidth * sizeScaler, mapHeight * sizeScaler))

pygame.display.set_caption("Breadth First")

map = MapGenerator(mapWidth, mapHeight, points).generateMap()
# using pygame, draw the map using rectangles of size sizeScaler as black or white pixels depending on the value of the map
start = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
while map[start[0]][start[1]] == 255:
    start = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
end = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
while map[end[0]][end[1]] == 255:
    end = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
for x in range(mapWidth):
    for y in range(mapHeight):
        if map[x][y] == 255:
            pygame.draw.rect(screen, (255, 255, 255), (x * sizeScaler, y * sizeScaler, sizeScaler, sizeScaler))
        else:
            pygame.draw.rect(screen, (0, 0, 0), (x * sizeScaler, y * sizeScaler, sizeScaler, sizeScaler))
        pygame.draw.rect(screen, (0, 255, 0), (start[0] * sizeScaler, start[1] * sizeScaler, sizeScaler, sizeScaler))
        pygame.draw.rect(screen, (255, 0, 0), (end[0] * sizeScaler, end[1] * sizeScaler, sizeScaler, sizeScaler))
pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if the user presses the space bar, generate a new map
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            map = MapGenerator(mapWidth, mapHeight, points).generateMap()
            print('map generated')
            # here we draw the map again and update the screen
            start = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
            while map[start[0]][start[1]] == 255:
                start = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
            end = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
            while map[end[0]][end[1]] == 255:
                end = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
            for x in range(mapWidth):
                for y in range(mapHeight):
                    if map[x][y] == 255:
                        pygame.draw.rect(screen, (255, 255, 255), (x * sizeScaler, y * sizeScaler, sizeScaler, sizeScaler))
                    else:
                        pygame.draw.rect(screen, (0, 0, 0), (x * sizeScaler, y * sizeScaler, sizeScaler, sizeScaler))
                    pygame.draw.rect(screen, (0, 255, 0), (start[0] * sizeScaler, start[1] * sizeScaler, sizeScaler, sizeScaler))
                    pygame.draw.rect(screen, (255, 0, 0), (end[0] * sizeScaler, end[1] * sizeScaler, sizeScaler, sizeScaler))
            pygame.display.update()