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
    return set(d["[sigma]"])


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
        delta_matrix = []
        return delta_matrix
    delta_matrix = [x.split(",") for x in d["[delta]"]]
    return delta_matrix


def test_delta(d):
    """
    test_delta verifies the [delta] section
    :param d: type dictionary
    :return: it returns True if [delta] section is correctly defined
    """
    mat = get_delta(d)
    rows = len(mat)
    if rows:
        errors = 0
        columns = len(mat[0])
        mat_transposed = [[mat[i][j]
                           for i in range(0, rows)] for j in range(0, columns)]
        states = mat_transposed[0]
        states.extend(mat_transposed[2])
        states = set(states)
        alphabet = set(mat_transposed[1])
        if states.issubset(get_states(d)) == False:
            print("States of Delta wrongly defined")
            errors += 1
        if alphabet.issubset(get_sigma(d)) == False:
            print("Alphabet of Delta wrongly defined")
            errors += 1

        if get_start(d).intersection(set(mat_transposed[0])) == set():
            print("Start state missing from delta configuration")
            errors += 1
        if get_final(d).intersection(set(mat_transposed[2])) == set():
            print("Final state(s) missing from delta configuration")
            errors += 1

        if not errors:
            print("Delta verified!")
            return True
        return False
    return False
