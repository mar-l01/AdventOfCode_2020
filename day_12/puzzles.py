from enum import IntEnum

NAVIGATION_INSTRUCTIONS_FILE = "navigation_instructions.txt"

INSTRUCTION = "instruction"
VALUE = "value"

class FacingPosition(IntEnum):
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3

def create_navigation_instructions_list():
    """
    Create a list of dictionaries, each dictionary containing the instruction and the respective
    value as key-value pairs.
    """
    navigation_instructions_list = []

    with open(NAVIGATION_INSTRUCTIONS_FILE, 'r') as navigation_instructions_file:
        for navigation_instruction in navigation_instructions_file:
            # create a dictionary with the instruction and respective value as keys
            navi_dict = {}
            navi_dict[INSTRUCTION] = navigation_instruction[0]
            navi_dict[VALUE] = int(navigation_instruction[1:].strip())
            
            navigation_instructions_list.append(navi_dict)

    return navigation_instructions_list

# -------------------------- Puzzle 1 --------------------------

def navigate_ship(navigation_instructions_list):
    """
    Starting from position E:0, N:0. In the beginning the ship is facing east.
    Iterate through the whole instruction list and update current position accordingly.
    """
    east_position = 0
    north_position = 0
    facing_position = FacingPosition.EAST
    
    for navigation_instruction in navigation_instructions_list:
        instruction = navigation_instruction[INSTRUCTION]
        value = navigation_instruction[VALUE]

        # update ship position accordingly
        if instruction == 'N':
            north_position += value
        elif instruction == 'E':
            east_position += value
        elif instruction == 'S':
            north_position -= value
        elif instruction == 'W':
            east_position -= value

        # turn ship around or move forward
        elif instruction == 'L' or instruction == 'R':
            facing_position = turn_to_position(facing_position, instruction, value)
        elif instruction == 'F':
            forward_east, forward_north = ship_forward(facing_position, value)
            east_position += forward_east
            north_position += forward_north

    return east_position, north_position

def ship_forward(current_facing_position, value):
    """ Depending on given 'current_facing_position' ship 'value' steps forward. """
    forward_to_the_east = 0
    forward_to_the_north = 0

    if current_facing_position == FacingPosition.EAST:
        forward_to_the_east += value
    elif current_facing_position == FacingPosition.SOUTH:
        forward_to_the_north -= value
    elif current_facing_position == FacingPosition.WEST:
        forward_to_the_east -= value
    elif current_facing_position == FacingPosition.NORTH:
        forward_to_the_north += value

    return forward_to_the_east, forward_to_the_north

def turn_to_position(current_facing_position, instruction, value):
    """ Return the updated facing position when instruction got applied. """
    updated_facing_position = current_facing_position
    
    if instruction == 'L':
        for i in range(value // 90):
            updated_facing_position = turn_90_degrees_to_the_left(updated_facing_position)
    elif instruction == 'R':
        for i in range(value // 90):
            updated_facing_position = turn_90_degrees_to_the_right(updated_facing_position)

    return updated_facing_position

def turn_90_degrees_to_the_right(current_facing_position):
    """ Turn around by 90 degrees to the right. """
    updated_facing_position = None

    if current_facing_position == FacingPosition.EAST:
        updated_facing_position = FacingPosition.SOUTH
    elif current_facing_position == FacingPosition.SOUTH:
        updated_facing_position = FacingPosition.WEST
    elif current_facing_position == FacingPosition.WEST:
        updated_facing_position = FacingPosition.NORTH
    elif current_facing_position == FacingPosition.NORTH:
        updated_facing_position = FacingPosition.EAST

    return updated_facing_position

def turn_90_degrees_to_the_left(current_facing_position):
    """ Turn around by 90 degrees to the left. """
    updated_facing_position = None

    if current_facing_position == FacingPosition.EAST:
        updated_facing_position = FacingPosition.NORTH
    elif current_facing_position == FacingPosition.NORTH:
        updated_facing_position = FacingPosition.WEST
    elif current_facing_position == FacingPosition.WEST:
        updated_facing_position = FacingPosition.SOUTH
    elif current_facing_position == FacingPosition.SOUTH:
        updated_facing_position = FacingPosition.EAST
        
    return updated_facing_position

# -------------------------- Puzzle 2 --------------------------

def navigate_ship_along_waypoint(navigation_instructions_list):
    """
    Starting from position E:0, N:0. In the beginning the ship is facing east.
    Iterate through the whole instruction list and update current position accordingly.
    Additional information in comparison to puzzle 1: The instructions are now applied to
    a waypoint which starts at E:10, N:1. 
    """
    ship_east_position = 0
    ship_north_position = 0
    waypoint_east_position = 10
    waypoint_north_position = 1
    
    for navigation_instruction in navigation_instructions_list:
        instruction = navigation_instruction[INSTRUCTION]
        value = navigation_instruction[VALUE]

        # update waypoint position accordingly
        if instruction == 'N':
            waypoint_north_position += value
        elif instruction == 'E':
            waypoint_east_position += value
        elif instruction == 'S':
            waypoint_north_position -= value
        elif instruction == 'W':
            waypoint_east_position -= value

        # rotate waypoint around ship or move ship towards waypoint
        elif instruction == 'L' or instruction == 'R':
            waypoint_east_position, waypoint_north_position = rotate_waypoint((waypoint_east_position,\
                                                                               waypoint_north_position),\
                                                                               instruction, value)
        elif instruction == 'F':
            ship_east_position, ship_north_position = ship_forward_to_waypoint((ship_east_position,\
                                                                                ship_north_position),\
                                                                               (waypoint_east_position,\
                                                                                waypoint_north_position),\
                                                                               value)

    return ship_east_position, ship_north_position

def ship_forward_to_waypoint(ship_position, waypoint_position, value):
    """
    Depending on given 'waypoint_position' ship 'value' steps forward towards the way-point.
    Both positions are given as tuples (E, N).
    Return the updated position of the ship
    """
    ship_east_pos = ship_position[0]
    ship_north_pos = ship_position[1]
    wp_east_pos = waypoint_position[0]
    wp_north_pos = waypoint_position[1]

    ship_east_pos += (wp_east_pos * value)
    ship_north_pos += (wp_north_pos * value)

    return ship_east_pos, ship_north_pos

def rotate_waypoint(waypoint_position, instruction, value):
    """
    Rotate current waypoint position around the ship depending on given 'instruction'
    (:= 'L' or 'R'). The position is provided as tuple (E, N)
    Return updated waypoint position.
    """
    updated_waypoint_position = waypoint_position
    
    if instruction == 'L':
        for i in range(value // 90):
            updated_waypoint_position = rotate_waypoint_90_degrees_to_the_left(updated_waypoint_position)

    elif instruction == 'R':
        for i in range(value // 90):
            updated_waypoint_position = rotate_waypoint_90_degrees_to_the_right(updated_waypoint_position)
            
    return updated_waypoint_position

def rotate_waypoint_90_degrees_to_the_left(waypoint):
    """ Rotate waypoint 90 degrees to the left. """
    east_position = waypoint[0]
    north_position = waypoint[1]

    # waypoint to the east
    if east_position >= 0:
        # waypoint north-east -> move to north-west
        if north_position >= 0:
            tmp_pos_east = east_position
            east_position = -north_position
            north_position = tmp_pos_east

        # waypoint south-east -> move to north-east
        else:
            tmp_pos_east = east_position
            east_position = -north_position
            north_position = tmp_pos_east
            
    # waypoint to the west
    elif east_position < 0:
        # waypoint north-west -> waypoint to south-west
        if north_position >= 0:
            tmp_pos_east = east_position
            east_position = -north_position
            north_position = tmp_pos_east

        # waypoint south-west -> waypoint to south-east
        else:
            tmp_pos_east = east_position
            east_position = -north_position
            north_position = tmp_pos_east

    return (east_position, north_position)

def rotate_waypoint_90_degrees_to_the_right(waypoint):
    """ Rotate waypoint 90 degrees to the right. """
    east_position = waypoint[0]
    north_position = waypoint[1]

    # waypoint to the east
    if east_position >= 0:
        # waypoint north-east -> waypoint to south-east
        if north_position >= 0:
            tmp_pos_east = east_position
            east_position = north_position
            north_position = -tmp_pos_east
            
        # waypoint to the south-east -> waypoint to south-west
        else:
            tmp_pos_east = east_position
            east_position = north_position
            north_position = -tmp_pos_east

    # waypoint to the west
    elif east_position < 0:
        # waypoint north-west -> waypoint to north-east
        if north_position >= 0:
            tmp_pos_east = east_position
            east_position = north_position
            north_position = -tmp_pos_east
            
        # waypoint at south-west -> waypoint to north-west
        else:
            tmp_pos_east = east_position
            east_position = north_position
            north_position = -tmp_pos_east

    return east_position, north_position  

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """
    Compute Manhattan Distance from starting point N:0 / E:0 to the end point after executing
    each navigation instructions.
    """
    navigation_instructions_list = create_navigation_instructions_list()
    east_position, north_position = navigate_ship(navigation_instructions_list)
    manhattan_distance = abs(east_position) + abs(north_position)

    print("[+] Solution of day12/puzzle1: Manhattan Distance of east/west and north/south = {}".format(manhattan_distance))

    east_position, north_position = navigate_ship_along_waypoint(navigation_instructions_list)
    manhattan_distance = abs(east_position) + abs(north_position)

    print("[+] Solution of day12/puzzle2: Manhattan Distance of east/west and north/south = {}".format(manhattan_distance))

if __name__ == "__main__":
    compute_solution_of_puzzle()
