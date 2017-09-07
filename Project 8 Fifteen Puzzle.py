"""
Modified version of Loyd's Fifteen puzzle - solver and visualizer

Note that solved configuration has the blank (zero) tile in upper left.
Use the arrows key to swap this tile with its neighbors.
After the board has been scrambled by a fairly number of key presses,
player can press the Solve button to solve the puzzle automatically.

To fully experience the performance of the game, 
please visit the following URL with Google Chrome.
"http://www.codeskulptor.org/#user43_vmB10ww7Rhblq1W.py"
"""

import simplegui

# constants
TILE_SIZE = 60

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
        
    def find_unsolve(self):
        """
        Helper function to find the unsolved tile 
        which should be solved first
        """
        # search for phase one
        for row in range(self._height - 1, 1, -1):
            for col in range(self._width - 1, 0, -1):
                if self.current_position(row, col) != (row, col):
                    return (row, col)
        # search for phase two
        for col in range(self._width - 1, 1, -1):
            for row in range(1, -1, -1):
                if self.current_position(row, col) != (row, col):
                    return (row, col)
        # search for phase three
        for row in range(0, 2):
            for col in range(0, 2):
                if self.current_position(row, col) != (row, col):
                    return (row, col)
        return None
    
    def position_tile(self, target_row, target_col, final_row, final_col):
        """
        Helper function to move the tile, the value of which is
        (target_row, target_col), to (final_row, final_col).
        """
        current_pos = self.current_position(target_row, target_col)
        if current_pos[1] == final_col:
            ans = self.move_above(target_row, target_col, final_row, final_col)
        elif current_pos[1] > final_col:
            ans = self.move_right(target_row, target_col, final_row, final_col)
        else:
            ans = self.move_left(target_row, target_col, final_row, final_col)
                    
        if self.current_position(0, 0) != (final_row, final_col - 1):
            ans += "ld"
            self.update_puzzle("ld")
        return ans
    
    def move_above(self, target_row, target_col, final_row, final_col):
        """
        Helper function for position_tile() when target tile is right
        above 0 tile.
        """
        current_pos = self.current_position(target_row, target_col)
        ans = ""
        row_distance = final_row - current_pos[0]
        for dummy_num in range(row_distance):
            ans += "u"
        self.update_puzzle(ans)
        while self.current_position(target_row, target_col) != (final_row, final_col):
            ans += "lddru"
            self.update_puzzle("lddru")
        return ans
    
    def move_left(self, target_row, target_col, final_row, final_col):
        """
        Helper function for position_tile() when target tile is on the
        left side of 0 tile.
        """
        current_pos = self.current_position(target_row, target_col)
        ans = ""
        col_distance = final_col - current_pos[1]
        row_distance = final_row - current_pos[0]        
        for dummy_num in range(row_distance):
            ans += "u"
        for dummy_num in range(col_distance):
            ans += "l"
        self.update_puzzle(ans)        
        for dummy_num in range(col_distance - 1):
            if current_pos[0] != 0:
                ans += "urrdl"
                self.update_puzzle("urrdl")
            else:
                ans += "drrul"
                self.update_puzzle("drrul")
        if self.current_position(target_row, target_col) != (final_row, final_col):
            ans += "dru"
            self.update_puzzle("dru")
        while self.current_position(target_row, target_col) != (final_row, final_col):
            ans += "lddru"
            self.update_puzzle("lddru")
        return ans

    def move_right(self, target_row, target_col, final_row, final_col):
        """
        Helper function for position_tile() when target tile is on the
        right side of 0 tile.
        """    
        current_pos = self.current_position(target_row, target_col)
        ans = ""
        col_distance = current_pos[1] - final_col
        row_distance = final_row - current_pos[0]        
        for dummy_num in range(row_distance):
            ans += "u"
        for dummy_num in range(col_distance):
            ans += "r"
        self.update_puzzle(ans)
        for dummy_num in range(col_distance - 1):
            if current_pos[0] == 0:
                ans += "dllur"
                self.update_puzzle("dllur")
            else:
                ans += "ulldr"
                self.update_puzzle("ulldr")
        if current_pos[0] == 0:
            ans += "dlu"
            self.update_puzzle("dlu")
        else:
            ans += "ul"
            self.update_puzzle("ul")
        while self.current_position(target_row, target_col) != (final_row, final_col):
            ans += "lddru"
            self.update_puzzle("lddru")
        return ans      
        
    def move0_to_unsolved(self):
        """
        Helper function to move 0 tile to the place of unsolved tile which should
        be deal with first.
        """    
        ans = ""
        unsolve = self.find_unsolve()
        if unsolve == None:
            return ""
        elif unsolve[0] < 2 and unsolve[1] < 2: # phase three
            while self.current_position(0, 0)[0] != 1:
                ans += "d"
                self.update_puzzle("d")
            while self.current_position(0, 0)[1] != 1:
                ans += "r"
                self.update_puzzle("r")
        elif unsolve[0] > 1: # phase one            
            while self.current_position(0, 0)[1] > unsolve[1]:
                ans += "l"
                self.update_puzzle("l")
            while self.current_position(0, 0)[1] < unsolve[1]:
                ans += "r"
                self.update_puzzle("r")
            while self.current_position(0, 0)[0] < unsolve[0]:
                ans += "d"
                self.update_puzzle("d")
        else: # phase two
            while self.current_position(0, 0)[0] < unsolve[0]:
                ans += "d"
                self.update_puzzle("d")
            while self.current_position(0, 0)[0] > unsolve[0]:
                ans += "u"
                self.update_puzzle("u")
            while self.current_position(0, 0)[1] < unsolve[1]:
                ans += "r"
                self.update_puzzle("r")
        return ans
    ##################################################################
    # Phase one methods: solve the bottom m-2 rows of the puzzle from 
    # bottom to top, each row will be solved in a right to left order 

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) != 0: 
            return False
        for col in range(target_col + 1, self._width):
            if self.current_position(target_row, col) != (target_row, col):
                return False
        for row in range(target_row + 1, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    return False
        return True
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        ans = self.position_tile(target_row, target_col, target_row, target_col)
        assert self.lower_row_invariant(target_row, target_col - 1)    
        return ans

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        ans = "ur"
        self.update_puzzle("ur")
        if self.current_position(target_row, 0) != (target_row, 0):
            ans += self.position_tile(target_row, 0, target_row - 1, 1)
            ans += "ruldrdlurdluurddlur"
            self.update_puzzle("ruldrdlurdluurddlur")
        while self.current_position(0, 0)[1] != self._width - 1:
            ans += "r"
            self.update_puzzle("r")
        assert self.lower_row_invariant(target_row - 1, self._width - 1)
        return ans

    #############################################################
    # Phase two methods: solve the rightmost n-2 columns of the top 
    # two rows of the puzzle in a right to left order, each column 
    # will be solved in a bottom to top order

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(0, target_col) != 0:
            return False
        for col in range(target_col + 1, self._width):
            for row in range(0, 2):                
                if self.current_position(row, col) != (row, col):
                    return False
        for row in range(2, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    return False
        if self.current_position(1, target_col) != (1, target_col):
            return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if self.get_number(1, target_col) != 0:
            return False
        for col in range(target_col + 1, self._width):
            for row in range(0, 2):                
                if self.current_position(row, col) != (row, col):
                    return False
        for row in range(2, self._height):
            for col in range(self._width):
                if self.current_position(row, col) != (row, col):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        ans = "ld"
        self.update_puzzle("ld")
        if self.current_position(0, target_col) != (0, target_col):
            ans += self.position_tile(0, target_col, 1, target_col - 1)
            ans += "urdlurrdluldrruld"
            self.update_puzzle("urdlurrdluldrruld")           
        assert self.row1_invariant(target_col - 1)
        return ans

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        ans = self.position_tile(1, target_col, 1, target_col)
        ans += "ur"
        self.update_puzzle("ur")
        assert self.row0_invariant(target_col)    
        return ans

    ###########################################################
    # Phase 3 methods: solve the upper left 2*2 portion of the puzzle directly

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        ans = "ul"
        self.update_puzzle("ul")
        while self.current_position(0,1) != (0,1) and self.current_position(1,1) != (1,1):
            ans += "rdlu"
            self.update_puzzle("rdlu")
        return ans

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        ans = ""
        unsolve = self.find_unsolve()
        if unsolve == None:
            return ""
        else:
            ans += self.move0_to_unsolved()
        
        if unsolve[0] > 1: 
            for col in range(unsolve[1], 0, -1):
                ans += self.solve_interior_tile(unsolve[0], col)
            ans += self.solve_col0_tile(unsolve[0])            
            for row in range(unsolve[0] - 1, 1, -1):
                for col in range(self._width - 1, 0, -1):
                    ans += self.solve_interior_tile(row, col)
                ans += self.solve_col0_tile(row)
            for col in range(self._width - 1, 1, -1):
                ans += self.solve_row1_tile(col)
                ans += self.solve_row0_tile(col)
            ans += self.solve_2x2()    
        if unsolve[1] > 1 and unsolve[0] <= 1: 
            if unsolve[0] == 1:
                ans += self.solve_row1_tile(unsolve[1])
                ans += self.solve_row0_tile(unsolve[1])
            else:
                ans += self.solve_row0_tile(unsolve[1])
            for col in range(unsolve[1] - 1, 1, -1):
                ans += self.solve_row1_tile(col)
                ans += self.solve_row0_tile(col)
            ans += self.solve_2x2()
        if unsolve[0] < 2 and unsolve[1] < 2: 
            ans += self.solve_2x2()    
        return ans    

class FifteenGUI:
    """
    Main GUI class
    """

    def __init__(self, puzzle):
        """
        Create frame and timers, register event handlers
        """
        self._puzzle = puzzle
        self._puzzle_height = puzzle.get_height()
        self._puzzle_width = puzzle.get_width()

        self._frame = simplegui.create_frame("The Fifteen puzzle",
                                             self._puzzle_width * TILE_SIZE,
                                             self._puzzle_height * TILE_SIZE)
        self._solution = ""
        self._current_moves = ""
        self._frame.add_button("Solve", self.solve, 100)
        self._frame.add_input("Enter moves", self.enter_moves, 100)
        self._frame.add_button("Print moves", self.print_moves, 100)
        self._frame.set_draw_handler(self.draw)
        self._frame.set_keydown_handler(self.keydown)
        self._timer = simplegui.create_timer(250, self.tick)
        self._timer.start()
        self._frame.start()

    def tick(self):
        """
        Timer for incrementally displaying computed solution
        """
        if self._solution == "":
            return
        direction = self._solution[0]
        self._solution = self._solution[1:]
        try:
            self._puzzle.update_puzzle(direction)
        except:
            print "invalid move:", direction

    def solve(self):
        """
        Event handler to generate solution string for given configuration
        """
        new_puzzle = self._puzzle.clone()
        self._solution = new_puzzle.solve_puzzle()

    def print_moves(self):
        """
        Event handler to print and reset current move string
        """
        print self._current_moves
        self._current_moves = ""

    def enter_moves(self, txt):
        """
        Event handler to enter move string
        """
        self._solution = txt

    def keydown(self, key):
        """
        Keydown handler that allows updates of puzzle using arrow keys
        """
        if key == simplegui.KEY_MAP["up"]:
            try:
                self._puzzle.update_puzzle("u")
                self._current_moves += "u"
            except:
                print "invalid move: up"
        elif key == simplegui.KEY_MAP["down"]:
            try:
                self._puzzle.update_puzzle("d")
                self._current_moves += "d"
            except:
                print "invalid move: down"
        elif key == simplegui.KEY_MAP["left"]:
            try:
                self._puzzle.update_puzzle("l")
                self._current_moves += "l"
            except:
                print "invalid move: left"
        elif key == simplegui.KEY_MAP["right"]:
            try:
                self._puzzle.update_puzzle("r")
                self._current_moves += "r"
            except:
                print "invalid move: right"

    def draw(self, canvas):
        """
        Draw the puzzle
        """
        for row in range(self._puzzle_height):
            for col in range(self._puzzle_width):
                tile_num = self._puzzle.get_number(row, col)
                if tile_num == 0:
                    background = "rgb(128, 128, 255)"
                else:
                    background = "Blue"
                tile = [[col * TILE_SIZE, row * TILE_SIZE],
                        [(col + 1) * TILE_SIZE, row * TILE_SIZE],
                        [(col + 1) * TILE_SIZE, (row + 1) * TILE_SIZE],
                        [col * TILE_SIZE, (row + 1) * TILE_SIZE]]
                canvas.draw_polygon(tile, 1, "White", background)
                canvas.draw_text(str(tile_num),
                                 [(col + .2) * TILE_SIZE,
                                  (row + 0.8) * TILE_SIZE],
                                 2 *  TILE_SIZE // 3, "White")

    
FifteenGUI(Puzzle(4, 4))    
