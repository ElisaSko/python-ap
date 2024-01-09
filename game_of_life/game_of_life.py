#IMPORTS
import argparse
import pygame
import copy
import logging
import sys

#PARSER 
parser = argparse.ArgumentParser(description='game of life')
parser.add_argument('-i', default = 'my_input_file.txt', type=str, help='input file')
parser.add_argument('-o', default= 'my_output_file.txt',type=str, help='output file')
parser.add_argument('--width', default= 800, type=int, help='width of the grid')
parser.add_argument('--height', default= 600, type=int, help='height of the grid')
parser.add_argument('-m', default= 20, type=int, help='number of iterations')
parser.add_argument('--cell_width', default= 10, type=int, help='width of a cell')
parser.add_argument('--cell_height', default= 10, type=int, help='height of a cell')
parser.add_argument('--alive_color', default= '#000000', help='color of a living cell, hexadecimal value')
parser.add_argument('--dead_color', default= '#FFFFFF', help='color of a dead cell, hexadecimal value')
parser.add_argument('--time', default= 5, type=int, help='number of frames per second')
parser.add_argument('-d', help='flag : activate to display', action='store_true')
parser.add_argument('--debug', help='flag : activate to get debug log messages', action='store_true')
args = parser.parse_args()

#LOGGER
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)

#CLASSES
class Cell :
    def __init__(self, x, y, alive):
        self.x = x
        self.y = y
        self.alive = alive
    
    #creates a list of the neighbours of a cell
    def neighbours(self, set_of_cells):
        neighbours=[]
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                if x >= 0 and x < set_of_cells.height and y >= 0 and y < set_of_cells.width and (x != self.x or y != self.y):
                    neighbours.append(set_of_cells.cells[x][y])
        return neighbours

    #counts the number of living neighbours of a cell using neighbours()
    def count_neighbours(self, set_of_cells):
        neighbours = self.neighbours(set_of_cells)
        count = 0
        for cell in neighbours:
            if cell.alive:
                count += 1
        return count
    
    #updates the state of a cell
    def update (self, set_of_cells):
        number = self.count_neighbours(set_of_cells)
        if self.alive:
            if number == 2 or number == 3:
                self.alive = True
            else :
                self.alive = False
        else:
            if number == 3:
                self.alive = True




class Set_Of_Cells  :
    def __init__(self, cells, height=args.height, width=args.width):
        self.cells = cells
        self.height = height
        self.width = width

    def initialize(self, pattern):
        #we check that the pattern is smaller than the grid
        if pattern.height > self.height or pattern.width > self.width:
            logger.error('The pattern is too big for the grid')
            raise ValueError('The pattern is too big for the grid')
        
        #we check that the size of the grid is a strictly positive integer
        if self.height <= 0 or self.width <= 0:
            logger.error('The size of the grid must be strictly positive')
            raise ValueError('The size of the grid must be strictly positive')
        
        if self.height != int(self.height) or self.width != int(self.width):
            logger.error('The size of the grid must be an integer')
            raise ValueError('The size of the grid must be an integer')
        
        #initializes the set of cells with the pattern :
        #adjusts the dimensions by adding dead cells around the pattern
        #the pattern is placed in the top left corner of the grid
        for x in range(self.height):
            line = []
            for y in range(self.width):
                line.append(Cell(x, y, False))
            self.cells.append(line)
        for l in pattern.cells:
            for cell in l:
                self.cells[cell.x][cell.y].alive = cell.alive
   
    #updates the whole set of cells
    def update(self, height, width):
        #create a provisional set of cells
        #to be able to update all the cells at the same time
        set_prov=copy.deepcopy(self)
        for x in range(self.height):
                for y in range(self.width):
                    self.cells[x][y].update(set_prov)
    
    #outputs the final pattern in the file
    #will only be used if the game is not displayed
    def output(self, file_name):
        file = open(file_name, 'w')
        for x in range(self.height):
            for y in range(self.width):
                if self.cells[x][y].alive:
                    file.write('1')
                else:
                    file.write('0')
            file.write('\n')
        file.close()
        logger.debug('Output written in output file')

      
class Pattern :
    def __init__(self, cells, height, width):
        self.cells = cells
        self.height = height
        self.width = width
    
    #loads the initial pattern from the file
    #does not take dimensions into account (initialize() method of Set_Of_Cells does)
    def load(self, file_name):

        file = open(file_name, 'r')
        lines = file.readlines()
        file.close()
        self.height = len(lines)
        self.width = len(lines[0])
        self.cells = []

        for x in range(self.height):
            line = []
            for y in range(self.width):
                if lines[x][y] == '0':
                    line.append(Cell(x, y, False))
                if lines[x][y]=='1':
                    line.append(Cell(x, y, True))
            self.cells.append(line)
        
        logger.debug('Pattern loaded from input file')

class Display :
    def __init__(self, time, height, width, cell_height, cell_width, set_of_cells,
                 alive_color, dead_color):
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.set_of_cells = set_of_cells
        self.height = height
        self.width = width
        self.alive_color = alive_color
        self.dead_color = dead_color
        self.time = time
        self.screen = pygame.display.set_mode((self.width, self.height))
    
    #draws the set of cells on the screen
    #we draw the alive cells and the background is the color of dead cells
    def draw(self, set_of_cells):
        self.screen.fill(self.dead_color)
        for l in set_of_cells.cells:
            for cell in l:
                if cell.alive:
                    rect = pygame.Rect(cell.x*self.cell_height,cell.y*self.cell_width, 
                                       self.cell_height, self.cell_width)
                    pygame.draw.rect(self.screen, self.alive_color, rect)
        pygame.display.update()
    
    #displays the game : updates the set of cells and draws it
    def display(self, set_of_cells):
        pygame.init()
        clock = pygame.time.Clock()

        logger.debug('Start main loop')

        iteration=0
        execute = True
        while execute:
            clock.tick(self.time)
            self.draw(set_of_cells)
            set_of_cells.update(self.height, self.width) 

            iteration+=1
            logger.info('Iteration number %d', iteration)

            #displays the number of iterations
            pygame.display.set_caption("Iteration:"+str(iteration))

            #if the user clicks on the cross, the game stops
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    execute = False
        pygame.quit()
        logger.debug('End main loop')
        
class Game_Of_Life :
    def __init__(self, time=args.time, height=args.height, width=args.width, 
                 cell_height=args.cell_height, cell_width=args.cell_width, 
                 max_iteration=args.m, output_file=args.o, input_file=args.i, 
                 alive_color=args.alive_color, dead_color=args.dead_color, 
                 display=args.d, debug=args.debug):
        self.time = time
        self.height = height
        self.width = width
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.max_iteration = max_iteration
        self.output_file = output_file
        self.input_file = input_file
        self.alive_color = alive_color
        self.dead_color = dead_color
        self.display = display
        self.debug = debug
    
    #here we check whether we have to display the game or not
    #then we run it accordingly
    def run(self):

        #afficher messages de debug s'il faut
        if self.debug :
            logger.setLevel(logging.DEBUG)

        pattern = Pattern([], 0, 0)
        pattern.load(self.input_file)
        #initializes using self.height//self.cell_height which is the number of rows
        #and self.width//self.cell_width which is the number of columns
        #i.e. the number of cells horizontally and vertically
        set_of_cells = Set_Of_Cells([],self.height//self.cell_height , self.width//self.cell_width)
        set_of_cells.initialize(pattern)

        if self.display:
            display = Display(self.time, self.height, self.width, self.cell_height, 
                              self.cell_width, set_of_cells, self.alive_color, self.dead_color)
            display.display(set_of_cells)
        else:
            for i in range(self.max_iteration):
                logger.info('Iteration number %d', i)
                set_of_cells.update(self.height//self.cell_height, self.width//self.cell_width)
            set_of_cells.output(self.output_file)

#RUNNING THE GAME
game_of_life=Game_Of_Life()
game_of_life.run()