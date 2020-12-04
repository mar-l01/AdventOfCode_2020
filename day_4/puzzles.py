PASSPORTS_FILE = "passports.txt"

PASSPORT_ENTRIES_DELIMITER = ' '
KEY_VALUE_DELIMITER = ':'

REQUIRED_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
OPTIONAL_FIELDS = ["cid"]

def get_list_of_passports():
    """
    Return a list of all passport which were scanned:
    - Each passport is represented internally as a dict-type
    - Iterate through each line
        > if an empty line is found, a passport was fully processed
        > if a new line char is found, continue to fill currently processed passport
          with all key-value pairs in that line
    """
    list_of_passports = []
    
    with open(PASSPORTS_FILE, 'r') as passports_file:
        passport = {}
        for pp_line in passports_file:
            # remove spaces
            pp_line = pp_line.strip()
            
            # empty line?
            if not pp_line:
                # yes -> end of currently processed passport: add it to list, start anew
                list_of_passports.append(passport)
                passport = {}
            else:
                # no -> continue to fill currently processed passport dict
                for key_value_pair in pp_line.split(PASSPORT_ENTRIES_DELIMITER):
                    key, value = key_value_pair.split(KEY_VALUE_DELIMITER)
                    passport[key] = value

        # do not forget to append the last passport
        list_of_passports.append(passport)

    return list_of_passports  

def get_number_of_valid_passports(list_of_passports):
    """
    Go through given list of passports (dictionaries) and count all passports which contain
    all required fields. Only "cid" field is optional.
    """
    nb_of_valid_passports = 0
    
    for passport in list_of_passports:
        fields_of_current_passport = list(passport.keys())
        required_fields_present = True

        # check if above list of keys of the current passport contains all required keys
        for req_field in REQUIRED_FIELDS:
            if not req_field in fields_of_current_passport:
                required_fields_present = False
                break

        if required_fields_present:
            nb_of_valid_passports += 1

    return nb_of_valid_passports

def compute_solution_of_puzzle():
    """ Find the total number of valid passports """
    list_of_passports = get_list_of_passports()
    nb_of_valid_passports = get_number_of_valid_passports(list_of_passports)

    print("[+] Solution of day4/puzzle1: {} passports are valid".format(nb_of_valid_passports))

if __name__ == "__main__":
    compute_solution_of_puzzle()
