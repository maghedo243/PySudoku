import math

import pygame
from pygame import FRect, Surface

import constants


class Board:
    def __init__(self,size):
        self.size = size
        self.sections = dict()
        self.rect = FRect(0,0,0,0)
        self.sqrt = int(math.sqrt(size))
        for i in range(self.sqrt):
            for j in range(self.sqrt):
                self.sections[(i,j)] = Section(size,(i,j),self)

    def process_events(self,events):
        for event in events:
            if event.type == constants.NUMDROP:
                for section in self.sections.values():
                    for cell in section.cells.values():
                        if cell.rect.collidepoint(event.pos[0],event.pos[1]):
                            cell.storedNum = event.num


    def setSize(self,surface: Surface):
        width, height = surface.get_size()
        height -= height*0.1
        if width < height:
            fivePer = width * 0.05
            square = int(width - (fivePer*2)) #making square perfectly divisible
            while square % self.size != 0:
                square -= 1
            x = (width - square) / 2
            self.rect.update(x,10,square,square)
        elif height < width:
            fivePer = height * 0.05
            square = int(height - (fivePer*2)) #making square perfectly divisible
            while square % self.size != 0:
                square -= 1
            x = (width - square)/2
            self.rect.update(x,10,square,square)

        for x in self.sections.values():
            x.setSize()

    def boardDupeCheck(self, num: int, cellCoords, sectionCoords):
        absoluteCoords = self.sectionCoordsToAbsCoords(cellCoords, sectionCoords)

        #vertical line check
        i = self.size-1
        count = 0
        while i > -1:
            cCoords, sCoords = self.absCoordsToSectionCoords((absoluteCoords[0],i))
            if self.sections[sCoords].cells[cCoords].storedNum == num:
                count += 1
            i -= 1

        if count > 1: return True

        #horizontal line check
        i = self.size - 1
        count = 0
        while i > -1:
            cCoords, sCoords = self.absCoordsToSectionCoords((i, absoluteCoords[1]))
            if self.sections[sCoords].cells[cCoords].storedNum == num:
                count += 1
            i -= 1

        if count > 1: return True

    def drawBoard(self, surface: Surface):
        pygame.draw.rect(surface, "black", self.rect,3)
        for x in self.sections.values():
            x.drawSection(surface)

    def sectionCoordsToAbsCoords(self,cellCoords,sectionCoords):
        return (sectionCoords[0] * self.sqrt) + cellCoords[0], (sectionCoords[1] * self.sqrt) + cellCoords[1]

    def absCoordsToSectionCoords(self,absoluteCoords):
        sectionX = absoluteCoords[0] // self.sqrt
        sectionY = absoluteCoords[1] // self.sqrt
        sectionCoords = (sectionX,sectionY)
        cellX = absoluteCoords[0] % self.sqrt
        cellY = absoluteCoords[1] % self.sqrt
        cellCoords = (cellX, cellY)

        return cellCoords, sectionCoords

    def getCells(self):
        return [y for x in self.sections.values() for y in x.cells.values()]

class Section:
    def __init__(self,area,coords,board:Board):
        self.rect = FRect(0,0,0,0)
        self.area = area
        self.len = int(math.sqrt(area))
        self.coords = coords
        self.board = board
        self.cells = dict()
        for i in range(self.len):
            for j in range(self.len):
                self.cells[(i, j)] = Cell((i, j), self)

    def innerDiffCheck(self):
        nums = list()
        for coords,cell in self.cells.items():
            if cell.storedNum not in nums and cell.storedNum != -1:
                nums.append(cell.storedNum)
            elif cell.storedNum in nums:
                return cell.storedNum, False
        return True

    def sectionDupeCheck(self,num: int):
        cellList = list(self.cells.values())
        threshold = 0
        for x in cellList:
            threshold += 1 if x.storedNum == num else 0
            if threshold > 1:
                return True
        return False

    def setSize(self):
        topLeft = (self.board.rect.x,self.board.rect.y)
        interval = self.board.rect.width/math.sqrt(self.area)
        x = topLeft[0] + (interval*self.coords[0])
        y = topLeft[1] + (interval*self.coords[1])
        self.rect.update(x,y,interval,interval)
        for x in self.cells.values():
            x.setSize(self.area)

    def drawSection(self, surface):
        pygame.draw.rect(surface, "black", self.rect, 2)
        for x in self.cells.values():
            x.drawCell(surface)


    def __str__(self):
        return "Coordinates: " + str(self.coords) + ", Area: " + str(self.area) + ", Length: " + str(self.len)




class Cell:
    def __init__(self,coords, section:Section):
        self.assignedNum = -1
        self.storedNum = -1
        self.storedNumText = None
        self.coords = coords
        self.section = section
        self.rect = FRect(0,0,0,0)
        self.numFont = pygame.font.SysFont("Impact",16)

    def setSize(self,area):
        topLeft = (self.section.rect.x, self.section.rect.y)
        interval = self.section.rect.width / math.sqrt(area)
        x = topLeft[0] + (interval * self.coords[0])
        y = topLeft[1] + (interval * self.coords[1])
        self.rect.update(x, y, interval, interval)
        self.numFont.set_point_size(250)
        while self.numFont.get_height() > int(self.rect.height - (self.rect.height*0.1)):
            self.numFont.point_size -= 1



    def drawCell(self, surface: Surface):
        pygame.draw.rect(surface, "black", self.rect, 1)
        if self.storedNum != -1:
            numColor = "red" if self.checkDupes() else "black"
            self.storedNumText = self.numFont.render(str(self.storedNum), True, numColor)
            centerX = (self.rect.width - self.numFont.size(str(self.storedNum))[0]) / 2
            centerY = (self.rect.width - self.numFont.size(str(self.storedNum))[1]) / 2
            surface.blit(self.storedNumText,(self.rect.x + centerX,self.rect.y + centerY))

    def checkDupes(self):
        sectionDupe = self.section.sectionDupeCheck(self.storedNum)
        lineDupe = self.section.board.boardDupeCheck(self.storedNum,self.coords,self.section.coords)
        return sectionDupe or lineDupe


