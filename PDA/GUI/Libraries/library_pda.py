"""
δ:Q×Σ×Γ→P(Q×Γ)
"""
from collections import deque
import copy


def get_file(content_file):
    """
    get_file is processing a file and eliminates comments, new line characters and empty lines
    :param file: type file
    :return: it returns a list in which every element is a line of the file
    """
    return [x.strip() for x in content_file if x[0] != '#' and len(x) > 1]


def get_section(processed_content_file):
    """
    get_section is processing a file and searches for [section] lines
    :param file: type file
    :return: it returns a list in which every element is a section of the file
    """
    return [x.lower() for x in processed_content_file if x[0] == "[" and x[len(x) - 1] == ']']


def dictionary(sections, processed_content_file):
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
        section = processed_content_file[0].lower()
        d[section] = []
        for line in processed_content_file[1:]:
            if line[0] != "[":
                d[section].append(line)
            else:
                d[line.lower()] = []
                section = line.lower()
    return d


def get_gamma(d):
    """
    get_gamma is processing a dictionary and verifies if [gamma] section exists
    :param d: type dictionary
    :return: it returns the gamma from the dictionary as a set
    """
    if "[gamma]".lower() not in d.keys():
        print("gamma wrongly defined")
        return set()
    return set(d["[gamma]"]) | set('$')


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


def test_gamma(d):
    if "[gamma]".lower() not in d.keys():
        print("Gamma wrongly defined")
        return False
    print("Gamma verified!")
    return True


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
        print("Error: start wrongly defined (more than 1 state)")
        errors += 1
    if d["[final]"] == []:
        print("Error: final wrongly defined (no final state)")
        errors += 1
    states = set(get_states(d))

    if set(d["[start]"]).issubset(states) == False:
        print("Error: start is not a subset of states")
        errors += 1
    if set(d["[final]"]).issubset(states) == False:
        print("Error: final is not a subset of states")
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
             elem[1]=symbol from [sigma] section
             elem[2]=symbol from gamma
             elem[3]=output state x gamma symbol
             elem[0] X elem[1] -> elem[2]
    """
    if "[delta]" not in d.keys():
        print("Error: delta wrongly defined (missing state title)")
        delta_dict = {}
        return delta_dict
    delta_dict = {}

    """
    structure : print("q1,$,$,(q2,$)".split(',')) -> ['q1', '$', '$', '(q2', '$)']
    """
    rows = list(map(lambda x: x.split(","), d['[delta]']))
    for line in rows:
        state1 = line[0]
        with_sigma_and = line[1]
        pop_gamma_to = line[2]
        state2 = line[3][1:]
        push_gamma = line[4][0]
        if state1 not in delta_dict:  # adding the whole row
            delta_dict[state1] = {}
            delta_dict[state1][with_sigma_and] = {}
            delta_dict[state1][with_sigma_and][pop_gamma_to] = {
                (state2, push_gamma)}
        elif with_sigma_and not in delta_dict[state1]:
            # if sigma is not found
            delta_dict[state1][with_sigma_and] = {}
            delta_dict[state1][with_sigma_and][pop_gamma_to] = {
                (state2, push_gamma)}
        elif pop_gamma_to not in delta_dict[state1][with_sigma_and]:
            delta_dict[state1][with_sigma_and][pop_gamma_to] = {
                (state2, push_gamma)}
        else:
            delta_dict[state1][with_sigma_and][pop_gamma_to].add(
                (state2, push_gamma))
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
    # Here we have two variables for states: one to store the key states we will iterate over, and another variable to store the states found after the arrow.
    # If we had only one variable, it would get overwritten each time during iteration.
    states1 = set(delta_dict.keys())  # Set to store the initial states
    sigma_alphabet = set()  # Empty set for the sigma alphabet
    gamma_alphabet = set()  # Empty set for the gamma alphabet
    states2 = set()  # Set for the states after the arrow

    # Iterate over the initial states
    for state in list(states1):
        # Keys are the symbols from the sigma alphabet
        keys_sigma = set(delta_dict[state].keys())
        keys_gamma = set()  # Set to store the pop gamma symbols

        # Iterate over the list of dictionaries
        for dict in list(delta_dict[state].values()):
            # Add the keys from the dictionaries as gamma symbols
            keys_gamma.update(set(dict.keys()))

            value_gamma = set()
            value_states = set()

            # Iterate over the list of tuples
            for value_tuple in list(dict.values()):
                s = set()
                s.add(list(value_tuple)[0][1])
                value_gamma.update(s)  # Add the gamma symbol to the set

                s = set()
                s.add(list(value_tuple)[0][0])
                value_states.update(s)  # Add the state to the set

            keys_gamma.update(value_gamma)
            states2.update(value_states)

        sigma_alphabet.update(keys_sigma)
        gamma_alphabet.update(keys_gamma)

    ALL_STATES = states1.union(states2)
    if ALL_STATES.issubset(get_states(d)) == False:
        print("States of Delta wrongly defined")
        errors += 1
    if sigma_alphabet.issubset(get_sigma(d)) == False:
        print("Alphabet Sigma of Delta wrongly defined")
        errors += 1
    if gamma_alphabet.issubset(get_gamma(d)) == False:
        print("Alphabet Gamma of Delta wrongly defined")
        errors += 1
    if get_start(d).intersection(states1) == set():
        print("Start state missing from delta configuration")
        errors += 1
    if get_final(d).intersection(states2) == set():
        print("Final state(s) missing from delta configuration")
        errors += 1
    if not errors:
        print("Delta verified!")
        return True
    return False


def string_validator(input_string,d):
    alphabet = get_sigma(d)-{'$'}
    if set(input_string) - alphabet != set():
        print("Invalid string")
        return False
    gamma_symbols = get_gamma(d)-{'$'}
    states = get_states(d)
    delta_dict = get_delta(d)
    current_states = {list(get_start(d))[0]}
    final_states = get_final(d)

    def calculate_closure(stack_dict):
        stack_dict_items_list = list(stack_dict.items())

        MAX_ITERATIONS = 12
        CURRENT_ITERATIONS = 0
        for state, stack_list in stack_dict_items_list:
            if CURRENT_ITERATIONS == MAX_ITERATIONS + 1:
                break
            CURRENT_ITERATIONS += 1
            if state in delta_dict:
                if '$' in delta_dict[state] and '$' in delta_dict[state]['$']:
                    next_states = list(delta_dict[state]['$']['$'])
                    for next_state, push_gamma in next_states:
                        if push_gamma == '$' and next_state not in stack_dict:
                            stack_dict[next_state] = copy.deepcopy(stack_list)
                            stack_dict_items_list.append(
                                (next_state, copy.deepcopy(stack_list)))
                        elif next_state not in stack_dict:
                            stack_dict[next_state] = copy.deepcopy(stack_list)
                            for inner_stack in stack_dict[next_state]:
                                inner_stack.append(push_gamma)
                            stack_dict_items_list.append(
                                (next_state, copy.deepcopy(stack_dict[next_state])))
                        else:
                            for inner_stack in stack_dict[next_state]:
                                inner_stack.append(push_gamma)
                            stack_dict_items_list.append(
                                (next_state, copy.deepcopy(stack_list)))
                elif '$' in delta_dict[state]:
                    for gamma_pop in delta_dict[state]['$'].keys():
                        for inner_stack in stack_list:
                            if len(inner_stack) and inner_stack[-1] == gamma_pop:
                                next_states = list(
                                    delta_dict[state]['$'][gamma_pop])
                                for next_state, push_gamma in next_states:
                                    if push_gamma == '$':
                                        if next_state not in stack_dict:
                                            stack_dict[next_state] = [
                                                inner_stack.copy()]
                                            stack_dict[next_state][0].pop()
                                            stack_dict_items_list.append((next_state, copy.deepcopy(
                                                stack_dict[next_state])))
                                        else:
                                            new_stack = inner_stack.copy()
                                            new_stack.pop()
                                            stack_dict[next_state].append(
                                                new_stack.copy())
                                            stack_dict_items_list.append(
                                                (next_state, copy.deepcopy(stack_dict[next_state])))
                                    else:
                                        if next_state not in stack_dict:
                                            stack_dict[next_state] = [
                                                inner_stack.copy()]
                                            stack_dict[next_state][0].pop()
                                            stack_dict[next_state][0].append(
                                                push_gamma)
                                            stack_dict_items_list.append((next_state, copy.deepcopy(
                                                stack_dict[next_state])))
                                        else:
                                            new_stack = inner_stack.copy()
                                            new_stack.pop()
                                            new_stack.append(push_gamma)
                                            stack_dict[next_state].append(
                                                new_stack.copy())
                                            stack_dict_items_list.append(
                                                (next_state, copy.deepcopy(stack_dict[next_state])))
        return stack_dict

    current_stack_dict = {list(get_start(d))[0]: [deque()]}
    current_stack_dict = calculate_closure(current_stack_dict)
    for symbol in input_string:
        new_stack_dict = {}

        for state, stack_list in current_stack_dict.items():
            # push/pop analysis
            if state in delta_dict and symbol in delta_dict[state]:
                for gamma_pop in delta_dict[state][symbol].keys():
                    if gamma_pop == '$':
                        for next_state, gamma_push in list(delta_dict[state][symbol][gamma_pop]):
                            if next_state not in new_stack_dict:
                                new_stack_dict[next_state] = copy.deepcopy(
                                    stack_list)
                                if gamma_push != '$':
                                    for inner_stack in new_stack_dict[next_state]:
                                        inner_stack.append(gamma_push)
                            else:
                                if gamma_push != '$':
                                    for inner_stack in new_stack_dict[next_state]:
                                        inner_stack.append(gamma_push)
                    else:
                        for inner_stack in stack_list:
                            if len(inner_stack) and inner_stack[-1] == gamma_pop:
                                for next_state, gamma_push in list(delta_dict[state][symbol][gamma_pop]):
                                    if next_state not in new_stack_dict:
                                        new_stack_dict[next_state] = []
                                    new_stack = inner_stack.copy()
                                    new_stack.pop()
                                    if gamma_push != '$':
                                        new_stack.append(gamma_push)
                                    new_stack_dict[next_state].append(
                                        new_stack.copy())
        current_stack_dict = calculate_closure(new_stack_dict)
    current_states = set(current_stack_dict.keys()) & final_states
    if bool(current_states):
        print("String accepted")
        return True
    print("String rejected!")
    return False
