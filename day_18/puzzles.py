import re

HOMEWORK_FILE = "homework.txt"

BRACKET_REGEX_PATTERN = "\(\d+(\s(\+|\*)\s\d+)+\)"
OPERATOR_REGEX_PATTERN = "\d+\s(\+|\*)\s\d+"

def get_homework_result_equations():
    """ Return each homework equation result in a list """
    homework_result_list = []
    
    with open(HOMEWORK_FILE, 'r') as homeowork_file:
        for equation in homeowork_file:
            result = solve_complete_equation(equation.strip())
            homework_result_list.append(result)

    return homework_result_list

def solve_complete_equation(equation):
    """
    Solve the whole given 'equation_str' by first solving each bracket and in the end compute the overall
    result by simply solving the equation from left to right. This function will identify all equations
    in brackets and solve them at first.
    """
    # find first occurrence of brackets
    bracketed_equation = re.search(BRACKET_REGEX_PATTERN, equation)

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

def solve_equation(equation_str):
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

def compute_solution_of_puzzle():
    """ Find the sum of all homework equations """
    homework_result_list = get_homework_result_equations()
    sum_of_all_equations = sum(homework_result_list)

    print("[+] Solution of day18/puzzle1: Sum of all homework equations is {}".format(sum_of_all_equations))

if __name__ == "__main__":
    compute_solution_of_puzzle()
