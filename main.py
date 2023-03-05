from library import *
with open("fisier.txt", "r") as f:
    content = f.readlines()  # content of the file
    # preworked content, without comment lines, newline character, and empty lines
    file = get_file(content)
    # Sections are lines that start with "[" and end with "]"
    sections = get_section(file)
    if len(sections) != len(set(sections)):
        # sections are unique, so there are not 2 equal sections
        print("Equal Sections")
    else:
        print("Sections verified!")
        d = {}  # dictionary where the key is the string section and the value is a list formed of the lines after the section in the file
        section = file[0].lower()
        d[section] = []
        for line in file[1:]:
            if line[0] != "[":
                d[section].append(line)
            else:
                d[line.lower()] = []
                section = line.lower()
        # Here ends the process of building the dictionary
        test_start_final(d)  # verify the start and final states
        test_delta(d)  # verify the delta function
