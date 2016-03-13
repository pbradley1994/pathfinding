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
DRAW_ARROWS = True
DRAW_PATH = True
arrow = pygame.image.load('arrow.png')
# Setup
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

class Node(object):
    def __init__(self, x, y, cost=1, reachable=True):
        self.x = x
        self.y = y
        self.cost = cost
        self.reachable = True
        self.status = "Unexplored"

class Graph(object):
    def __init__(self):
        self.nodes = {}
        for x in range(NUM_TILES_X):
            for y in range(NUM_TILES_Y):
                self.nodes[(x, y)] = Node(x, y)

        self.start_node = self.nodes[(1, 4)]
        self.goal_node = self.nodes[(13, 4)]

        self.algorithm = Algorithms.algorithm_dict['Breadth First Search'](self.start_node, self.goal_node)
        self.update_flag = False

    def change_algorithm(self, new_algorithm_name):
        self.algorithm = Algorithms.algorithm_dict[new_algorithm_name](self.start_node, self.goal_node)
        self.reset()

    def update(self):
        if self.update_flag:
            self.update_flag = self.algorithm.update(self)

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
            if node is self.start_node:
                pygame.draw.rect(surf, colorDict.colorDict['dark_green'], imageRect)
            # If goal, fill with red
            if node is self.goal_node:
                pygame.draw.rect(surf, colorDict.colorDict['red'], imageRect)
            # If not reachable, fill with dark_gray:
            if not node.reachable:
                pygame.draw.rect(surf, colorDict.colorDict['dark_gray'], imageRect)

            # Draw outline
            pygame.draw.rect(surf, colorDict.colorDict['light_gray'], imageRect, 1)

        if DRAW_ARROWS and self.algorithm.came_from:
            for child_node, parent_node in self.algorithm.came_from.iteritems():
                if child_node and parent_node:
                    if child_node.x < parent_node.x:
                        surf.blit(arrow, (child_node.x*TILESIZE + TILESIZE/2, child_node.y*TILESIZE + TILESIZE/2 - arrow.get_height()/2))
                    elif child_node.x > parent_node.x:
                        surf.blit(pygame.transform.flip(arrow, 1, 0), (child_node.x*TILESIZE - TILESIZE/4, child_node.y*TILESIZE + TILESIZE/2 - arrow.get_height()/2))
                    elif child_node.y < parent_node.y:
                        surf.blit(pygame.transform.rotate(arrow, -90), (child_node.x*TILESIZE + TILESIZE/2 - arrow.get_height()/2, child_node.y*TILESIZE + TILESIZE/2))
                    else:
                        surf.blit(pygame.transform.rotate(arrow, 90), (child_node.x*TILESIZE + TILESIZE/2 - arrow.get_height()/2, child_node.y*TILESIZE - TILESIZE/4))

        if DRAW_PATH and self.algorithm.came_from and self.goal_node in self.algorithm.came_from:
            current = self.goal_node
            path = [current]
            while current is not self.start_node:
                old_pos = current.x*TILESIZE + TILESIZE/2 - 2, current.y*TILESIZE + TILESIZE/2 - 2
                current = self.algorithm.came_from[current]
                new_pos = current.x*TILESIZE + TILESIZE/2 - 2, current.y*TILESIZE + TILESIZE/2 - 2
                # Draw line
                pygame.draw.line(surf, colorDict.colorDict['dark_purple'], old_pos, new_pos, 4)
                path.append(current)

    def get_neighbors(self, node):
        adj_positions = {(node.x, node.y - 1), (node.x, node.y + 1), (node.x - 1, node.y), (node.x + 1, node.y)}
        neighbors = set()
        for adj_position in adj_positions:
            if adj_position in self.nodes and self.nodes[adj_position].reachable:
                neighbors.add(self.nodes[adj_position])
        return neighbors

    def reset(self):
        for pos, node in self.nodes.iteritems():
            node.status = "Unexplored"
        self.algorithm.reset()

    def start(self):
        self.update_flag = True

    def get_node_at_pos(self, pos):
        pos_x = pos[0]/TILESIZE
        pos_y = pos[1]/TILESIZE

        if (pos_x, pos_y) in self.nodes:
            return self.nodes[(pos_x, pos_y)]
        else:
            return None

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

        for event in eventList:
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    my_graph.reset()
                    my_graph.start()

                elif event.key == K_1:
                    my_graph.change_algorithm("Breadth First Search")
                elif event.key == K_2:
                    my_graph.change_algorithm("Dijkstra's Algorithm")
                elif event.key == K_3:
                    my_graph.change_algorithm("Greedy Best-First Search")

            elif event.type == MOUSEBUTTONUP:
                node_under_cursor = my_graph.get_node_at_pos(pygame.mouse.get_pos())
                node_under_cursor.reachable = not node_under_cursor.reachable
                my_graph.reset()

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