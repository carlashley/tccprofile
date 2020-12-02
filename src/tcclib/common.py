"""Common."""

import subprocess

from collections import namedtuple
from distutils.version import StrictVersion
from sys import exit, stderr


def errmsg(msg, returncode=1):
    """Print an error message and exit."""
    print(msg, file=stderr)
    exit(returncode)


def sw_ver():
    """Return the output of 'sw_ver' as a named tuple."""
    result = None

    Version = namedtuple('Version', ['product_name',
                                     'product_version',
                                     'product_build'])

    _cmd = ['/usr/bin/sw_vers']
    _p = subprocess.run(_cmd, check=True, capture_output=True)

    if _p.returncode == 0:
        _result = _p.stdout.decode('utf-8').strip() if isinstance(_p.stdout, bytes) else _p.stdout.strip()
        _vers = dict()

        for _l in _result.splitlines():
            _l = _l.strip().split(':')
            _k = ''.join(' ' + _char if _char.isupper() else _char.strip() for _char in _l[0]).strip().replace(' ', '_').lower()
            _v = ''.join(_l[1:]).strip()

            _vers[_k] = _v

        result = Version(product_name=_vers.get('product_name', None),
                         product_version=StrictVersion(_vers.get('product_version', None)),
                         product_build=_vers.get('product_build', None))

    return result
