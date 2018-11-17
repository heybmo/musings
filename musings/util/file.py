# -*- coding: utf-8 -*-
"""All utility functions related to files.

This module contains several importable functions to deal with files.
We're using typing (Python >= 3.5). 
"""
import os
import tempfile
from typing import List

# See:
# https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
def is_pathname_valid(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    '''
    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
        # if any. Since Windows prohibits path components from containing `:`
        # characters, failing to strip this `:`-suffixed prefix would
        # erroneously invalidate all valid absolute Windows pathnames.
        _, pathname = os.path.splitdrive(pathname)

        # Directory guaranteed to exist. If the current OS is Windows, this is
        # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
        # environment variable); else, the typical root directory.
        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law

        # Append a path separator to this directory if needed.
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        # Test whether each path component split from this pathname is valid or
        # not, ignoring non-existent and non-readable path components.
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            # If an OS-specific exception is raised, its error code
            # indicates whether this pathname is valid or not. Unless this
            # is the case, this exception implies an ignorable kernel or
            # filesystem complaint (e.g., path not found or inaccessible).
            #
            # Only the following exceptions indicate invalid pathnames:
            #
            # * Instances of the Windows-specific "WindowsError" class
            #   defining the "winerror" attribute whose value is
            #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
            #   fine-grained and hence useful than the generic "errno"
            #   attribute. When a too-long pathname is passed, for example,
            #   "errno" is "ENOENT" (i.e., no such file or directory) rather
            #   than "ENAMETOOLONG" (i.e., file name too long).
            # * Instances of the cross-platform "OSError" class defining the
            #   generic "errno" attribute whose value is either:
            #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
            #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    # If a "TypeError" exception was raised, it almost certainly has the
    # error message "embedded NUL character" indicating an invalid pathname.
    except TypeError as exc:
        return False
    # If no exception was raised, all path components and hence this
    # pathname itself are valid. (Praise be to the curmudgeonly python.)
    else:
        return True
    # If any other exception was raised, this is an unrelated fatal issue
    # (e.g., a bug). Permit this exception to unwind the call stack.
    #
    # Did we mention this should be shipped with Python already?

def _is_path_sibling_creatable(pathname: str) -> bool:
    """
    `True` if the current user has sufficient permissions to create 
    **siblings** (i.e., arbitrary files in the parent directory) of the 
    passed pathname; `False` otherwise.
    """
    # Parent directory of the passed path. 
    # If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    # Check if we can actually create a temporary file.
    try:
        # For safety, explicitly close and hence delete this temporary 
        # file immediately after creating it in the passed path's parent 
        # directory.
        with tempfile.TemporaryFile(dir=dirname):
            pass
        return True
    # While the exact type of exception raised by the above function 
    # depends on the current version of the Python interpreter, all such
    # types subclass the following exception superclass.
    except EnvironmentError:
        return False


def _is_path_exists(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname on the current OS _and_
    either currently exists or is hypothetically creatable in a cross-platform
    manner optimized for POSIX-unfriendly filesystems; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    '''
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        return _is_pathname_valid(pathname) and (
            os.path.exists(pathname) or _is_path_sibling_creatable(pathname))
    # Report failure on non-fatal filesystem complaints (e.g., connection
    # timeouts, permissions issues) implying this path to be inaccessible. All
    # other exceptions are unrelated fatal issues and should not be caught here.
    except OSError:
        return False

def _resolve_dirpath(dirpath: str) -> str:
    """
    Clean up dirpaths (relative and absolute).

    Args:
        dirpath (str): The path.
    
    Returns:
        str: Resolved path in the form of a string.
    
    Raises:
        ValueError: If an empty string is supplied, a ValueError is
                    raised.
    """
    if dirpath == "":
        raise ValueError("Supplied argument was an empty string")
    
    # If the dirpath is already absolute, we don't have to do anything
    # to it.
    if os.path.isabs(dirpath):
        return dirpath
    
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
    # If either arg is empty, return false.
    if fname == "" or dirpath == "":
        return False

    resolved_dirpath: str = dirpath

    # Check if the directory is an abs or rel path.
    if not os.path.isabs(dirpath):
        resolved_dirpath = os.path.abspath(dirpath)
    
    abs_filepath: str = os.path.join(resolved_dirpath, fname)
    res_dirpath_exists: bool = os.path.isfile(abs_filepath)

    if res_dirpath_exists:
        return True
    
    return False

    
def mkfile(fname: str, dirpath: str=None) -> bool:
    """
    Make a file.
    """
    pass

def mkdir(dirname: str) -> bool:
    pass
