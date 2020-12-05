BOARDING_PASSES_FILE = "boarding_passes.txt"

TAKE_FRONT_HALF = ['F', 'L']
TAKE_BACK_HALF = ['B', 'R']

LIST_OF_SEAT_ROWS = [i for i in range(128)]
LIST_OF_SEAT_COLUMNS = [i for i in range(8)]

def get_list_of_boarding_passes():
    """
    Return a list of boarding passes, each element representing one pass.
    Passes a separated into:
    - letter 0..6: row of seat
    - letter 7..9: column of seat
    """
    list_of_boarding_passes = []

    with open(BOARDING_PASSES_FILE, 'r') as boarding_passes_file:
        for line in boarding_passes_file:
            # separate into row and column (remove newline char \n)
            boarding_pass = {"row": line[:7], "column": line[7:].strip()}
            list_of_boarding_passes.append(boarding_pass)

    return list_of_boarding_passes

# -------------------------- Puzzle 1 (used for Puzzle 2, too) --------------------------

def get_seat_row(bin_code_row):
    """ Get the row of given 'binary' code of a seat """
    return decode_seat(bin_code_row, LIST_OF_SEAT_ROWS)

def get_seat_column(bin_code_column):
    """ Get the column of given 'binary' code of a seat """
    return decode_seat(bin_code_column, LIST_OF_SEAT_COLUMNS)

def decode_seat(bin_code, list_of_seats):
    """
    'Decode' given 'binary' code of a certain seat:
    - 'F' or 'L' := front half
    - 'B' or 'R' := back half
    The number of available seats (either rows or columns) are given in 'list_of_seats'.
    """
    # check character to process (F,L or R,B)
    next_step = bin_code[0]

    # stop of recursion: if it is the last char, return the correct value
    if len(bin_code) == 1:
        return list_of_seats[0] if next_step in TAKE_FRONT_HALF else list_of_seats[1]

    if next_step in TAKE_FRONT_HALF:
        # use lower half of list, e.g. [0..127] -> [0..63]
        end_idx = len(list_of_seats) // 2
        list_of_seats = list_of_seats[:end_idx]
    else:
        # use lower half of list, e.g. [0..127] -> [64..127]
        start_idx = len(list_of_seats) // 2
        list_of_seats = list_of_seats[start_idx:]

    return decode_seat(bin_code[1:], list_of_seats)

def compute_seat_ID(row, column):
    """ Use following formula to compute seat ID: row * 8 + column """
    return row * 8 + column

def get_all_seat_IDs(list_of_boarding_passes):
    """
    Get all seat IDs of given list of boarding passes.
    Each boarding pass is given as dictionary of row and column.
    """
    list_of_seat_IDs = []

    for boarding_pass in list_of_boarding_passes:
        row = get_seat_row(boarding_pass["row"])
        column = get_seat_column(boarding_pass["column"])

        list_of_seat_IDs.append(compute_seat_ID(row, column))

    return list_of_seat_IDs

# -------------------------- Puzzle 2 --------------------------

def find_my_seat_ID(list_of_seat_IDs):
    """
    Iterate through the given list of several seat IDs and find the one missing.
    At first, sort list in ascending order and check if each seat-ID is +1 above
    the previous seat-ID. Once this condition does not hold, stop searching. As a
    result my seat-ID is one above the last previous seat-ID.

    Note: Some seats at the very front / back are also missing. Assume that my seat
    is between seats which are not missing!
    """
    # sort list in ascending order
    list_of_seat_IDs.sort(reverse=False)

    prev_seat_ID = list_of_seat_IDs[0]

    for seat_ID in list_of_seat_IDs[1:]:
        # check if current seat-ID is +1 above the previous one
        if seat_ID - prev_seat_ID != 1:
            # if this is not the case, stop loop -> found my seat-ID
            break

        prev_seat_ID = seat_ID

    return prev_seat_ID + 1

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """ Find the highest seat ID and my seat-ID in all boarding passes """
    list_of_boarding_passes = get_list_of_boarding_passes()
    list_of_seat_IDs = get_all_seat_IDs(list_of_boarding_passes)

    print("[+] Solution of day5/puzzle1: {} is the highest seat ID".format(max(list_of_seat_IDs)))

    my_seat_ID = find_my_seat_ID(list_of_seat_IDs)
    print("[+] Solution of day5/puzzle2: {} is my seat ID".format(my_seat_ID))

if __name__ == "__main__":
    compute_solution_of_puzzle()
