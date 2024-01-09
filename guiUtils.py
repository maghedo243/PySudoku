from abc import ABC, abstractmethod

import pygame


class Draggable(ABC):
    def __init__(self):
        self.beingDragged = False
        self.mousePos = None
        self.x = None
        self.y = None
        self.normalX = None
        self.normalY = None

    def process_events(self,events):
        for event in events:
            if event == pygame.MOUSEBUTTONDOWN:
                self.beingDragged = True
                self.x = event.pos.x
                self.y = event.pos.y

            if event == pygame.MOUSEBUTTONUP:
                self.beingDragged = False
                self.x = self.normalX
                self.y = self.normalY

    @abstractmethod
    def dragMovement(self):
        pass

class DraggableNumber(Draggable):
    def __init__(self,num):
        super().__init__()
        self.num = num
        self.size = None

    def dragMovement(self):
        pass