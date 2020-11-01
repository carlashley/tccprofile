"""Codesign."""

import subprocess
import re


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


def requirements(path):
    """Codesign."""
    result = dict()

    # Lines with useful output start with these strings
    _dsgn_prefix = 'designated => '
    _idnt_prefix = 'Identifier='

    # Bundle ID regex test string
    _bnid_regex = re.compile(r'^\w+\.')

    _cmd = ['/usr/bin/codesign', '-v', '-dr', '-', path]
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
                result['csreq'] = _res

        for _line in _e.splitlines():
            if _line.startswith(_idnt_prefix):
                if _idnt_prefix in _line:
                    result['client'] = _line.replace(_idnt_prefix, '')
                    result['client_type'] = 'bundleID'

                    # Test to make sure that the bundle ID matches
                    # expected style of 'org.example.foo'. This is
                    # not a terribly strict test, but it is aimed to
                    # avoid scenarios like the 'python3' binary
                    # deep in the framework has an identifier value
                    # of 'python3'.
                    if not re.match(_bnid_regex, result['client']):
                        result['client'] = path
                        result['client_type'] = 'path'
    elif _p.returncode == 1 and 'not signed' in _e:
        result['csreq'] = None
        result['client'] = None
        result['client_type'] = None

    result['is_signed'] = result.get('csreq', None) is not None

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
