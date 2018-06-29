import os
from os import listdir
from os.path import isfile, join
def go():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cwd = os.getcwd()

    print(dir_path)
    print(cwd)