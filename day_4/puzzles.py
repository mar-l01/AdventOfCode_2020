import re

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

# -------------------------- Puzzle 1 --------------------------

def get_passports_with_required_fields(list_of_passports):
    """
    Go through given list of passports (dictionaries) and get all passports which contain
    all required fields. Only "cid" field is optional. Add them to a list and return it.
    """
    list_of_valid_passports = []

    for passport in list_of_passports:
        if all_required_fields_present(passport):
            list_of_valid_passports.append(passport)

    return list_of_valid_passports

def all_required_fields_present(passport):
    """ Return True if given passport contains all required fields """
    fields_of_current_passport = list(passport.keys())
    required_fields_present = True

    # check if above list of keys of the current passport contains all required keys
    for req_field in REQUIRED_FIELDS:
        if not req_field in fields_of_current_passport:
            required_fields_present = False
            break

    return required_fields_present

# -------------------------- Puzzle 2 --------------------------

def get_passports_with_valid_entries(list_of_valid_passports):
    """
    Given a list of valid passports (all required fields present), go through all
    of them and check if each field holds a valid entry.
    """
    list_of_passports_with_valid_entries = []

    for passport in list_of_valid_passports:
        if all_passport_entries_valid(passport):
            list_of_passports_with_valid_entries.append(passport)

    return list_of_passports_with_valid_entries

def all_passport_entries_valid(passport):
    """
    Check if all fields in given passport hold valid values.
    Note: We assume here that only valid passports (:= all required fields present)
    are given.
    """
    all_entries_valid = True

    # check if each entry of required fields holds a valid value
    for passport_entry in passport.items():
        if not is_passport_entry_valid(passport_entry):
            all_entries_valid = False
            break

    return all_entries_valid

def is_passport_entry_valid(passport_entry):
    """ Check if given passport entry (key, value) is valid """
    pp_key = passport_entry[0]
    pp_value = passport_entry[1]
    is_pp_entry_valid = False

    if pp_key == "byr":
        is_pp_entry_valid = is_year_valid(pp_value, 1920, 2002)
    elif pp_key == "iyr":
        is_pp_entry_valid = is_year_valid(pp_value, 2010, 2020)
    elif pp_key == "eyr":
        is_pp_entry_valid = is_year_valid(pp_value, 2020, 2030)
    elif pp_key == "hgt":
        is_pp_entry_valid = is_height_valid(pp_value)
    elif pp_key == "hcl":
        is_pp_entry_valid = is_hcl_valid(pp_value)
    elif pp_key == "ecl":
        is_pp_entry_valid = is_ecl_valid(pp_value)
    elif pp_key == "pid":
        is_pp_entry_valid = is_pid_valid(pp_value)
    elif pp_key == "cid":
        is_pp_entry_valid = True # cid is optional, thus ignored

    return is_pp_entry_valid

def is_number_valid(number_str, number_min, number_max):
    """ Return true if number (given as str) is within given range and convertible to an integer """
    is_nb_valid = False

    # make sure string is convertible to an integer
    try:
        number = int(number_str)
        if number_min <= number <= number_max:
            is_nb_valid = True
    except:
        print("[!] Could not parse given string: {})".format(pp_value))

    return is_nb_valid

def is_year_valid(str_year, year_min, year_max):
    """ Check if given year (as str) is valid under given conditions (:= min, max value) """
    is_year_valid = False

    # year has to be given as 4 digits
    if len(str_year) == 4:
        is_year_valid = is_number_valid(str_year, year_min, year_max)

    return is_year_valid

def is_height_valid(str_height):
    """
    Check if given height (as str) is valid under given conditions:
    - if 'cm': height at least 150 and at most 193
    - if 'in': height must be at least 59 and at most 76

    Note: str_height is given as 192cm or 70in assuming that the last two
    characters denote the unit and the first characters until the second to
    last denote the height value.
    """
    is_height_valid = False

    # make sure string is long enough (expect at least 1 number and 2 chars for 'cm' or 'in')
    if len(str_height) <= 3:
        return is_height_valid

    # expect the first characters until the second to last to determine the height
    height = str_height[:-2]

    # expect the last two characters to determine the height unit
    height_unit = str_height[-2:]

    if height_unit == "cm":
        is_height_valid = is_number_valid(height, 150, 193)
    elif height_unit == "in":
        is_height_valid = is_number_valid(height, 59, 76)

    return is_height_valid

def is_hcl_valid(str_hcl):
    """
    Check if given hair color (as str) is valid under given conditions:
    - '#' followed by exactly six characters (0-9 or a-f)
    """
    is_hcl_valid = False
    expected_length = 7
    pattern = "(^#)[0-9, a-f]{" + str(expected_length - 1) + "}"

    if len(str_hcl) == expected_length and re.match(pattern, str_hcl):
        is_hcl_valid = True

    return is_hcl_valid

def is_ecl_valid(str_ecl):
    """
    Check if given eye color (as str) is valid under given conditions:
    - exactly one of: amb blu brn gry grn hzl oth
    """
    return str_ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

def is_pid_valid(str_pid):
    """
    Check if given pid (as str) is valid under given conditions:
    - a nine-digit number, including leading zeroes
    """
    is_pid_valid = False
    expected_length = 9
    pattern = "[0-9]{" + str(expected_length) + "}"

    if len(str_pid) == expected_length and re.match(pattern, str_pid):
        is_pid_valid = True

    return is_pid_valid

# -------------------------- Solution of puzzles 1 and 2 --------------------------

def compute_solution_of_puzzle():
    """ Find the total number of valid passports """
    list_of_passports = get_list_of_passports()
    list_of_valid_passports = get_passports_with_required_fields(list_of_passports)

    print("[+] Solution of day4/puzzle1: {} passports are valid".format(len(list_of_valid_passports)))

    list_of_passports_with_valid_entries = get_passports_with_valid_entries(list_of_valid_passports)
    print("[+] Solution of day4/puzzle2: {} passports have all entries containing valid values"\
          .format(len(list_of_passports_with_valid_entries)))

if __name__ == "__main__":
    compute_solution_of_puzzle()
