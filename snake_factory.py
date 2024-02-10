import argparse
import datetime
import logging
import operator
import os
import pygame
import random
import re

# Constants
MIN_WND_SIZE = 200 # Minimum for window height or width.
MIN_SNAKE_LEN = 2 # Minimum length of the snake.
MIN_TILE_SIZE = 10 # Minimum for tile size.
MIN_NB_ROWS = 12
MIN_NB_COLS = 20
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
HALT = (0, 0)
BLACK = '#000000'
WHITE = '#ffffff'
RED = '#ff0000'
GREEN = '#00ff00'
FPS = 5
WIDTH = 640
HEIGHT = 480
MAX_HIGH_SCORES = 5
SNAKE_INIT_LENGTH = 3
TILE_SIZE = 20
SCORE_FILE = os.path.join(os.environ['HOME'], '.snake_scores.txt')

def read_args():
    """Read command line arguments."""

    # Define parser
    parser = argparse.ArgumentParser(
            description='An implementation of the Snake & Fruit game.',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--bg-color-1', help='Background color 1.',
            default=WHITE)
    parser.add_argument('--bg-color-2', help='Background color 2.',
            default=BLACK)
    parser.add_argument('--height', help='Window height', type=int,
            default=HEIGHT)
    parser.add_argument('--width', help='Window width', type=int, default=WIDTH)
    parser.add_argument('--fps', help='Number of frames per second', type=int,
            default=FPS)
    parser.add_argument('--fruit-color', help='Fruit color.',
            default=RED)
    parser.add_argument('-G', '--gameover-on-exit',
            help='Terminate game when snake exit window.', action='store_true')
    parser.add_argument('-g', '--debug', help='Set debug mode.',
            action='store_true')
    parser.add_argument('--high-scores-file', default=SCORE_FILE,
            help="The path to the file in which to store high scores.")
    parser.add_argument('--max-high-scores', type=int, default=MAX_HIGH_SCORES,
            help='The maximum of high scores to store')
    parser.add_argument('--snake-color', help='Snake color.',
            default=GREEN)
    parser.add_argument('--snake-init-length', '--snake-length',
            help='The initial length of the snake', type=int,
            default=SNAKE_INIT_LENGTH)
    parser.add_argument('--tile-size', help='Tile size', type=int,
            default=TILE_SIZE)
    
    # Parse arguments
    args = parser.parse_args()

    # Enable debug messages
    if args.debug:
        logger.setLevel(logging.DEBUG)

    return args

def get_random_number(first, last):

    # Init random seed with system clock (default)
    random.seed()

    return random.randint(first, last)

# *** EXPLANATION ***
# WE NOW HAVE CLASSES TO HANDLE THE DIFFERENT OBJECTS OF THE GAME:
# Score, Scores, CheckerBackground, Snake, Fruit.
# MOST FUNCTIONS HAVE BEEN MOVED INTO THESE CLASSES.
# WHEN TESTING WE NOW TEST A WHOLE CLASS INSTEAD OF INDIVIDUAL FUNCTIONS.
# THE CODE IS ALSO EASIER TO PUT IN A MODULE AND EXPORT, EACH CLASS BEING A TYPE
# OF MODULE (I.E.: MODULARIZED CODE) BY ITSELF, AT THE CONDITION THEY DO NOT
# HAVE TOO MUCH DEPENDENCIES BETWEEN THEM OR WITH OTHER COMPONENTS.
# *******************

class Factory:
    def __init__(self, board, tile_fruit, tiles_snake, direction):
        self._board = board
        self._tile_fruit = tile_fruit
        self._tiles_snake = tiles_snake
        self._direction = direction
        self.dico={}
    
    def createFruit(self, name):
        if name in self.dico:
            self._color_fruit, self._points = self.dico[name]
            return Fruit(board=self._board, tile=self._tile_fruit, color=self._color_fruit,
                      points=self._points)
        else : 
            raise ValueError("This fruit does not exist")
    
    def createSnake(self, length, color=GREEN, **args):
        return Snake(board=self._board, tiles=self._tiles_snake, direction=self._direction, 
                     color, **args)
    
    def declareFruit(self, name, color_fruit, points):
        self.dico[name] = (color_fruit, points)

    
# Game over exception
class GameOver(Exception):
    pass

class Score:
    
    def __init__(self, score=0, name=None):
        self._score = score
        self._name = name

    def get(self):
        return self._score
        
    def toInt(self):
        return self.get()
    
    def getName(self):
        return self._name
    
    def setName(self, name):
        self._name = name

    def addPoints(self, points):
        self._score += points
    
    def __lt__(self, other):
        return (self._name < other._name if self._score == other._score else
                self._score < other._score)

    def __eq__(self, other):
        return self._score == other._score and self._name == other._name

    @classmethod
    def fromString(cls, s):
        (name, score) = s.split(',') # Split line in two
        score = int(score) # Convert from string to integer
        return cls(name=name, score=score)

    def toString(self):
        return "%s,%d" % ("Unknown" if self._name is None else self._name,
                self._score)

class Scores:
    
    def __init__(self, file, max_scores=None):
        if file is None:
            raise ValueError("You must provide a valid path for a file.")
        self._file = file
        self._scores = []
        self._max_scores = max_scores 
        self.load()

    def getSize(self):
        return len(self._scores)

    def get(self, index):
        if index < len(self._scores):
            return self._scores[index]
        return None

    def load(self):
        
        # Test if file exists
        if os.path.exists(self._file):

            # Open file for reading
            with open(self._file, 'r') as f:

                # Loop on all lines
                for line in f:
                    line = line.rstrip() # Get rid of new line character
                    logger.debug("Line in scores file: %s" % line)
                    self._scores.append(Score.fromString(line)) # Add to list

    def save(self):
        
        # Open file for writing
        with open(self._file, 'w') as f:

            # Loop on all scores
            for score in self._scores:
                print(score.toString(), file=f)

    def setMax(self, max_scores):
        self._max_scores = max_scores
        self._shorten_scores()

    def _shorten_scores(self):

        self._scores.sort()
        if self._max_scores is not None and len(self._scores) > self._max_scores:
            self._scores[0:len(self._scores) - self._max_scores] = []

    def addScore(self, new_score):

        # Add new score
        if new_score.get() > 0 and (self._max_scores is None
                or len(self._scores) < self._max_scores
                or len(self._scores) == 0 or
                new_score.get() > self._scores[0].get()):
            if new_score.getName() is None:
                new_score.setName(input("Write your name: "))
            self._scores.append(new_score)

        self._shorten_scores()

    def print(self):
        
        if len(self._scores) > 0:
            logger.info("\nHIGH SCORES:")
            for score in sorted(self._scores, reverse=True):
                logger.info("  %s: %d" % (score.getName(), score.get()))

class Board:

    def __init__(self, width, height, tile_size):
        self._width = width
        self._height = height
        self._tile_size = tile_size

        # Check arguments
        if self._height < MIN_WND_SIZE or self._width < MIN_WND_SIZE:
            raise ValueError(("Window height and width must be greater or " +
                "equal to %d.") % MIN_WND_SIZE)
        if self._tile_size < MIN_TILE_SIZE:
            raise ValueError("Tile size must be greater or equal to %d."
                    % MIN_TILE_SIZE)
        if (self._height % self._tile_size != 0 or
                self._width % self._tile_size != 0):
            raise ValueError(("Window width (%d) and window height (%d) must" +
                " be dividable by the tile size (%d).") % (self._width,
                    self._height, self._tile_size))
        if self._width // self._tile_size < MIN_NB_COLS:
            raise ValueError(("Number of columns must be greater or equal to" + 
                " %d, but width / tile_size = %d / %d = %d.") % (MIN_NB_COLS,
                    self._width, self._tile_size,
                    self._width // self._tile_size))
        if self._height // self._tile_size < MIN_NB_ROWS:
            raise ValueError(("Number of rows must be greater or equal to" + 
                " %d, but height / tile_size = %d / %d = %d.") % (MIN_NB_ROWS,
                    self._height, self._tile_size,
                    self._height // self._tile_size))

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def getNbCols(self):
        return self._width // self._tile_size

    def getNbRows(self):
        return self._height // self._tile_size

    def getRandomTile(self):
        return (get_random_number(0, self.getNbCols() - 1),
                get_random_number(0, self.getNbRows() - 1))

    def drawTiles(self, screen, tiles, color):
        
        # Loop on all tiles
        for tile in tiles:

            # Is tile inside display?
            if (tile[0] >=0 and tile[0] < self.getNbCols() and tile[1] >= 0 and
                    tile[1] < self.getNbRows()):

                # Compute rectangle
                tile_rect = pygame.Rect(tile[0] * self._tile_size,
                        tile[1] * self._tile_size,
                        self._tile_size, self._tile_size)
                
                # Draw tile
                pygame.draw.rect(screen, pygame.Color(color), tile_rect)

class CheckerBackground:

    def __init__(self, board, color_1=WHITE, color_2=BLACK):
        self._board = board
        self._color_1 = pygame.Color(color_1)
        self._color_2 = pygame.Color(color_2)

    def draw(self, screen):

        # Loop on all rows and columns
        for i in range(self._board.getNbCols()):
            for j in range(self._board.getNbRows()):
                
                # Alternate color
                tile_color = (self._color_1 if (i + j) % 2 == 0 else
                        self._color_2)

                self._board.drawTiles(screen, [(i, j)], color=tile_color)

class Fruit:

    def __init__(self, board, tile, color='#ff0000', points=1):
        self._board = board
        self._tile = tile
        self._color = color
        self._points = points
        self._eaten = False

    @classmethod
    def createRandom(cls, board, forbidden_tiles, **args):
        
        fruit = None

        # We search for a random place of the fruit that does no collide with the
        # snake.
        while fruit is None or fruit.getTile() in forbidden_tiles:
            fruit = cls(board, tile=board.getRandomTile(), **args)
        
        return fruit

    def getColor(self):
        return self._color

    def getTile(self):
        return self._tile

    def getPoints(self):
        return self._points

    def setEaten(self, eaten):
        self._eaten = eaten

    def hasBeenEaten(self):
        return self._eaten

    def draw(self, screen):
        self._board.drawTiles(screen, [self._tile], color=self._color)

class Snake:

    def __init__(self, board, tiles, direction, color='#00ff00',
            gameover_on_exit=True):
        self._board = board
        self._tiles = tiles
        self._color = color
        self._score = Score()
        self._direction = direction
        self._gameover_on_exit = gameover_on_exit

    @classmethod
    def createRandom(cls, board, length, **args):

        # Check arguments
        if length < MIN_SNAKE_LEN:
            raise ValueError("Snake length must be greater or equal to %d." %
                    MIN_SNAKE_LEN)

        # Set first cell randomly
        init_pos = board.getRandomTile()
        tiles = [init_pos]
        
        # Get random direction
        snake_dir = [LEFT, RIGHT, UP, DOWN][get_random_number(0, 3)]
        
        # Make other cells
        for i in range(length - 1):
            x = tiles[-1][0] + snake_dir[0]
            y = tiles[-1][1] + snake_dir[1]
            if x < 0:
                x = 0
            if x >= board.getNbCols():
                x = board.getNbCols() - 1
            if y < 0:
                y = 0
            if y >= board.getNbRows():
                y = board.getNbRows() - 1
            tiles.append((x, y))

        return cls(board, tiles=tiles, direction=snake_dir, **args)

    def getScore(self):
        return self._score

    def getHeadTile(self):
        return self._tiles[-1]

    def getTiles(self):
        return self._tiles.copy()
    
    def setDirection(self, direction):
        self._direction = direction

    def hasTile(self, tile):
        return tile in self._tiles
    
    def move(self, fruit):

        # Make snake grow (i.e.: compute new head)
        new_head = tuple(map(operator.add, self._tiles[-1], self._direction))

        # Game over if exit window
        if self._gameover_on_exit:
            if (new_head[0] < 0 or new_head[0] >= self._board.getNbCols() or
                    new_head[1] < 0 or new_head[1] >= self._board.getNbRows()):
                raise GameOver()

        # Snake continues on opposite side of the window  
        else: 
            if new_head[0] < 0: # Exit by the left
                new_head = (self._board.getNbCols() - 1, new_head[1])
            elif new_head[0] >= self._board.getNbCols(): # Exit by the right
                new_head = (0, new_head[1])
            elif new_head[1] < 0: # Exit by the top
                new_head = (new_head[0], self._board.getNbRows() - 1)
            elif new_head[1] >= self._board.getNbRows(): # Exit by the bottom
                new_head = (new_head[0], 0)
                
        # Detect collision on itself
        if new_head in self._tiles:
            raise GameOver()
            
        else:
            # Append new head
            self._tiles.append(new_head)

            # Shorten snake
            # Is the snake on the fruit ?
            if new_head == fruit.getTile():
                self._score.addPoints(fruit.getPoints())
                fruit.setEaten(True)

            # Fruit has not been eaten => we shorten the snake by the queue.
            else:
                del(self._tiles[0])

    def draw(self, screen):
        self._board.drawTiles(screen, self._tiles, color=self._color)

class Game:

    def __init__(self, width=WIDTH, height=HEIGHT, tile_size=TILE_SIZE,
            max_high_scores=MAX_HIGH_SCORES,
            snake_init_length=SNAKE_INIT_LENGTH, high_score_file=SCORE_FILE,
            bg_color_1=WHITE, bg_color_2=BLACK, fruit_color=RED,
            snake_color=GREEN, fps=FPS, gameover_on_exit=False,
            **_): # **_ ignore remaining arguments

        self._max_high_scores = max_high_scores
        self._high_score_file = high_score_file
        self._fps = fps

        # Check color arguments using regular expressions.
        color_re = re.compile(r'^#[0-9a-f]{6}$')
        if not re.match(color_re, fruit_color):
            raise ValueError("Bad format for fruit color %s."
                    % fruit_color)
        if not re.match(color_re, snake_color):
            raise ValueError("Bad format for snake color %s."
                    % snake_color)
        if not re.match(color_re, bg_color_1):
            raise ValueError("Bad format for background color 1 %s." %
                    bg_color_1)
        if not re.match(color_re, bg_color_2):
            raise ValueError("Bad format for background color 2 %s." %
                    bg_color_2)

        # Initialize the Pygame library.
        # This is a special step needed by Pygame. Most (99%) libraries do not
        # need an initialization step.
        pygame.init()
        
        # Create a screen for display, choosing its size (width x height).
        self._screen = pygame.display.set_mode((width, height))

        # Create a clock object that we will use to control the speed of our
        # game.
        self._clock = pygame.time.Clock()

        # Create the game space
        self._board = Board(width=width, height=height, tile_size=tile_size)

        # Create the checkerboard background
        self._bg = CheckerBackground(self._board, color_1=bg_color_1,
                color_2=bg_color_2)

        # Create snake
        self._snake = Snake.createRandom(self._board,
                length=snake_init_length,
                color=snake_color, gameover_on_exit=gameover_on_exit)
        
        # Create first fruit
        self._fruit = Fruit.createRandom(self._board,
                forbidden_tiles=self._snake.getTiles(), color=fruit_color)

    def _process_events(self):
        """Process new events (keyboard, mouse)."""

        for event in pygame.event.get():
            
            # Catch selection of exit icon (Window "cross" icon)
            if event.type == pygame.QUIT:
                raise GameOver()

            # Catch a key press
            elif event.type == pygame.KEYDOWN:
                
                # "Q" key has been pressed
                if event.key == pygame.K_q:
                    raise GameOver()
        
                # Arrow keys
                elif event.key == pygame.K_UP:
                    self._snake.setDirection(UP)
                elif event.key == pygame.K_DOWN:
                    self._snake.setDirection(DOWN)
                elif event.key == pygame.K_RIGHT:
                    self._snake.setDirection(RIGHT)
                elif event.key == pygame.K_LEFT:
                    self._snake.setDirection(LEFT)

    def _update_objects(self):
        
        # Update snake
        self._snake.move(fruit=self._fruit)
        
        # Update fruit
        if self._fruit.hasBeenEaten():
            self._fruit = Fruit.createRandom(board=self._board,
                    forbidden_tiles=self._snake.getTiles(),
                    color=self._fruit.getColor())
        
    def _update_display(self):
        
        # Draw background and objects
        self._bg.draw(self._screen)
        self._fruit.draw(self._screen)
        self._snake.draw(self._screen)

        # Update title with score.
        pygame.display.set_caption("Snake - score: %d"
                % self._snake.getScore().get())

        # Display the display
        pygame.display.update()

    def _process_score(self):

        logger.info("\nScore: %d." % self._snake.getScore().get())
        
        # Read table from file
        scores = Scores(file=self._high_score_file,
                max_scores=self._max_high_scores) 

        # Update table
        scores.addScore(self._snake.getScore())
        
        # Print table
        scores.print()
        
        # Save table to file
        scores.save()

    def start(self):

        # Loop forever
        logger.debug("Start main loop.")
        try:
            while True:
                
                # Wait 1/FPS of a second, starting from last display or now
                self._clock.tick(self._fps)
                
                self._process_events()
                self._update_objects()
                self._update_display()

        except GameOver:
            pass

        logger.info("\nGame over.")

        # Terminate Pygame
        pygame.quit()
        self._process_score()

def main():

    # Read command line arguments
    args = read_args()

    # Create the game instance
    game = Game(**vars(args)) # vars() transforms mapping (args) into
                              # a dictionary

    # Run the game instance
    game.start()

# Create a logger for this module
logger = logging.getLogger(__name__)
        
if __name__ == "__main__":

    import sys

    # Setup the logger
    handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Call main function
    main()

    # Quit program properly
    quit(0)
