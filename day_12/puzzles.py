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

def go_through_navigation_instructions_list(navigation_instructions_list):
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

        if instruction == 'N':
            north_position += value
        elif instruction == 'E':
            east_position += value
        elif instruction == 'S':
            north_position -= value
        elif instruction == 'W':
            east_position -= value

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

def compute_solution_of_puzzle():
    """
    Compute Manhattan Distance from starting point N:0 / E:0 to the end point after executing
    each navigation instructions.
    """
    navigation_instructions_list = create_navigation_instructions_list()
    east_position, north_position = go_through_navigation_instructions_list(navigation_instructions_list)
    manhattan_distance = abs(east_position) + abs(north_position)

    print("[+] Solution of day7/puzzle1: Manhattan Distance of east/west and north/south = {}".format(manhattan_distance))

if __name__ == "__main__":
    compute_solution_of_puzzle()
