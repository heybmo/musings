# -*- coding: utf-8 -*-

"""
Utility functions for strings.
"""

def expect_nonempty_str(s: str) -> bool:
    """
    Expect a string, `s`, to be a non-empty string.
    """
    arg_is_not_str = not isinstance(s, str)

    if s is None or arg_is_not_str or len(s) == 0:
        return False
    
    return True

    
