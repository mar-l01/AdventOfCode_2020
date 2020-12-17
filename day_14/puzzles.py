INIT_PROGRAM_FILE = "init_program.txt"

BIT_MASK_KEY = "bitmask"
MEMORY_ADDRESS_KEY = "memory_address"
ADDRESS_VALUE_KEY = "address_value"

def get_init_program_file_as_list():
    """
    Read in above file and create a list of dictionaries, each dictionary describing either
    the bit-mask or the address to write a given value to.
    """
    init_program_list = []
    
    with open(INIT_PROGRAM_FILE, 'r') as init_program_file:
        for program_line in init_program_file:
            program_line_dict = {}
            if "mask" in program_line:
                # bitmask is right part of 'mask = XXXXXXXXXXXXXXXXXX1X0X'
                bitmask = program_line.split('=')[1].strip()
                program_line_dict[BIT_MASK_KEY] = bitmask
            else:
                # memory value is given as 'mem[8] = 11'
                memory_address, memory_value = program_line.split('=')
                memory_address = memory_address[memory_address.find('[') + 1 : memory_address.find(']')]
                
                program_line_dict[MEMORY_ADDRESS_KEY] = int(memory_address)
                program_line_dict[ADDRESS_VALUE_KEY] = int(memory_value.strip())

            init_program_list.append(program_line_dict)

    return init_program_list

# -------------------------- Puzzle 1 --------------------------

def run_init_program_v1(init_program_list):
    """
    Iterate through the given program list and execute each command in there.
    Use a dictionary to emulate the address area, key is memory address, value is value at that address.
    Each given bitmask is applied to the values of all following write operations.
    """
    memory_address_space = {}

    # holds bitmask which is applied to all following memory operations
    bit_mask = 0

    for program_command in init_program_list:
        if BIT_MASK_KEY in program_command:
            bitmask = program_command[BIT_MASK_KEY]

        else:
            # apply bitmask to value which should be written to memory
            address_value = program_command[ADDRESS_VALUE_KEY]
            value_to_memory = apply_bitmask_to_value(bitmask, address_value)

            memory_address_space[program_command[MEMORY_ADDRESS_KEY]] = value_to_memory

    return memory_address_space

def apply_bitmask_to_value(bitmask, address_value):
    """ Apply given 'bitmask' to given 'address_value', return new value """
    # transform to binary
    bin_address_value = "{0:b}".format(address_value)

    # pad value with leading 0s in case length do not match
    if len(bin_address_value) < len(bitmask):
        bin_address_value = ('0' * (len(bitmask) - len(bin_address_value))) + bin_address_value

    # iterate over bitmask and apply change to binary address value (both as string)
    for pos, b in enumerate(bitmask):
        if b == 'X':
            # no change of values
            continue
        else:
            # set address value at current position to either 0 or 1
            bin_address_value = bin_address_value[:pos] + b + bin_address_value[pos + 1:]

    return int(bin_address_value, 2)

# -------------------------- Puzzle 2 --------------------------

def run_init_program_v2(init_program_list):
    """
    Iterate through the given program list and execute each command in there.
    Use a dictionary to emulate the address area, key is memory address, value is value at that address.
    Each given bitmask is applied to the memory address of all following write operations.
    """
    memory_address_space = {}

    # holds bitmask which is applied to all following memory operations
    bit_mask = 0

    for program_command in init_program_list:
        if BIT_MASK_KEY in program_command:
            bitmask = program_command[BIT_MASK_KEY]

        else:
            # apply bitmask to memoery address
            memory_address = program_command[MEMORY_ADDRESS_KEY]
            memory_address_with_Xs = apply_bitmask_to_address(bitmask, memory_address)

            # set value in each possible memory address
            for memory_address in compute_all_addresses_by_replacing_X(memory_address_with_Xs):
                memory_address_space[memory_address] = program_command[ADDRESS_VALUE_KEY]

    return memory_address_space

def apply_bitmask_to_address(bitmask, memory_address):
    """
    Apply given 'bitmask' to given 'memory_address', return new value which contains Xs.

    Use following rules
    If the bitmask bit is 0, the corresponding memory address bit is unchanged.
    If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
    If the bitmask bit is X, the corresponding memory address bit is floating --> either 0 or 1.
    """
    # transform to binary
    bin_memory_address = "{0:b}".format(memory_address)

    # pad value with leading 0s in case length do not match
    if len(bin_memory_address) < len(bitmask):
        bin_memory_address = ('0' * (len(bitmask) - len(bin_memory_address))) + bin_memory_address

    # iterate over bitmask and apply change to binary address value (both as string)
    for pos, b in enumerate(bitmask):
        if b == '0':
            # no change of values
            continue
        else:
            # set value at respective position either to 1 or set 'X'
            bin_memory_address = bin_memory_address[:pos] + b + bin_memory_address[pos + 1:]

    return bin_memory_address

def compute_all_addresses_by_replacing_X(bin_memory_address):
    """
    Replace all Xs in given 'bin_memory_address' with either 0s or 1s. Go through all possible
    value combinations. Return all thus computed addresses as a list.
    
    Idea of replacing X with 0 or 1: compute total number of possibilites (:= 2^(#X's)), loop over
    them and replace each X with the converted binary value at its respective position.
    """
    all_memory_addresses = []
    nb_of_X = bin_memory_address.count('X')

    # iterate over computed memory address and replace 'X' one by one with 0 or 1
    for x in range(2**nb_of_X):
        new_memory_address = bin_memory_address

        # convert x to binary and pad it with leading zeroes
        bin_x = "{0:b}".format(x)
        bin_x = ('0' * (nb_of_X - len(bin_x))) + bin_x

        # replace all 'X' with the respective binary values
        x_pos = 0
        for bin_val in bin_x:
            x_pos = new_memory_address.find('X', x_pos)
            new_memory_address = new_memory_address[:x_pos] + bin_val + new_memory_address[x_pos + 1:]

        all_memory_addresses.append(new_memory_address)

    return all_memory_addresses

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_sum_of_all_address_values(memory_address_space):
    """ Sum up all values in given 'memory_address_space' """
    sum_values = 0

    for value in memory_address_space.values():
        sum_values += value
    
    return sum_values

def compute_solution_of_puzzle():
    """ Find the sum of all set memory addresses entries """
    init_program_list = get_init_program_file_as_list()

    memory_address_space = run_init_program_v1(init_program_list)
    sum_of_all_memory_values = compute_sum_of_all_address_values(memory_address_space)
    print("[+] Solution of day14/puzzle1: {} is the sum of all memory address entries".format(sum_of_all_memory_values))

    memory_address_space = run_init_program_v2(init_program_list)
    sum_of_all_memory_values = compute_sum_of_all_address_values(memory_address_space)
    print("[+] Solution of day14/puzzle2: {} is the sum of all memory address entries".format(sum_of_all_memory_values))

if __name__ == "__main__":
    compute_solution_of_puzzle()
