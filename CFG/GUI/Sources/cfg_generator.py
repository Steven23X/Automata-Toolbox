import Libraries.library_cfg as lib
import os

import sys
sys.setrecursionlimit(5000)

with open(os.path.abspath('Files/input.txt'),"r") as f:
    content=f.readlines()
    file=lib.get_file(content)
    sections=lib.get_section(file)
    d=lib.dictionary(sections,file)
    
    with open(os.path.abspath('Files/string.txt'),"r") as g:
        nr_strings = int(g.readline())

    for i in range(nr_strings) :
        print(f"{i+1} -- {lib.generate_string(d,lib.get_start(d))}")
    
    