import numpy as np

MAP_FILE = "map.txt"

def create_matrix_of_map():
    """
    Fill a matrix with the map given in above file name:
    Each line is handled as single row with '.' denoting a 0,
    and each '#' representing a 1
    """
    map_matrix = None

    with open(MAP_FILE, 'r') as map_file:
        for map_line in map_file:
            map_line = map_line.strip()
            if map_matrix is None:
                # initialize matrix once (number of columns known)
                map_matrix = np.empty([0, len(map_line)], dtype=int)

            # create new row with respective entries set to 0 (:= .) or 1 (:= #)
            map_row = []
            for obstacle in map_line:
                map_row.append(0 if obstacle == '.' else 1)

            # add row to matrix
            map_matrix = np.append(map_matrix, np.array([map_row]), axis=0)

    return map_matrix

# -------------------------- Puzzle 1 (slope is (3,1)) --------------------------
# -------------------------- Puzzle 2 (different slopes) ------------------------

def fly_through_matrix_and_count_trees(map_matrix, slope):
    """
    Fly through the map with the given slope (:= (right, down)) and count all
    trees which come into our way.

    Note: Due to the fact that the matrix is repeated to the right several times,
    a modulo operation with the number of columns is used to simulate it.
    """
    nb_rows = map_matrix.shape[0]
    nb_cols = map_matrix.shape[1]
    slope_right = slope[0]
    slope_down = slope[1]
    nb_trees = 0
    col = 0

    # starting at index [0][0] our first stop is at index [slope_down][slope_right]
    for row in range(slope_down, nb_rows, slope_down):
        # wrap around matrix using modulo operation
        col = (col + slope_right) % nb_cols

        # tree encountered?
        if map_matrix[row][col] == 1:
            nb_trees += 1

    return nb_trees

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """ Find the number of trees one encounters following the map in given slopes """
    map_matrix = create_matrix_of_map()

    nb_of_trees = fly_through_matrix_and_count_trees(map_matrix, (3, 1)) # slope: 3 right, 1 down

    print("[+] Solution of day3/puzzle1: {} trees encountered on the flight through the map"\
          .format(nb_of_trees))

    nb_of_trees_slope_1 = fly_through_matrix_and_count_trees(map_matrix, (1, 1)) # slope: 1 right, 1 down
    nb_of_trees_slope_2 = fly_through_matrix_and_count_trees(map_matrix, (3, 1)) # slope: 3 right, 1 down
    nb_of_trees_slope_3 = fly_through_matrix_and_count_trees(map_matrix, (5, 1)) # slope: 5 right, 1 down
    nb_of_trees_slope_4 = fly_through_matrix_and_count_trees(map_matrix, (7, 1)) # slope: 7 right, 1 down
    nb_of_trees_slope_5 = fly_through_matrix_and_count_trees(map_matrix, (1, 2)) # slope: 1 right, 2 down

    print("[+] Solution of day3/puzzle2: {} trees encountered on the flights through the map"\
          .format(nb_of_trees_slope_1 * nb_of_trees_slope_2 * nb_of_trees_slope_3 * nb_of_trees_slope_4 *\
                  nb_of_trees_slope_5))

if __name__ == "__main__":
    compute_solution_of_puzzle()
