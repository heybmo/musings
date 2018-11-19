# -*- coding: utf-8 -*-
"""All utility functions related to files.

This module contains several importable functions to deal with files.
We're using typing (Python >= 3.5). 
"""
import os
from typing import List


def _resolve_dirpath(dirpath: str, add_to_path=None) -> str:
    """
    Clean up dirpaths (relative and absolute).

    Args:
        dirpath (str): The path.
        add_to_path (str): A value to add to the existing path
                           (default: None)
    
    Returns:
        str: Resolved path in the form of a string.
    
    Raises:
        ValueError: If an empty string is supplied, a ValueError is
                    raised.
    """
    if not isinstance(dirpath, str) or dirpath == "":
        raise ValueError("Supplied argument was an empty string")
    
    # If the dirpath is already absolute, we don't have to do anything
    # to it.
    if os.path.isabs(dirpath):
        if add_to_path is not None:
            return os.path.join(dirpath, add_to_path)
    
    return os.path.abspath(dirpath)


def _resolve_dirpaths(
    dirpaths: List[str], add_to_path: str=None) -> None:
    """
    Same functionality as _resolve_dirpaths but accepts a list of
    paths and attempts to resolve them independently of each other.
    However, if an additional argument, add_to_path, is supplied,
    then we attempt to add the `add_to_path` value to each existing 
    dirpath.
    
    Args:
        dirpaths (List[str]): A list of dirpaths to resolve.
        add_to_path (str): A value to add to each existing dirpath
                           (default: None)
    
    Returns:
        None. The same list of strings (not a new list) will be used to
        generate the resolved list.
    """
    pass

def check_file_exists(fname: str, dirpath: str) -> bool:
    """
    Check if a file exists in a given directory. If it doesn't and there
    are folders within the dirpath, return False. This function does not
    recursively traverse subdirectories.
    
    The file name must include its extension. The dirpath may be 
    relative to the caller function's location, but it is preferable to
    use an absolute path with the dunder, '__file__'.

    Args:
        fname -- The file's name.
        dirpath -- The path to a directory. The path may be relative to
                   the caller of this function.
    
    Returns:
        bool: The return value. True if the file exists, False
              otherwise.
    """
    # If either arg is not a string...
    fname_not_str = not isinstance(fname, str)
    dirpath_not_str = not isinstance(dirpath, str)
    args_not_str = fname_not_str and dirpath_not_str

    # or either arg is empty...
    args_empty = fname == "" or dirpath == ""

    # return false
    if args_not_str or args_empty:
        return False

    resolved_dirpath: str = dirpath

    # Check if the directory is an abs or rel path.
    if not os.path.isabs(dirpath):
        resolved_dirpath = os.path.abspath(dirpath)
    
    abs_filepath: str = os.path.join(resolved_dirpath, fname)

    # Check if directory exists
    res_dirpath_exists: bool = os.path.isfile(abs_filepath)

    if res_dirpath_exists:

        return True
    
    return False

    
def mkfile(fname: str, dirpath: str=None) -> bool:
    """
    Make a file in the provided `dirpath` directory. If dirpath is not
    a directory
    """
    pass

def mkdir(dirname: str) -> bool:
    pass
