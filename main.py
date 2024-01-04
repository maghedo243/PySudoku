import time

import pygame
import pygame.gfxdraw
from pygame import Window

from boardUtils import Board

# while True:
#     size = input("Enter size 1(4x4), 2(9x9), 3 (16x16): ")
#     if size.isnumeric() and int(size) in range(1,4): break
#     print("Invalid Size")


pygame.init()

size = "3"

match size:
    case "1":
        size = 4
    case "2":
        size = 9
    case "3":
        size = 16

obj = Board(size)
obj.sections[(0,0)].cells[(0,0)].storedNum = 1
obj.sections[(0,0)].cells[(0,1)].storedNum = 2
obj.sections[(0,0)].cells[(1,0)].storedNum = 16
obj.sections[(0,0)].cells[(1,1)].storedNum = 1
obj.sections[(0,0)].cells[(2,2)].storedNum = 10
obj.sections[(1,2)].cells[(3,2)].storedNum = 3
obj.sections[(1,1)].cells[(3,2)].storedNum = 3
obj.sections[(0,1)].cells[(3,2)].storedNum = 3
obj.sections[(0,1)].cells[(1,1)].storedNum = 3

mainWindow = Window("Sudoku",(500,625))
screen = mainWindow.get_surface()

mainWindow.resizable = True
mainWindow.minimum_size = (400,500)
print(mainWindow.minimum_size)

clock = pygame.time.Clock()
running = True
dt = 0

while running:
    screen.fill("white")

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    obj.setSize(screen)
    obj.drawBoard(screen)

    mainWindow.flip()
    #time.sleep(2)
    #time.sleep(10)

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()