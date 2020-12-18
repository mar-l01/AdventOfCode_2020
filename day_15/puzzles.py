STARTING_NUMBERS = [7,14,0,17,11,1,2]

# -------------------------- Puzzle 1 --------------------------

def simulate_memory_game():
    """
    Play the game: Each turn consists of considering the most recently spoken number:

    If that was the first time the number has been spoken, the current player says 0.
    Otherwise, the number had been spoken before; the current player announces how many turns apart
    the number is from when it was previously spoken.
    So, after the starting numbers, each turn results in that player speaking aloud either
    0 (if the last number is new) or an age (if the last number is a repeat).
    """
    # simulate first round (last value will be used in first 'real' round)
    already_spoken_numbers = STARTING_NUMBERS
    current_round = len(STARTING_NUMBERS)
    
    while current_round != 2020:
        last_spoken_number = already_spoken_numbers[-1]

        # last spoken number was not spoken before --> speak 0
        if last_spoken_number not in already_spoken_numbers[:-1]:
            already_spoken_numbers.append(0)

        # last spoken number was already spoken before --> speak difference of turn numbers
        else:
            # turn number, the number was last spoken (turn starts at 1)
            last_spoken_turn_number = len(already_spoken_numbers) - (already_spoken_numbers[:-1])[::-1].index(last_spoken_number) - 1
            turn_difference = current_round - last_spoken_turn_number

            already_spoken_numbers.append(turn_difference)
            
        current_round += 1

    return already_spoken_numbers[-1]

# -------------------------- Puzzle 2 --------------------------

def simulate_memory_game_more_efficient(turn_number):
    """
    Play the game: Each turn consists of considering the most recently spoken number:

    Instead of appending the last spoken number to an array (pretty long array when millions of turns),
    use a dictionary which holds the latest turn of each spoken value.
    """
    already_spoken_numbers = dict(zip(STARTING_NUMBERS[:-1], [i for i in range(1, len(STARTING_NUMBERS))]))
    last_spoken_number = (STARTING_NUMBERS[-1], len(STARTING_NUMBERS))

    for current_round in range(len(STARTING_NUMBERS) + 1, turn_number + 1):
        next_last_spoken_number = None

        # last spoken number was not spoken before --> speak 0
        if last_spoken_number[0] not in already_spoken_numbers.keys():
            next_last_spoken_number = (0, current_round)

        # last spoken number was already spoken before --> speak difference of turn numbers
        else:
            turn_difference = last_spoken_number[1] - already_spoken_numbers[last_spoken_number[0]]
            next_last_spoken_number = (turn_difference, current_round)

        # add value from last round
        already_spoken_numbers[last_spoken_number[0]] = current_round - 1
        last_spoken_number = next_last_spoken_number
        
    return last_spoken_number[0]

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """ Find the sum of all set memory addresses entries """
    number_spoken_at_2020th_turn = simulate_memory_game()
    print("[+] Solution of day15/puzzle1: {} is the 2020th spoken number".format(number_spoken_at_2020th_turn))

    number_spoken_at_30000000th_turn = simulate_memory_game_more_efficient(30000000)
    print("[+] Solution of day15/puzzle2: {} is the 30000000th spoken number".format(number_spoken_at_30000000th_turn))

if __name__ == "__main__":
    compute_solution_of_puzzle()
