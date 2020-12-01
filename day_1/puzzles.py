EXPENSE_REPORT_FILE = "expense_report.txt"

def get_list_of_expenses():
    """ Return the values of the expense report as a list of integers """
    expenses_list = []
    with open(EXPENSE_REPORT_FILE, 'r') as expense_report:
        for expense in expense_report:
            expenses_list.append(int(expense))

    return expenses_list

def find_two_expenses(expenses_list):
    """
    Imagine a matrix with row and colum representing the given list of
    expenses. Check if row and colum value add up to 2020 and if so,
    return both values. In case no value is found, return a default of 0.
    """
    for expense_value_1 in expenses_list:
        for expense_value_2 in expenses_list:
            if expense_value_1 + expense_value_2 == 2020:
                print("[+] Found following two values: {} + {} = 2020" \
                      .format(expense_value_1, expense_value_2))
                return expense_value_1, expense_value_2

    print("[!] Did not find two values 'a' and 'b' which met the condition: sum(a,b) = 2020")
    return 0, 0

def find_three_expenses(expenses_list):
    """
    Imagine a tensor with row, colum and depth representing the given list of
    expenses. Check if row, colum and depth value add up to 2020 and if so,
    return all three values. In case no value is found, return a default of 0.
    """
    for expense_value_1 in expenses_list:
        for expense_value_2 in expenses_list:
            for expense_value_3 in expenses_list:
                if expense_value_1 + expense_value_2 + expense_value_3 == 2020:
                    print("[+] Found following three values: {} + {} + {} = 2020" \
                          .format(expense_value_1, expense_value_2, expense_value_3))
                    return expense_value_1, expense_value_2, expense_value_3

    print("[!] Did not find three values 'a', 'b' and 'c' which met the condition: sum(a,b,c) = 2020")
    return 0, 0, 0

def compute_solution_of_puzzle():
    """ Find the numbers which add up to 2020 and return their product. """
    expenses_list = get_list_of_expenses()

    expense_1, expense_2 = find_two_expenses(expenses_list)
    solution_puzzle_1 = expense_1 * expense_2
    print("[+] Solution of day1/puzzle1: {} * {} = {}".format(expense_1, expense_2, solution_puzzle_1))

    expense_1, expense_2, expense_3 = find_three_expenses(expenses_list)
    solution_puzzle_2 = expense_1 * expense_2 * expense_3
    print("[+] Solution of day1/puzzle2: {} * {} * {} = {}".format(expense_1, expense_2, expense_3,\
                                                                   solution_puzzle_2))

if __name__ == "__main__":
    compute_solution_of_puzzle()
