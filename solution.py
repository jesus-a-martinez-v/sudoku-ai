assignments = []


def assign_value(values, box, value):
    """
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def cross(string1, string2):
    """Cross product of elements in A and elements in B."""
    return [x + y for x in string1 for y in string2]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81

    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    """Eliminates repeated values among peer boxes."""
    for box, val in values.items():
        if len(val) == 1:
            box_peers = peers[box]

            for p in box_peers:
                values = assign_value(values, p, values[p].replace(val, ''))

    return values


def only_choice(values):
    # Remember: An unit is a row or a column, or a 3x3 square.
    for unit in units_list:
        # For each digit, check in how many places it appears.
        for digit in "123456789":
            digit_places = [box for box in unit if digit in values[box]]

            # If appears in only one box in the unit, then that box should contain that digit.
            if len(digit_places) == 1:
                values = assign_value(values, digit_places[0], digit)

    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    def find_twins(unit_of_interest):
        # Let's select the boxes with only two values as our twin candidates.
        possible_twins = [b for b in unit_of_interest if len(values[b]) == 2]

        # In order to consider the possibility of twins, we'll need at least two candidates.
        if len(possible_twins) >= 2:
            for i, first_candidate in enumerate(possible_twins):
                for j in range(i + 1, len(possible_twins)):
                    second_candidate = possible_twins[j]
                    if values[first_candidate] == values[second_candidate]:
                        return first_candidate, second_candidate
        return None

    def eliminate_twin_possibilities_from_peers(maybe_twins, unit_of_interest, current_values):
        if maybe_twins:
            first_twin_box, second_twin_box = maybe_twins
            twin_values = current_values[first_twin_box]

            for peer in unit_of_interest:
                if peer != first_twin_box and peer != second_twin_box:
                    peer_values = current_values[peer]
                    for digit in peer_values:
                        if digit in twin_values:
                            current_values = assign_value(current_values, peer, current_values[peer].replace(digit, ''))

        return current_values

    for unit in units_list:
        twins = find_twins(unit)
        values = eliminate_twin_possibilities_from_peers(twins, unit, values)

    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Apply strategies
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = (solved_values_before == solved_values_after)

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values: dict):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False
    elif all(len(v) == 1 for _, v in values.items()):
        return values

    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recurrence to solve each one of the resulting sudokus
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    values = grid_values(grid)
    return search(values)
    # return False


rows = "ABCDEFGHI"
cols = "123456789"

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows, cols[::-1])]]
units_list = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in units_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)

if __name__ == '__main__':
    diagonal_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    representation = solve(diagonal_sudoku_grid)
    if representation is not False:
        display(representation)
    else:
        print("Unsolvable puzzle.")

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
