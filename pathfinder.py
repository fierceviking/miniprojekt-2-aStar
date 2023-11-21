import random
import pygame
import numpy as np
from queue import PriorityQueue

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

class Node:
    def __init__(self, x, y, cost, heuristic):
        self.x = x
        self.y = y
        self.cost = cost
        self.heuristic = heuristic
        self.f = cost + heuristic
        self.parent = None

    @staticmethod
    def heuristic_cal(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __lt__(self, other):
        return self.f < other.f


class AStar:
    def __init__(self, start, end):
        self.start = self.create_node(start[0], start[1], 0, Node.heuristic_cal(Node(*start), Node(*end)))
        self.end = self.create_node(end[0], end[1], 0, 0)
        self.open = PriorityQueue()
        self.open.put(self.start)
        self.closed = set()
        self.path = []

    def create_node(self, x, y, cost, heuristic):
        return Node(x, y, cost, heuristic)

    def search(self, mapCost):
        while not self.open.empty():
            current = self.open.get()
            if current == self.end:
                while current.parent:
                    self.path.append((current.x, current.y))
                    current = current.parent
                self.path.append((current.x, current.y))
                return self.path[::-1]
            self.closed.add(current)
            for x, y in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                neighbor = self.create_node(
                    current.x + x, current.y + y,
                    current.cost + mapCost[current.x + x, current.y + y],
                    Node.heuristic_cal((current.x + x, current.y + y), self.end)
                )
                if 0 <= neighbor.x < mapWidth and 0 <= neighbor.y < mapHeight:
                    if neighbor in self.closed:
                        continue
                    if neighbor not in self.open.queue:
                        neighbor.parent = current
                        self.open.put(neighbor)
        print(self.path)
        return None

map = MapGenerator(mapWidth, mapHeight)
map.generateMap()
mapCost = map.mapCost
np.savetxt('mapCost.txt', mapCost, fmt='%d')
start = (random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1))
end = (random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1))
search = AStar(start, end)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            map = MapGenerator(mapWidth, mapHeight)
            map.generateMap()
            mapCost = map.mapCost
            np.savetxt('mapCost.txt', mapCost, fmt='%d')
            start = (random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1))
            end = (random.randint(0, mapWidth - 1), random.randint(0, mapHeight - 1))
            search = AStar(start, end)

    for x in range(mapWidth):
        for y in range(mapHeight):
            pygame.draw.rect(screen, map.map[x][y], (x * sc_modifier, y * sc_modifier, sc_modifier, sc_modifier))

    if search and search.path:
        for i in range(len(search.path) - 1):
            start_point = (search.path[i][0] * sc_modifier + sc_modifier // 2, search.path[i][1] * sc_modifier + sc_modifier // 2)
            end_point = (search.path[i + 1][0] * sc_modifier + sc_modifier // 2, search.path[i + 1][1] * sc_modifier + sc_modifier // 2)
            pygame.draw.line(screen, (255, 0, 0), start_point, end_point, 2)

    pygame.display.flip()

pygame.quit()