OUTPUT_JOLTAGE_FILE = "output_joltage.txt"

def get_output_joltage_list():
    """ Return the content of above file as a list of values. """
    output_joltate_list = []

    with open(OUTPUT_JOLTAGE_FILE, 'r') as output_joltage_file:
        for output_joltage in output_joltage_file:
           output_joltate_list.append(int(output_joltage))

    return output_joltate_list

# -------------------------- Puzzle 1 --------------------------

def find_number_of_n_jolt_differences(sorted_joltage_list):
    """
    First of all, sort given input list. Then, count the difference of n and n-1 element: If it is 1
    increment the count of 1-difference, if it is 3 increment the count of 3-difference.

    Notes:
    - The rating of the charging-outlet is 0 jolts: First value to consider when calculating the difference.
    - Since your device's built-in adapter is always 3 higher, increment 3-difference count at the end.
    """

    difference_1 = 0
    difference_3 = 0

    def increment_diff(cur_diff):
        nonlocal difference_1
        nonlocal difference_3

        if cur_diff == 1:
            difference_1 += 1
        elif cur_diff == 3:
            difference_3 += 1

    # first difference: from charging-outlet to first joltage adapter
    increment_diff(sorted_joltage_list[0] - 0)
    
    # iterate over list and count differences
    for i in range(1, len(sorted_joltage_list)):
        cur_diff = sorted_joltage_list[i] - sorted_joltage_list[i - 1]
        increment_diff(cur_diff)

    # last difference: from joltage adapters to device: difference of 3
    increment_diff(3)

    return difference_1, difference_3

# -------------------------- Puzzle 2 --------------------------

def get_device_joltage(sorted_joltage_list):
    """ Increment the last element by 3 and return it as the device's jolt value. """
    return (sorted_joltage_list[-1]) + 3

def get_all_ways_to_connect_to_charging_outlet(sorted_joltage_list, device_joltage):
    """
    Repeatedly, iterate over given 'sorted_joltage_list' and count all ways which
    lead to the device joltage provided in the respective variable.

    Note: Add charging-outlet joltage and device-joltage to list as [0]th and [-1]th element
    """
    combined_joltage_list = [0] # charing-outlet joltage
    combined_joltage_list += sorted_joltage_list # adapters joltage
    combined_joltage_list.append(device_joltage) # device joltage

    return find_all_ways_efficiently(combined_joltage_list)

def find_all_ways_efficiently(joltage_list):
    """
    Iterate through given 'joltage_list' and check for every list-element (:= node) how many possible
    ways to proceed from there exist, i.e. how many of the following three elements are within the
    intervall [node + 1 : node + 3].

    For example, let joltage-list be [0,1,4,5,6,7]. The only possible way to continue from 0 is 1 as
    it is the only node reachable by adding 1, 2 or 3. However, from node 4 on, we can go to 5,
    6 or 7, each is within the intervall [4+1 :  4+3].
    
    For each node in given list, check if it branches next, i.e. more than one other node can be found
    as next possible node. If so count the number of branches (1, 2, 3). If it branches the first time,
    do not forget to remove the default branch --> reduce number of branches by 1. While branched, sum
    up the following number of branches. If a 'leaf-node' is reached, multiply the overall number of
    branches by the number of subbranches found.

    As an example, take above joltage-list:
    1) 0 --> next nodes: 1 --> nothing happens, still 1 branch
    2) 1 --> next nodes: 4 --> nothing happens, still 1 branch
    3) 4 --> next nodes: 5,6,7 --> we are branching --> sum of subbranches = 3
    4) 5 --> next nodes: 6,7 --> we are already branched --> sum of subbranches = 4 (= 3 + 2 - 1 (:= remove default branch))
    5) 6 --> next nodes: 7 --> we left branched way --> sum of total branches = 4 (= 1 * 4)
    6) and so on
    """
    all_possible_branches = 1 # default path
    sum_of_sub_branches = 0

    currently_branched = False
    remove_default_branch = False
    
    for node in joltage_list:
        # compute possible next nodes
        nb_of_next_nodes = len([node + i for i in range(1, 4) if (node + i) in joltage_list])
        
        if not currently_branched:
            # check if list branches, e.g. more than 1 node could be next
            if nb_of_next_nodes > 1:
                sum_of_sub_branches = nb_of_next_nodes
                currently_branched = True
                remove_default_branch = True
        else:
            # 'leaf-node' reached, e.g. no branches anymore only 1 node can be next
            if nb_of_next_nodes == 1:
                currently_branched = False
                all_possible_branches *= sum_of_sub_branches
            else:
                # everytime the list branches, the default branch needs to be removed once
                if remove_default_branch:
                    sum_of_sub_branches += (len(next_nodes) - 1)
                    remove_default_branch = False
                else:                   
                    sum_of_sub_branches += len(next_nodes)

    return all_possible_branches

def find_all_ways(joltage_list):
    """
    Iterate through the list. For each node (:= list-element) in the list, check how many different
    ways exist to continue from there. Recursively, check each of the different ways until a 'leaf'-
    node was reached. A 'leaf'-node is thereby defined by reaching the end of the list (:= device joltage)

    Warning: This is example can take hours/days, as this recursive algorithm will try every possible way
             like a brute-force process. So, it's only recommended for a small list of numbers, e.g.
             the first example list.
    """
    if len(joltage_list) == 1:
        # 'leaf' reached
        return 1

    current_node = joltage_list[0]
    next_nodes = [current_node + i for i in range(1, 4) if (current_node + i) in joltage_list]
    
    possible_ways = 0
    possible_next_nodes = len(next_nodes)

    if possible_next_nodes == 0:
        return 0  
    elif possible_next_nodes == 1:
        return find_all_ways(joltage_list[1:])
    elif possible_next_nodes == 2:
        joltage_list_cpy = joltage_list[2:]
        return find_all_ways(joltage_list[1:]) + find_all_ways(joltage_list_cpy)
    elif possible_next_nodes == 3:
        joltage_list_cpy = joltage_list[2:]
        joltage_list_cpy_2 = joltage_list[3:]
        return find_all_ways(joltage_list[1:]) + find_all_ways(joltage_list_cpy) + find_all_ways(joltage_list_cpy_2)

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """
    Find a chain that uses all of your adapters to connect the charging outlet to your device's built-in
    adapter and count the joltage differences between the charging outlet, the adapters, and your device.
    """
    sorted_joltage_list = get_output_joltage_list()
    sorted_joltage_list.sort()

    diff_1, diff_3 = find_number_of_n_jolt_differences(sorted_joltage_list)
    print("Diff 1: {}".format(diff_1))
    print("Diff 3: {}".format(diff_3))

    print("[+] Solution of day10/puzzle1: {} is the number of 1-jolt differences multiplied by the number "\
          "of 3-jolt differences".format(diff_1 * diff_3))

    device_joltage = get_device_joltage(sorted_joltage_list)
    nb_of_different_ways_to_connect = get_all_ways_to_connect_to_charging_outlet(sorted_joltage_list, device_joltage)

    print("[+] Solution of day10/puzzle2: There are {} different ways to connect my device to the output "\
          "joltage".format(nb_of_different_ways_to_connect))
  
if __name__ == "__main__":
    compute_solution_of_puzzle()

