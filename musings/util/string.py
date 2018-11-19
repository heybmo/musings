# -*- coding: utf-8 -*-

"""
Utility functions for strings.
"""

def expect_nonempty_str(s: str) -> bool:
    """
    Expect a passed in value to be a non-empty string.
    """
    if s is None:
        return False
    
    arg_is_str = isinstance(s, str)

    if not arg_is_str:
        return False
    
    if not len(s):
        return False
    
    return True

    