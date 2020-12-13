BUS_SCHEDULE_FILE = "bus_schedule.txt"

def get_bus_schedules():
    """
    Get the earliset timestamp to depart from above file, and all busses as list
    (ignore 'x' busses -> out of service).
    """
    earliest_timestamp_to_depart = 0
    possible_busses = []
    
    with open(BUS_SCHEDULE_FILE, 'r') as bus_schedule_file:
        bus_schedule = bus_schedule_file.readlines()
        earliest_timestamp_to_depart = int(bus_schedule[0].strip())
        possible_busses = [int(bus_id) for bus_id in bus_schedule[1].strip().split(',')\
                           if bus_id != 'x']

    return earliest_timestamp_to_depart, possible_busses  

def get_earliest_possible_bus_departure(earliset_timestamp_to_depart, possible_busses):
    """
    Using the given list 'possible_busses' compute the earliest possible time to depart a bus.
    Return this bus-ID together with the number of minutes to wait for this bus.

    Note: Assuming that the modulo operation gives us the minutes the bus arrives before we arrive,
    as it returns the 'rest'. As the bus needs to arrive after we are at the station, this 'rest'
    is substracted from the next bus iteration. This gives us the time to wait for the next bus,
    after we have arrived at the bus station
    """
    # list contains the minutes the bus arrives BEFORE we arrive at the station
    bus_arrival_before_us = [(bus_id, (earliset_timestamp_to_depart % bus_id)) for bus_id in possible_busses]

    # list contains the minutes the bus arrives NEXT once we are at the station
    next_bus_arrival = [(id_min_pair[0], id_min_pair[0] - id_min_pair[1]) for id_min_pair in bus_arrival_before_us]

    # find minimum value (depending on minutes to wait := tuple parameter at index [1])
    bus_id_minimum_waiting_time = min(next_bus_arrival, key=lambda id_min_pair: id_min_pair[1])

    return bus_id_minimum_waiting_time

def compute_solution_of_puzzle():
    """ Find the earliest bus to take to the airport. """
    earliset_timestamp_to_depart, possible_busses = get_bus_schedules()
    bus_id_minimum_waiting_time = get_earliest_possible_bus_departure(earliset_timestamp_to_depart, possible_busses)

    print("[+] Solution of day13/puzzle1: Bus-ID times number of minutes to wait = {}"\
          .format(bus_id_minimum_waiting_time[0] * bus_id_minimum_waiting_time[1]))

if __name__ == "__main__":
    compute_solution_of_puzzle()
