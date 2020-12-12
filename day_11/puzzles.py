import numpy as np

SEAT_LAYOUT_FILE = "seat_layout.txt"

SEAT_EMPTY = 0
SEAT_OCCUPIED = 1
FLOOR = -1

def get_seat_layout_matrix():
    """
    Return the content of above file as a matrix:
    - 1 if seat is empty (:= 'L')
    - -1 if floor (:= '.')
    - occupied seats (:= '#') do not need to be taken into account as all seats are empty)
    """
    seat_layout_matrix = None

    with open(SEAT_LAYOUT_FILE, 'r') as seat_layout_file:
        for seat_row in seat_layout_file:
            seat_row = seat_row.strip()
            if seat_layout_matrix is None:
                # initialize matrix once (number of columns known)
                seat_layout_matrix = np.empty([0, len(seat_row)], dtype=int)

            # create new row with respective entries set to 0 (:= L) or -1 (:= .)
            matrix_row = []
            for seat in seat_row:
                matrix_row.append(SEAT_EMPTY if seat == 'L' else FLOOR)

            # add row to matrix
            seat_layout_matrix = np.append(seat_layout_matrix, np.array([matrix_row]), axis=0)

    return seat_layout_matrix

def simulate_rounds_until_stabilization(seat_layout, is_puzzle_1=True):
    """
    Start simulating different rounds, always changing the seat_layout. Once the layout does
    not change anymore, a stable state is reached. Then, stop simulation and return the current
    seat layout.
    If 'is_puzzle_1' is set, the simulation for puzzle 1 is executed, otw. for puzzle 2
    """
    current_seat_layout = seat_layout.copy()
    current_round = 1

    # set function to be run depending on the given flag
    simulate_one_round = simulate_one_round_puzzle_1 if is_puzzle_1 else\
                         simulate_one_round_puzzle_2

    while(True):
        print("Round #{}".format(current_round))

        simulated_seat_layout = simulate_one_round(current_seat_layout)

        # stable state reached?
        if np.all(current_seat_layout == simulated_seat_layout):
            break

        # update current seat layout matrix
        current_seat_layout = simulated_seat_layout
        current_round += 1

    return current_seat_layout

def number_of_occupied_seats(surrounding_seat_area):
    """
    Check, how many occupied seats (:= 1) are within given 'surrounding_seat_area':
    """
    return np.sum(surrounding_seat_area==SEAT_OCCUPIED)

# -------------------------- Puzzle 1 --------------------------

def simulate_one_round_puzzle_1(current_seat_layout):
    """
    Simulate one round of seat occupying / leaving according to following rules:
    - if a seat is empty and there are no occupied adjascent seats within range of 8 seats,
      the seat becomes occupied
    - if a seat is occupied and there are four or more adjacent seats occupied,
      the seat becomes empty
    """
    simulated_seat_layout = current_seat_layout.copy()
    max_row_idx, max_col_idx = current_seat_layout.shape

    # iterate over each matrix element and check adjacent 8 neighbours
    for row_idx, row in enumerate(current_seat_layout):
        for col_idx, col in enumerate(row):
            # only consider seats
            if col != FLOOR:
                # create surrounding area
                top, bottom, left, right = compute_surrounding_area(row_idx, col_idx,\
                                                                    max_row_idx, max_col_idx)
                surrounding_seat_area = current_seat_layout[top : bottom, left : right]

                nb_of_occupied_seats = number_of_occupied_seats(surrounding_seat_area)

                if col == SEAT_EMPTY:
                    if nb_of_occupied_seats == 0:
                        # no occupied seats -> seat occupied from now on
                        simulated_seat_layout[row_idx, col_idx] = SEAT_OCCUPIED

                elif col == SEAT_OCCUPIED:
                    if nb_of_occupied_seats > 4:
                        # 4 or more occupied seats (without current seat) -> seat is empty from now on
                        simulated_seat_layout[row_idx, col_idx] = SEAT_EMPTY

    return simulated_seat_layout

def compute_surrounding_area(row_idx, col_idx, max_row_idx, max_col_idx):
    """
    Use given input to calculate the indices required for spinning up the surrounding area
    by taking only adjacent seats into account.
    Adjacent seats are defined to be one of the eight positions to the lef, right, above,
    below or diagonal to current seat.
    """
    top = row_idx - 1 if (row_idx - 1) > 0 else 0
    bottom = row_idx + 2 if (row_idx + 2) < max_row_idx else max_row_idx
    left = col_idx - 1 if (col_idx - 1) > 0 else 0
    right = col_idx + 2 if (col_idx + 2) < max_col_idx else max_col_idx

    return top, bottom, left, right

# -------------------------- Puzzle 2 --------------------------

def simulate_one_round_puzzle_2(current_seat_layout):
    """
    Simulate one round of seat occupying / leaving according to following rules:
    - if all adjacent seats (which can be seen from current seat) are empty, occupy seat
    - if 5 or more adjacent seats (whic can be seen from current seat) are occupied, leave seat
    """
    simulated_seat_layout = current_seat_layout.copy()

    # iterate over each matrix element and check adjacent neighbours
    for row_idx, row in enumerate(current_seat_layout):
        for col_idx, col in enumerate(row):
            # only consider seats
            if col != FLOOR:
                number_of_occupied_seats = number_of_occupied_seats_seen_from_current_seat(current_seat_layout,\
                                                                                           row_idx, col_idx)
                if col == SEAT_EMPTY:
                    if number_of_occupied_seats == 0:
                        # no occupied seats -> seat occupied from now on
                        simulated_seat_layout[row_idx, col_idx] = SEAT_OCCUPIED

                elif col == SEAT_OCCUPIED:
                    if number_of_occupied_seats >= 5:
                        # 5 or more occupied seats (without current seat) -> seat is empty from now on
                        simulated_seat_layout[row_idx, col_idx] = SEAT_EMPTY

    return simulated_seat_layout

def number_of_occupied_seats_seen_from_current_seat(current_seat_layout, row, col):
    """
    From current seat, look to the right, left, top, bottom, top-right, bottom-left,
    top-left, bottom-right and check the first seat which can be seen.
    Return the total number of occupied seats seen from current position.
    """
    number_of_occupied_seats = 0

    number_of_occupied_seats += (1 if is_right_seat_occupied(current_seat_layout, row, col) else 0)
    number_of_occupied_seats += (1 if is_left_seat_occupied(current_seat_layout, row, col) else 0)
    number_of_occupied_seats += (1 if is_top_seat_occupied(current_seat_layout, row, col) else 0)
    number_of_occupied_seats += (1 if is_bottom_seat_occupied(current_seat_layout, row, col) else 0)
    number_of_occupied_seats += (1 if is_top_left_seat_occupied(current_seat_layout, row, col) else 0)
    number_of_occupied_seats += (1 if is_bottom_right_seat_occupied(current_seat_layout, row, col) else 0)
    number_of_occupied_seats += (1 if is_top_right_seat_occupied(current_seat_layout, row, col) else 0)
    number_of_occupied_seats += (1 if is_bottom_left_seat_occupied(current_seat_layout, row, col) else 0)

    return number_of_occupied_seats

def is_right_seat_occupied(current_seat_layout, row, col):
    """
    Starting from current seat (row, col) go to the right until the first seat is found.
    Return true if it is occupied, false otw.
    """
    is_seat_occupied = False

    i = 0 # iterating index
    while(True):
        i += 1

        # out of range?
        if (col + i) >= current_seat_layout.shape[1]:
            break

        # once a seat was reached, stop and set flag accordingly
        if current_seat_layout[row, col + i] != FLOOR:
            is_seat_occupied = (current_seat_layout[row, col + i] == SEAT_OCCUPIED)
            break

    return is_seat_occupied

def is_left_seat_occupied(current_seat_layout, row, col):
    """
    Starting from current seat (row, col) go to the left until the first seat is found.
    Return true if it is occupied, false otw.
    """
    is_seat_occupied = False

    i = 0 # iterating index
    while(True):
        i += 1

        # out of range?
        if (col - i) < 0:
            break

        # once a seat was reached, stop and set flag accordingly
        if current_seat_layout[row, col - i] != FLOOR:
            is_seat_occupied = (current_seat_layout[row, col - i] == SEAT_OCCUPIED)
            break

    return is_seat_occupied

def is_top_seat_occupied(current_seat_layout, row, col):
    """
    Starting from current seat (row, col) go to the top until the first seat is found.
    Return true if it is occupied, false otw.
    """
    is_seat_occupied = False

    i = 0 # iterating index
    while(True):
        i += 1

        # out of range?
        if (row - i) < 0:
            break

        # once a seat was reached, stop and set flag accordingly
        if current_seat_layout[row - i, col] != FLOOR:
            is_seat_occupied = (current_seat_layout[row - i, col] == SEAT_OCCUPIED)
            break

    return is_seat_occupied

def is_bottom_seat_occupied(current_seat_layout, row, col):
    """
    Starting from current seat (row, col) go to the bottom until the first seat is found.
    Return true if it is occupied, false otw.
    """
    is_seat_occupied = False

    i = 0 # iterating index
    while(True):
        i += 1

        # out of range?
        if (row + i) >= current_seat_layout.shape[0]:
            break

        # once a seat was reached, stop and set flag accordingly
        if current_seat_layout[row + i, col] != FLOOR:
            is_seat_occupied = (current_seat_layout[row + i, col] == SEAT_OCCUPIED)
            break

    return is_seat_occupied

def is_top_left_seat_occupied(current_seat_layout, row, col):
    """
    Starting from current seat (row, col) go to the top-left until the first seat is found.
    Return true if it is occupied, false otw.
    """
    is_seat_occupied = False

    i = 0 # iterating index
    while(True):
        i += 1

        # out of range?
        if (row - i) < 0 or (col - i) < 0:
            break

        # once a seat was reached, stop and set flag accordingly
        if current_seat_layout[row - i, col - i] != FLOOR:
            is_seat_occupied = (current_seat_layout[row - i, col - i] == SEAT_OCCUPIED)
            break

    return is_seat_occupied

def is_bottom_right_seat_occupied(current_seat_layout, row, col):
    """
    Starting from current seat (row, col) go to the bottom-right until the first seat is found.
    Return true if it is occupied, false otw.
    """
    is_seat_occupied = False

    i = 0 # iterating index
    while(True):
        i += 1

        # out of range?
        if (row + i) >= current_seat_layout.shape[0] or (col + i) >= current_seat_layout.shape[1]:
            break

        # once a seat was reached, stop and set flag accordingly
        if current_seat_layout[row + i, col + i] != FLOOR:
            is_seat_occupied = (current_seat_layout[row + i, col + i] == SEAT_OCCUPIED)
            break

    return is_seat_occupied

def is_top_right_seat_occupied(current_seat_layout, row, col):
    """
    Starting from current seat (row, col) go to the top-right until the first seat is found.
    Return true if it is occupied, false otw.
    """
    is_seat_occupied = False

    i = 0 # iterating index
    while(True):
        i += 1

        # out of range?
        if (row - i) < 0 or (col + i) >= current_seat_layout.shape[1]:
            break

        # once a seat was reached, stop and set flag accordingly
        if current_seat_layout[row - i, col + i] != FLOOR:
            is_seat_occupied = (current_seat_layout[row - i, col + i] == SEAT_OCCUPIED)
            break

    return is_seat_occupied

def is_bottom_left_seat_occupied(current_seat_layout, row, col):
    """
    Starting from current seat (row, col) go to the top-right until the first seat is found.
    Return true if it is occupied, false otw.
    """
    is_seat_occupied = False
    max_positions_bottom_left = min(current_seat_layout.shape[0] - row, col)

    i = 0 # iterating index
    while(True):
        i += 1

        # out of range?
        if (row + i) >= current_seat_layout.shape[0] or (col - i) < 0:
            break

        # once a seat was reached, stop and set flag accordingly
        if current_seat_layout[row + i, col - i] != FLOOR:
            is_seat_occupied = (current_seat_layout[row + i, col - i] == SEAT_OCCUPIED)
            break

    return is_seat_occupied

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """ Find the total number of occupied seats once the layout of above map does not change anymore """
    seat_layout_matrix = get_seat_layout_matrix()
    stable_seat_layout = simulate_rounds_until_stabilization(seat_layout_matrix)
    nb_of_occupied_seats = number_of_occupied_seats(stable_seat_layout)

    print("[+] Solution of day11/puzzle1: There are {} seats occupied in the end. ".format(nb_of_occupied_seats))

    stable_seat_layout = simulate_rounds_until_stabilization(seat_layout_matrix, is_puzzle_1=False)
    nb_of_occupied_seats = number_of_occupied_seats(stable_seat_layout)

    print("[+] Solution of day11/puzzle2: There are {} seats occupied in the end. ".format(nb_of_occupied_seats))

if __name__ == "__main__":
    compute_solution_of_puzzle()

