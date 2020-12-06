GROUP_ANSWERS = "group_answers.txt"

def get_list_of_group_answers():
    """
    Return a list of answers of each group listed in above file:
    - Each list element represents the answers of one group as a list
    """
    list_of_group_answers = []

    with open(GROUP_ANSWERS, 'r') as group_answers_file:
        single_group_answers = []
        for answer_line in group_answers_file:
            # remove spaces
            answer_line = answer_line.strip()

            # empty line?
            if not answer_line:
                # yes -> end of currently processed group: add it to list, start anew
                list_of_group_answers.append(single_group_answers)
                single_group_answers = []
            else:
                # no -> continue to fill currently processed answers of a single group
                for answer in answer_line:
                    single_group_answers.append(answer)

        # do not forget to append the last group answers
        list_of_group_answers.append(single_group_answers)

    return list_of_group_answers

def filter_duplicated_entries(list_of_group_answers):
    """
    Return the input list with all duplicated entries of each sub-list (:= answers of a single
    group) removed, e.g.
    [['a', 'b', 'c', 'a', 'c'], ['d', 'd'], ['x', 'y', 'z']] becomes
    [['a', 'b', 'c'],           ['d'],      ['x', 'y', 'z']].

    Note: using set() duplicated entries are removed -> drawback: ordering of elements is lost
    """
    return [list(set(single_group_answers)) for single_group_answers in list_of_group_answers]

def compute_solution_of_puzzle():
    """ Find the sum of 'yes' answers of all groups """
    list_of_group_answers = filter_duplicated_entries(get_list_of_group_answers())
    # sum-up the length of each sub-list (:= 'yes' answers of each single group without duplicates)
    sum_of_yes_group_answers = sum([len(single_group_answers) for single_group_answers in list_of_group_answers])

    print("[+] Solution of day6/puzzle1: {} is the sum of 'yes' answers of all groups"\
          .format(sum_of_yes_group_answers))

if __name__ == "__main__":
    compute_solution_of_puzzle()
