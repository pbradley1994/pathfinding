# /usr/bin/env python2.7

import pygame, sys
from pygame import *
import colorDict, Algorithms, UserInterface

TILESIZE = 32
FPS = 120
NUM_TILES_X = 20
NUM_TILES_Y = 12
UI_HEIGHT = 96
WINWIDTH = NUM_TILES_X*TILESIZE
WINHEIGHT = NUM_TILES_Y*TILESIZE + UI_HEIGHT
DRAW_ARROWS = True
DRAW_PATH = True
DRAW_NUMBERS = True
# Setup
pygame.init()
BASICFONT = pygame.font.Font('KhmerUI.ttf', 20)
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

IMAGESDICT = UserInterface.get_images()
dithered_surf = UserInterface.create_dithered_surf(TILESIZE, TILESIZE, 'dark_gray')

class Node(object):
    def __init__(self, x, y, cost=1, reachable=True):
        self.x = x
        self.y = y
        self.cost = cost
        self.status = "Unexplored"

        self.state = "Open"

    def cycle_state(self):
        if self.state == 'Open':
            self.state = 'Difficult'
            self.cost = 5
        elif self.state == 'Difficult':
            self.state = 'Wall'
            self.cost = 0
        elif self.state == 'Wall':
            self.state = 'Open'
            self.cost = 1

class Graph(object):
    def __init__(self):
        self.nodes = {}
        for x in range(NUM_TILES_X):
            for y in range(NUM_TILES_Y):
                self.nodes[(x, y)] = Node(x, y)

        self.start_node = self.nodes[(2, 5)]
        self.goal_node = self.nodes[(17, 5)]

        self.change_algorithm('Breadth First Search')

    def change_algorithm(self, new_algorithm_name):
        self.current_algorithm = new_algorithm_name
        self.algorithm = Algorithms.algorithm_dict[new_algorithm_name](self.start_node, self.goal_node)
        self.reset()

    def update(self, gameStateObj):
        if gameStateObj['current_algorithm'] != self.current_algorithm:
            self.change_algorithm(gameStateObj['current_algorithm'])
        if self.update_flag:
            self.update_flag = self.algorithm.update(self)

    def draw(self, surf, gameStateObj):
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
            if not node.cost:
                pygame.draw.rect(surf, colorDict.colorDict['dark_gray'], imageRect)
            # If cost is greater than one, fill with dithered surf
            if node.cost > 1:
                surf.blit(dithered_surf, imageRect)

            # Draw outline
            pygame.draw.rect(surf, colorDict.colorDict['light_gray'], imageRect, 1)

        if gameStateObj['draw_arrows'] and self.algorithm.came_from:
            arrow = IMAGESDICT['arrow']
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

        if gameStateObj['draw_numbers'] and self.algorithm.cost_so_far:
            for node, value in self.algorithm.cost_so_far.iteritems():
                value_surf = BASICFONT.render(str(value), True, colorDict.colorDict['black'])
                value_rect = value_surf.get_rect()
                value_rect.center = (node.x * TILESIZE + TILESIZE/2, node.y * TILESIZE + TILESIZE/2)
                surf.blit(value_surf, value_rect)

    def get_neighbors(self, node):
        adj_positions = {(node.x, node.y - 1), (node.x, node.y + 1), (node.x - 1, node.y), (node.x + 1, node.y)}
        neighbors = set()
        for adj_position in adj_positions:
            if adj_position in self.nodes and self.nodes[adj_position].cost:
                neighbors.add(self.nodes[adj_position])
        return neighbors

    def reset(self):
        for pos, node in self.nodes.iteritems():
            node.status = "Unexplored"
        self.algorithm.reset()
        self.update_flag = False

    def start(self):
        self.update_flag = True

    def get_node_at_pos(self, pos):
        pos_x = pos[0]/TILESIZE
        pos_y = pos[1]/TILESIZE

        if (pos_x, pos_y) in self.nodes:
            return self.nodes[(pos_x, pos_y)]
        else:
            return None

    def take_input(self, eventList):
        for event in eventList:
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    self.reset()
                    self.start()

                elif event.key == K_1:
                    self.change_algorithm("Breadth First Search")
                elif event.key == K_2:
                    self.change_algorithm("Dijkstra's Algorithm")
                elif event.key == K_3:
                    self.change_algorithm("Greedy Best-First Search")
                elif event.key == K_4:
                    self.change_algorithm("A* Algorithm")

            elif event.type == MOUSEBUTTONUP:
                if event.pos[1] <= WINHEIGHT - UI_HEIGHT:
                    node_under_cursor = self.get_node_at_pos(event.pos)
                    if node_under_cursor is not self.goal_node or self.start_node:
                        node_under_cursor.cycle_state()
                        self.reset()

# === MAIN ===================================================================
def main():
    # Initial Setup
    gameStateObj = {'draw_arrows': False,
                    'draw_numbers': False,
                    'current_algorithm': 'Breadth First Search',
                    'lock_to_ui': False}
    my_graph = Graph()
    main_ui = UserInterface.MainUI(WINWIDTH, UI_HEIGHT, [name for name in Algorithms.algorithm_dict], (0, NUM_TILES_Y*TILESIZE), BASICFONT)

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

        # Take Input
        if not gameStateObj['lock_to_ui']:
            my_graph.take_input(eventList)
        gameStateObj['lock_to_ui'] = main_ui.take_input(eventList)

        # Update
        main_ui.update(gameStateObj)
        my_graph.update(gameStateObj)
        # Draw 
        my_graph.draw(DISPLAYSURF, gameStateObj)
        main_ui.draw(DISPLAYSURF, IMAGESDICT)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

# === TERMINATE ==============================================================
def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()