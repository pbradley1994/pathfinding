# /usr/bin/env python2.7

import pygame, sys
from pygame import *
import colorDict
import Algorithms

TILESIZE = 32
FPS = 120
NUM_TILES_X = 15
NUM_TILES_Y = 10
WINWIDTH = NUM_TILES_X*TILESIZE
WINHEIGHT = NUM_TILES_Y*TILESIZE
# Setup
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

class Node(object):
    def __init__(self, x, y, cost=1):
        self.x = x
        self.y = y
        self.cost = cost
        self.status = "Unexplored"

class Graph(object):
    def __init__(self):
        self.nodes = {}
        for x in range(NUM_TILES_X):
            for y in range(NUM_TILES_Y):
                self.nodes[(x, y)] = Node(x, y)

        self.start_pos = (1, 4)
        self.goal_pos = (14, 4)

        self.algorithm = Algorithms.BreadthFirstSearch1(self.nodes[self.start_pos]) 

    def update(self):
        self.algorithm.update(self)

    def draw(self, surf):
        surf.fill(colorDict.colorDict['white'])
        for position, node in self.nodes.iteritems():
            imageRect = pygame.Rect(node.x*TILESIZE, node.y*TILESIZE, 32, 32)

            # If in visited, fill with light green
            if node.status == 'Visited':
                pygame.draw.rect(surf, colorDict.colorDict['green_white'], imageRect)
            # If in frontier, fill with light blue
            if node.status == 'Frontier':
                pygame.draw.rect(surf, colorDict.colorDict['light_blue'], imageRect)
            # If start, fill with green
            if position == self.start_pos:
                pygame.draw.rect(surf, colorDict.colorDict['dark_green'], imageRect)
            # If goal, fill with red
            if position == self.goal_pos:
                pygame.draw.rect(surf, colorDict.colorDict['red'], imageRect)

            # Draw outline
            pygame.draw.rect(surf, colorDict.colorDict['light_gray'], imageRect, 1)

    def get_neighbors(self, node):
        adj_positions = {(node.x, node.y - 1), (node.x, node.y + 1), (node.x - 1, node.y), (node.x + 1, node.y)}
        neighbors = set()
        for adj_position in adj_positions:
            if adj_position in self.nodes:
                neighbors.add(self.nodes[adj_position])
        return neighbors

# === MAIN ===================================================================
def main():
    # Initial Setup
    my_graph = Graph()

    # Main game loop
    while(True):
        # Take input
        eventList = [] # Clear event list
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
            eventList.append(event)
        # Update
        my_graph.update()
        # Draw 
        my_graph.draw(DISPLAYSURF)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# === TERMINATE ==============================================================
def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()