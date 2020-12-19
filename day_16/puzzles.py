import re
import numpy as np

TICKET_TRANSLATION_FILE = "ticket_translation.txt"

def get_ticket_translation_notes_as_list():
    """
    Read in above file and create three objects out of it. First, the rules given will be returned as dictionary.
    My ticket numbers as well as the nearby ticket numbers will be returned as list of numbers.
    """
    ticket_rules = {}
    my_ticket = []
    nearby_tickets = []

    rule_key_pattern = "\w*[\s\w*]*:"
    rule_value_pattern = "\d+-\d+"
    
    with open(TICKET_TRANSLATION_FILE, 'r') as ticket_translation_file:
        # flags used to determine if following tickets are one out of those
        is_my_ticket = False
        is_nearby_ticket = False
        
        for ticket_translation_line in ticket_translation_file:
            
            # if line contains a 'or' assume its a rules line
            if "or" in ticket_translation_line:
                # extract key -> remove colon
                key = (re.findall(rule_key_pattern, ticket_translation_line)[0])[:-1]

                # extract intervalls
                range1, range2 = re.findall(rule_value_pattern, ticket_translation_line)

                # extract single numbers of range intervalls
                value1_range1, value2_range1 = range1.split('-')
                value1_range2, value2_range2 = range2.split('-')

                # add key-value pairs to dict
                ticket_rules[key] = [(int(value1_range1), int(value2_range1)),\
                                     (int(value1_range2), int(value2_range2))]

            elif "your ticket" in ticket_translation_line:
                is_my_ticket = True
            elif is_my_ticket:
                is_my_ticket = False # reset flag as it is only a single line to read
                my_ticket = [int(value) for value in ticket_translation_line.strip().split(',')]

            elif "nearby tickets" in ticket_translation_line:
                is_nearby_ticket = True
            elif is_nearby_ticket: # no need to reset flag --> read until end
                nearby_tickets.append([int(value) for value in ticket_translation_line.strip().split(',')])

    return ticket_rules, my_ticket, nearby_tickets

# -------------------------- Puzzle 1 --------------------------

def check_invalid_nearby_tickets(ticket_rules, nearby_tickets):
    """
    Iterate over all given tickets in 'nearby_tickets' and remember all invalid ticket values.
    Return them as a list. Return an additional list which contains all remaining valid tickets.
    Tickets which contain an invalid number are thus discarded completely.
    """
    invalid_ticket_values = []
    remaining_valid_tickets = []
    
    for nearby_ticket in nearby_tickets:
        invalid_values_of_ticket = get_invalid_ticket_values(ticket_rules, nearby_ticket)

        # assume that an empty list refers to a valid ticket
        if invalid_values_of_ticket == []:
            remaining_valid_tickets.append(nearby_ticket)
        else:
            invalid_ticket_values += invalid_values_of_ticket

    return invalid_ticket_values, remaining_valid_tickets

def get_invalid_ticket_values(ticket_rules, nearby_ticket):
    """
    Use given 'nearby_ticket' and check if each value int this list matches at least one rule of given
    'ticket_rules'. If a value does not match the given rule, add them to a list. In the end return
    this list.
    """
    invalid_values = []

    # go through each value of given ticket
    for value in nearby_ticket:
        # check if value matches at least 1 rule (which one does not matter!)
        value_does_not_match_rule = True
        for intervalls in ticket_rules.values():
            if value_matches_rule(intervalls, value):
                value_does_not_match_rule = False

        # value did not match to any rule --> add it to non-matching values list
        if value_does_not_match_rule:
            invalid_values.append(value)

    return invalid_values

def value_matches_rule(intervalls, value):
    """ Check if given 'value' is in intervall given as list of two intervalls in 'ticket_rule' """
    interval_1, interval_2 = intervalls
    if interval_1[0] <= value <= interval_1[1] or\
        interval_2[0] <= value <= interval_2[1]:
        return True

    return False    

# -------------------------- Puzzle 2 --------------------------

def determine_possible_ticket_fields(ticket_rules, my_ticket, nearby_tickets):
    """
    Check each element of each list in parallel if it matches any rule. If so, assume that it represents
    the respective rule. Use a dictionary to map rules to index of list. In case more than one column matches
    a given rule -> add them as list.

    Note: The list out of lists is transformed into a numpy matrix for easier search.
    """
    rules_to_index_dict = {}

    # add my ticket to list of tickets and transform it to a matrix
    nearby_tickets.append(my_ticket)
    all_tickets_matrix = np.array(nearby_tickets)

    # iterate over each rule and check if it matches any column
    for ticket_rule in ticket_rules.items():
        name, intervalls = ticket_rule

        # iterate over each column
        for idx in range(all_tickets_matrix.shape[1]):
            column = all_tickets_matrix[:, idx]
            column_matches_rule = True
            
            # check each column value
            for value in column:
                # value does not match above rule -> rule cannot be applied to this column
                if not value_matches_rule(intervalls, value):
                    column_matches_rule = False
                    break

            # did all values in column match this rule? start with next rule
            if column_matches_rule:
                # add more matching rules as list to key
                if name in rules_to_index_dict.keys():
                      rules_to_index_dict[name] += [idx]
                else:
                    rules_to_index_dict[name] = [idx]

    return rules_to_index_dict

def identify_ticket_fields(rules_to_index_dict):
    """
    Use given dictionary of rules mapped to array positions to identify the matching fields.
    How to: Iterate over all dicitionary values and check if only 1 element is present in the
    respective list. If so, remove this value from all other values of the other rules.
    Hopefully, in the end a dictionary which holds only values of length 1 for each key is
    present.

    Note: since Python uses pass by reference for dictionary object/list objects, the elements
    are removed in place without copying.
    """
    single_indices_removed = []
    
    # if only 1 index is present for a single rule, this index is removed from all other rules
    while True:
        single_indices = []
        single_index_found = False

        # find single index 
        for rule, indices in rules_to_index_dict.items():
            # only consider single indices which were not processed before
            if len(indices) == 1 and indices[0] not in single_indices_removed:
                single_indices.append(indices[0])
                single_index_found = True

        # remove it from other rules list
        for rule, indices in rules_to_index_dict.items():
            for single_index in single_indices:
                if single_index in indices and len(indices) != 1:
                    indices.remove(single_index)

        # mark currently removed indices as removed
        single_indices_removed += single_indices

        if not single_index_found:
            break

def multiply_values_at_departure_fields_of_my_ticket(possible_ticket_fields, my_ticket):
    """ Multiply the values of 'my_ticket' which belongs to the respective fields marked 'departure X' """
    departure_field_indices = [values[0] for key, values in possible_ticket_fields.items() if "departure" in key]

    product = 1
    for idx in departure_field_indices:
        product *= my_ticket[idx]
    
    return product

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """ Find ticket scanning error rate """
    ticket_rules, my_ticket, nearby_tickets = get_ticket_translation_notes_as_list()
    invalid_nearby_ticket_values, remaining_valid_tickets = check_invalid_nearby_tickets(ticket_rules, nearby_tickets)

    ticket_scanning_error_rate = sum(invalid_nearby_ticket_values)
    print("[+] Solution of day16/puzzle1: The ticket scanning error rate is {}".format(ticket_scanning_error_rate))

    possible_ticket_fields = determine_possible_ticket_fields(ticket_rules, my_ticket, remaining_valid_tickets)
    identify_ticket_fields(possible_ticket_fields)
    multiplied_departure_fields = multiply_values_at_departure_fields_of_my_ticket(possible_ticket_fields, my_ticket)
    print("[+] Solution of day16/puzzle2: The product of 'departure X' values of my ticket is {}".format(multiplied_departure_fields))

if __name__ == "__main__":
    compute_solution_of_puzzle()
