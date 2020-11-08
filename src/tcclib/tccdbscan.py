"""TCC Database Scan."""

import pathlib

from sys import exit

from .appscan import installed
from .common import errmsg
from .conf import KTCC_MAP
from .sqlitedb import SQLiteDB
from .payloadobj import ServicesDict


def user_managed(services=[_v for _k, _v in KTCC_MAP.items()]):
    """Items added to TCC database via System Preferences."""
    result = dict()

    _db_path = 'Library/Application Support/com.apple.TCC/TCC.db'
    _current_user = pathlib.Path().home() / _db_path
    _system = pathlib.Path('/') / _db_path

    _query = 'SELECT * FROM access'

    _user_db = {_r for _r in SQLiteDB(db=_current_user).query(q=_query)}
    _system_db = {_r for _r in SQLiteDB(db=_system).query(q=_query)}
    _installed_apps = dict()

    for _app in installed():
        if _app.is_signed:
            _installed_apps[_app.identifier] = _app

    for _app in _user_db.union(_system_db):
        # Some apps in the TCC db don't have a 'csreq' value for some reason
        # so check if it exists in the installed apps
        if not _app.csreq:  # and _installed_apps.get(_app.identifier, None):
            try:
                _app.csreq = _installed_apps[_app.identifier].csreq
            except (KeyError, AttributeError):
                pass

        if _app.service in services:
            try:
                result[_app.service].append(ServicesDict(**_app.__dict__).service)
            except KeyError:
                result[_app.service] = list()
                result[_app.service].append(ServicesDict(**_app.__dict__).service)

    return result


def list_services():
    """Unique list of all PPPCP service names from the TCC database."""
    result = None

    _db_path = 'Library/Application Support/com.apple.TCC/TCC.db'
    _current_user = pathlib.Path().home() / _db_path
    _system = pathlib.Path('/') / _db_path

    _query = 'SELECT * FROM access'

    _user_db = {_r for _r in SQLiteDB(db=_current_user).query(q=_query)}
    _system_db = {_r for _r in SQLiteDB(db=_system).query(q=_query)}

    _services = set()

    for _app in _user_db.union(_system_db):
        _services.add(_app.service)

    result = list(_services)
    result.sort()

    if result:
        print('Supported services found in TCC databases:')
        for _r in result:
            print('  {}'.format(_r))
    else:
        errmsg('No supported services found in TCC databases.')

    exit()
