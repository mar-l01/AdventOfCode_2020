EXPENSE_REPORT_FILE = "expense_report.txt"

def find_both_expenses(expenses_list):
    """
    Imagine a matrix with row and colum representing the given list of
    expenses. Check if row and colum value add up to 2020 and if so,
    return both values. In case no value is found, return a default of 0.
    """
    for expense_value_1 in expenses_list:
        for expense_value_2 in expenses_list:
            if expense_value_1 + expense_value_2 == 2020:
                print("[+] Found both values: {} + {} = 2020" \
                      .format(expense_value_1, expense_value_2))
                return expense_value_1, expense_value_2

    print("[!] Did not find two values 'a' and 'b' which met the condition: sum(a,b) = 2020")
    return 0, 0        

def compute_solution_of_puzzle_1():
    """
    Iterate through given text file which contains the values of the expense
    report. Find the numbers which add up to 2020 and return their product.
    """
    expenses_list = []
    with open(EXPENSE_REPORT_FILE, 'r') as expense_report:
        for expense in expense_report:
            expenses_list.append(int(expense))

    expense_1, expense_2 = find_both_expenses(expenses_list)
    solution_puzzle_1 = expense_1 * expense_2
    
    print("[+] Solution of puzzle 1: {} * {} = {}".format(expense_1, expense_2, solution_puzzle_1))

if __name__ == "__main__":
    compute_solution_of_puzzle_1()
