"""App Scan."""

import subprocess

from os import walk
from pathlib import Path, PurePath

from . import plist
from .codesign import requirements
from .tccobj import TCCApplication


def _walk_path(path):
    """Walk path."""
    result = set()

    for _dir, _, _ in walk(path):
        if PurePath(_dir).suffix == '.app':
            # Partition on '.app' because only want top '.app' info
            _app = ''.join(_dir.partition('.app')[:2])
            result.add(_app)

    return result


def _applications():
    """System, standard, user applications."""
    result = set()

    _apple_apps = _walk_path('/System/Applications')
    _local_apps = _walk_path('/Applications')
    _usr_apps = _walk_path(str(Path().home()))

    _app_dirs = _apple_apps.union(_local_apps).union(_usr_apps)

    for _a in _app_dirs:
        _app = {'path': _a}
        _codesig = requirements(_a)
        _app.update(_codesig)  # Updates with results from 'requirements()' dict

        _bn = PurePath(_a).name
        _app['name'] = str(_bn.replace(str(PurePath(_bn).suffix), ''))

        if _app.get('is_signed', False):
            _obj = TCCApplication(**_app)
            result.add(_obj)

    return result


def _binaries():
    """System binaries"""
    result = set()
    _binaries = set()
    _paths = ['/usr/local/bin',
              '/usr/bin',
              '/bin',
              '/usr/sbin',
              '/sbin',
              '/usr/libexec/',
              '/Library/Apple/usr/bin']

    for _p in _paths:
        _bins = [Path(_b) for _b in Path(_p).glob('*')]

        for _b in _bins:
            if not _b.is_symlink() and _b.is_file():
                _binaries.add(_b)

    for _b in _binaries:
        _app = {'path': _b}
        _codesig = requirements(_b)
        _app.update(_codesig)  # Updates with results from 'requirements()' dict
        _app['name'] = str(_b)

        if _app.get('is_signed', False):
            _obj = TCCApplication(**_app)
            result.add(_obj)

    return result


def _system_profiler_apps():
    """System Profiler Applications List."""
    result = set()

    _cmd = ['/usr/sbin/system_profiler', 'SPApplicationsDataType', '-xml']

    _p = subprocess.Popen(_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _r, _e = _p.communicate()

    if _p.returncode == 0 and _r:
        _items = plist.readPlistFromString(_r)[0].get('_items')

        for _i in _items:
            _path = _i.get('path', None)

            if _path and Path(_path).exists():
                _codesig = requirements(_path)

                _app = _i.copy()
                _app['name'] = _app['_name']
                del _app['_name']

                _app.update(_codesig)  # Updates with results from 'requirements()' dict

                if _app.get('is_signed', False):
                    _obj = TCCApplication(**_app)
                    result.add(_obj)

    return result


def installed():
    """Installed applications."""
    result = set()

    _profiler_apps = _system_profiler_apps()
    _local_apps = _applications()
    _bins = _binaries()

    result = _profiler_apps.union(_local_apps.union(_bins))

    return result
