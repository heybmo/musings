# -*- coding: utf-8 -*-
"""All file utility functions.

This module includes the following exported functions:

check_file_exists
touch
rm
mkdir

This module contains several importable functions to deal with files.
We're using typing (Python >= 3.5). 

TODO: Change all print statements to log statements.
"""
import os
from typing import List
from . import strtool


def _resolve_dirpath(dirpath: str, add_to_path: str = "") -> str:
    """
    Clean up dirpaths (relative and absolute).

    Args:
        dirpath (str): The path.
        add_to_path (str): A value to add to the existing path
                           (default: str)
    Returns:
        str: Resolved path in the form of a string.

    Raises:
        ValueError: If an empty string is supplied, a ValueError is
                    raised. If the path is invalid (path is a file) or
                    path is not valid, this exception will also be
                    raised.
    """
    dirpath_is_valid = strtool.expect_nonempty_str(dirpath)

    if not dirpath_is_valid:
        raise ValueError("Argument supplied was in an invalid format.")

    # If the dirpath is relative, convert it to an absolute path.
    if not os.path.isabs(dirpath):
        dirpath = os.path.abspath(dirpath)

    # Check if directory is a valid directory.
    if os.path.isdir(dirpath):
        return os.path.join(dirpath, add_to_path)

    elif os.path.isfile(dirpath):
        raise ValueError("Dirpath was a file, not a directory")

    raise ValueError("Dirpath was not valid.")


def _resolve_dirpaths(dirpaths: List[str], add_to_path: str = "") -> None:
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

    Raises:
        ValueError -- Raised if the supplied argument(s) are invalid.
    """
    dirpaths_is_valid = strtool.expect_nonempty_str(dirpaths)
    atp = True if add_to_path is not None else False

    if not dirpaths_is_valid:
        raise ValueError("Supplied argument was invalid.")
    
    if atp:
        atp = strtool.expect_nonempty_str(add_to_path)
        
    # If the dirpath is already absolute, we don't have
    # to do anything to it.
    for i, path in enumerate(dirpaths):
        dirpaths[i] = os.path.abspath(path)
        if atp:
            dirpaths[i] = os.path.join(dirpaths[i], add_to_path)


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
    fname_valid = strtool.expect_nonempty_str(fname)
    dirpath_valid = strtool.expect_nonempty_str(dirpath)
    args_valid = (fname_valid is True) and (dirpath_valid is True)

    if not args_valid:
        return False

    resolved_dirpath: str = _resolve_dirpath(dirpath, add_to_path=fname)

    # Check if the directory is an abs or rel path.
    if not os.path.isabs(dirpath):
        resolved_dirpath = os.path.abspath(dirpath)
    
    abs_filepath: str = os.path.join(resolved_dirpath, fname)

    # Check if directory exists
    res_dirpath_exists: bool = os.path.isfile(abs_filepath)

    if res_dirpath_exists:
        return True
    
    return False

    
def touch(fname: str, dirpath: str = None, overwrite: bool = False) -> bool:
    """
    Make a file in the provided `dirpath` directory. If dirpath is not
    a directory, an error is raised. If a dirpath is not supplied, a new
    file is created in the same directory as the caller function's
    module location. If overwrite is set to `True`, any file matching the
    fname in the expected dirpath will be automatically overwritten (w).
    If it is false and the file exists, the file will simply be appended
    to (a).

    Args:
        fname (str) -- The file name.
        dirpath (str) -- The directory in which the new file should be
                         created (default: None).
        overwrite (bool) -- Overwrite if the file already exists.
                        
    Raises:
        ValueError -- If `fname` is invalid, an error is raised.
    """
    fname_valid = strtool.expect_nonempty_str(fname)
    mode = "w"
    resolved_dirpath = ""

    if not fname_valid:
        raise ValueError("The file name supplied was invalid.")
    
    # we have a relative path. raise an error.
    # TODO: Create missing directories when a relative path is supplied
    #       as a file name.
    if "/" in fname:
        raise ValueError("Supplied fname cannot have '/' characters.")

    if dirpath is not None:
        try:
            resolved_dirpath = _resolve_dirpath(dirpath)
        except ValueError as ve:
            # Log value error.
            print(ve) 
    else:
        resolved_dirpath = os.getcwd()
    
    resolved_dirpath = os.path.join(resolved_dirpath, fname)
    
    mode = "w" if overwrite else "a"
    with open(resolved_dirpath, mode):
        os.utime(resolved_dirpath, None)
    
    return True

    
def rm(fname: str, dirpath: str = None) -> bool:
    pass


def mkdir(dirname: str, dirpath: str = None) -> bool:
    pass
