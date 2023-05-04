import Libraries.library_nfa as lib
import os
with open(os.path.abspath('Files/input.txt'), "r") as f:
    content = f.readlines()
    file = lib.get_file(content)
    sections = lib.get_section(file)
    d = lib.dictionary(sections, file)
    if len(d):
        t1 = lib.test_sigma(d)
        t2 = lib.test_start_final(d)
        t3 = lib.test_delta(d)
print("___________________________________________")
print()
if t1 and t2 and t3:
    print("NFA is Valid!")
    print()
    print("___________________________________________")
    print("Status:")
    print()
    with open(os.path.abspath('Files/string.txt'), "r") as f:
        input_string = f.readline().strip()
        lib.string_validator(input_string, d)
else:
    print("NFA is NOT Valid!")
print()
print("___________________________________________")