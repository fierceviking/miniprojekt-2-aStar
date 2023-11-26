import math

class breadthFirst:
    # first we need a constructor for the breadth first class
    def __init__(self, map, start, end):
        # the map is a 2D array of 0s and 255s which represent the walkable and unwalkable areas respectively
        self.map = map
        # the start is the starting node the algorithm will start from
        self.start = start
        # and the end is the end node the algorithm will try to reach
        self.end = end
        # the path is the final path the algorithm will find
        self.path = []
        # the queue is the queue of nodes the algorithm will visit
        self.queue = []
        # the visited list is the list of nodes the algorithm has already visited
        self.visited = []
        # the prev dictionary is the dictionary of nodes and their previous nodes
        self.prev = {}
        # the found boolean is whether or not the algorithm has found the end node
        self.found = False
    
    # the heuristic function is to optimize the algorithm to find the end node faster 
    # by prioritizing nodes closer to the end node
    def heuristic(self, node):
        # here we return a simple distance from the node to the end node
        return abs(node[0] - self.end[0]) + abs(node[1] - self.end[1])
    
    # the findPath function is the function that will find the path from the start node to the end node 
    # and contains the bulk of the algorithm
    def findPath(self):
        # first we add the start node to the queue and the visited list
        self.queue.append(self.start)
        self.visited.append(self.start)
        
        # then we loop through the queue until it is empty
        while len(self.queue) > 0:
            # here we sort the queue by the heuristic function 
            # i.e. the distance from the node to the end node
            self.queue.sort(key=lambda node: self.heuristic(node))

            # then we pop the first node from the queue
            current = self.queue.pop(0)
            
            # if the current node is the end node, we break out of the loop
            if current == self.end:
                self.found = True
                break
            
            # otherwise we loop through the neighbors of the current node in a 3x3 grid
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    # we check if the neighbor is in the map and is not in the visited list and is not an unwalkable node
                    neighbor = [current[0] + dx, current[1] + dy]
                    if 0 <= neighbor[0] < len(self.map) and 0 <= neighbor[1] < len(self.map[0]):
                        if neighbor not in self.visited and self.map[neighbor[0]][neighbor[1]] != 255:
                            # if it is, we add it to the queue and the visited list and set its previous node to the current node
                            self.queue.append(neighbor)
                            self.visited.append(neighbor)
                            self.prev[str(neighbor)] = current
        
        # here we check if the algorithm has found the end node
        if self.found:
            # if it has, we loop through the previous nodes from the end node to the start node and add them to the path
            self.path.append(self.end)
            # we loop until the current node is the start node
            while self.path[-1] != self.start:
                self.path.append(self.prev[str(self.path[-1])])
            # here we reverse the path because we added the nodes from the end node to the start node
            # but we want the path from the start node to the end node
            self.path.reverse()
            # here we remove the start and end nodes from the path because we don't want to draw them
            self.path.pop(0)
            self.path.pop(-1)
            # here we print the path
            print(self.path)
            # and return the path
            return self.path
        else:
            # if the algorithm has not found the end node, we print that there is no path
            return None