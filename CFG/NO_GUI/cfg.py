import library_cfg as lib

import sys
sys.setrecursionlimit(5000)

with open("input.txt") as f:
    content=f.readlines()
    file=lib.get_file(content)
    sections=lib.get_section(file)
    d=lib.dictionary(sections,file)
    
    nr_strings = int(input("Number of strings to generate: "))
    for i in range(nr_strings) :
        print(f"{i+1} -- {lib.generate_string(d,lib.get_start(d))}")
    
    