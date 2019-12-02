'''
Takes a text file and returns it, either as a string or string list
'''
from pathlib import Path

def dump(file):
    folder = Path("inputs/")
    file = folder / file
    d = open(file, "r")
    return d.read()

def dump_list_newline(file):
    return dump(file).split()

def dump_list_spaces(file):
    return dump_list_newline(file)

#Note that this won't clear escape characters. However, if parsed to int Python will remove them
def dump_list_comma(file):
    return dump(file).split(",")
