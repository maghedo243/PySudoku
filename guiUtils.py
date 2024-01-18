import pygame
from pygame import FRect, Surface

import constants


class Draggable:
    def __init__(self):
        self.beingDragged = False
        self.recentlyActive = (False,None,None)
        self.mousePos = None
        self.x = 0
        self.y = 0
        self.normalX = 0
        self.normalY = 0
        self.centerX = 0
        self.centerY = 0

    def process_events(self,events,rect):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and rect.collidepoint(event.pos[0],event.pos[1]):
                self.beingDragged = True
                self.x = event.pos[0]
                self.y = event.pos[1]

            elif event.type == pygame.MOUSEBUTTONUP and self.beingDragged:
                self.beingDragged = False
                self.x = self.normalX
                self.y = self.normalY
                self.recentlyActive = (True,event.pos[0],event.pos[1])

            elif event.type == pygame.MOUSEMOTION and self.beingDragged:
                self.x = event.pos[0]
                self.y = event.pos[1]





class DraggableNumber(Draggable):
    def __init__(self,num):
        super().__init__()
        self.num = num
        self.size = None
        self.rect = FRect(0,0,10,10)
        self.font = pygame.font.SysFont("Impact", 36)

    def process_events(self,events):
        super().process_events(events,self.rect)
        if self.recentlyActive[0]:
            pygame.event.post(pygame.event.Event(constants.NUMDROP, {"pos": (self.recentlyActive[1],self.recentlyActive[2]), "num": self.num},pos=(self.recentlyActive[1],self.recentlyActive[2]),num=self.num))
            self.recentlyActive = (False,None,None)


    def setSize(self,x,y,width,height):
        self.normalX = x
        self.normalY = y
        self.rect.update(self.normalX,self.normalY,width,height)

        self.font.set_point_size(250)
        while self.font.get_height() > int(self.rect.height - (self.rect.height * 0.1)):
            self.font.point_size -= 1

        self.centerX = (self.rect.width - self.font.size(str(self.num))[0]) / 2
        self.centerY = (self.rect.height - self.font.size(str(self.num))[1]) / 2


    def draw(self,screen):
        x = self.x - (self.font.size(str(self.num))[0] / 2) if self.beingDragged else self.rect.x + self.centerX
        y = self.y - (self.font.size(str(self.num))[1] / 2) if self.beingDragged else self.rect.y + self.centerY
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
        height = min((surface.get_height() - y)*0.75,surface.get_height()*0.2)
        self.rect.update(x,y,width,height)

        match self.numMax:
            case 4:
                numWidth = self.rect.width / 4
                for i in range(4):
                    self.numbers[i].setSize(self.rect.x + (i*numWidth),self.rect.y,numWidth,self.rect.height)
            case 9:
                topRowWidth = self.rect.width / 5
                bottomRowWidth = self.rect.width / 4
                for i in range(5):
                    self.numbers[i].setSize(self.rect.x + (i*topRowWidth),self.rect.y,topRowWidth,self.rect.height/2)

                for i in range(4):
                    self.numbers[i+5].setSize(self.rect.x + (i*bottomRowWidth),self.rect.y+(self.rect.height/2),bottomRowWidth,self.rect.height/2)
            case 16:
                numWidth = self.rect.width / 8
                for i in range(8):
                    self.numbers[i].setSize(self.rect.x + (i*numWidth),self.rect.y,numWidth,self.rect.height/2)

                for i in range(8):
                    self.numbers[i+8].setSize(self.rect.x + (i*numWidth),self.rect.y+(self.rect.height/2),numWidth,self.rect.height/2)




    def drawNumbers(self,surface: Surface):
        pygame.draw.rect(surface,"black",self.rect,2)
        for x in self.numbers:
            x.draw(surface)

