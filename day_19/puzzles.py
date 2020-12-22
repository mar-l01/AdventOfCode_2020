import re

MONSTER_MESSAGES_FILE = "monster_messages.txt"

def get_rules_and_messages():
    """ Extract the rules from given file as dictionar and return the messages as list """
    rules_dict = {}
    messages_list = []
    
    with open(MONSTER_MESSAGES_FILE, 'r') as monster_messages_file:
        # rules are separated from messages by a blank line
        is_rule = True
        
        for line in monster_messages_file:
            # empty line? if yes, messages will come on next iteration
            if len(line.strip()) == 0:
                is_rule = False
                continue
            
            # rules
            if is_rule:
                # rule has, for example, following layout --> 118: 47 17 | 84 57, split at : first to get key
                rule_number, rule = line.strip().split(':')
                rule_number = int(rule_number)
                rule = rule.strip()

                # two rules applicable? --> split at | and then at space to extract both options
                if '|' in rule:
                    rule_opt_1, rule_opt_2 = rule.split('|')

                    # split at space to get inner rules
                    rules_opt_1 = rule_opt_1.strip().split(' ')
                    rules_opt_2 = rule_opt_2.strip().split(' ')

                    # check if a single rule is given or two rules
                    if len(rules_opt_1) == 1 and len(rules_opt_2) == 1:
                        rule = [[int(rules_opt_1[0])], [int(rules_opt_2[0])]]
                    else:
                        rule = [[int(rules_opt_1[0]), int(rules_opt_1[1])],\
                                [int(rules_opt_2[0]), int(rules_opt_2[1])]]

                # more than one rule number available? --> split at space and add both numbers to list
                elif ' ' in rule:
                    rule_1, rule_2 = rule.split(' ')
                    rule = [int(rule_1), int(rule_2)]
                
                # single char in rule
                elif '"' in rule:
                    rule = rule.replace('"', '') # remove ".." from char

                # single value written
                else:
                    rule = int(rule)

                rules_dict[rule_number] = rule

            # messages
            else:
                messages_list.append(line.strip())

    return rules_dict, messages_list

def find_matching_messages_for_rule(rules_dict, messages_list, rule_nb):
    """
    Iterate over given 'messages_list' and check if given rule (represented via 'rule_nb') is
    applicable to each message.
    Return the total number of matching messages.
    """
    nb_of_matching_messages = 0

    for msg in messages_list:
        if is_given_rule_applicable(rules_dict, rule_nb, msg):
            nb_of_matching_messages += 1

    return nb_of_matching_messages

def is_given_rule_applicable(rules_dict, rule_nb, message):
    """
    Check if rule which is defined by given 'rule_nb' is applicable on given 'message'.
    Iterate over message and test if the rule matches.
    """
    rule_matches_message = False
    rule_pattern = create_regex_pattern(rules_dict, 0)
    
    # test if whole string matches computed pattern
    matching_message = re.fullmatch(rule_pattern, message)
    if matching_message:
        rule_matches_message = True

    return rule_matches_message

def create_regex_pattern(rules_dict, key):
    """
    Use given 'rules_dict' to resolve the rules given in 'key'. Return the resolved rule
    as a sequence of 'a's and 'b's, which in turn represents a regular expression
    """
    rule = rules_dict[key]

    # stop condition: rule is either 'a' or 'b'
    if rule == 'a':
        return 'a'
    elif rule == 'b':
        return 'b'

    # continue resolving of rule recursively
    else:
        # rule consists of a pipe ('|') or is simply combined out of two rules (' ')
        if type(rule) is list:
            # piped rule
            if type(rule[0]) is list:
                rule_opt_1, rule_opt_2 = rule[0], rule[1]
                # check if a single rule is given or two rules at each side of the pipe
                if len(rule_opt_1) == 1 and len(rule_opt_2) == 1:
                    return '(' + create_regex_pattern(rules_dict, rule_opt_1[0]) + '|' +\
                            create_regex_pattern(rules_dict, rule_opt_2[0]) + ')'
                else:
                    return '(' + create_regex_pattern(rules_dict, rule_opt_1[0]) + \
                            create_regex_pattern(rules_dict, rule_opt_1[1]) + '|' +\
                            create_regex_pattern(rules_dict, rule_opt_2[0]) + \
                            create_regex_pattern(rules_dict, rule_opt_2[1]) + ')'
    
            # combined rule
            else:
                rule_1, rule_2 = rule[0], rule[1]
                return create_regex_pattern(rules_dict, rule_1) +\
                       create_regex_pattern(rules_dict, rule_2)

        # rule consists of only a single number
        else:
            return create_regex_pattern(rules_dict, rule) 

def compute_solution_of_puzzle():
    """ Find the total number of valid messages given a specific rule """
    rules_dict, messages_list = get_rules_and_messages()
    nb_of_matching_messages = find_matching_messages_for_rule(rules_dict, messages_list, 0)
    
    print("[+] Solution of day19/puzzle1: {} messages are valid using rule 0".format(nb_of_matching_messages))

if __name__ == "__main__":
    compute_solution_of_puzzle()
