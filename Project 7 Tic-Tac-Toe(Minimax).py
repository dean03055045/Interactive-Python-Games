"""
Implement a machine player for Tic-Tac-Toe with
Minimax strategy by using recursion to search 
the tree in a depth-first manner.

The game can also be a reversed version and the 
dimension can be modified.

To fully experience the performance of the game, 
please visit the following URL with Google Chrome.
"http://www.codeskulptor.org/#user43_GcZD8MyEnb67yIt.py"
"""

import random
import simplegui
import codeskulptor

# Set timeout, as mini-max can take a long time
codeskulptor.set_timeout(60)

EMPTY = 1
PLAYERX = 2
PLAYERO = 3 
DRAW = 4

GUI_WIDTH = 400
GUI_HEIGHT = GUI_WIDTH
BAR_WIDTH = 5

SCORES = {PLAYERX: 1,
          DRAW: 0,
          PLAYERO: -1}

# Map player constants to letters for printing
STRMAP = {EMPTY: " ",
          PLAYERX: "X",
          PLAYERO: "O"}

class TTTBoard:
    """
    Class to represent a Tic-Tac-Toe board.
    """

    def __init__(self, dim, reverse = False, board = None):
        """
        Initialize the TTTBoard object with the given dimension and 
        whether or not the game should be reversed.
        """ 
        self._dim = dim
        self._reverse = reverse
        if board == None:
            # Create empty board
            self._board = [[EMPTY for dummycol in range(dim)] 
                           for dummyrow in range(dim)]
        else:
            # Copy board grid
            self._board = [[board[row][col] for col in range(dim)] 
                           for row in range(dim)]
            
    def __str__(self):
        """
        Human readable representation of the board.
        """
        rep = ""
        for row in range(self._dim):
            for col in range(self._dim):
                rep += STRMAP[self._board[row][col]]
                if col == self._dim - 1:
                    rep += "\n"
                else:
                    rep += " | "
            if row != self._dim - 1:
                rep += "-" * (4 * self._dim - 3)
                rep += "\n"
        return rep

    def get_dim(self):
        """
        Return the dimension of the board.
        """
        return self._dim
    
    def square(self, row, col):
        """
        Returns one of the three constants EMPTY, PLAYERX, or PLAYERO 
        that correspond to the contents of the board at position (row, col).
         """
        return self._board[row][col]

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """
        empty = []
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] == EMPTY:
                    empty.append((row, col))
        return empty

    def move(self, row, col, player):
        """
        Place player on the board at position (row, col).
        player should be either the constant PLAYERX or PLAYERO.
        Does nothing if board square is not empty.
        """
        if self._board[row][col] == EMPTY:
            self._board[row][col] = player

    def check_win(self):
        """
        Returns a constant associated with the state of the game
            If PLAYERX wins, returns PLAYERX.
            If PLAYERO wins, returns PLAYERO.
            If game is drawn, returns DRAW.
            If game is in progress, returns None.
        """
        board = self._board
        dim = self._dim
        dimrng = range(dim)
        lines = []

        # rows
        lines.extend(board)

        # cols
        cols = [[board[rowidx][colidx] for rowidx in dimrng]
                for colidx in dimrng]
        lines.extend(cols)

        # diags
        diag1 = [board[idx][idx] for idx in dimrng]
        diag2 = [board[idx][dim - idx -1] 
                 for idx in dimrng]
        lines.append(diag1)
        lines.append(diag2)

        # check all lines
        for line in lines:
            if len(set(line)) == 1 and line[0] != EMPTY:
                if self._reverse:
                    return switch_player(line[0])
                else:
                    return line[0]

        # no winner, check for draw
        if len(self.get_empty_squares()) == 0:
            return DRAW

        # game is still in progress
        return None
            
    def clone(self):
        """
        Return a copy of the board.
        """
        return TTTBoard(self._dim, self._reverse, self._board)

class TicTacGUI:
    """
    GUI for Tic Tac Toe game.
    """    
    def __init__(self, size, aiplayer, aifunction, ntrials, reverse = False):
        # Game board
        self._size = size
        self._bar_spacing = GUI_WIDTH // self._size
        self._turn = PLAYERX
        self._reverse = reverse

        # AI setup
        self._humanplayer = switch_player(aiplayer)
        self._aiplayer = aiplayer
        self._aifunction = aifunction
        self._ntrials = ntrials
        
        # Set up data structures
        self.setup_frame()

        # Start new game
        self.newgame()
        
    def setup_frame(self):
        """
        Create GUI frame and add handlers.
        """
        self._frame = simplegui.create_frame("Tic-Tac-Toe",
                                             GUI_WIDTH,
                                             GUI_HEIGHT)
        self._frame.set_canvas_background('White')
        
        # Set handlers
        self._frame.set_draw_handler(self.draw)
        self._frame.set_mouseclick_handler(self.click)
        self._frame.add_button("New Game", self.newgame)
        self._label = self._frame.add_label("")

    def start(self):
        """
        Start the GUI.
        """
        self._frame.start()

    def newgame(self):
        """
        Start new game.
        """
        self._board = TTTBoard(self._size, self._reverse)
        self._inprogress = True
        self._wait = False
        self._turn = PLAYERX
        self._label.set_text("")
        
    def drawx(self, canvas, pos):
        """
        Draw an X on the given canvas at the given position.
        """
        halfsize = .4 * self._bar_spacing
        canvas.draw_line((pos[0]-halfsize, pos[1]-halfsize),
                         (pos[0]+halfsize, pos[1]+halfsize),
                         BAR_WIDTH, 'Black')
        canvas.draw_line((pos[0]+halfsize, pos[1]-halfsize),
                         (pos[0]-halfsize, pos[1]+halfsize),
                         BAR_WIDTH, 'Black')
        
    def drawo(self, canvas, pos):
        """
        Draw an O on the given canvas at the given position.
        """
        halfsize = .4 * self._bar_spacing
        canvas.draw_circle(pos, halfsize, BAR_WIDTH, 'Black')
        
    def draw(self, canvas):
        """
        Updates the tic-tac-toe GUI.
        """
        # Draw the '#' symbol
        for bar_start in range(self._bar_spacing,
                               GUI_WIDTH - 1,
                               self._bar_spacing):
            canvas.draw_line((bar_start, 0),
                             (bar_start, GUI_HEIGHT),
                             BAR_WIDTH,
                             'Black')
            canvas.draw_line((0, bar_start),
                             (GUI_WIDTH, bar_start),
                             BAR_WIDTH,
                             'Black')
            
        # Draw the current players' moves
        for row in range(self._size):
            for col in range(self._size):
                symbol = self._board.square(row, col)
                coords = self.get_coords_from_grid(row, col)
                if symbol == PLAYERX:
                    self.drawx(canvas, coords)
                elif symbol == PLAYERO:
                    self.drawo(canvas, coords)
                
        # Run AI, if necessary
        if not self._wait:
            self.aimove()
        else:
            self._wait = False
                
    def click(self, position):
        """
        Make human move.
        """
        if self._inprogress and (self._turn == self._humanplayer):        
            row, col = self.get_grid_from_coords(position)
            if self._board.square(row, col) == EMPTY:
                self._board.move(row, col, self._humanplayer)
                self._turn = self._aiplayer
                winner = self._board.check_win()
                if winner is not None:
                    self.game_over(winner)
                self._wait = True
                
    def aimove(self):
        """
        Make AI move.
        """
        if self._inprogress and (self._turn == self._aiplayer):
            row, col = self._aifunction(self._board, 
                                        self._aiplayer, 
                                        self._ntrials)
            if self._board.square(row, col) == EMPTY:
                self._board.move(row, col, self._aiplayer)
            self._turn = self._humanplayer
            winner = self._board.check_win()
            if winner is not None:
                self.game_over(winner)        
            
    def game_over(self, winner):
        """
        Game over
        """
        # Display winner
        if winner == DRAW:
            self._label.set_text("It's a tie!")
        elif winner == PLAYERX:
            self._label.set_text("X Wins!")
        elif winner == PLAYERO:
            self._label.set_text("O Wins!") 
            
        # Game is no longer in progress
        self._inprogress = False

    def get_coords_from_grid(self, row, col):
        """
        Given a grid position in the form (row, col), returns
        the coordinates on the canvas of the center of the grid.
        """
        # X coordinate = (bar spacing) * (col + 1/2)
        # Y coordinate = height - (bar spacing) * (row + 1/2)
        return (self._bar_spacing * (col + 1.0/2.0), # x
                self._bar_spacing * (row + 1.0/2.0)) # y
    
    def get_grid_from_coords(self, position):
        """
        Given coordinates on a canvas, gets the indices of
        the grid.
        """
        posx, posy = position
        return (posy // self._bar_spacing, # row
                posx // self._bar_spacing) # col

def run_gui(board_size, ai_player, ai_function, ntrials, reverse = False):
    """
    Instantiate and run the GUI
    """
    gui = TicTacGUI(board_size, ai_player, ai_function, ntrials, reverse)
    gui.start()

def switch_player(player):
    """
    Convenience function to switch players.
    Returns other player.
    """
    if player == PLAYERX:
        return PLAYERO
    else:
        return PLAYERX

def play_game(mc_move_function, ntrials, reverse = False):
    """
    Function to play a game with two MC players.
    """
    # Setup game
    board = TTTBoard(3, reverse)
    curplayer = PLAYERX
    winner = None
    
    # Run game
    while winner == None:
        # Move
        row, col = mc_move_function(board, curplayer, ntrials)
        board.move(row, col, curplayer)

        # Update state
        winner = board.check_win()
        curplayer = switch_player(curplayer)

        # Display board
        print board
        print
        
    # Print winner
    if winner == PLAYERX:
        print "X wins!"
    elif winner == PLAYERO:
        print "O wins!"
    elif winner == DRAW:
        print "Tie!"
    else:
        print "Error: unknown winner"

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """    
    empty_list = board.get_empty_squares()
    winner = board.check_win()
    score_compare = float("-inf")
    if winner != None:                           # base case
        return SCORES[winner], (-1, -1)
    for children_num in range(len(empty_list)):        
        current_board = board.clone()
        row = empty_list[children_num][0]
        col = empty_list[children_num][1]        
        current_board.move(row, col, player)     # build the new board of subtree
        child_result = mm_move(current_board, switch_player(player))  # count score for subtree
        score = child_result[0]
        score_temporary = score * SCORES[player]
        if score_temporary == 1:                 # found the max or min score we want    
            return score, (row, col)
        else:
            if score_temporary > score_compare:  
                score_compare = score_temporary
                final_score = score
                final_pos = (row, col)   # if there's no max(+1) or min(-1) score we want in subtrees
    return final_score, final_pos        # return the second max(0 or -1) or min(0 or +1) score

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

  
# Uncomment play_game() to test the game 
# with two machine players with console if needed.
       
# play_game(move_wrapper, 1, False)        
run_gui(3, PLAYERO, move_wrapper, 1, False)