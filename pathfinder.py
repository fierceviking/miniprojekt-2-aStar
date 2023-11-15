import random
import pygame
import numpy as np
from queue import PriorityQueue

mapWidth = 100
mapHeight = 75
# mapWidth = int(input("Enter map width: "))
# mapHeight = int(input("Enter map height: "))
running = True

# define the dictionary with terrain types along with their color and move cost
terrainTypes = {
    'ocean': {'color': (0, 0, 255), 'moveCost': 6},
    'water': {'color': (50, 50, 255), 'moveCost': 3},
    'sand': {'color': (255, 255, 0), 'moveCost': 1},
    'grassland': {'color': (52, 140, 49), 'moveCost': 1},
    'forest': {'color': (4, 99, 4), 'moveCost': 2},
    'mountain': {'color': (83, 86, 91), 'moveCost': 5},
    'mountainTop': {'color': (250, 250, 250), 'moveCost': 10}
}

# pygame boilerplate code
pygame.init()
if mapWidth > mapHeight:
    sc_modifier = 800 // mapWidth
else:
    sc_modifier = 800 // mapHeight
screen = pygame.display.set_mode((mapWidth * sc_modifier, mapHeight * sc_modifier))
pygame.display.set_caption("Pathfinder")

# here we start the good stuff
class MapGenerator:
    def __init__(self, mapWidth, mapHeight):
        # initiate map by mapWidth and mapHeight and make a 2D array which is filled with 0's
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.map = np.zeros((mapWidth, mapHeight, 3), dtype=np.uint8)
        self.mapCost = np.zeros((mapWidth, mapHeight), dtype=np.uint8)

    def generateMap(self):
        # select num_points random points to use for terrain generation
        # (lower num_points means more water as there are less points to generate land)
        num_points = 10
        # and make a list with the random coordinates within the map borders. The coordinates are tuples of (x, y)
        points = [(random.randint(0, self.mapWidth - 1), random.randint(0, self.mapHeight - 1)) for _ in range(num_points)]
        # loop over the entire map
        for x in range(self.mapWidth):
            for y in range(self.mapHeight):
                # calculate the distance from the current point to all the random points
                # the starting value is infinity so that the first distance will always be smaller
                min_distance = float('inf')
                for point_x, point_y in points:
                    distance = np.sqrt((x - point_x) ** 2 + (y - point_y) ** 2)
                    if distance < min_distance:
                        min_distance = distance
                # scale the distance to be between 0 and 1
                normalized_distance = min_distance / max(self.mapWidth, self.mapHeight)
                # get the average height of the neighbors
                neighborHeight = self.averageNeighborHeight(x, y)
                # calculate the height value based on the distance and the neighbor's height
                height_value = 0.5 + (0.1 - normalized_distance) + neighborHeight * 0.1
                # set the color of the pixel based on the height value
                if height_value > 0.65:
                    terrain_type = 'mountainTop'
                elif height_value > 0.6:
                    terrain_type = 'mountain'
                elif height_value > 0.56:
                    terrain_type = 'forest'
                elif height_value > 0.5:
                    terrain_type = 'grassland'
                elif height_value > 0.46:
                    terrain_type = 'sand'
                elif height_value > 0.38:
                    terrain_type = 'water'
                else:
                    terrain_type = 'ocean'
                # set the color of the pixel
                self.map[x][y] = np.array(terrainTypes[terrain_type]['color'])
                self.mapCost[x][y] = np.array(terrainTypes[terrain_type]['moveCost'])

    def averageNeighborHeight(self, x, y):
        total_height = 0
        num_neighbors = 0
        # loop over the neighbors of the current point in a 3x3 grid
        # [[][][]
        #  [][][]
        #  [][][]]
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # make sure the neighbor is within the map
                if 0 <= x + dx < self.mapWidth and 0 <= y + dy < self.mapHeight:
                    # add the height of the neighbor to the total height
                    total_height += random.random()
                    num_neighbors += 1

        if num_neighbors == 0:
            return 0
        # return the average height of the neighbors
        return total_height / num_neighbors

class node:
    def __init__(self, x, y, cost, heuristic):
        self.x = x
        self.y = y
        self.cost = cost
        self.heuristic = heuristic
        self.f = cost + heuristic
        self.parent = None
    
    def heuristic(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def __lt__(self, other):
        return self.f < other.f

class aStar:
    def __init__(self, start, end):
        self.start = node(*start, 0, node.heuristic(start, end))
        self.end = node(*end, 0, 0)

map = MapGenerator(mapWidth, mapHeight)
map.generateMap()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if space is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # generate a new map
            map = MapGenerator(mapWidth, mapHeight)
            map.generateMap()
            mapCost = map.mapCost
            np.savetxt('mapCost.txt', mapCost, fmt='%d')
    # draw the map in pygame
    for x in range(mapWidth):
        for y in range(mapHeight):
            pygame.draw.rect(screen, map.map[x][y], (x * sc_modifier, y * sc_modifier, sc_modifier, sc_modifier))

    # update the display
    pygame.display.flip()
# exit pygame
pygame.quit()