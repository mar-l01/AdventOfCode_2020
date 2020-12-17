STARTING_NUMBERS = [7,14,0,17,11,1,2]

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

def compute_solution_of_puzzle():
    """ Find the sum of all set memory addresses entries """
    number_spoken_at_2020th_turn = simulate_memory_game()
    print("[+] Solution of day15/puzzle1: {} is the 2020th spoken number".format(number_spoken_at_2020th_turn))

if __name__ == "__main__":
    compute_solution_of_puzzle()
