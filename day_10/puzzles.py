OUTPUT_JOLTAGE_FILE = "output_joltage.txt"

def get_output_joltage_list():
    """ Return the content of above file as a list of values. """
    output_joltate_list = []

    with open(OUTPUT_JOLTAGE_FILE, 'r') as output_joltage_file:
        for output_joltage in output_joltage_file:
           output_joltate_list.append(int(output_joltage))

    return output_joltate_list

def find_number_of_1_and_3_jolt_differences(output_joltage_list):
    """
    First of all, sort given input list. Then, count the difference of n and n-1 element: If it is 1
    increment the count of 1-difference, if it is 3 increment the count of 3-difference.

    Notes:
    - The rating of the charging-outlet is 0 jolts: Added to list of output_joltage, so it is included,
      when calculating the difference.
    - Since your device's built-in adapter is always 3 higher, increment 3-difference count at the start.
    """
    # copy list and sort it in ascending order
    sorted_joltage_list = output_joltage_list[:]
    sorted_joltage_list.append(0) # charging-outlet rating of 0 jolts
    sorted_joltage_list.sort()

    difference_1 = 0
    difference_3 = 1 # device's built-in adapter is always 3 higher

    # iterate over list and count differences
    for i in range(1, len(sorted_joltage_list)):
        cur_diff = sorted_joltage_list[i] - sorted_joltage_list[i - 1]

        if cur_diff == 1:
            difference_1 += 1
        elif cur_diff == 3:
            difference_3 += 1

    return difference_1, difference_3

def compute_solution_of_puzzle():
    """
    Find a chain that uses all of your adapters to connect the charging outlet to your device's built-in
    adapter and count the joltage differences between the charging outlet, the adapters, and your device.
    """
    output_joltage_list = get_output_joltage_list()
    diff_1, diff_3 = find_number_of_1_and_3_jolt_differences(output_joltage_list)

    print("[+] Solution of day10/puzzle1: {} is the number of 1-jolt differences multiplied by the number "\
          "of 3-jolt differences".format(diff_1 * diff_3))
  
if __name__ == "__main__":
    compute_solution_of_puzzle()

