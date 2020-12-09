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
    - run instruction and recursively execute next instruction, always incrementing the acc-value if needed
    """
    # stop if cycle was detected
    if idx in visited_idxs:
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

def compute_solution_of_puzzle():
    """ Find the accumulator value right before a second cycle (:= start of infinite loop) is executed. """
    instruction_list = get_boot_instruction_list()
    acc_value_before_infinite_loop = find_acc_value_right_before_infinite_loop(instruction_list)
 
    print("[+] Solution of day8/puzzle1: Accumulator value before starting of infinite loop = {}".format(acc_value_before_infinite_loop))
  
if __name__ == "__main__":
    compute_solution_of_puzzle()
