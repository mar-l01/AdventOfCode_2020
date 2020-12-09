BOOT_CODE_FILE = "boot_code.txt"

OPCODE_KEY = "op"
SIGN_KEY = "sgn"
VALUE_KEY = "val"
NOP = "nop"
ACC = "acc"
JMP = "jmp"

def get_boot_instruction_list():
    """
    Read above file and extract the boot code sequence as a list of instruction. Each instruction
    is represented as a dictionary, holding the operation, the sign (+ or -) and the actual value.

    For example, jmp +248 results in [{"op": "jmp", "sgn": "+", "val": 248}]
    """
    instruction_list = []

    with open(BOOT_CODE_FILE, 'r') as boot_code_file:
        single_instruction = {}
        for instruction_line in boot_code_file:
            # split at space -> operation and argument (:= "+123" -> [0] := "+", [1:] := 123)
            op_code, argument = instruction_line.strip().split(' ')

            instruction_list.append({OPCODE_KEY: op_code, SIGN_KEY: argument[0], VALUE_KEY: int(argument[1:])})

    return instruction_list

# -------------------------- Puzzle 1 --------------------------

def find_acc_value_right_before_infinite_loop(instruction_list):
    """
    Iterate over provided 'instruction_list' and execute the instructions (:= list-elements). Increase the
    accumulator value accordingly.
    Note: It is assumed that an infinite loop is found once an instruction is executed a second time.
    """
    return run_instruction(instruction_list, 0, [])

def run_instruction(instruction_list, idx, visited_idxs):
    """
    Get instruction at index 'idx' of 'instruction_list':
    - if instruction at index 'idx' was already run, stop --> cycle detected (:= infinite loop assumption)
    - if 'idx' is out-of-range, stop --> end of instruction list reached (:= successful case)
    - run instruction and recursively execute next instruction, always incrementing the acc-value if needed
    """
    # stop if cycle was detected or end of list reached
    if idx in visited_idxs or idx == len(instruction_list):
        return 0

    # mark index as visited
    visited_idxs.append(idx)

    acc_val = 0
    next_idx = idx
    instruction = instruction_list[idx]
    op_code = instruction[OPCODE_KEY]
    sign = instruction[SIGN_KEY]
    value = instruction[VALUE_KEY]

    if op_code == NOP:
        # no operation, go on with next instruction
        next_idx += 1
    
    elif op_code == ACC:
        # depending on given sign, adapt the acc-value
        if sign == "+":
            acc_val += value
        elif sign == "-":
            acc_val -= value
        # go on with next instruction
        next_idx += 1

    elif op_code == JMP:
        # depending on given sign, adapt the index of the next instruction
        if sign == "+":
            next_idx += value
        elif sign == "-":
            next_idx -= value

    return acc_val + run_instruction(instruction_list, next_idx, visited_idxs)

# -------------------------- Puzzle 2 --------------------------

def get_instructions_to_change(instruction_list):
    """
    Return a list of tuples, each tuple holding the index and operation code which needs
    to be applied/changed, e.g. index 1 and operation code JMP will result in following
    entry: (1, NOP)
    """
    instruction_indices_list = []
    for idx, instruction in enumerate(instruction_list):
        op_code = instruction[OPCODE_KEY]

        # do not care about ACC operation code
        if op_code in [NOP, JMP]:
            if op_code == JMP:
                # change JMP to NOP
                instruction_indices_list.append((idx, NOP))
            elif op_code == NOP:
                # change NOP to JMP
                instruction_indices_list.append((idx, JMP))

    return instruction_indices_list                                           

def find_acc_value_of_loop_break(instruction_list):
    """
    Use the recursive function defined below to try every NOP/JMP change until a break in the infinite
    loop is found. Once the break was found, calculate the accumulated value like in puzzle 1 and
    return it.
    """
    acc_value = -1
    instruction_indices_list = get_instructions_to_change(instruction_list) 
    
    for idx, op_code in instruction_indices_list:
        inst_list = get_boot_instruction_list() # new un-manipulated list of instructions
        (inst_list[idx])[OPCODE_KEY] = op_code

        # found a break in the infinite loop
        if find_non_infinite_loop(inst_list, 0, []):
            acc_value = run_instruction(inst_list, 0, [])
            break

    return acc_value

def find_non_infinite_loop(instruction_list, idx, visited_idxs):
    """
    Get instruction at index 'idx' of 'instruction_list':
    - if instruction at index 'idx' was already run, stop --> cycle detected (:= infinite loop assumption)
    - if instruction at index 'idx' is out of range, stop --> end of instruction-list reached --> success
      in un-breaking infinite loop
    - run instruction and recursively execute next instruction
    """
    # stop if cycle was detected, or last line was not executed --> fail
    if idx in visited_idxs or idx > len(instruction_list):
        return False

    # stop if end of instruction list is reached --> success
    if idx == len(instruction_list):
        return True

    # mark index as visited
    visited_idxs.append(idx)
    
    next_idx = idx
    instruction = instruction_list[idx]
    op_code = instruction[OPCODE_KEY]
    sign = instruction[SIGN_KEY]
    value = instruction[VALUE_KEY]

    if op_code == NOP:
        # no operation, go on with next instruction
        next_idx += 1
    
    elif op_code == ACC:
        # no need to care about it now, go on with next instruction
        next_idx += 1

    elif op_code == JMP:
        # depending on given sign, adapt the index of the next instruction
        if sign == "+":
            next_idx += value
        elif sign == "-":
            next_idx -= value

    return (True and find_non_infinite_loop(instruction_list, next_idx, visited_idxs))
    
# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """ Find the accumulator value right before a second cycle (:= start of infinite loop) is executed. """
    instruction_list = get_boot_instruction_list()
    acc_value_before_infinite_loop = find_acc_value_right_before_infinite_loop(instruction_list)
 
    print("[+] Solution of day8/puzzle1: Accumulator value before starting of infinite loop = {}".format(acc_value_before_infinite_loop))

    acc_value_after_finishing_boot_loop = find_acc_value_of_loop_break(instruction_list)
    print("[+] Solution of day8/puzzle2: Accumulator value after successfully finishing boot sequence = {}".format(acc_value_after_finishing_boot_loop))

  
if __name__ == "__main__":
    compute_solution_of_puzzle()

