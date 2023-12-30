import argparse
import pygame
import copy

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
args = parser.parse_args()

class Cell :
    def __init__(self, x, y, alive):
        self.x = x
        self.y = y
        self.alive = alive
    
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
    def __init__(self, cells, height=args.height, width=args.width):
        self.cells = cells
        self.height = height
        self.width = width

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
   
        
    def update(self, height, width):
        set_prov=copy.deepcopy(self)
        for x in range(self.height):
                for y in range(self.width):
                    self.cells[x][y].update(set_prov)
    
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
    
    def draw(self, set_of_cells):
        self.screen.fill(self.dead_color)
        for l in set_of_cells.cells:
            for cell in l:
                if cell.alive:
                    rect = pygame.Rect(cell.x*self.cell_height,cell.y*self.cell_width, 
                                       self.cell_height, self.cell_width)
                    pygame.draw.rect(self.screen, self.alive_color, rect)
        pygame.display.update()
    
    def display(self, set_of_cells):
        pygame.init()
        clock = pygame.time.Clock()
        execute = True
        while execute:
            clock.tick(self.time)
            self.draw(set_of_cells)
            set_of_cells.update(self.height, self.width) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    execute = False
        pygame.quit()
        
class Game_Of_Life :
    def __init__(self, time=args.time, height=args.height, width=args.width, 
                 cell_height=args.cell_height, cell_width=args.cell_width, 
                 max_iteration=args.m, output_file=args.o, input_file=args.i, 
                 alive_color=args.alive_color, dead_color=args.dead_color, display=args.d):
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
    
    def run(self):
        pattern = Pattern([], 0, 0)
        pattern.load(self.input_file)
        set_of_cells = Set_Of_Cells([], 0, 0)
        set_of_cells.initialize(self.height//self.cell_height, self.width//self.cell_width, 
                                    pattern)
        if self.display:
            display = Display(self.time, self.height, self.width, self.cell_height, 
                              self.cell_width, set_of_cells, self.alive_color, self.dead_color)
            display.display(set_of_cells)
        else:
            for i in range(self.max_iteration):
                set_of_cells.update(self.height//self.cell_height, self.width//self.cell_width)
            set_of_cells.output(self.output_file)

game_of_life=Game_Of_Life()
game_of_life.run()