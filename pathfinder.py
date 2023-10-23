import random
import pygame
import numpy as np
from queue import PriorityQueue

mapWidth = 75
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
screen = pygame.display.set_mode((mapWidth * 8, mapHeight * 8))
pygame.display.set_caption("Pathfinder")

class MapGenerator:
    def __init__(self, mapWidth, mapHeight):
        # initiate map by mapWidth and mapHeight and make a 2D array which is filled with 0
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.map = np.zeros((mapWidth, mapHeight, 3), dtype=np.uint8)
        self.mapCost = np.zeros((mapWidth, mapHeight), dtype=np.uint8)

    def generateMap(self):
        # select num_points random points to use for terrain generation
        num_points = 10
        # and make a list with the random coordinates
        points = [(random.randint(0, self.mapWidth - 1), random.randint(0, self.mapHeight - 1)) for _ in range(num_points)]
        # loop over the entire map
        for x in range(self.mapWidth):
            for y in range(self.mapHeight):
                # calculate the distance from the current point to all the random points
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

class Pathfinder:
    def __init__(self, mapCost):
        self.mapCost = mapCost
        self.start = (random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1))
        print(self.start)
        self.end = (random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1))
        print(self.end)
        while self.end == self.start:
            self.end = (random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1))
    
    def aStar(self):
        frontier = PriorityQueue()
        frontier.put(self.start, 0)
        cameFrom = {}
        costSoFar = {}
        cameFrom[self.start] = None
        costSoFar[self.start] = 0
        while not frontier.empty():
            # current is a tuple of (priority, coordinate)
            current = frontier.get()
            if current[1] == self.end:
                break
            for next in self.neighbors(current[1]):
                newCost = costSoFar[current[1]] + self.cost(current[1], next)
                if next not in costSoFar or newCost < costSoFar[next]:
                    costSoFar[next] = newCost
                    priority = newCost + self.heuristic(self.end, next)
                    frontier.put(next, priority)
                    cameFrom[next] = current[1]
    
    def heuristic(self, current, end):
        return abs(current.x - self.end.x) + abs(current.y - self.end.y)
    
    def neighbors(self, current):
        neighbors = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= x + i < mapWidth and 0 <= y + j < mapHeight:
                    neighbors += 1
        return neighbors
    
    def neighborsCost(self, x, y):
        neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if 0 <= x + i < mapWidth and 0 <= y + j < mapHeight:
                    value = 
            
map = MapGenerator(mapWidth, mapHeight)
map.generateMap()
cost = Pathfinder(map.mapCost)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if space is pressed
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # generate a new map
            map = MapGenerator(mapWidth, mapHeight)
            map.generateMap()
            cost = Pathfinder(map.mapCost)
    # draw the map in pygame
    for x in range(mapWidth):
        for y in range(mapHeight):
            pygame.draw.rect(screen, map.map[x][y], (x * 8, y * 8, 8, 8))
            pygame.draw.rect(screen, (255,0,0), (cost.start[0] * 8, cost.start[1] * 8, 8, 8))
            pygame.draw.rect(screen, (0,255,255), (cost.end[0] * 8, cost.end[1] * 8, 8, 8))
    # update the display
    pygame.display.flip()
# exit pygame
pygame.quit()