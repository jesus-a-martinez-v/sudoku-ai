## Diagonal Sudoku Solver

Diagonal Sudoku Solver implemented using Constraint Propagation and Search techniques as part of the [Artificial Intelligence Nanodegree by Udacity](https://www.udacity.com/course/artificial-intelligence-nanodegree--nd889). A diagonal sudoku is similar to a traditional sudoku, with the added requirement that no value can repeat in any diagonal.

# How do we use constraint propagation to solve the naked twins problem?  
To reduce the number of possibilities and search space, we made use of an strategy called Naked Snakes, which consists of finding boxes within a given unit that share the same pair of possibilities (for instance, 2 and 6). Then, all remaining boxes in that unit must discard 2 and 6 as possibilities given that either option will be assigned to one of the twins. Here's the code that applies this strategy: 

```
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
```

# How do we use constraint propagation to solve the diagonal sudoku problem?  
 In order of being able to solve diagonal sudokus, we constrained our solution by forbidding repeated values along the two diagonals (A1, B2, C3, D4, E5, F6, G7, H8, I9 and A9,  B8, C7, D6, E5, F4, G3, H2, I1). More concretely, no number can be repeated within the same unit, where a unit is a row, a column, a diagonal or a 3x3 square.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see our visualization.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Pretty straightforward.
* `solution_test.py` - Code for testing the solution by running `python solution_test.py`.
* `PySudoku.py` - Code for visualizing the solution.
* `visualize.py` - Code for visualizing the solution.


### Environment

```
conda env -f aind-environment-unix.yml
source activate aind
```