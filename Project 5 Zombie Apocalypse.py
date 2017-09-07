"""
Zombie Apocalypse simulation with the application of breadth-first-search.

Click "Mouse click" button to toggle items added by mouse clicks.
Zombies are red cells and humans are green cells. Black cells are impassable obstacles.
Cells that are occupied by both are purple, and since computer scientists
have plenty of brains to spare, they can continue to live on in this simulation. 
Zombies have four way movement, humans have eight way movement.

To fully experience the performance of the game, 
please visit the following URL with Google Chrome.
"http://www.codeskulptor.org/#user43_0QHX4pzDjkfa1tp.py"
"""

import random
import simplegui

# Global constants
EMPTY = 0
FULL = 1
HAS_ZOMBIE = 2
HAS_HUMAN = 4
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7
CELL_COLORS = {EMPTY: "White",
               FULL: "Black",
               HAS_ZOMBIE: "Red",
               HAS_HUMAN: "Green",
               HAS_ZOMBIE|HAS_HUMAN: "Purple"}

NAME_MAP = {OBSTACLE: "obstacle",
            HUMAN: "human",
            ZOMBIE: "zombie"}

# GUI constants
CELL_SIZE = 10
LABEL_STRING = "Mouse click: Add "

class Grid:
    """
    Implementation of 2D grid of cells
    Includes boundary handling
    """
    
    def __init__(self, grid_height, grid_width):
        """
        Initializes grid to be empty, take height and width of grid as parameters
        Indexed by rows (left to right), then by columns (top to bottom)
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
                
    def __str__(self):
        """
        Return multi-line string represenation for grid
        """
        ans = ""
        for row in range(self._grid_height):
            ans += str(self._cells[row])
            ans += "\n"
        return ans
    
    def get_grid_height(self):
        """
        Return the height of the grid for use in the GUI
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Return the width of the grid for use in the GUI
        """
        return self._grid_width

    def clear(self):
        """
        Clears grid to be empty
        """
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]
                
    def set_empty(self, row, col):
        """
        Set cell with index (row, col) to be empty
        """
        self._cells[row][col] = EMPTY
    
    def set_full(self, row, col):
        """
        Set cell with index (row, col) to be full
        """
        self._cells[row][col] = FULL
    
    def is_empty(self, row, col):
        """
        Checks whether cell with index (row, col) is empty
        """
        return self._cells[row][col] == EMPTY
 
    def four_neighbors(self, row, col):
        """
        Returns horiz/vert neighbors of cell (row, col)
        """
        ans = []
        if row > 0:
            ans.append((row - 1, col))
        if row < self._grid_height - 1:
            ans.append((row + 1, col))
        if col > 0:
            ans.append((row, col - 1))
        if col < self._grid_width - 1:
            ans.append((row, col + 1))
        return ans

    def eight_neighbors(self, row, col):
        """
        Returns horiz/vert neighbors of cell (row, col) as well as
        diagonal neighbors
        """
        ans = []
        if row > 0:
            ans.append((row - 1, col))
        if row < self._grid_height - 1:
            ans.append((row + 1, col))
        if col > 0:
            ans.append((row, col - 1))
        if col < self._grid_width - 1:
            ans.append((row, col + 1))
        if (row > 0) and (col > 0):
            ans.append((row - 1, col - 1))
        if (row > 0) and (col < self._grid_width - 1):
            ans.append((row - 1, col + 1))
        if (row < self._grid_height - 1) and (col > 0):
            ans.append((row + 1, col - 1))
        if (row < self._grid_height - 1) and (col < self._grid_width - 1):
            ans.append((row + 1, col + 1))
        return ans
    
    def get_index(self, point, cell_size):
        """
        Takes point in screen coordinates and returns index of
        containing cell
        """
        return (point[1] / cell_size, point[0] / cell_size) 

class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return the number of items in the queue.
        """
        return len(self._items)
    
    def __iter__(self):
        """
        Create an iterator for the queue.
        """
        for item in self._items:
            yield item

    def __str__(self):
        """
        Return a string representation of the queue.
        """
        return str(self._items)

    def enqueue(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)

    def dequeue(self):
        """
        Remove and return the least recently inserted item.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []        
    
class Apocalypse(Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        Grid.clear(self)        
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        num = 0
        while num < self.num_zombies():
            yield self._zombie_list[num]
            num += 1

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for idx in range(self.num_humans()):
            yield self._human_list[idx]
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        # visited is used to check whether the grid has been searched as a neighbor
        visited = [[EMPTY for dummy_col in range(self._grid_width)]
                   for dummy_row in range(self._grid_height)]
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)]
                          for dummy_row in range(self._grid_height)]
        
        # boundry is a waiting list for grids to be checked
        # create a copy of either the zombie or the human list 
        boundary = Queue() 
        if entity_type == ZOMBIE:            
            for item in self._zombie_list:
                boundary.enqueue(item)
        else:
            for item in self._human_list:
                boundary.enqueue(item)
        
        # set visited to be FULL and distance_field to be zero
        for item in boundary:
            visited[item[0]][item[1]] = FULL
            distance_field[item[0]][item[1]] = 0
        
        # BFS search
        while len(boundary) != 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor_cell in neighbors:
                # if this grid has not been searched and is not a obstacle
                if visited[neighbor_cell[0]][neighbor_cell[1]] == EMPTY and self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    visited[neighbor_cell[0]][neighbor_cell[1]] = FULL
                    boundary.enqueue(neighbor_cell)
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                    
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for human in self.humans():
            neighbors = self.eight_neighbors(human[0], human[1])
            neighbors.append(human) # human can stay in current cell
            human_plus_neighbors = neighbors
            distance = []             
            for cell in human_plus_neighbors:
                if self.is_empty(cell[0], cell[1]): # if not a obstacle
                    distance.append(zombie_distance_field[cell[0]][cell[1]])            
            max_distance = max(distance) # maximize its distance from zombie
            possible_move = []
            for cell in human_plus_neighbors:
                if zombie_distance_field[cell[0]][cell[1]] == max_distance and self.is_empty(cell[0], cell[1]):
                    possible_move.append(cell)
            move = random.choice(possible_move)            
            idx = self._human_list.index(human)
            self._human_list[idx] = move # make human move to the grid       
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in self.zombies():
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            neighbors.append(zombie) # zombie can stay in current cell
            zombie_plus_neighbors = neighbors
            distance = []
            for cell in zombie_plus_neighbors:
                if self.is_empty(cell[0], cell[1]): # if not a obstacle
                    distance.append(human_distance_field[cell[0]][cell[1]])            
            min_distance = min(distance) # minimize its distance to human
            possible_move = []
            for cell in zombie_plus_neighbors:
                if human_distance_field[cell[0]][cell[1]] == min_distance and self.is_empty(cell[0], cell[1]):
                    possible_move.append(cell)
            move = random.choice(possible_move)            
            idx = self._zombie_list.index(zombie)
            self._zombie_list[idx] = move # make zombie move to the grid
            
class ApocalypseGUI:
    """
    Container for interactive content
    """

    def __init__(self, simulation):
        """
        Create frame and timers, register event handlers
        """
        self._simulation = simulation
        self._grid_height = self._simulation.get_grid_height()
        self._grid_width = self._simulation.get_grid_width()
        self._frame = simplegui.create_frame("Zombie Apocalypse simulation",
                                             self._grid_width * CELL_SIZE,
                                             self._grid_height * CELL_SIZE)
        self._frame.set_canvas_background("White")
        self._frame.add_button("Clear all", self.clear, 200)
        self._item_type = OBSTACLE

        label = LABEL_STRING + NAME_MAP[self._item_type]
        self._item_label = self._frame.add_button(label,
                                                  self.toggle_item, 200)
        self._frame.add_button("Humans flee", self.flee, 200)
        self._frame.add_button("Zombies stalk", self.stalk, 200)
        self._frame.set_mouseclick_handler(self.add_item)
        self._frame.set_draw_handler(self.draw)

    def start(self):
        """
        Start frame
        """
        self._frame.start()

    def clear(self):
        """
        Event handler for button that clears everything
        """
        self._simulation.clear()

    def flee(self):
        """
        Event handler for button that causes humans to flee zombies by one cell
        Diagonal movement allowed
        """
        zombie_distance = self._simulation.compute_distance_field(ZOMBIE)
        self._simulation.move_humans(zombie_distance)

    def stalk(self):
        """
        Event handler for button that causes zombies to stack humans by one cell
        Diagonal movement not allowed
        """
        human_distance = self._simulation.compute_distance_field(HUMAN)
        self._simulation.move_zombies(human_distance)

    def toggle_item(self):
        """
        Event handler to toggle between new obstacles, humans and zombies
        """
        if self._item_type == OBSTACLE:
            self._item_type = ZOMBIE
            self._item_label.set_text(LABEL_STRING + NAME_MAP[ZOMBIE])
        elif self._item_type == ZOMBIE:
            self._item_type = HUMAN
            self._item_label.set_text(LABEL_STRING + NAME_MAP[HUMAN])
        elif self._item_type == HUMAN:
            self._item_type = OBSTACLE
            self._item_label.set_text(LABEL_STRING + NAME_MAP[OBSTACLE])

    def add_item(self, click_position):
        """
        Event handler to add new obstacles, humans and zombies
        """
        row, col = self._simulation.get_index(click_position, CELL_SIZE)
        if self._item_type == OBSTACLE:
            if not self.is_occupied(row, col):
                self._simulation.set_full(row, col)
        elif self._item_type == ZOMBIE:
            if self._simulation.is_empty(row, col):
                self._simulation.add_zombie(row, col)
        elif self._item_type == HUMAN:
            if self._simulation.is_empty(row, col):
                self._simulation.add_human(row, col)

    def is_occupied(self, row, col):
        """
        Determines whether the given cell contains any humans or zombies
        """
        cell = (row, col)
        human = cell in self._simulation.humans()
        zombie = cell in self._simulation.zombies()
        return human or zombie

    def draw_cell(self, canvas, row, col, color="Cyan"):
        """
        Draw a cell in the grid
        """
        upper_left = [col * CELL_SIZE, row * CELL_SIZE]
        upper_right = [(col + 1) * CELL_SIZE, row * CELL_SIZE]
        lower_right = [(col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE]
        lower_left = [col * CELL_SIZE, (row + 1) * CELL_SIZE]
        canvas.draw_polygon([upper_left, upper_right,
                             lower_right, lower_left],
                            1, "Black", color)

    def draw_grid(self, canvas, grid):
        """
        Draw entire grid
        """
        for col in range(self._grid_width):
            for row in range(self._grid_height):
                status = grid[row][col]
                if status in CELL_COLORS:
                    color = CELL_COLORS[status]
                    if color != "White":
                        self.draw_cell(canvas, row, col, color)
                else:
                    if status == (FULL | HAS_HUMAN):
                        raise ValueError, "human moved onto an obstacle"
                    elif status == (FULL | HAS_ZOMBIE):
                        raise ValueError, "zombie moved onto an obstacle"
                    elif status == (FULL | HAS_HUMAN | HAS_ZOMBIE):
                        raise ValueError, "human and zombie moved onto an obstacle"
                    else:
                        raise ValueError, "invalid grid status: " + str(status)

    def draw(self, canvas):
        """
        Handler for drawing obstacle grid, human queue and zombie queue
        """
        grid = [[FULL] * self._grid_width for
                dummy_row in range(self._grid_height)]
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._simulation.is_empty(row, col):
                    grid[row][col] = EMPTY
        for row, col in self._simulation.humans():
            grid[row][col] |= HAS_HUMAN
        for row, col in self._simulation.zombies():
            grid[row][col] |= HAS_ZOMBIE
        self.draw_grid(canvas, grid)

# Start interactive simulation
def run_gui(sim):
    """
    Encapsulate frame
    """
    gui = ApocalypseGUI(sim)
    gui.start()
            
run_gui(Apocalypse(30, 40))
