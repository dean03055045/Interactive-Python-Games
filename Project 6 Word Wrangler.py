"""
Implement a Word Wrangler game with the application of recursion
and the concept of ordered data.

This game will take an input word and generate all valid words
that can be created using the letters in the input word. 
Player then play the game by guessing all of the words.

To fully experience the performance of the game, 
please visit the following URL with Google Chrome.
"http://www.codeskulptor.org/#user43_4ViESGEhezlR3eD.py"
"""

import urllib2
import codeskulptor
import simplegui

WORDFILE = "assets_scrabble_words3.txt"

# Global constants
FONT_SIZE = 20
OFFSET = 4
ROW_HEIGHT = FONT_SIZE + OFFSET
COLUMN_WIDTH = 80
GRID_SIZE = [25, 4]
CANVAS_WIDTH = COLUMN_WIDTH * GRID_SIZE[1]
CANVAS_HEIGHT = ROW_HEIGHT * GRID_SIZE[0]


def draw_word(canvas, word, pos):
    """
    Helper function to draw word on canvas at given position
    """
    box = [pos, 
           [pos[0], pos[1] - ROW_HEIGHT], 
           [pos[0] + COLUMN_WIDTH, pos[1] - ROW_HEIGHT], 
           [pos[0] + COLUMN_WIDTH, pos[1]], 
           pos]
    canvas.draw_text(word, [pos[0] + 2, pos[1] - 4], FONT_SIZE, "White")
    canvas.draw_polyline(box, 1, "White")

class WordWranglerGUI:
    """
    Container for interactive content
    """    

    def __init__(self, game):
        """ 
        Create frame and timers, register event handlers
        """
        self.game = game
        self.frame = simplegui.create_frame("Word Wrangler", 
                                            CANVAS_WIDTH, CANVAS_HEIGHT, 250)
        self.frame.set_canvas_background("Blue")        
               
        self.enter_input = self.frame.add_input("Enter word for new game", 
                                                self.enter_start_word, 250)
        labelmsg = "Stars correspond to hidden words formed using letters "
        labelmsg += "from the entered word. Hidden words are listed in alphabetical order"
        self.frame.add_label(labelmsg, 250)
        self.frame.add_label("", 250)
        self.guess_label = self.frame.add_input("Enter a word", 
                                                self.enter_guess, 250)       
        self.frame.add_label("For a hint, click on a starred word", 250)
        self.frame.set_mouseclick_handler(self.peek)
        self.frame.set_draw_handler(self.draw)

        self.enter_input.set_text("python")
        self.game.start_game("python")
        
    def start(self):
        """
        Start frame
        """
        self.frame.start()
        
    def enter_start_word(self, entered_word):
        """ 
        Event handler for input field to enter letters for new game
        """
        self.game.start_game(entered_word)

    def enter_guess(self, guess):
        """ 
        Event handler for input field to enter guess
        """
        self.game.enter_guess(guess)
        self.guess_label.set_text("")

    def peek(self, pos):
        """ 
        Event handler for mouse click, exposes clicked word
        """
        [index_i, index_j] = [pos[1] // ROW_HEIGHT, pos[0] // COLUMN_WIDTH]
        peek_idx = index_i + index_j * GRID_SIZE[0]
        if peek_idx < len(self.game.get_strings()):
            self.game.peek(peek_idx)
                         
    def draw(self, canvas):
        """
        Handler for drawing subset words list
        """
        string_list = self.game.get_strings()
        
        for col in range(GRID_SIZE[1]):
            for row in range(GRID_SIZE[0]):
                pos = [col * COLUMN_WIDTH, (row + 1) * ROW_HEIGHT]
                idx = row + col * GRID_SIZE[0]
                if idx < len(string_list):
                    draw_word(canvas, string_list[idx], pos)


class WordWrangler:
    """
    Game class for Word Wrangler
    """
    
    def __init__(self, word_list, remdup, intersect, mergesort, substrs):
        self._word_list = word_list
        self._subset_strings = []
        self._guessed_strings = []

        self._remove_duplicates = remdup
        self._intersect = intersect
        self._merge_sort = mergesort
        self._substrs = substrs

    def start_game(self, entered_word):
        """
        Start a new game of Word Wrangler
        """
        if entered_word not in self._word_list:
            print "Not a word"
            return
        
        strings = self._substrs(entered_word)
        sorted_strings = self._merge_sort(strings)
        all_strings = self._remove_duplicates(sorted_strings)
        self._subset_strings = self._intersect(self._word_list, all_strings)
        self._guessed_strings = []        
        for word in self._subset_strings:
            self._guessed_strings.append("*" * len(word))
        self.enter_guess(entered_word)           
        
    def enter_guess(self, guess):
        """
        Take an entered guess and update the game
        """        
        if ((guess in self._subset_strings) and 
            (guess not in self._guessed_strings)):
            guess_idx = self._subset_strings.index(guess)
            self._guessed_strings[guess_idx] = self._subset_strings[guess_idx]

    def peek(self, peek_index):
        """
        Exposed a word given in index into the list self._subset_strings
        """
        self.enter_guess(self._subset_strings[peek_index])
        
    def get_strings(self):
        """
        Return the list of strings for the GUI
        """
        return self._guessed_strings    

    
def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    """
    new_list = list(list1)
    for item in list1:
        while new_list.count(item) > 1:
            new_list.remove(item)
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    """
    new_list = []
    idx_i = 0
    idx_j = 0
    while idx_i < len(list1) and idx_j < len(list2):
        if list1[idx_i] == list2[idx_j]:
            new_list.append(list1[idx_i])
            idx_i += 1
            idx_j += 1
        elif list1[idx_i] < list2[idx_j]:
            idx_i += 1
        else:
            idx_j += 1    
    return new_list

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.
    """   
    copy_list1 = list(list1)
    copy_list2 = list(list2)
    new_list = []
    while len(copy_list1) > 0 and len(copy_list2) > 0:
        if copy_list1[0] <= copy_list2[0]:
            new_list.append(copy_list1[0])
            copy_list1.pop(0)
        else:
            new_list.append(copy_list2[0])
            copy_list2.pop(0)
    new_list.extend(copy_list1)
    new_list.extend(copy_list2)
    return new_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """    
    if len(list1) <= 1: # base case
        return list1
    length = len(list1) / 2
    new_list1 = list(list1[:length])
    new_list2 = list(list1[length:])
    sorted_new_list1 = merge_sort(new_list1)
    sorted_new_list2 = merge_sort(new_list2)
    return merge(sorted_new_list1, sorted_new_list2)

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0: # base case
        return [word]
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    new_strings = []
    for item in rest_strings: # insert first in all possible positions    
        for index in range(len(item) + 1):
            new_item = list(item)
            new_item.insert(index, first)
            new_word = ""
            for letter in new_item:
                new_word += letter
            new_strings.append(new_word)
    return new_strings + rest_strings    

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    dictionary_file = urllib2.urlopen(codeskulptor.file2url(filename))
    word_list = []
    for line in dictionary_file.readlines():
        word_list.append(line[:-1])
    return word_list
   
def run_gui(game):
    """
    Encapsulate frame
    """
    gui = WordWranglerGUI(game)
    gui.start()

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = WordWrangler(words, remove_duplicates, intersect, merge_sort, gen_all_strings)
    run_gui(wrangler)


run()
