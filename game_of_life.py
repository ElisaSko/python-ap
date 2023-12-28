import argparse
import pygame

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
parser.add_argument('--time', default= 10, type=int, help='time between two frames')
args = parser.parse_args()

class Cell :
    def __init__(self, x, y, alive):
        self.x = x
        self.y = y
        self.alive = alive
    
    '''def __str__(self):
        return str(int(self.alive))'''
    
    def neighbours(self, set_of_cells):
        neighbours=[]
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                if x >= 0 and x < set_of_cells.height and y >= 0 and y < set_of_cells.width and (x != self.x or y != self.y):
                    neighbours.append(set_of_cells.cells[x][y])
        return neighbours

    def count_neighbours(self, set_of_cells):
        neighbours = self.neighbours(set_of_cells)
        count = 0
        for cell in neighbours:
            if cell.alive:
                count += 1
        return count
    
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
    def __init__(self, cells, height=args.height, width=args.width, iteration=0):
        self.cells = cells
        self.height = height
        self.width = width
        self.iteration = iteration

    '''
    def __str__(self):
        c=''
        for l in self.cells:
            for cell in l:
                c+=str(cell)
            c+='\n'
        return c
    '''

    def initialize(self, height, width, pattern):
        self.height = height
        self.width = width
        self.cells = []
        for x in range(self.height):
            line = []
            for y in range(self.width):
                line.append(Cell(x, y, False))
            self.cells.append(line)
        for l in pattern.cells:
            for cell in l:
                self.cells[cell.x][cell.y].alive = cell.alive
        
    def update(self, height, width, max_iteration, output_file, input_file):
        if self.iteration < max_iteration:
            for x in range(self.height):
                for y in range(self.width):
                    self.cells[x][y].update(self)
            self.iteration += 1
        elif self.iteration == max_iteration:
            self.output(self,output_file)
    
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

      
class Pattern :
    def __init__(self, cells, height, width):
        self.cells = cells
        self.height = height
        self.width = width
    
    def load(self, file_name):
        file = open(file_name, 'r')
        lines = file.readlines()
        file.close()

        self.height = len(lines)
        self.width = len(lines[0]) - 1
        self.cells = []
        for x in range(self.height):
            line = []
            for y in range(self.width):
                if lines[x][y] == '0':
                    line.append(Cell(x, y, False))
                if lines[x][y]=='1':
                    line.append(Cell(x, y, True))
            self.cells.append(line)

class Display :
    def __init__(self, time, size, height, width, cell_height, cell_width, set_of_cells,alive_color,dead_color):
        self.size = size
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.set_of_cells = set_of_cells
        self.height = height
        self.width = width
        self.alive_color = alive_color
        self.dead_color = dead_color
        self.time = time
        self.screen = pygame.display.set_mode((self.width, self.height))
    
    def draw(self, set_of_cells):
        self.screen.fill(self.dead_color)
        for l in set_of_cells.cells:
            for cell in l:
                if cell.alive:
                    rect = pygame.Rect(cell.y*self.cell_height,cell.x*self.cell_width, self.cell_height, self.cell_width)
                    pygame.draw.rect(self.screen, self.alive_color, rect)
        pygame.display.update()
    
    def display(self, set_of_cells):
        pygame.init()
        clock = pygame.time.Clock()
        execute = True
        while execute:
            clock.tick(self.time)
            self.draw(set_of_cells)
            set_of_cells.update(self.height, self.width, args.m, args.o, args.i)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    execute = False
        pygame.quit()
        

pattern = Pattern([], 0, 0)
pattern.load(args.i)
set_of_cells = Set_Of_Cells([], 0, 0, 0)
set_of_cells.initialize(pattern.height, pattern.width, pattern)
#set_of_cells.update(pattern, args.height, args.width, 1, args.o, args.i)
set_of_cells.output(args.o)

display = Display(args.time,(args.width, args.height), args.height, args.width, args.cell_height, args.cell_width, set_of_cells, args.alive_color, args.dead_color)
display.display(set_of_cells)