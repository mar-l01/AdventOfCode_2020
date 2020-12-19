import itertools
import numpy as np

INITIAL_CUBE_STATE_FILE = "conway_cube.txt"

ADJACENT_CUBES_COORDINATES_3DIM = [coord for coord in itertools.product((-1, 0, 1), repeat=3) if coord != (0, 0, 0)]
ADJACENT_CUBES_COORDINATES_4DIM = [coord for coord in itertools.product((-1, 0, 1), repeat=4) if coord != (0, 0, 0, 0)]

CUBE_MAX_Y= 21
CUBE_MAX_X = 21
CUBE_MAX_Z = 21
CUBE_MAX_W = 21
CUBE_MIDDLE = 10

def get_initial_cube_state():
    """ initial_cube_state the content the inital cube state as matrix, replacing '#' with 1 and '.' with 0 """
    initial_cube_state = None

    with open(INITIAL_CUBE_STATE_FILE, 'r') as initial_cube_state_file:
        for state_row in initial_cube_state_file:
            state_row = state_row.strip()
            if initial_cube_state is None:
                # initialize matrix once (number of columns known)
                initial_cube_state = np.empty([0, len(state_row)], dtype=int)

            # create new row with respective entries set to 0 (:= .) or 1 (:= #)
            matrix_row = []
            for state in state_row:
                matrix_row.append(1 if state == '#' else 0)

            # add row to matrix
            initial_cube_state = np.append(initial_cube_state, np.array([matrix_row]), axis=0)

    return initial_cube_state

def is_coordinate_in_cube(coordinate, is_4d=False):
    """ Check if given coordinate is inside the cube """
    if 0 <= coordinate[0] < CUBE_MAX_Y and\
       0 <= coordinate[1] < CUBE_MAX_X and\
       0 <= coordinate[2] < CUBE_MAX_Z:
        if is_4d:
           if 0 <= coordinate[3] < CUBE_MAX_W:
               return True
        else:
            return True 

    return False

def embed_initial_state_in_bigger_cube(initial_state, is_4d=False):
    """
    Create a n x n x n (x n) cube and embedd the initial state right in the middle of it, i.e. z-coordinate = n/2.
    """
    cube = np.zeros((CUBE_MAX_Y, CUBE_MAX_X, CUBE_MAX_Z, CUBE_MAX_W)) if is_4d\
           else np.zeros((CUBE_MAX_Y, CUBE_MAX_X, CUBE_MAX_Z))
    
    top_left_x = CUBE_MIDDLE - (initial_state.shape[0] // 2)
    top_left_y = CUBE_MIDDLE - (initial_state.shape[0] // 2)
    top_left_z = CUBE_MIDDLE
    top_left_w = CUBE_MIDDLE

    # fill cube with initial state
    if is_4d:
        for idx, row in enumerate(initial_state):
            cube[top_left_y + idx, top_left_x : top_left_x + len(row), top_left_z, top_left_w] = row
    else:
        for idx, row in enumerate(initial_state):
            cube[top_left_y + idx, top_left_x : top_left_x + len(row), top_left_z] = row

    return cube

def run_initial_boot_loop(cube_state, is_4d=False):
    """ Perform 6 cycles which represent the boot-loop. Return the number of all active cubes afterwards. """
    current_cube_state = cube_state.copy()

    # set function to be run depending on the given flag
    run_one_boot_loop = perform_single_cycle_4d if is_4d else\
                         perform_single_cycle_3d
    
    for i in range(6):
        print("Round #{}".format(i))
        current_cube_state = run_one_boot_loop(current_cube_state)

    return np.sum(current_cube_state)

# -------------------------- Puzzle 1 --------------------------

def perform_single_cycle_3d(cube_state):
    """
    Using given 'cube_state' matrix, perform a single cycle by applying following rules simultaneously:
    - If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
      Otherwise, the cube becomes inactive.
    - If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
      Otherwise, the cube remains inactive.
    """
    current_cube_state = cube_state.copy()
    
    # bit too much, but for simplicity here, check each element of matrix
    for y in range(cube_state.shape[0]):
        for x in range(cube_state.shape[1]):
            for z in range(cube_state.shape[2]):
                adjacent_cubes = get_all_adjacent_cubes_3d((y, x, z))
                active_cubes_around = 0
                for adjacent_cube in adjacent_cubes:
                    if is_coordinate_in_cube(adjacent_cube):
                        if cube_state[adjacent_cube] == 1: # cube is active
                            active_cubes_around += 1

                # cube stays active if exactly 2 or 3 around it are active, too
                if cube_state[(y, x, z)] == 1:
                    if active_cubes_around not in [2,3]:
                        current_cube_state[(y, x, z)] = 0

                # inactive cube becomes active if exactly 3 around it are active 
                elif cube_state[(y, x, z)] == 0:
                    if active_cubes_around == 3:
                        current_cube_state[(y, x, z)] = 1

    return current_cube_state

def get_all_adjacent_cubes_3d(cube):
    """
    Using the coordinates given in 'cube', compute all adjacent cubes and return their coordinates.

    Note: each cube has 26 adjacent cubes.
    """
    return [tuple(map(lambda i, j: i - j, cube, adj_cube_coord)) for adj_cube_coord in ADJACENT_CUBES_COORDINATES_3DIM]

# -------------------------- Puzzle 2 --------------------------

def perform_single_cycle_4d(cube_state):
    """
    Using given 'cube_state' matrix, perform a single cycle by applying following rules simultaneously:
    - If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
      Otherwise, the cube becomes inactive.
    - If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active.
      Otherwise, the cube remains inactive.
    """
    current_cube_state = cube_state.copy()
    
    # bit too much, but for simplicity here, check each element of matrix
    for y in range(cube_state.shape[0]):
        for x in range(cube_state.shape[1]):
            for z in range(cube_state.shape[2]):
                for w in range(cube_state.shape[3]):
                    adjacent_cubes = get_all_adjacent_cubes_4d((y, x, z, w))
                    active_cubes_around = 0
                    for adjacent_cube in adjacent_cubes:
                        if is_coordinate_in_cube(adjacent_cube, is_4d=True):
                            if cube_state[adjacent_cube] == 1: # cube is active
                                active_cubes_around += 1

                    # cube stays active if exactly 2 or 3 around it are active, too
                    if cube_state[(y, x, z, w)] == 1:
                        if active_cubes_around not in [2,3]:
                            current_cube_state[(y, x, z, w)] = 0

                    # inactive cube becomes active if exactly 3 around it are active 
                    elif cube_state[(y, x, z, w)] == 0:
                        if active_cubes_around == 3:
                            current_cube_state[(y, x, z, w)] = 1

    return current_cube_state

def get_all_adjacent_cubes_4d(cube):
    """
    Using the coordinates given in 'cube', compute all adjacent cubes and return their coordinates.

    Note: each cube has 80 adjacent cubes.
    """
    return [tuple(map(lambda i, j: i - j, cube, adj_cube_coord)) for adj_cube_coord in ADJACENT_CUBES_COORDINATES_4DIM]

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """ Find state of conway cube if executing 6 cycles """
    initial_state = get_initial_cube_state()
    
    cube_state = embed_initial_state_in_bigger_cube(initial_state)
    active_cubes_after_6th_round = run_initial_boot_loop(cube_state)
    print("[+] Solution of day17/puzzle1: {:.0f} cubes are active after performing the 6th cycle"\
          .format(active_cubes_after_6th_round))

    cube_state = embed_initial_state_in_bigger_cube(initial_state, is_4d=True)
    active_cubes_after_6th_round = run_initial_boot_loop(cube_state, is_4d=True)
    print("[+] Solution of day17/puzzle2: {:.0f} cubes are active after performing the 6th cycle"\
          .format(active_cubes_after_6th_round))

if __name__ == "__main__":
    compute_solution_of_puzzle()
