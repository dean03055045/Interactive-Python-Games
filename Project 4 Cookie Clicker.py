"""
Implement a simplified simulation of the Cookie Clicker game,
with the application of higher order functions and the principle
of function growth rate.

Cookie Clicker is a web game built around a simulation in which
your goal is to bake as many cookies as fast as possible. The main
strategy component of the game is choosing how to allocate the 
cookies that you have produced to upgrade your ability (buy 
different tools) to produce even more cookies faster.

In this simplified version, instead of actual "clicking", player
will start with a "cookies per second" (CPS) of 1.0.

To fully experience the performance of this project,
please visit the following URL with Google Chrome.
"http://www.codeskulptor.org/#user43_Gzh7SlNlEHKslnL.py"
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

# Constants
SIM_TIME = 5000.0
BUILD_GROWTH = 1.15

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._cookies = 0.0 # total cookies produced throughout the game
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0 # cps = cookies per second
        self._history = [(0.0, None, 0.0, 0.0)] #(time, item, cost of item, total cookies)
        
    def __str__(self):
        """
        Return human readable state
        """
        return ("\n" + "Time: " + str(self._current_time) + "\n" +
                "Current Cookies: " + str(self._current_cookies) + "\n" + 
                "CPS: " + str(self._current_cps) + "\n" + 
                "Total Cookies: " + str(self._cookies) + "\n")    
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """        
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= cookies:
            waiting_time = 0.0
        else:
            waiting_time = math.ceil((cookies - self._current_cookies) / self._current_cps)
        return waiting_time
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        else:
            self._cookies += self._current_cps * time
            self._current_cookies += self._current_cps * time
            self._current_time += time
                
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self._current_cookies:
            return
        else:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._cookies))
    
    def print_history(self):
        """
        Print history list for code checking
        """
        print self._history
    
class BuildInfo:
    """
    Class to track build information.
    """
    
    def __init__(self, build_info = None, growth_factor = BUILD_GROWTH):
        self._build_growth = growth_factor
        if build_info == None:
            self._info = {"Cursor": [15.0, 0.1],
                          "Grandma": [100.0, 0.5],
                          "Farm": [500.0, 4.0],
                          "Factory": [3000.0, 10.0],
                          "Mine": [10000.0, 40.0],
                          "Shipment": [40000.0, 100.0],
                          "Alchemy Lab": [200000.0, 400.0],
                          "Portal": [1666666.0, 6666.0],
                          "Time Machine": [123456789.0, 98765.0],
                          "Antimatter Condenser": [3999999999.0, 999999.0]}
        else:
            self._info = {}
            for key, value in build_info.items():
                self._info[key] = list(value)

        self._items = sorted(self._info.keys())
            
    def build_items(self):
        """
        Get a list of buildable items
        """
        return list(self._items)
            
    def get_cost(self, item):
        """
        Get the current cost of an item
        Will throw a KeyError exception if item is not in the build info.
        """
        return self._info[item][0]
    
    def get_cps(self, item):
        """
        Get the current CPS of an item
        Will throw a KeyError exception if item is not in the build info.
        """
        return self._info[item][1]
    
    def update_item(self, item):
        """
        Update the cost of an item by the growth factor
        Will throw a KeyError exception if item is not in the build info.
        """
        cost, cps = self._info[item]
        self._info[item] = [cost * self._build_growth, cps]
        
    def clone(self):
        """
        Return a clone of this BuildInfo
        """
        return BuildInfo(self._info, self._build_growth)

    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    clone = build_info.clone()
    new_game = ClickerState()
    current_time = new_game.get_time()
    while current_time <= duration:
        # check current time
        current_time = new_game.get_time() 
        if current_time > duration: 
            break
        left_time = duration - current_time
        # determine which item to buy next
        item = strategy(new_game.get_cookies(), new_game.get_cps(), new_game.get_history(), left_time, clone)
        if item == None: 
            break
        # determine how much time to wait
        waiting_time = new_game.time_until(clone.get_cost(item))
        if current_time + waiting_time > duration: 
            break
        new_game.wait(waiting_time)
        new_game.buy_item(item, clone.get_cost(item), clone.get_cps(item))
        clone.update_item(item)
    remaining_time = duration - current_time
    new_game.wait(remaining_time)
    return new_game


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left,
    simulate_clicker function must be able to deal with such broken
    strategies. Further, strategy functions must correctly check
    if player can buy the item in the time left and return None if can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    item_list = build_info.build_items()
    cost_list = [build_info.get_cost(item) for item in item_list]
    cheapest_cost = min(cost_list)
    cheapest_idx = cost_list.index(cheapest_cost)
    max_cookies = cookies + cps * time_left
    if cheapest_cost > max_cookies:
        return None
    else:
        return item_list[cheapest_idx]    

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    item_list = build_info.build_items()
    cost_list = [build_info.get_cost(item) for item in item_list]
    clone_cost_list = [build_info.get_cost(item) for item in item_list]
    max_cookies = cookies + cps * time_left    
    for cost in list(cost_list):
        if cost > max_cookies:            
            cost_list.remove(cost)            
    if cost_list == []:
        return None
    else:
        most_expensive_cost = max(cost_list)
        most_expensive_idx = clone_cost_list.index(most_expensive_cost)
        return item_list[most_expensive_idx]
         
def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    Devided cost by CPS and buy the most cost-effective item.
    """
    item_list = build_info.build_items()
    item_cost_cps_list = [(build_info.get_cost(item) / build_info.get_cps(item),
                           build_info.get_cost(item), item) for item in item_list]    
    sorted_item_cost_cps_list = sorted(item_cost_cps_list)
    max_cookies = cookies + cps * time_left
    for item in sorted_item_cost_cps_list:
        if max_cookies >= item[1]:
            return item[2]
    return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """        
    # Add calls to run_strategy to run additional strategies
    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    