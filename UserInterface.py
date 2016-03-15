import pygame
from pygame import *
import colorDict, os

def get_images():
    nameList = [image[:-4] for image in os.listdir('./Sprites/') if image.endswith('.png')]
    imageList = [pygame.image.load('./Sprites/' + image) for image in os.listdir('./Sprites/') if image.endswith('.png')]
    return dict(zip(nameList, imageList))

def create_dithered_surf(x_size, y_size, color):
    back_surf = pygame.Surface((x_size, y_size), pygame.SRCALPHA, 32).convert_alpha()

    for x in range(x_size):
        for y in range(y_size):
            if ((x + y)/2)%2 == 0:
                back_surf.set_at((x, y), colorDict.colorDict[color])

    return back_surf

class MainUI(object):
    def __init__(self, x_size, y_size, options, position, font):
        self.position = position
        self.algorithm_menu = PopOutMenu(options, (position[0] + x_size/2, position[1] + 8), font)
        self.arrow_check_box = CheckBox('Draw Arrows', (position[0] + 8, position[1] + 8), font)
        self.cost_check_box = CheckBox('Draw Cost', (position[0] + 8, position[1] + 40), font)
        self.background = pygame.Surface((x_size, y_size))
        self.background.fill(colorDict.colorDict['maroon'])

    def take_input(self, eventList):
        lock_to_ui = self.algorithm_menu.take_input(eventList)
        self.arrow_check_box.take_input(eventList)
        self.cost_check_box.take_input(eventList)
        return lock_to_ui

    def update(self, gameStateObj):
        gameStateObj['current_algorithm'] = self.algorithm_menu.update()
        gameStateObj['draw_arrows'] = self.arrow_check_box.update()
        gameStateObj['draw_numbers'] = self.cost_check_box.update()

    def draw(self, surf, IMAGESDICT):
        surf.blit(self.background, self.position)
        self.algorithm_menu.draw(surf, IMAGESDICT)
        self.arrow_check_box.draw(surf, IMAGESDICT)
        self.cost_check_box.draw(surf, IMAGESDICT)

class CheckBox(object):
    def __init__(self, label, position, font):
        self.label = label
        self.position = position
        self.font = font
        self.size = (17, 17)
        self.checked = False

    def take_input(self, eventList):
        for event in eventList:
            if event.type == MOUSEBUTTONUP:
                input_x = event.pos[0]
                input_y = event.pos[1]

                if input_x >= self.position[0] - 4 and input_x <= self.position[0] + self.size[0] + 112 and \
                    input_y >= self.position[1] - 4 and input_y <= self.position[1] + self.size[1] + 4:
                    self.checked = not self.checked

    def update(self):
        return self.checked
        
    def draw(self, surf, IMAGESDICT):
        if self.checked:
            surf.blit(IMAGESDICT['CheckboxFilled'], (self.position[0], self.position[1] + 4))
        else:
            surf.blit(IMAGESDICT['CheckboxOpen'], (self.position[0], self.position[1] + 4))
        font_position = self.position[0] + self.size[0] + 4, self.position[1]
        surf.blit(self.font.render(self.label, True, colorDict.colorDict['white']), font_position)

class PopOutMenu(object):
    def __init__(self, options, position, font):
        self.options = options
        self.selection = 0
        self.position = position
        self.font = font
        self.size = self.getSize()

        self.state = "closed"

    def getSize(self):
        long_option = max(self.font.size(option)[0] for option in self.options)
        offset = long_option%8
        return (long_option + 16 - offset + 32, 32)

    def take_input(self, eventList):
        for event in eventList:
            if self.state == "closed":
                if event.type == MOUSEBUTTONUP:
                    input_x = event.pos[0]
                    input_y = event.pos[1]

                    if input_x >= self.position[0] and input_x <= self.position[0] + self.size[0] and \
                       input_y >= self.position[1] and input_y <= self.position[1] + self.size[1]:
                        self.state = "open"

            elif self.state == "open":
                if event.type == MOUSEBUTTONUP:
                    input_x = event.pos[0]
                    input_y = event.pos[1]

                    if input_x >= self.position[0] and input_x <= self.position[0] + self.size[0] and \
                        input_y >= self.position[1] - 32 * len(self.options) and input_y <= self.position[1]:
                        self.selection = -(input_y - self.position[1])/32
                    # No matter what, close the selector on click
                    self.state = "closed"

        if self.state == "open":
            return True
        return False

    def update(self):
        return self.options[self.selection]

    def draw(self, surf, IMAGESDICT):
        surf.blit(IMAGESDICT['DropDownLeft'], self.position)
        for x in range(1, (self.size[0] - 32)/8):
            surf.blit(IMAGESDICT['DropDownMid'], (self.position[0] + x*8, self.position[1]))
        surf.blit(IMAGESDICT['DropDownRight'], (self.position[0] + self.size[0] - 32, self.position[1]))

        font_position = self.position[0] + 8, self.position[1] + 4
        surf.blit(self.font.render(self.options[self.selection], True, colorDict.colorDict['white']), font_position)

        if self.state == 'open':
            for index, option in enumerate(self.options):
                y_position = self.position[1] - 32*(index+1)

                if index >= len(self.options) - 1:
                    surf.blit(IMAGESDICT['OpenTopLeft'], (self.position[0], y_position))
                    for x in range(1, (self.size[0] - 8)/8):
                        surf.blit(IMAGESDICT['OpenTop'], (self.position[0] + x*8, y_position))
                    surf.blit(pygame.transform.flip(IMAGESDICT['OpenTopLeft'], 1, 0), (self.position[0] + self.size[0] - 8, y_position))
                
                else:
                    surf.blit(IMAGESDICT['OpenLeft'], (self.position[0], y_position))
                    for x in range(1, (self.size[0] - 8)/8):
                        surf.blit(IMAGESDICT['OpenMid'], (self.position[0] + x*8, y_position))
                    surf.blit(pygame.transform.flip(IMAGESDICT['OpenLeft'], 1, 0), (self.position[0] + self.size[0] - 8, y_position))
                
                font_position = self.position[0] + 8, y_position + 4
                surf.blit(self.font.render(self.options[index], True, colorDict.colorDict['white']), font_position)