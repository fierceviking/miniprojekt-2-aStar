import numpy as np
import random

class MapGenerator:
    def __init__(self, mapwidth, mapheight, points):
        self.mapwidth = mapwidth
        self.mapheight = mapheight
        self.points = points
        self.map = np.zeros((mapwidth, mapheight), dtype=np.uint8)

    def generateMap(self):
        self.map = np.zeros((self.mapwidth, self.mapheight), dtype=np.uint8)
        # generate a list of random points
        for _ in range(self.points):
            x = random.randint(0, self.mapwidth - 1)
            y = random.randint(0, self.mapheight - 1)
            self.map[x][y] = 255
            # let points adjacent to the random point also have a chance to be set
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    if 0 <= x + dx < self.mapwidth and 0 <= y + dy < self.mapheight:
                        if random.random() < 0.5:
                            self.map[x + dx][y + dy] = 255
        np.savetxt('breadth_first/map.txt', self.map, fmt='%d')
        return self.map
        

if __name__ == '__main__':
    mapWidth = int(input("Enter map width: "))
    mapHeight = int(input("Enter map height: "))
    points = int(input("Enter number of points: "))
    map = MapGenerator(mapWidth, mapHeight, points).generateMap()
    print(map)