from map_generator import MapGenerator
from breadth_first import breadthFirst
import numpy as np
import pygame
import random

# here pygame is initialized
pygame.init()

# then we take some user input for the map width, map height, and number of points
print('map sizes above xx125 may cause lag')
mapWidth = int(input("Enter map width: "))
mapHeight = int(input("Enter map height: "))
points = int(input("Enter number of points: "))

# here we set the size scaler which is the size of each node in the pygame window
sizeScaler = 5

# here we set the running boolean to true
running = True

# here we set the pygame window and the caption
screen = pygame.display.set_mode((mapWidth * sizeScaler, mapHeight * sizeScaler))
pygame.display.set_caption("Breadth First")

# here we initialize the map generator and the breadth first algorithm
map_generator = MapGenerator(mapWidth, mapHeight, points)
bfs = breadthFirst(map_generator.generateMap(), [0, 0], [mapWidth - 1, mapHeight - 1])

# here we define the draw_map function which draws the map
def draw_map():
    # first the screen is filled with black
    screen.fill((0, 0, 0))
    # then we loop through the map and draw each node
    for x in range(mapWidth):
        for y in range(mapHeight):
            # if the map node is 255, we draw a white node to represent an unwalkable node
            if map_generator.map[x][y] == 255:
                pygame.draw.rect(screen, (255, 255, 255), (x * sizeScaler, y * sizeScaler, sizeScaler, sizeScaler))
            # otherwise we draw a black node to represent a walkable node
            else:
                pygame.draw.rect(screen, (0, 0, 0), (x * sizeScaler, y * sizeScaler, sizeScaler, sizeScaler))

    # and here we draw the start and end nodes
    pygame.draw.rect(screen, (0, 255, 0), (bfs.start[0] * sizeScaler, bfs.start[1] * sizeScaler, sizeScaler, sizeScaler))
    pygame.draw.rect(screen, (255, 0, 0), (bfs.end[0] * sizeScaler, bfs.end[1] * sizeScaler, sizeScaler, sizeScaler))

    # and update the pygame window
    pygame.display.update()

# here we define the draw_path function which draws the path
def draw_path(path):
    # here we loop through the path-list and draw each node
    for node in path:
        pygame.draw.rect(screen, (0, 0, 255), (node[0] * sizeScaler, node[1] * sizeScaler, sizeScaler, sizeScaler))
    # and update the pygame window
    pygame.display.update()

# here we draw the map and update the pygame window
draw_map()
pygame.display.update()

# this is the main loop which runs until the user closes the pygame window
while running:
    # here we check all the events in pygame
    for event in pygame.event.get():
        # if the pygame window is closed, we set the running boolean to false
        if event.type == pygame.QUIT:
            running = False
        # if the user presses the space bar, we generate a new map and find a new path
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # first we generate new start and end nodes on nodes that are walkable
            start = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
            while map_generator.map[start[0]][start[1]] == 255:
                start = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
            end = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
            while map_generator.map[end[0]][end[1]] == 255:
                end = [random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1)]
            # then we generate a new map and run the breadth first algorithm
            bfs = breadthFirst(map_generator.generateMap(), start, end)
            # then we draw the map and update the pygame window
            draw_map()
            pygame.display.update()
    # 
    if not bfs.found:
        bfs.findPath()
        draw_path(bfs.path)

# here we quit pygame
pygame.quit()