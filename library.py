def get_file(file):
    # contents of the file without comments and newline character and empty lines
    return [x.strip() for x in file if x[0] != '#' and len(x) > 1]


def get_section(file):
    # sections of the file, also case sensitive
    return [x.lower() for x in file if x[0] == "[" and x[len(x)-1] == ']']


def get_sigma(d):  # verifies sigma which is the alphabet of the automaton
    if "[sigma]".lower() not in d.keys():
        print("Sigma wrongly defined")
        return False
    # returns the alphabet from the dictionary as a set
    return set(d["[sigma]"])


def get_states(d):  # verifies the states of the automaton
    if "[states]".lower() not in d.keys():
        print("states wrongly defined")
        return False
    return set(d["[states]"])  # returns the states from a dictionary as a set


def test_start_final(d):  # function which verifies the start state and the final states
    if len(d["[start]"]) != 1:  # there is only ONE start state
        print("Start wrongly defined (more than 1 state)")
        return False
    if d["[final]"] == []:
        print("Final wrongly defined (no final state)")
        return False
    states = set(get_states(d))

    if set(d["[start]"]).issubset(states) == False:  # tests if the start state is a valid one
        print("Start is not a subset of states")
        return False
    if set(d["[final]"]).issubset(states) == False:  # tests if the final state is a valid one
        print("Final is not a subset of states")
        return False
    print("Start and Final verified!")
    return True


def get_start(d):  # function which tests the start
    if "[start]" not in d.keys():
        print("Start wrongly defined")
        return False
    return set(d["[start]"])  # returns the start state from the dictionary


def get_final(d):  # function which tests the final states
    if "[final]" not in d.keys():
        print("Final states wrongly defined")
        return False
    return set(d["[final]"])  # returns the final states from the dictionary


def get_delta(d):  # function which tests the automaton function delta
    if "[delta]" not in d.keys():
        print("Delta definit Gresit")
        return False
    # returns a nx3 matrix where a line is a delta input and output
    mat = [x.split(",") for x in d["[delta]"]]
    # first and second colums are the inputs
    # the third column is the output
    return mat  # also, returns the specified matrix


def test_delta(d):
    mat = get_delta(d)  # matrix of delta
    n = len(mat)  # lines
    m = len(mat[0])  # columns
    # as it says, we transpose this matrix
    mat_transposed = [[mat[i][j] for i in range(0, n)] for j in range(0, m)]
    """
    why transpose the matrix?
    so that we can get easily the list of inputs/outputs that are (or should be) included in the states and sigma set as it follows:
    Line 1<= States set
    Line 2<= Sigma set
    Line 3<= States set
    because:
    delta : States x Sigma --> States
    """
    states = mat_transposed[0]
    # put into one list line 1 and 3, because they are states
    states.extend(mat_transposed[2])
    states = set(states)
    alphabet = set(mat_transposed[1])  # get the alphabet (sigma)
    if states.issubset(get_states(d)) == False:
        print("States of Delta wrongly defined")
        return False
    if alphabet.issubset(get_sigma(d)) == False:
        print("Alphabet of Delta wrongly defined")
        return False
    # if the states and alphabet are valid, the functions makes it clear and returns  true, otherwise false
    print("Delta Ready")
    return True
