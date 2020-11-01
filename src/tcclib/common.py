"""Common."""

from sys import exit, stderr


def errmsg(msg, returncode=1):
    """Print an error message and exit."""
    print(msg, file=stderr)
    exit(returncode)
