import re

HOMEWORK_FILE = "homework.txt"

BRACKET_REGEX_PATTERN = "\(\d+(\s(\+|\*)\s\d+)+\)"
OPERATOR_REGEX_PATTERN = "\d+\s(\+|\*)\s\d+"
PLUS_REGEX_PATTERN = "\d+\s\+\s\d+"
MULTIPLY_REGEX_PATTERN = "\d+\s\*\s\d+"

def get_homework_result_equations(use_operator_precedence=False):
    """ Return each homework equation result in a list """
    homework_result_list = []
    
    with open(HOMEWORK_FILE, 'r') as homeowork_file:
        for equation in homeowork_file:
            result = solve_complete_equation(equation.strip(), use_operator_precedence)
            homework_result_list.append(result)

    return homework_result_list

def solve_complete_equation(equation, use_operator_precedence=False):
    """
    Solve the whole given 'equation_str' by first solving each bracket and in the end compute the overall
    result by simply solving the equation from left to right. This function will identify all equations
    in brackets and solve them at first.
    Depending on given flag, operator precedence is applied or not.
    """
    # find first occurrence of brackets
    bracketed_equation = re.search(BRACKET_REGEX_PATTERN, equation)

    solve_equation = solve_equation_with_operator_precedence if use_operator_precedence\
                     else solve_equation_without_operator_precedence

    while bracketed_equation is not None:
        # solve equation
        result = solve_equation(bracketed_equation.group())

        # replace current match with computed value
        equation = re.sub(BRACKET_REGEX_PATTERN, str(result), equation, 1)

        # find next match
        bracketed_equation = re.search(BRACKET_REGEX_PATTERN, equation)

    # no brackets left in equation --> solve remaining equation
    equation_result = solve_equation(equation)

    return equation_result

# -------------------------- Puzzle 1 --------------------------

def solve_equation_without_operator_precedence(equation_str):
    """
    Solve given 'equation_str' and return the computed value. Given equation will not contain any brackets
    and is hence solvable by only considering each value and operator from left to right.
    """
    current_result = 0
    found_match =  re.search(OPERATOR_REGEX_PATTERN, equation_str)
    
    while found_match is not None:
        # equation will look exactly like this: value-1 (+ or *) value-2 --> split it at space
        value_1, operator, value_2 = found_match.group().split(' ')

        # get result of found equation
        current_result = compute_result(value_1, value_2, operator)

        # replace current match with computed value
        equation_str = re.sub(OPERATOR_REGEX_PATTERN, str(current_result), equation_str, 1)

        # find next match
        found_match = re.search(OPERATOR_REGEX_PATTERN, equation_str)

    return current_result

def compute_result(a, b, operator):
    if operator == '*':
        return int(a) * int(b)
    elif operator == '+':
        return int(a) + int(b)

# -------------------------- Puzzle 2 --------------------------

def solve_equation_with_operator_precedence(equation_str):
    """
    Solve given 'equation_str' and return the computed value. Given equation will not contain any brackets
    and is hence solvable by only considering each value and operator from left to right.
    However, addition takes precedence over multiplication! Hence, solve this parts first.
    Afterwards only multiplication operations are left. Solve them from left to right.
    """
    current_result = 0

    # solve all plus operations first
    found_match =  re.search(PLUS_REGEX_PATTERN, equation_str)
    while found_match is not None:
        # equation will look exactly like this: value-1 + value-2 --> split it at space
        value_1, _, value_2 = found_match.group().split(' ')

        # get result of found equation
        current_result = int(value_1) + int(value_2)

        # replace current match with computed value
        equation_str = re.sub(PLUS_REGEX_PATTERN, str(current_result), equation_str, 1)

        # find next match
        found_match = re.search(PLUS_REGEX_PATTERN, equation_str)

    # only multiplication left, solve equation from left to right
    found_match =  re.search(MULTIPLY_REGEX_PATTERN, equation_str)
    while found_match is not None:
        # equation will look exactly like this: value-1 + value-2 --> split it at space
        value_1, _, value_2 = found_match.group().split(' ')

        # get result of found equation
        current_result = int(value_1) * int(value_2)

        # replace current match with computed value
        equation_str = re.sub(MULTIPLY_REGEX_PATTERN, str(current_result), equation_str, 1)

        # find next match
        found_match = re.search(MULTIPLY_REGEX_PATTERN, equation_str)

    return current_result

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """ Find the sum of all homework equations """
    homework_result_list = get_homework_result_equations()
    sum_of_all_equations = sum(homework_result_list)
    print("[+] Solution of day18/puzzle1: Sum of all homework equations is {}".format(sum_of_all_equations))

    homework_result_list = get_homework_result_equations(use_operator_precedence=True)
    sum_of_all_equations = sum(homework_result_list)
    print("[+] Solution of day18/puzzle2: Sum of all homework equations with operator precedence is {}"\
          .format(sum_of_all_equations))

if __name__ == "__main__":
    compute_solution_of_puzzle()
