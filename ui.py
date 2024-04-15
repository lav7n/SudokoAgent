import pygame
from sudoko import *
from level import *
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
L_GREEN = (150, 255, 150)
RED = (255, 0, 0)
L_RED = (255, 204, 203)
GRAY = (60, 60, 60)
L_GRAY = (220, 220, 220)
YELLOW = (255, 255, 0)

# Set the width and height of each grid location
WIDTH = HEIGHT = 50

# Set the margin between each cell
MARGIN = 5

# Set the width and height of the screen
size = (500, 500)

# Initialize pygame
pygame.init()

# Set the font for text
font = pygame.font.Font('freesansbold.ttf', 32)

# Flag to control the main loop
done = False

# Function to cheat and fill in the whole board with solution
def cheatingAllTheWay(sol):
    for row in range(len(Board)):
        for column in range(len(Board[row])):
            if Board[row][column] == 0:
                Board[row][column] = sol[row][column]
                addNumToBoard(Board[row][column], row, column, L_GREEN)
                time.sleep(0.05)
                pygame.display.flip()
    finish(sol)

# Function to add a number to the board
def addNumToBoard(number, row, column, color):
    addNewRect(row, column, WHITE, 5)
    addNewRect(row, column, color, None)
    text = font.render(str(number), True, BLACK)
    textRect = text.get_rect()
    textRect.center = ((MARGIN + WIDTH) * column + MARGIN + WIDTH / 2, (MARGIN + HEIGHT) * row + MARGIN + WIDTH / 2)
    screen.blit(text, textRect)
    drawTheBorder()

# Function to check if the board is solved correctly
def finish(sol):
    if sol == Board:
        print("Good")
    else:
        print("Not good")

# Function to draw the border of the grid
def drawTheBorder():
    dif = 500 // 9
    for i in range(10):
        thick = 5
        pygame.draw.line(screen, GRAY, (0, i * dif + 2), (500, i * dif + 2), thick)
        pygame.draw.line(screen, GRAY, (i * dif + 2, 0), (i * dif + 2, 500), thick)
    for i in range(10):
        if i % 3 == 0:
            thick = 8
            pygame.draw.line(screen, BLACK, (0, i * dif), (500, i * dif), thick)
            pygame.draw.line(screen, BLACK, (i * dif, 0), (i * dif, 500), thick)

# Function to draw the initial board
def drawInitBoard():
    for row in range(len(Board)):
        for column in range(len(Board[row])):
            color = L_GRAY
            if Board[row][column] == 0:
                color = WHITE
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
            text = font.render(str(Board[row][column]) if Board[row][column] != 0 else "", True, BLACK)
            textRect = text.get_rect()
            textRect.center = ((MARGIN + WIDTH) * column + MARGIN + WIDTH / 2, (MARGIN + HEIGHT) * row + MARGIN + WIDTH / 2)
            screen.blit(text, textRect)
            drawTheBorder()

# Main program loop
if __name__ == "__main__":
    flag1 = True
    while flag1:
        level = chooseLevel()
        if level in [1, 2, 3]:
            print(level)
            flag1 = False
    pygame.display.set_caption("Sudoku King")
    screen = pygame.display.set_mode(size)

    sol = mainSolver(level)

    print("Solved Board:")
    printBoard(sol)

    pygame.init()
    screen.fill(BLACK)
    drawInitBoard()
    readyForInput = False
    key = None

    # Main event loop
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in numbers_1to9:
                    key = chr(event.key)
                if event.key == pygame.K_RETURN:
                    finish(sol)
                if event.key == pygame.K_c:
                    cheatingAllTheWay(sol)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if readyForInput is True:
                    addNewRect(row, column, WHITE, None)
                    drawTheBorder()
                    readyForInput = False

                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (WIDTH + MARGIN)
                if Board[row][column] == 0:
                    addNewRect(row, column, YELLOW, 5)
                    readyForInput = True

        if readyForInput and key is not None:
            if int(key) == sol[row][column]:
                Board[row][column] = key
                flickering(0.1, GREEN)
                addNumToBoard(key, row, column, L_GREEN)
            else:
                flickering(0.1, RED)
                addNumToBoard(key, row, column, L_RED)

            drawTheBorder()
            readyForInput = False

        key = None
        pygame.display.flip()
        pygame.display.update()

# Close the window and quit.
pygame.quit()
