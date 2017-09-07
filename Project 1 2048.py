"""
Use grids to create a clone of 2048 game.

Although the original game is played on a 4*4 grid, 
this version is able to have an arbitrary height and width.

To fully experience the performance of the game, 
please visit the following URL with Google Chrome.
"http://www.codeskulptor.org/#user43_WlfBV9AIWBJsFyp.py"
"""

import random
import simplegui
import codeskulptor
import math

# Tile Images
IMAGENAME = "assets_2048.png"
TILE_SIZE = 100
HALF_TILE_SIZE = TILE_SIZE / 2
BORDER_SIZE = 45

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

class GUI:
    """
    Class to run game GUI.
    """

    def __init__(self, game):
        self._rows = game.get_grid_height()
        self._cols = game.get_grid_width()
        self._frame = simplegui.create_frame('2048',
                        self._cols * TILE_SIZE + 2 * BORDER_SIZE,
                        self._rows * TILE_SIZE + 2 * BORDER_SIZE)
        self._frame.add_button('New Game', self.start)
        self._frame.set_keydown_handler(self.keydown)
        self._frame.set_draw_handler(self.draw)
        self._frame.set_canvas_background("#BCADA1")
        self._frame.start()
        self._game = game
        url = codeskulptor.file2url(IMAGENAME)
        self._tiles = simplegui.load_image(url)
        self._directions = {"up": UP, "down": DOWN,
                            "left": LEFT, "right": RIGHT}

    def keydown(self, key):
        """
        Keydown handler
        """
        for dirstr, dirval in self._directions.items():
            if key == simplegui.KEY_MAP[dirstr]:
                self._game.move(dirval)
                break

    def draw(self, canvas):
        """
        Draw handler
        """
        for row in range(self._rows):
            for col in range(self._cols):
                tile = self._game.get_tile(row, col)
                if tile == 0:
                    val = 0
                else:
                    val = int(math.log(tile, 2))
                canvas.draw_image(self._tiles,
                    [HALF_TILE_SIZE + val * TILE_SIZE, HALF_TILE_SIZE],
                    [TILE_SIZE, TILE_SIZE],
                    [col * TILE_SIZE + HALF_TILE_SIZE + BORDER_SIZE,
                     row * TILE_SIZE + HALF_TILE_SIZE + BORDER_SIZE],
                    [TILE_SIZE, TILE_SIZE])

    def start(self):
        """
        Start the game.
        """
        self._game.reset()

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._up_initial_tiles = [(0,col) for col in range(self._grid_width)]
        self._down_initial_tiles = [(self._grid_height-1,col) for col in range(self._grid_width)]
        self._left_initial_tiles = [(row,0) for row in range(self._grid_height)]
        self._right_initial_tiles = [(row,self._grid_width-1) for row in range(self._grid_height)]
        self._move_dictionary = {UP: self._up_initial_tiles,
                                 DOWN: self._down_initial_tiles,
                                 LEFT: self._left_initial_tiles,
                                 RIGHT: self._right_initial_tiles}
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two initial tiles.
        """
        self._cells = [[0 for dummy_col in range(self._grid_width)]for dummy_row in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """        
        return str(self._cells)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width
        
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """        
        steps = self._grid_height
        changed = False
        if direction == RIGHT or direction == LEFT:
            steps = self._grid_width
        # Use OFFSETS dictionary to iterate over the entries. 
        # Retrieve the tile values and store them in a temporary list.
        for initial_tile in self._move_dictionary[direction]:
            temporary_list = []    
            for step in range(steps):                
                row = initial_tile[0] + step * OFFSETS[direction][0]
                col = initial_tile[1] + step * OFFSETS[direction][1]
                val = self.get_tile(row,col)
                temporary_list.append(val)
            merged_value = merge(temporary_list)
            # Store the merged tile values back into the grid.
            for step in range(steps):
                row = initial_tile[0] + step * OFFSETS[direction][0]
                col = initial_tile[1] + step * OFFSETS[direction][1]
                self.set_tile(row, col, merged_value[step])
                if merged_value != temporary_list:
                    changed = True

        if changed:
            self.new_tile()
    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty square.  
        The tile should be 2 90% of the time and 4 10% of the time.
        """
        possible_input_num = [2,2,2,2,2,2,2,2,2,4]
        input_number = random.choice(possible_input_num)
        non_value_pos = []
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._cells[row][col] == 0:
                    non_value_pos.append([row,col])
        if non_value_pos != []:
            input_pos = random.choice(non_value_pos)
            self.set_tile(input_pos[0], input_pos[1], input_number)
            
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._cells[row][col]

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = []
    for num in line:
        if num != 0:
            result.append(num)
    
    for index in range(len(result)-1):
        if result[index] == result[index+1]:
            result[index] *= 2
            result[index+1] = 0
    
    for num in result:
        if num == 0:
            result.remove(num)
    
    while len(result) < len(line):
        result.append(0)
    
    return result

def run_gui(game):
    """
    Instantiate and run the GUI.
    """
    gui = GUI(game)
    gui.start()

run_gui(TwentyFortyEight(4, 4))