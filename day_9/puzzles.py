import numpy as np

XMAS_CODE_FILE = "xmas_code.txt"

def get_numbers_list():
    """ Return the content of above file as a list of numbers. """
    numbers_list = []

    with open(XMAS_CODE_FILE, 'r') as numbers_file:
        for number in numbers_file:
           numbers_list.append(int(number))

    return numbers_list

# -------------------------- Puzzle 1 --------------------------

def create_sum_matrix(numbers_list):
    """
    Create a matrix (m x m) with the provided 'numbers_list' as row and column.
    Each cell content will be the sum of the numbers associated with current row and column.
    """
    matrix_size = len(numbers_list)
    sum_matrix = np.empty((matrix_size, matrix_size))

    for row_idx in range(matrix_size):
        for col_idx in range(matrix_size):
            if row_idx != col_idx:
                sum_matrix[row_idx][col_idx] = numbers_list[row_idx] + numbers_list[col_idx]

    return sum_matrix

def find_non_matching_number(numbers_list, sum_matrix):
    """
    Iterate to provided 'numbers_list' and check if 2 values out of the previous 25 numbers
    add up to the currently checked number.
    
    Note: first 25 numbers are skipped as präamble.
    """
    idx = 25
    non_matching_number = -1

    for number in numbers_list[25:]:
        if not is_number_valid(sum_matrix, number, idx):
            # found number which does not match the requirements
            non_matching_number = number
            break

        idx += 1

    return non_matching_number

def is_number_valid(sum_matrix, number, idx):
    """
    Go through each row of the matrix which is within given range (determined by 'idx').
    If 'number' is within one of these rows, it is valid, because the cell contents contain
    the summed-up values.
    """
    # define range of matrix -> m[idx_low : idx][idx_low : idx]
    idx_low = idx - 25

    return np.any(sum_matrix[idx_low:idx, idx_low:idx] == number)

# -------------------------- Puzzle 2 --------------------------

def create_continuous_sum_matrix(numbers_list):
    """
    Create a matrix (m x m) with the provided 'numbers_list' as row and column.
    Each cell content will be the sum of the previous numbers plus the current one.

    Note: created matrix will be symmetrical --> only consider one half of it!
    """
    matrix_size = len(numbers_list)
    cont_sum_matrix = np.empty((matrix_size, matrix_size))

    for row_idx in range(matrix_size):
        for col_idx in range(matrix_size):
            if row_idx < col_idx:
                cont_sum_matrix[row_idx][col_idx] = cont_sum_matrix[row_idx][col_idx - 1] + numbers_list[col_idx]
    
    return cont_sum_matrix

def find_continuous_sequence_which_add_up_to_given_number(numbers_list, cont_sum_matrix, magic_number):
    """
    Find a continuous sequence in above list of numbers which add up to the given
    'magic_number'. Use a matrix where each adjacent cell in a row is the sum of the
    previous cell content plus the number associated with current cell.
    Return those sequence in the 'numbers_list' which is determined by the found sequence.
    """
    start_idx = -1
    end_idx = -1
    
    for idx, row in enumerate(cont_sum_matrix):
        current_sum = 0

        # symmetrical matrix --> consider only upper half of it
        for row_idx, value in enumerate(row[idx:]):
            if value == magic_number:
                start_idx = idx
                end_idx = start_idx + row_idx + 1
                break

        if start_idx != -1:
            break

    return numbers_list[start_idx:end_idx]

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """
    Find the first number in the list of numbers which does not met the requirement: value
    needs to be the sum of two values out of the 25 previous numbers.
    """
    numbers_list = get_numbers_list()
    sum_matrix = create_sum_matrix(numbers_list)
    non_matching_number = find_non_matching_number(numbers_list, sum_matrix)

    print("[+] Solution of day9/puzzle1: {} breaks the list of numbers".format(non_matching_number))

    continuous_sum_matrix = create_continuous_sum_matrix(numbers_list)
    continuous_sequence = find_continuous_sequence_which_add_up_to_given_number(numbers_list,\
                                continuous_sum_matrix, non_matching_number)
    sum_of_largest_and_smallest_value = max(continuous_sequence) + min(continuous_sequence)

    print("[+] Solution of day9/puzzle2: The sum of the smallest and largest number in continous sequence is: {}"\
          .format(sum_of_largest_and_smallest_value))
  
if __name__ == "__main__":
    compute_solution_of_puzzle()

