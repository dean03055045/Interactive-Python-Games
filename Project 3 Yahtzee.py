""" 
Implement a strategy function for Yahtzee with the application of Combinatorics.

Yahtzee is a dice game played with 5 dice where player try to 
score the most points by matching certain combinations. 

This function will consider all possible choices of dice to hold and recommend 
the choice that maximizes the expected value of player's score after the final roll.

Simplifications: only allow discard and roll, only score against upper level

To fully experience the performance of this function, 
please visit the following URL with Google Chrome.
"http://www.codeskulptor.org/#user43_LtwkxJjN8m6u9qM.py"
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    score_list = []
    for value in hand:
        each_score = value * hand.count(value)
        score_list.append(each_score)            
    if score_list == []:
        return 0
    else:
        return max(score_list)

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = set(range(1, num_die_sides + 1))
    sequences = gen_all_sequences(outcomes, num_free_dice)
    exp_value = 0
    for sequence in sequences:
        seq_list = list(sequence)
        held_list = list(held_dice)
        seq_list.extend(held_list)
        tuple(seq_list)
        exp_value += score(seq_list) * 1.0/(num_die_sides ** num_free_dice)    
    return exp_value

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_holds = set([()])
    for dummy in range(len(hand)+1):
        length = dummy
        hold = gen_all_sequences(hand, length)
        all_holds.update(hold)
    # check whether the dice has already being held 
    for hold in set(all_holds):
        for num in hand:
            if hand.count(num) < hold.count(num):
                all_holds.discard(hold)
    sorted_holds = [tuple(sorted(holds))for holds in all_holds]
    return set(sorted_holds)
        
def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    holds = gen_all_holds(hand)
    exp_value_list = []
    for hold in holds:
        num_free_dice = len(hand) - len(hold)
        exp_value = expected_value(hold, num_die_sides, num_free_dice)
        exp_value_list.append(exp_value)
    max_value = max(exp_value_list)
    hold_list = list(holds)
    should_hold = hold_list[exp_value_list.index(max_value)]    
    return (max_value, should_hold)

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

# Test suite for gen_all_holds(hands), uncomment if needed
# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)
                                       