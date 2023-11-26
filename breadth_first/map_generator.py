import numpy as np
import random

class MapGenerator:
    # first we need a constructor for the map generator class
    def __init__(self, mapwidth, mapheight, points):
        # these are the map width, map height, and number of points
        self.mapwidth = mapwidth
        self.mapheight = mapheight
        self.points = points
        self.map = np.zeros((mapwidth, mapheight), dtype=np.uint8)

    # the generateMap function is the function that will generate the map
    def generateMap(self):
        # first we initialize the map as a 2D array of 0s
        self.map = np.zeros((self.mapwidth, self.mapheight), dtype=np.uint8)
        # then we loop through the number of points
        for _ in range(self.points):
            # here we set a random point in the map to 255
            x = random.randint(0, self.mapwidth - 1)
            y = random.randint(0, self.mapheight - 1)
            self.map[x][y] = 255
            # then we allow the point to spread to its neighbors in a 5x5 grid
            for dx in [-2, -1, 0, 1, 2]:
                for dy in [-2, -1, 0, 1, 2]:
                    # and check if the neighbor is in the map
                    if 0 <= x + dx < self.mapwidth and 0 <= y + dy < self.mapheight:
                        # and if it is, we set it to 255 with a 50% chance
                        if random.random() < 0.5:
                            self.map[x + dx][y + dy] = 255
        # here we save the map to a text file (mostly for testing purposes)
        np.savetxt('breadth_first/map.txt', self.map, fmt='%d')
        # and return the map
        return self.map
        
# here the map generator can be run as a standalone program for testing purposes
if __name__ == '__main__':
    mapWidth = int(input("Enter map width: "))
    mapHeight = int(input("Enter map height: "))
    points = int(input("Enter number of points: "))
    map = MapGenerator(mapWidth, mapHeight, points).generateMap()
    print(map)