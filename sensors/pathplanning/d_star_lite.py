import numpy as np
import heapq

class DStarLite:
    def __init__(self, grid_map, start, goal):
        self.grid_map = grid_map
        self.start = start
        self.goal = goal
        self.k_m = 0
        self.rhs = {}
        self.g = {}
        self.open_set = []
        self.init()

    def init(self):
        for x in range(self.grid_map.shape[0]):
            for y in range(self.grid_map.shape[1]):
                self.rhs[(x, y)] = float('inf')
                self.g[(x, y)] = float('inf')
        self.rhs[self.goal] = 0
        self.update_key(self.start)

    def update_key(self, state):
        g_val = self.g[state]
        rhs_val = self.rhs[state]
        key = (min(g_val, rhs_val) + self.k_m, min(g_val, rhs_val))
        heapq.heappush(self.open_set, (key, state))

    def compute_shortest_path(self):
        while self.open_set:
            key, state = heapq.heappop(self.open_set)
            if self.g[state] > self.rhs[state]:
                self.g[state] = self.rhs[state]
                for neighbor in self.get_neighbors(state):
                    self.update_rhs(neighbor)
            elif self.g[state] < self.rhs[state]:
                self.g[state] = float('inf')
                self.update_rhs(state)

    def update_rhs(self, state):
        min_rhs = min([self.g[neighbor] + 1 for neighbor in self.get_neighbors(state)])
        self.rhs[state] = min_rhs
        self.update_key(state)

    def get_neighbors(self, state):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (state[0] + dx, state[1] + dy)
            if self.is_valid(neighbor):
                neighbors.append(neighbor)
        return neighbors

    def is_valid(self, state):
        x, y = state
        return 0 <= x < self.grid_map.shape[0] and 0 <= y < self.grid_map.shape[1] and self.grid_map[x, y] == 0

    def plan(self):
        self.compute_shortest_path()
        path = []
        state = self.start
        while state != self.goal:
            path.append(state)
            neighbors = self.get_neighbors(state)
            state = min(neighbors, key=lambda s: self.g[s] + 1)
        path.append(self.goal)
        return path
