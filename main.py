import time

import pygame
import pygame.gfxdraw
from pygame import Window

import constants
from boardUtils import Board
from guiUtils import DraggableNumber, SudokuNumbers

# while True:
#     size = input("Enter size 1(4x4), 2(9x9), 3 (16x16): ")
#     if size.isnumeric() and int(size) in range(1,4): break
#     print("Invalid Size")


pygame.init()

size = "1"

match size:
    case "1":
        size = 4
    case "2":
        size = 9
    case "3":
        size = 16

obj = Board(size)

mainWindow = Window("Sudoku",(500,625))
screen = mainWindow.get_surface()

mainWindow.resizable = True
mainWindow.minimum_size = (400,500)

clock = pygame.time.Clock()
running = True
dt = 0

nums = SudokuNumbers(size)

while running:
    screen.fill("white")

    events = pygame.event.get()
    nums.process_events(events)
    obj.process_events(events)
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    obj.setSize(screen)
    nums.setSize(obj.rect, screen)
    obj.drawBoard(screen)
    nums.drawNumbers(screen)

    mainWindow.flip()
    #time.sleep(2)
    #time.sleep(10)

    # limits FPS to 60
    clock.tick(60)


pygame.quit()