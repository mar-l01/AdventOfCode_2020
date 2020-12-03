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

def fly_through_matrix_and_count_trees(map_matrix):
    """
    Fly through the map with the given slope (3 right, 1 down)
    and count all trees which come to our way.

    Note: Due to the fact that the matrix is repeated to the right several times,
    a modulo operation with the number of columns is used to simulate it.
    """
    nb_rows = map_matrix.shape[0]
    nb_cols = map_matrix.shape[1]
    nb_trees = 0
    col = 0

    # starting at index [0][0] our first top is [1][3]
    for row in range(1, nb_rows):
        # wrap around matrix using modulo operation
        col = (col + 3) % nb_cols

        # tree encountered?
        if map_matrix[row][col] == 1:
            nb_trees += 1

    return nb_trees

def compute_solution_of_puzzle():
    """ Find the number of trees one encounters following the map in given slope """
    map_matrix = create_matrix_of_map()
    nb_of_trees = fly_through_matrix_and_count_trees(map_matrix)

    print("[+] Solution of day3/puzzle1: {} trees encountered on the fly through the map"\
          .format(nb_of_trees))

if __name__ == "__main__":
    compute_solution_of_puzzle()
