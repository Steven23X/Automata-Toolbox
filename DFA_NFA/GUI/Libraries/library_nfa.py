def get_file(file):
    """
    get_file is processing a file and eliminates comments, new line characters and empty lines
    :param file: type file
    :return: it returns a list in which every element is a line of the file
    """
    return [x.strip() for x in file if x[0] != '#' and len(x) > 1]


def get_section(file):
    """
    get_section is processing a file and searches for [section] lines
    :param file: type file
    :return: it returns a list in which every element is a section of the file
    """
    return [x.lower() for x in file if x[0] == "[" and x[len(x)-1] == ']']


def dictionary(sections, file):
    """
    dictionary verifies if the sections are correctly defined and creates a dictionary
    :param sections: type list
    :param file: type file
    :return: it returns a dictionary where the key is the string section and
    the value is a list formed of the lines after the section in the file
    """
    if len(sections) != len(set(sections)):
        d = {}
        print("Similar sections detected!")
        return d
    else:
        print("Sections verified!")
        d = {}
        section = file[0].lower()
        d[section] = []
        for line in file[1:]:
            if line[0] != "[":
                d[section].append(line)
            else:
                d[line.lower()] = []
                section = line.lower()
    return d


def get_sigma(d):
    """
    get_sigma is processing a dictionary and verifies if [sigma] section exists
    :param d: type dictionary
    :return: it returns the alphabet from the dictionary as a set
    """
    if "[sigma]".lower() not in d.keys():
        print("Sigma wrongly defined")
        return set()
    return set(d["[sigma]"]) | set('$')


def get_states(d):
    """
    get_states is processing a dictionary and verifies if [states] section exists
    :param d: type dictionary
    :return: it returns the states from the dictionary as a set
    """
    if "[states]".lower() not in d.keys():
        print("states wrongly defined")
        return set()
    return set(d["[states]"])


def test_sigma(d):
    if "[sigma]".lower() not in d.keys():
        print("Sigma wrongly defined")
        return False
    print("Sigma verified!")
    return True


def test_start_final(d):
    """
    test_start_final verifies the start state and the final states
    :param d: type dictionary
    :return: it returns True if start and final states are correctly defined
    """
    errors = 0
    if len(d["[start]"]) != 1:
        print("Start wrongly defined (more than 1 state)")
        errors += 1
    if d["[final]"] == []:
        print("Final wrongly defined (no final state)")
        errors += 1
    states = set(get_states(d))

    if set(d["[start]"]).issubset(states) == False:
        print("Start is not a subset of states")
        errors += 1
    if set(d["[final]"]).issubset(states) == False:
        print("Final is not a subset of states")
        errors += 1
    if errors:
        return False
    print("Start and Final verified!")
    return True


def get_start(d):
    """
    get_start is processing a dictionary and verifies if [start] section exists
    :param d: type dictionary
    :return: it returns the start state from the dictionary as a set
    """
    if "[start]" not in d.keys():
        print("Start wrongly defined")
        return set()
    return set(d["[start]"])


def get_final(d):
    """
    get_final is processing a dictionary and verifies if [final] section exists
    :param d: type dictionary
    :return: it returns the final state from the dictionary as a set
    """
    if "[final]" not in d.keys():
        print("Final states wrongly defined")
        return set()
    return set(d["[final]"])


def get_delta(d):
    """
    get_delta is processing a dictionary and verifies if [delta] section exists
    :param d: type dictionary
    :return: it returns a list in which every element is a line of the [delta] section
             elem[0]=input state
             elem[1]=letter from [sigma] section
             elem[2]=output state
             elem[0] X elem[1] -> elem[2]
    """
    if "[delta]" not in d.keys():
        print("Delta wrongly defined")
        delta_dict = {}
        return delta_dict
    delta_dict = {}
    rows = list(map(lambda x: x.split(","), d['[delta]']))
    for line in rows:
        state1 = line[0]
        with_sigma_to = line[1]
        state2 = line[2]
        if state1 not in delta_dict:
            delta_dict[state1] = {}
            delta_dict[state1][with_sigma_to] = {state2}
        elif with_sigma_to not in delta_dict[state1]:
            delta_dict[state1][with_sigma_to] = {state2}
        else:
            delta_dict[state1][with_sigma_to].add(state2)
    # add states that do not have symbols attached to them
    for state in get_states(d):
        if state not in delta_dict:
            delta_dict[state] = {}
        for symbol in get_sigma(d)-{'$'}:
            if symbol not in delta_dict[state]:
                delta_dict[state][symbol]={state}

    
    return delta_dict


def test_delta(d):
    """
    test_delta verifies the [delta] section
    :param d: type dictionary
    :return: it returns True if [delta] section is correctly defined
    """
    delta_dict = get_delta(d)
    if len(list(delta_dict.items())) == 0:
        return False
    else:
        errors = 0
        states = set(delta_dict.keys())
        alphabet = set()
        states2 = set()
        for state in list(states):
            keys = set(delta_dict[state].keys())
            values = set()
            for el in list(delta_dict[state].values()):
                values.update(el)
            states2.update(values)
            alphabet.update(keys)
        ALL_STATES = states.union(states2)
        if ALL_STATES.issubset(get_states(d)) == False:
            print("States of Delta wrongly defined")
            errors += 1
        if alphabet.issubset(get_sigma(d)) == False:
            print("Alphabet of Delta wrongly defined")
            errors += 1

        if get_start(d).intersection(states) == set():
            print("Start state missing from delta configuration")
            errors += 1
        if get_final(d).intersection(states2) == set():
            print("Final state(s) missing from delta configuration")
            errors += 1

        if not errors:
            print("Delta verified!")
            return True
        return False
    
def string_validator(string, d):
    delta_dict = get_delta(d)
    current_states = get_start(d)

    # Helper function to compute epsilon closure for a set of states
    def epsilon_closure(states):
        closure = set(states)
        stack = list(states)
        while stack:
            current_state = stack.pop()
            if current_state in delta_dict and '$' in delta_dict[current_state]:
                epsilon_neighbors = delta_dict[current_state]['$']
                for neighbor in epsilon_neighbors:
                    if neighbor not in closure:
                        closure.add(neighbor)
                        stack.append(neighbor)
        return closure

    current_states = epsilon_closure(current_states)
    print(current_states)
    for symbol in string:
        print(symbol)
        new_states = set()
        
        for state in current_states:
            if state in delta_dict and symbol in delta_dict[state]:
                new_states |= delta_dict[state][symbol]
        current_states = epsilon_closure(new_states)

    print(current_states)
    current_states &= get_final(d)

    if bool(current_states):
        print("String accepted!")
        return True
    print("String rejected!")
    return False