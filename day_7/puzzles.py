import numpy as np
import re

BAG_RULES_FILE = "bag_rules.txt"

def create_bag_rules_dictionary():
    """
    Iterate over above file and extract each bag (to which a rule is applied) and add it together with its according rule
    - key ----> 'bag-name' := first part of a single line, e.g. 'bright blue bags contain 5 [...]' -> 'bright blue'
    - value --> 'bag-rule' := dict consisting of each bag and its respective amount, e.g. '[...] contain 5 plaid teal bags,
      4 muted teal bags, 3 shiny salmon bags, 4 dull red bags.' -> {"palid teal": 5, "muted teal": 4, "shiny salmon": 3, ...}

    Furthermore, create a dictionary which maps a bag-name to a unique index, which is uesd for accessing the row/column in
    a matrix which gets created later.
    """
    bag_rule_dict = {} # name: rule
    bag_index_dict = {} # name: index
    
    with open(BAG_RULES_FILE, 'r') as bag_rules_file:
        for idx, bag_rule_line in enumerate(bag_rules_file):
            # extract bag-name to which the current rule is applied
            bag_name = bag_rule_line[:bag_rule_line.find('bag')].strip()
            bag_rule_dict[bag_name] = extract_bag_rule(bag_rule_line)
            bag_index_dict[bag_name] = idx

    return bag_rule_dict, bag_index_dict

def extract_bag_rule(bag_rule):
    """
    Use given bag rule line to extract all bags which should be contained in currently processed bag:
    [...] contain 5 plaid teal bags, 4 muted teal bags, 3 shiny salmon bags, 4 dull red bags.' will result in
    {"palid teal": 5, "muted teal": 4, "shiny salmon": 3, "dull red": 4}

    Note: Use regular expresions to extract necessary parts of string, e.g. <number><space><adj-1><adj-2>, where
    <adj-1> and <adj-2> denote the adjectives used to describe the contained bag, for example, 'dull red'.
    
    For interessted people: the pattern "(\w|\s)+(contain\s)(\d+\s\w+\s\w+\sbag[s]*,\s)*(\d+\s\w+\s\w+\sbag[s]*.)$"
    matches one whole 'bag_rule'
    """
    bag_rule_dict = {}
    pattern_bag_rule = "\d+\s\w+\s\w+"

    for contained_bag in re.findall(pattern_bag_rule, bag_rule):
        # splits number from bag-name (assume first space separates both)
        first_space_pos = contained_bag.find(' ')
        
        bag_amount = int(contained_bag[:first_space_pos])
        bag_name = contained_bag[first_space_pos:].strip()
        bag_rule_dict[bag_name] = bag_amount

    return bag_rule_dict

def create_bag_rules_matrix(bag_rules_dict, bag_index_dict):
    """
    Read all bag-rules which are present in provided dictionary and feed them into a matrix (n x n):
    - the rows represent the bag which rule was processed
    - the columns contain the rules (one rule per column), e.g. the number of bags which are contained in the 'row-bag'

    For example, the matrix might look as follows:
    
    |bags |bag-1|bag-2|bag-3|...|bag-n|
    |bag-1|  0  |  3  |  1  |...|  0  |  --> bag-1 must contain 3 bag-2 and 1 bag-3
    |bag-2|  1  |  0  |  0  |...|  1  |  --> bag-2 must contain 1 bag-1 and 1 bag-n
    """
    matrix_size_n = len(bag_rules_dict)
    bag_rules_matrix = np.empty([matrix_size_n, matrix_size_n], dtype=int)

    # iterate over bag rules (e.g. {"b1": {"b2": 3, "b3": 1}, "b2": {}, ..})
    for bag_name, bag_rules in bag_rules_dict.items():
        # get row of matrix depending on bag-name
        row = bag_index_dict[bag_name]

        # iterate over all rules for above bag-name (e.g. {"b2": 3, "b3": 1})
        for bag_rule_name, bag_rule_value in bag_rules.items():
            # fill respective matrix entry depending on given single bag rule
            col = bag_index_dict[bag_rule_name]
            bag_rules_matrix[row][col] = bag_rule_value 

    return bag_rules_matrix

def get_number_of_bags_containing_given_bag(bag_rules_matrix, bag_name_col):
    """
    Get the total amount of bags which can contain given bag (defined by 'bag_name_col').
    For each entry in the column (defined by given 'bag_name_col' index) which is > 0,
    the respective index is recursively added to the list.
    Return the length of created list which represents the number of bags which can
    contain provided bag.
    """
    list_of_bags = [] # will contain all bag-indices which can contain a gold bag
    recursive_bag_find(bag_rules_matrix, bag_name_col, list_of_bags)

    return len(list_of_bags)

def recursive_bag_find(bag_rules_matrix, bag_idx, list_of_bags):
    """
    Recursively, add all indices which contain the bag-name defined by 'bag_idx' to the
    'list_of_bags'. Function stops if no bag is found
    """
    column = bag_rules_matrix[:, bag_idx]

    for idx, item in enumerate(column):
        if idx in list_of_bags:
            continue
        if item > 0:
            list_of_bags.extend([idx])
            recursive_bag_find(bag_rules_matrix, idx, list_of_bags)

def compute_solution_of_puzzle():
    """ Find the sum of 'yes' answers of all groups """
    bag_rules_dict, bag_index_dict = create_bag_rules_dictionary()
    bag_rules_matrix = create_bag_rules_matrix(bag_rules_dict, bag_index_dict)

    shiny_gold_bag_column = bag_index_dict["shiny gold"]
    nb_bags_containing_a_shiny_gold_bag = get_number_of_bags_containing_given_bag(bag_rules_matrix, shiny_gold_bag_column)
    
    print("[+] Solution of day7/puzzle1: {} bags can contain a shiny gold bag".format(nb_bags_containing_a_shiny_gold_bag))

if __name__ == "__main__":
    compute_solution_of_puzzle()
