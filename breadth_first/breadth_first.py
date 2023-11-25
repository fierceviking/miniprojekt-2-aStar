class breadthFirst:
    def __init__(self, map, start, end):
        self.map = map
        self.start = start
        self.end = end
        self.path = []
        self.queue = []
        self.visited = []
        self.prev = {}
        self.found = False
    
    def findPath(self):
        self.queue.append(self.start)
        self.visited.append(self.start)
        while len(self.queue) > 0:
            current = self.queue.pop(0)
            if current == self.end:
                self.found = True
                break
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= current[0] + dx < len(self.map) and 0 <= current[1] + dy < len(self.map[0]):
                        if [current[0] + dx, current[1] + dy] not in self.visited and self.map[current[0] + dx][current[1] + dy] != 255:
                            self.queue.append([current[0] + dx, current[1] + dy])
                            self.visited.append([current[0] + dx, current[1] + dy])
                            self.prev[str([current[0] + dx, current[1] + dy])] = current
        if self.found:
            self.path.append(self.end)
            while self.path[-1] != self.start:
                self.path.append(self.prev[str(self.path[-1])])
            self.path.reverse()
            print(self.path)
            return self.path
        else:
            return None