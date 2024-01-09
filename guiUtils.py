from abc import ABC, abstractmethod

import pygame
from pygame import FRect, Surface


class Draggable:
    def __init__(self):
        self.beingDragged = False
        self.mousePos = None
        self.x = 0
        self.y = 0
        self.normalX = 0
        self.normalY = 0
        self.centerX = 0
        self.centerY = 0

    def process_events(self,events):

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.beingDragged = True
                print("DOWN")

            elif event.type == pygame.MOUSEBUTTONUP:
                self.beingDragged = False
                self.x = self.normalX
                self.y = self.normalY
                print(self.x)
                print("UP")

            elif event.type == pygame.MOUSEMOTION and self.beingDragged:
                self.x = event.pos[0]
                self.y = event.pos[1]
                print("E")





class DraggableNumber(Draggable):
    def __init__(self,num):
        super().__init__()
        self.num = num
        self.size = None
        self.rect = FRect(0,0,10,10)
        self.font = pygame.font.SysFont("Impact", 36)

    def process_events(self,events):
        super().process_events(events)

    def setSize(self,x,y,width,height):
        self.normalX = x
        self.normalY = y
        self.rect.update(self.x,self.y,width,height)

        self.font.set_point_size(250)
        while self.font.get_height() > int(self.rect.height - (self.rect.height * 0.1)):
            self.font.point_size -= 1

        self.centerX = (self.rect.width - self.font.size(str(self.num))[0]) / 2
        self.centerY = (self.rect.width - self.font.size(str(self.num))[1]) / 2


    def draw(self,screen):
        x = self.rect.x - self.centerX if self.beingDragged else self.rect.x + self.centerX
        y = self.rect.y - self.centerY if self.beingDragged else self.rect.y + self.centerY
        screen.blit(self.font.render(str(self.num),True,"black"),(x,y))

class SudokuNumbers:
    def __init__(self,numSize):
        self.numMax = numSize
        self.rect = FRect(0,0,0,0)
        self.numbers = [DraggableNumber(x) for x in range(1,numSize+1)]

    def process_events(self,events):
        for x in self.numbers:
            x.process_events(events)

    def setSize(self,boardRect: FRect,surface: Surface):
        x = ((surface.get_width() - boardRect.width) / 2) + boardRect.width*0.025
        y = boardRect.y + boardRect.height + surface.get_height()*0.025
        width = boardRect.width*0.95
        height = (surface.get_height() - y)*0.75
        self.rect.update(x,y,width,height)

        match self.numMax:
            case 4:
                numWidth = self.rect.width / 4
                for i in range(4):
                    self.numbers[i].setSize(self.rect.x + (i*numWidth),self.rect.y,numWidth,self.rect.height)


    def drawNumbers(self,surface: Surface):
        pygame.draw.rect(surface,"black",self.rect,2)
        for x in self.numbers:
            x.draw(surface)

