GROUP_ANSWERS = "group_answers.txt"

def get_list_of_group_answers():
    """
    Return a list of answers of each group listed in above file:
    - Each list element represents the answers of one group as a list
    - Each answer of an individual (:= 'ind n') in a single group (:= 'group n') is represented
      in an additional sublist, e.g.:
    [[['a', 'b', 'c'], ['a', 'c', 'f', 'o']], ...]
      |<-- ind 1 -->|  |<----  ind 2 ---->|
      |<-------------- group 1 ----------->|  ...
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
                single_group_answers.append([answer for answer in answer_line])

        # do not forget to append the last group answers
        list_of_group_answers.append(single_group_answers)

    return list_of_group_answers

# -------------------------- Puzzle 1 --------------------------

def filter_duplicated_entries(list_of_group_answers):
    """
    Return the input list with all duplicated entries of each sub-list (:= answers of a single
    group) removed, e.g.
    1) [['a', 'b', 'c', 'a', 'c'], ['d', 'd'], ['x', 'y', 'z']] becomes
    2) [['a', 'b', 'c'],           ['d'],      ['x', 'y', 'z']].

    First of all, the input list has to be transformed to the list mentioned in 1) by merging
    the sub-sub-lists (:= answers of a individual in a single group) into one list representing
    all answers of a single group, e.g.:
    [[['a', 'b', 'c'], ['a', 'c']], [['d'], ['d']], ['x', 'y', 'z']] becomes 1).

    Note: using set() duplicated entries are removed -> drawback: ordering of elements is lost
    """
    # transform input list
    list_of_group_answers = [[j for i in single_group_answers for j in i] for single_group_answers in list_of_group_answers]

    return [list(set(single_group_answers)) for single_group_answers in list_of_group_answers]

# -------------------------- Puzzle 2 --------------------------

def filter_uniform_yes_answers_of_each_group(list_of_group_answers):
    """
    In each group, get the answers which are present in each sub-list (:= answer of an individual).
    Assume that if 'element' of 'list a' is in 'list b' AND 'element' of 'list b' is in 'list c',
    then 'element' of 'list a' is also in 'list c'.

    E.g.: Given [[['a', 'b', 'c'], ['a', 'c']], [['d'], ['d']], ['x', 'y', 'z']], we iterate over
    each sub-list which contains all group answers (here: [['a', 'b', 'c'], ['a', 'c']] and [['d'], ['d']]
    and ['x', 'y', 'z']). Then, we iterate over each individual answers and check if 'individual answer a'
    for 'individual 1' is also contained
    """
    list_of_uniform_yes_group_answers = []

    # iterate over each group
    for group_answers in list_of_group_answers:
        uniform_single_group_answers = None

        # iterate over one individual answers (:= single line in given file)
        for individual_answers in group_answers:
            # first list of individual answers is always uniform
            if uniform_single_group_answers is None:
                uniform_single_group_answers = individual_answers
            else:
                # keep only those answers which are also present in currently processed individual answers
                uniform_single_group_answers = [uni_ans for uni_ans in uniform_single_group_answers if uni_ans in individual_answers]

        # finished processing answers of a single group -> found uniform answers
        list_of_uniform_yes_group_answers.append(uniform_single_group_answers)

    return list_of_uniform_yes_group_answers

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """ Find the sum of 'yes' answers of all groups """
    list_of_group_answers = get_list_of_group_answers()
    list_of_filtered_duplicated_group_answers = filter_duplicated_entries(list_of_group_answers)
    # sum-up the length of each sub-list (:= 'yes' answers of each single group without duplicates)
    sum_of_yes_group_answers = sum([len(single_group_answers) for single_group_answers in list_of_filtered_duplicated_group_answers])

    print("[+] Solution of day6/puzzle1: {} is the sum of 'yes' answers of all groups".format(sum_of_yes_group_answers))

    list_of_uniformed_yes_group_answers = filter_uniform_yes_answers_of_each_group(list_of_group_answers)
    sum_of_uniform_yes_group_answers = sum([len(single_group_answers) for single_group_answers in list_of_uniformed_yes_group_answers])

    print("[+] Solution of day6/puzzle2: {} is the sum of 'uniform yes' answers of all groups".format(sum_of_uniform_yes_group_answers))

if __name__ == "__main__":
    compute_solution_of_puzzle()
