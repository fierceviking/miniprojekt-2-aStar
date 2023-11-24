import pygame
import numpy as np
from queue import PriorityQueue
import random

mapWidth = int(input("Enter map width: "))
mapHeight = int(input("Enter map height: "))
running = True

screen = pygame.display.set_mode((mapWidth * 10, mapHeight * 10))

map = np.zeros((mapWidth, mapHeight, 3), dtype=np.uint8)
print(map)
