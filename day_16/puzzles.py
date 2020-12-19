import re

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

def check_invalid_nearby_tickets(ticket_rules, nearby_tickets):
    """
    Iterate over all given tickets in 'nearby_tickets' and remember all invalid ticket values.
    Return them as a list.
    """
    invalid_ticket_values = []
    
    for nearby_ticket in nearby_tickets:
        invalid_values_of_ticket = get_invalid_ticket_values(ticket_rules, nearby_ticket)
        invalid_ticket_values += invalid_values_of_ticket

    return invalid_ticket_values

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

def compute_solution_of_puzzle():
    """ Find ticket scanning error rate """
    ticket_rules, my_ticket, nearby_tickets = get_ticket_translation_notes_as_list()
    invalid_nearby_ticket_values = check_invalid_nearby_tickets(ticket_rules, nearby_tickets)

    ticket_scanning_error_rate = sum(invalid_nearby_ticket_values)
    print("[+] Solution of day16/puzzle1: The ticket scanning error rate is {}".format(ticket_scanning_error_rate))

if __name__ == "__main__":
    compute_solution_of_puzzle()
