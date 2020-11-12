"""Codesign."""

import re
import subprocess

from os import remove
from pathlib import Path, PurePath
from tempfile import gettempdir


def _xxd(blob):
    """XXD"""
    result = None

    # Note, this requires input passed in via 'stdin', so include 'stdin' for piping input.
    _cmd = ['/usr/local/bin/xxd', '-r', '-p']
    _p = subprocess.Popen(_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _p.stdin.write(blob)
    _r, _e = _p.communicate()

    if _p.returncode == 0 and _r:
        result = _r
    elif _p.returncode != 0 and _e:
        result = _e

    return result


def csreq(blob):
    """csreq"""
    result = None

    # Note, this requires input passed in via 'stdin', so include 'stdin' for piping input.
    _cmd = ['/usr/bin/csreq', '-vvv', '-r', '-', '-t']
    _p = subprocess.Popen(_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _p.stdin.write(_xxd(blob))
    _r, _e = _p.communicate()

    if _r and isinstance(_r, bytes):
        _r = _r.decode('utf-8').strip()

    if _e and isinstance(_e, bytes):
        _e = _e.decode('utf-8').strip()

    if _p.returncode == 0 and _r:
        result = _r
    elif _p.returncode != 0 and _e:
        result = _e

    return result


def detached_signature(path):
    """Codesign using a detached signature."""
    result = None

    _tmp = gettempdir()
    _path_sig = '{}.sig'.format(PurePath(path).name)
    _sig_file = Path(_tmp) / _path_sig

    _cmd = ['/usr/bin/codesign', '--detached', str(_sig_file), '-s', '-', path]
    _p = subprocess.Popen(_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _r, _e = _p.communicate()

    if _r and isinstance(_r, bytes):
        _r = _r.decode('utf-8')

    if _e and isinstance(_e, bytes):
        _e = _e.decode('utf-8')

    if _p.returncode == 0:
        result = requirements(path, detached_sig=_sig_file)

        if result:
            remove(str(_sig_file))

    return result


def requirements(path, detached_sig=None, apple_event=False):
    """Codesign."""
    result = dict()

    # Change the dict keys if this is an AppleEvent style requirement
    if apple_event:
        _id_key = 'apple_events_identifier'
        _id_type_key = 'apple_events_identifier_type'
        _csreq_key = 'apple_events_csreq'
    else:
        _id_key = 'identifier'
        _id_type_key = 'identifier_type'
        _csreq_key = 'csreq'

    # Lines with useful output start with these strings
    _dsgn_prefix = 'designated => '
    _idnt_prefix = 'Identifier='

    # Bundle ID regex test string
    _bnid_regex = re.compile(r'^\w+\.')

    if not detached_sig:
        _cmd = ['/usr/bin/codesign', '-v', '-dr', '-', path]
    elif detached_sig:
        _cmd = ['/usr/bin/codesign', '-vvv', '-d', '-r', '-', '--detached', detached_sig, path]

    _p = subprocess.Popen(_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _r, _e = _p.communicate()

    if _r and isinstance(_r, bytes):
        _r = _r.decode('utf-8')

    if _e and isinstance(_e, bytes):
        _e = _e.decode('utf-8')

    if _p.returncode == 0:
        # Extract the code signature from the result. Handle circumstances
        # where the output may not explicitly start with 'designated => '
        # and where the code signature is split across multiple lines.
        for _line in _r.splitlines():
            if _dsgn_prefix in _line:
                _res = _line.partition(_dsgn_prefix)
                _res = _res[_res.index(_dsgn_prefix) + 1:][0]
                result[_csreq_key] = _res

        for _line in _e.splitlines():
            if _line.startswith(_idnt_prefix):
                if _idnt_prefix in _line:
                    result[_id_key] = _line.replace(_idnt_prefix, '')
                    result[_id_type_key] = 'bundleID'

                    # Test to make sure that the bundle ID matches
                    # expected style of 'org.example.foo'. This is
                    # not a terribly strict test, but it is aimed to
                    # avoid scenarios like the 'python3' binary
                    # deep in the framework has an identifier value
                    # of 'python3'.
                    if not re.match(_bnid_regex, result[_id_key]):
                        result[_id_key] = path
                        result[_id_type_key] = 'path'
    elif _p.returncode == 1 and 'not signed' in _e:
        result[_csreq_key] = None
        result[_id_key] = None
        result[_id_type_key] = None

    result['is_signed'] = result.get('csreq', None) is not None

    return result
