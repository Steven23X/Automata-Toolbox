import library as lib
with open("input.txt", "r") as f:
    content = f.readlines()
    file = lib.get_file(content)
    sections = lib.get_section(file)
    d = lib.dictionary(sections, file)
    if len(d):
        lib.test_sigma(d)
        lib.test_start_final(d)
        lib.test_delta(d)
