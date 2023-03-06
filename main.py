from library import *
with open("fisier.txt", "r") as f:
    content = f.readlines()
    file = get_file(content)
    sections = get_section(file)
    d=dictionary(sections,file)
    test_start_final(d) 
    test_delta(d)
#linie 
