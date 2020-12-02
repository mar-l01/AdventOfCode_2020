LIST_OF_PASSWORDS_FILE = "list_of_passwords.txt"
POLICY_PASSWORD_DELIMITER = ':'
MIN_MAX_DELIMITER = '-'

def get_policy_password_list():
    """
    Return a list of tuples. Each tuple contains the password-policy
    as a dictionary {"letter" : 'a', "min" : 1, "max", 3} (here: policy
    is '1-3 a') and the respective password.
    """
    policy_password_list = []
    with open(LIST_OF_PASSWORDS_FILE, 'r') as password_file:
        for policy_pw in password_file:
            # split single line into policy and password
            policy, password = policy_pw.split(POLICY_PASSWORD_DELIMITER)
            # extract max and min letter value from policy
            # do not care about last two letters (space and letter, e.g. ' a')
            min_letter, max_letter = policy[:-2].split(MIN_MAX_DELIMITER)
            policy_dict = {"letter": policy[-1], "min": int(min_letter),\
                           "max": int(max_letter)}
            policy_password_list.append((policy_dict, password))

    return policy_password_list

def is_valid_password(policy, password):
    """
    Check if given password matches its policy: Iterate over the
    password and count the letter of given policy. In the end check
    if it matches the required amount of occurrences.
    """
    nb_of_occurrences = 0
    
    for char in password:
        if char == policy["letter"]:
            nb_of_occurrences += 1

    return policy["min"] <= nb_of_occurrences <= policy["max"]     
    
def compute_solution_of_puzzle():
    """ Find the passwords which do not match their according policy """
    policy_password_list = get_policy_password_list()
    nb_of_valid_passwords = 0

    for policy, password in policy_password_list:
        if is_valid_password(policy, password):
            nb_of_valid_passwords += 1

    print("[+] Solution of day2/puzzle1: {} valid passwords are given"\
          .format(nb_of_valid_passwords)) 

if __name__ == "__main__":
    compute_solution_of_puzzle()
