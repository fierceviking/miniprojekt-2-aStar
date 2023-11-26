import random
import pygame
import numpy as np

mapWidth = 100
mapHeight = 75
running = True

terrainTypes = {
    'ocean': {'color': (0, 0, 255), 'moveCost': 6},
    'water': {'color': (50, 50, 255), 'moveCost': 3},
    'sand': {'color': (255, 255, 0), 'moveCost': 1},
    'grassland': {'color': (52, 140, 49), 'moveCost': 1},
    'forest': {'color': (4, 99, 4), 'moveCost': 2},
    'mountain': {'color': (83, 86, 91), 'moveCost': 5},
    'mountainTop': {'color': (250, 250, 250), 'moveCost': 10}
}

pygame.init()
if mapWidth > mapHeight:
    sc_modifier = 800 // mapWidth
else:
    sc_modifier = 800 // mapHeight
screen = pygame.display.set_mode((mapWidth * sc_modifier, mapHeight * sc_modifier))
pygame.display.set_caption("Pathfinder")

class MapGenerator:
    def __init__(self, mapWidth, mapHeight):
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.map = np.zeros((mapWidth, mapHeight, 3), dtype=np.uint8)
        self.mapCost = np.zeros((mapWidth, mapHeight), dtype=np.uint8)

    def generateMap(self):
        num_points = 10
        points = [(random.randint(0, self.mapWidth - 1), random.randint(0, self.mapHeight - 1)) for _ in range(num_points)]
        for x in range(self.mapWidth):
            for y in range(self.mapHeight):
                min_distance = float('inf')
                for point_x, point_y in points:
                    distance = np.sqrt((x - point_x) ** 2 + (y - point_y) ** 2)
                    if distance < min_distance:
                        min_distance = distance
                normalized_distance = min_distance / max(self.mapWidth, self.mapHeight)
                neighborHeight = self.averageNeighborHeight(x, y)
                height_value = 0.5 + (0.1 - normalized_distance) + neighborHeight * 0.1
                terrain_type = self.getTerrainType(height_value)
                self.map[x][y] = np.array(terrainTypes[terrain_type]['color'])
                self.mapCost[x][y] = np.array(terrainTypes[terrain_type]['moveCost'])

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

    def getTerrainType(self, height_value):
        if height_value > 0.65:
            return 'mountainTop'
        elif height_value > 0.6:
            return 'mountain'
        elif height_value > 0.56:
            return 'forest'
        elif height_value > 0.5:
            return 'grassland'
        elif height_value > 0.46:
            return 'sand'
        elif height_value > 0.38:
            return 'water'
        else:
            return 'ocean'