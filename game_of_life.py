import argparse

parser = argparse.ArgumentParser(description='game of life')
parser.add_argument('-i', default = 'my_input_file.txt', type=str, help='input file')
parser.add_argument('-o', default= 'my_output_file.txt',type=str, help='output file')
parser.add_argument('--width', default= 800, type=int, help='width of the grid')
parser.add_argument('--height', default= 600, type=int, help='height of the grid')
parser.add_argument('-m', default= 20, type=int, help='number of iterations')
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
            if number = 2 or number = 3:
                self.alive = True
            else :
                self.alive = False
        else:
            if number == 3:
                self.alive = True

class Set_Of_Cells  :
    def __init__(self, cells, height, width, iteration):
        self.cells = cells
        self.height = height
        self.width = width
        self.iteration = iteration
    
    def initialize(self, height, width, pattern):
        self.height = height
        self.width = width
        self.cells = []
        for x in range(self.height):
            line = []
            for y in range(self.width):
                line.append(Cell(x, y, False))
            self.cells.append(line)
        for cell in pattern.cells:
            self.cells[cell.x][cell.y].alive = cell.alive
        
    def update(self, pattern, height, width, max_iteration, output_file, input_file):
        if self.iteration == 0:
            self.initialize(self, height, width, pattern)
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