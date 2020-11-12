"""Version."""

from pathlib import PurePath
from sys import argv, version_info

from .common import errmsg

NAME = PurePath(argv[0]).name
VER = '1.0.1.202011130750'
VERSION_STR = '{} version {} - Apache License Version 2.0'.format(NAME, VER)


def compatibility_check():
    """Version compatibility check."""
    vers = '{}.{}.{}'.format(version_info.major, version_info.minor, version_info.micro)
    needs = '3.7.9'

    if not (version_info.major, version_info.minor, version_info.micro) >= (3, 4, 0):
        errmsg('{} is not supported on Python {}. Please update to Python {}'.format(NAME, vers, needs))
