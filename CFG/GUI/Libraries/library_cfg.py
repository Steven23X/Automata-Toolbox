import random
import string

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
    return [x.lower() for x in file if x[0] == '[' and x[len(x)-1] == ']']

def dictionary(sections, file):
    """
    dictionary verifies if the sections are correctly defined and creates a dictionary
    :param sections: type list
    :param file: type file
    :return: it returns a dictionary where the key is the string section and
    the value is a list formed of the lines after the section in the file
    """
    if len(sections) != len(set(sections)):
        d={}
        print("Equal Sections")
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

def get_rules(d):
    """
    get_rules is processing a dictionary and verifies if [rules] section exists
    :param d: type dictionary
    :return: it returns the alphabet from the dictionary as a set
    """
    if "[rules]".lower() not in d.keys():
        print("Rules wrongly defined")
        return set()
    return set(d["[rules]"])

def get_variables(d):
    """
    get_variables is processing a dictionary and verifies if [variables] section exists
    :param d: type dictionary
    :return: it returns the alphabet from the dictionary as a set
    """
    if "[variables]".lower() not in d.keys():
        print("Variables wrongly defined")
        return set() #am modificat ce returneza
    return set(d["[variables]"])

def get_start(d):
    """
    get_start is processing a dictionary and verifies if [start] section exists
    :param d: type dictionary
    :return: it returns the alphabet from the dictionary as a set
    """
    if "[start]".lower() not in d.keys():
        print("start wrongly defined")
        return set() #am modificat ce returneza
    return d["[start]"][0]


def get_terminals(d):
    """
    get_terminals is processing a dictionary and verifies if [terminals] section exists
    :param d: type dictionary
    :return: it returns the alphabet from the dictionary as a set
    """
    if "[terminals]".lower() not in d.keys():
        print("Terminals wrongly defined")
        return set() #am modificat ce returneza
    return set(d["[terminals]"])

def get_rules_dict(d):
    """
    obtine dictionarul de reguli
    """
    rules_dict={} # incepem cu dictionarul gol
    for rule in get_rules(d): # parcurgem regulile
        rule=rule.split("->") # separam variabila de regula sa
        if(rule[0]) not in rules_dict: # daca variabila nu exista in dictionar
            rules_dict[rule[0]]=[]     #o adaugam si o sa aiba o lista ca valuare
            rules_dict[rule[0]].append(rule[1]) # adaugam la lista regula respectiva
        else:
            rules_dict[rule[0]].append(rule[1]) # daca e deja doar adaugam regula
    return rules_dict 
    
def generate_string(d,string): # ia ca parametrii dictionarul cu sectiunile si un string care ar trebui sa aiba by default variabila de start
    rules_dict=get_rules_dict(d) #aici formam dictionarul de reguli
    new_string="" #stringul care se genereaza incepe gol
    num_var=0 #contor de variabile pentru a determina daca stringul a fost procesat cu succes
    for variable in string.split(','): #facem split dupa , pentru a desparti variabilele de caracterele din sigma
        if variable in rules_dict: #daca "variable" este variabila
            num_var+=1 # o numaram
            rule_index=random.randint(0,len(rules_dict[variable])-1) # generam un index random din posibilele sale reguli
            new_string+=',' # despartim prin virgula noua regula adaugata , nu face pagube
            new_string+=rules_dict[variable][rule_index] # adaugam regula respectiva
            new_string+=',' # despartim prin virgula noua regula adaugata , nu face pagube
        else:
            new_string+=variable #altfel daca nu e variabila, adaugam direct la string
    if num_var: # daca am gasit variabile 
        return generate_string(d,new_string) #mai procesam o data stringul
    else:
        return new_string.replace('$',"") # daca nu s-au mai gasit returnam stringul fara aparitiile lui '$' care e epsilon

