'''
Takes a text file and returns it, either as a string or string list
'''
from pathlib import Path

def dump(file):
    folder = Path("inputs/")
    file = folder / file
    d = open(file, "r")
    return d.read()

def dump_list(file):
    return dump(file).split()
