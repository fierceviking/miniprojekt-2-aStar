import random
import pygame
import numpy as np
from queue import PriorityQueue

# mapWidth = int(input("Enter map width: "))
# mapHeight = int(input("Enter map height: "))
mapWidth = 75
mapHeight = 75
running = True

terrainTypes = {
    'ocean': {'color': (0, 0, 255), 'moveCost': 5},
    'water': {'color': (50, 50, 255), 'moveCost': 3},
    'sand': {'color': (255, 255, 0), 'moveCost': 1},
    'grassland': {'color': (52, 140, 49), 'moveCost': 1},
    'forest': {'color': (4, 99, 4), 'moveCost': 2},
    'mountain': {'color': (83, 86, 91), 'moveCost': 5},
    'mountainTop': {'color': (250, 250, 250), 'moveCost': 10}
}

pygame.init()

screen = pygame.display.set_mode((mapWidth * 8, mapHeight * 8))
pygame.display.set_caption("Pathfinder")

class MapGenerator:
    def __init__(self, mapWidth, mapHeight):
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.map = np.zeros((mapWidth, mapHeight, 3), dtype=np.uint8)
        self.mapCost = np.zeros((mapWidth, mapHeight), dtype=np.uint8)

    def generateMap(self):
        num_points = 30
        points = [(random.randint(0, self.mapWidth - 1), random.randint(0, self.mapHeight - 1)) for _ in range(num_points)]

        for x in range(self.mapWidth):
            for y in range(self.mapHeight):
                min_distance = float('inf')
                for point_x, point_y in points:
                    distance = ((x - point_x) ** 2 + (y - point_y) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance

                normalized_distance = min_distance / max(self.mapWidth, self.mapHeight)
                neighborHeight = self.averageNeighborHeight(x, y)

                height_value = 0.5 + (0.1 - normalized_distance) + neighborHeight * 0.1

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
                else:
                    terrain_type = 'water'

                self.map[x][y] = np.array(terrainTypes[terrain_type]['color'])
                self.mapCost[x][y] = terrainTypes[terrain_type]['moveCost']

    def averageNeighborHeight(self, x, y):
        total_height = 0
        num_neighbors = 0

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x + dx < self.mapWidth and 0 <= y + dy < self.mapHeight:
                    total_height += random.random()
                    num_neighbors += 1

        if num_neighbors == 0:
            return 0

        return total_height / num_neighbors

class Pathfinder:
    def __init__(self, map):
        self.map = map
        self.start = (random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1))
        print(self.start)
        self.end = (random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1))
        print(self.end)
    
    def heuristic(self, current, end):
        return abs(current.x - end.x) + abs(current.y - end.y)
    
    def neighborsCost(self, x, y):
        neighbors = []
        neighbors.append((x - 1, y))
            

    
map = MapGenerator(mapWidth, mapHeight)
map.generateMap()
cost = Pathfinder(map.mapCost)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            map = MapGenerator(mapWidth, mapHeight)
            map.generateMap()
            cost = Pathfinder(map.mapCost)

            
    for x in range(mapWidth):
        for y in range(mapHeight):
            pygame.draw.rect(screen, map.map[x][y], (x * 8, y * 8, 8, 8))
            pygame.draw.rect(screen, (255,0,0), (cost.start[0] * 8, cost.start[1] * 8, 8, 8))
            pygame.draw.rect(screen, (0,255,255), (cost.end[0] * 8, cost.end[1] * 8, 8, 8))
    
    pygame.display.flip()

pygame.quit()