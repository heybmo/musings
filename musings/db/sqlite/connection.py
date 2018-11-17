"""
Connection to SQLite Class.
"""
import sqlite3


class Connection(object):

    def __init__(self, config=None) -> None:
        """
        Constructor method for a SQLite connection. An optional config
        file in the INI format may be passed in to set up the connection
        instead of using default values.

        config -- An INI config file (default: None)
        """
        