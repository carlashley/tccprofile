"""Wrapper for plistlib."""

import plistlib

from .common import errmsg


class PlistErr(Exception):
    pass


def readPlist(f):
    """Read Property List"""
    result = None

    with open(f, 'rb') as _f:
        result = plistlib.load(_f)

    return result


def readPlistFromString(s):
    """Read Property List from string."""
    result = None

    result = plistlib.loads(s)

    return result


def writePlist(values, f=None, fmt='xml', stdout=False):
    """Write Property List. Defaults to binary property list file output."""
    _fmt = {'bin': plistlib.FMT_BINARY,
            'xml': plistlib.FMT_XML}

    if fmt and fmt not in ['bin', 'xml']:
        raise PlistErr('Format is either \'bin\' (binary) or \'xml\' type.')

    if not stdout:
        if not f:
            errmsg('\writePlist()\' requires a file path to write to.')

        with open(f, 'wb') as _f:
            plistlib.dump(values, _f, fmt=_fmt[fmt])
    elif stdout:
        _plist = plistlib.dumps(values, fmt=_fmt[fmt])

        if isinstance(_plist, bytes):
            _plist = _plist.decode('utf-8')

        _plist = _plist.strip('\n')

        print(_plist)
