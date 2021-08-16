#!/usr/bin/python
import sys
import argparse

def cross(a, b):
    """
    Given two strings — a and b — will return the list formed 
    by all the possible concatenations of a letter s in string a with a letter t in string b
    """ 
    return [s+t for s in a for t in b]

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(i_string):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.
    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    if len(i_string) > 81:
        sys.stdout.write("Input string is longer than 81 characters. Exiting.\n")
        sys.exit(1)
    # returns a zip object, which is an iterator of tuples where the first item in each passed iterator is paired together, 
    # and then the second item in each passed iterator are paired together etc.
    # If the passed iterators have different lengths, the iterator with the least items decides the length of the new iterator.
    result_dict = dict(zip(boxes,i_string))
    all_values = '123456789'
    # instead of empty value store all possible values for now
    for key in result_dict:
        if result_dict[key] == '.' or result_dict[key] == '':
            result_dict[key] = all_values
    return result_dict

################################################################################
# REDUCING TECHNIQUE - Elimination
################################################################################
def eliminate(sudoku_dict):
    """
    Eliminate values from peers of each box with a single value.
    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for key_sd in sudoku_dict:
        current_value = sudoku_dict[key_sd]
        if len(str(current_value)) == 1:
            # returns a dict with all its peers
            current_peers = peers[key_sd]
            for key_cp in current_peers:
                sudoku_dict[key_cp] = sudoku_dict[key_cp].replace(current_value,'')
    return sudoku_dict

################################################################################
# REDUCING TECHNIQUE - Only choice
################################################################################
def only_choice(sudoku_dict):
    """
    Finalize all values that are the only choice for a unit.
    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    possible_values = ['1','2','3','4','5','6','7','8','9']
    for unit in unitlist:
        for v in possible_values:
            box_list_found_v = [box for box in unit if v in sudoku_dict[box]]
            if len(box_list_found_v) == 1:
                sudoku_dict[box_list_found_v[0]] = v
    return sudoku_dict

def reduce_puzzle(sudoku_dict):
    stalled = False
    while(not(stalled)):

        # Check how many boxes have a determined value
        solved_values_before = len([box for box in sudoku_dict.keys() if len(sudoku_dict[box]) == 1])

        # if the sudoku is solved return the dictionary (i.e all nodes have only one value)
        if solved_values_before == len(boxes):
            return sudoku_dict

        # Use the Eliminate Strategy
        sudoku_dict = eliminate(sudoku_dict)

        # Use the Only Choice Strategy
        sudoku_dict = only_choice(sudoku_dict)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in sudoku_dict.keys() if len(sudoku_dict[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

    # Sanity check, return False if there is a box with zero available values:
    if len([box for box in sudoku_dict.keys() if len(sudoku_dict[box]) == 0]):
        return False
    return sudoku_dict

def df_search(sudoku_dict):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    """

    # First, reduce the puzzle
    sudoku_dict = reduce_puzzle(sudoku_dict)

    # if reducing the puzzle returned false (box with zero available values)
    # try the next puzzle in the tree
    if sudoku_dict is False:
        return False

    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_nodes_len = {}
    for key in sudoku_dict:
        if len(sudoku_dict[key]) > 1:
            unsolved_nodes_len[key] = len(sudoku_dict[key])

    # exit condition: return the dict if it's solved
    if len(unsolved_nodes_len) == 0:
        return sudoku_dict

    # box that is unsolved, but has the fewest choices to start the search
    unsolved_node_min_values = min(unsolved_nodes_len, key=unsolved_nodes_len.get)
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer
    for digit in sudoku_dict[unsolved_node_min_values]:
        # need to copy by value and not by reference
        tmp_sudoku_dict = sudoku_dict.copy()
        tmp_sudoku_dict[unsolved_node_min_values] = digit
        # recurse with the new dict
        attempt = df_search(tmp_sudoku_dict)
        if isinstance(attempt,dict) and len([box for box in attempt.keys() if len(attempt[box]) > 1]) == 0:
            break

    return attempt

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# dictionaries of units and peers given a key representing a box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def solve(input):
    if(len(input) != 81):
        return "The 3x3 Sudoku should have 81 cells."
    if(isinstance(input,str)):
        values = grid_values(input)
    else:
        values = input
    out = df_search(values)
    return out

def main(argv):
    parser = argparse.ArgumentParser(description='Sudoku Solver.')
    parser.add_argument('-i', '--input', type=str, help='The input sudoku as an 81 character string.', required=True)
    args = vars(parser.parse_args())
    #values = grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
    #values = grid_values('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
    out = solve(args['input'])
    print("=" * 100)
    print("====== INPUT ======")
    display(grid_values(args['input']))
    print("=" * 100)
    print("====== OUTPUT ======")
    display(out)

if __name__ == "__main__":
    main(sys.argv[1:])
