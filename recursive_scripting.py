"""
Python recursive scripting

Write and run a simple python script.
Write a python script that receives a regular expression and a path,
and prints out all the files whose content matches the regular expression provided.

@author carlosacg [2022-05-17]
"""

import argparse
import os
from time import perf_counter
from typing import Optional
from fnutils import is_match


def get_files(regex: str, path: str) -> float:
    t1_start = perf_counter()
    content = os.listdir(path)
    list_of_files = recursive_is_match(regex, path, content)
    print("Files whose content matches the regular expression provided", list_of_files)
    t1_stop = perf_counter()
    return t1_stop - t1_start


def recursive_is_match(regex: str, path: str, files_list: Optional[list]) -> list:
    """
    This function show the head's file name if its content matches with a specific regular expression.
    And calls itself with the tail of the list until the list is empty.
    """
    if not files_list:
        return []
    else:
        if is_match(regex, path, files_list[0]):
            return [files_list[0]] + recursive_is_match(regex, path, files_list[1:])
        else:
            return recursive_is_match(regex, path, files_list[1:])


parser = argparse.ArgumentParser()
parser.add_argument("regex", type=str,
                    help="regular expresion to search files in the path")
parser.add_argument("path", type=str, help="path that contains files in it")
args = parser.parse_args()

elapsed_time = get_files(args.regex, args.path)
print("Elapsed time was: ", elapsed_time)
