import numpy as np
import random
from opensimplex import OpenSimplex

class MapGenerator:
    def __init__(self, mapWidth, mapHeight):
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.map = np.zeros((mapWidth, mapHeight, 3), dtype=np.uint8)
        self.mapCost = np.zeros((mapWidth, mapHeight), dtype=np.uint8)
        self.terrainTypes = {
            'ocean': {'color': (0, 0, 255), 'moveCost': 6},
            'water': {'color': (50, 50, 255), 'moveCost': 3},
            'sand': {'color': (255, 255, 0), 'moveCost': 1},
            'grassland': {'color': (52, 140, 49), 'moveCost': 1},
            'forest': {'color': (4, 99, 4), 'moveCost': 2},
            'mountain': {'color': (83, 86, 91), 'moveCost': 5},
            'mountainTop': {'color': (250, 250, 250), 'moveCost': 10}
        }
        self.noise_gen = OpenSimplex(seed=random.randint(0, 1000))  # Use a random seed

    def generateMap(self):
        scale = 20.0  # Adjust the scale for the noise
        for x in range(self.mapWidth):
            for y in range(self.mapHeight):
                normalized_distance = self.noise_gen.noise2d(x / scale, y / scale)
                neighborHeight = self.averageNeighborHeight(x, y)
                height_value = 0.5 + (0.1 - normalized_distance) + neighborHeight * 0.1
                terrain_type = self.getTerrainType(height_value)
                self.map[x][y] = np.array(self.terrainTypes[terrain_type]['color'])
                self.mapCost[x][y] = np.array(self.terrainTypes[terrain_type]['moveCost'])

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
