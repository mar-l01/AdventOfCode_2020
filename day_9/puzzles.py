import numpy as np

XMAS_CODE_FILE = "xmas_code.txt"

def get_numbers_list():
    """ Return the content of above file as a list of numbers. """
    numbers_list = []

    with open(XMAS_CODE_FILE, 'r') as numbers_file:
        for number in numbers_file:
           numbers_list.append(int(number))

    return numbers_list

def create_sum_matrix(numbers_list):
    """ Create a matrix (m x m) with the provided 'numbers_list' as row and column. """
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

def compute_solution_of_puzzle():
    """
    Find the first number in the list of numbers which does not met the requirement: value
    needs to be the sum of two values out of the 25 previous numbers.
    """
    numbers_list = get_numbers_list()
    sum_matrix = create_sum_matrix(numbers_list)
    non_matching_number = find_non_matching_number(numbers_list, sum_matrix)

    print("[+] Solution of day9/puzzle1: {} breaks the list of numbers".format(non_matching_number))

  
if __name__ == "__main__":
    compute_solution_of_puzzle()

