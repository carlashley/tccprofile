"""TCC Database Scan."""

import pathlib

from sys import exit

from .conf import KTCC_MAP
from .sqlitedb import SQLiteDB
from .payloadobj import ServicesDict


def user_managed(services=[_v for _k, _v in KTCC_MAP.items()]):
    """Read TCC SQLite Database."""
    result = dict()

    _db_path = 'Library/Application Support/com.apple.TCC/TCC.db'
    _current_user = pathlib.Path().home() / _db_path
    _system = pathlib.Path('/') / _db_path

    _query = 'SELECT * FROM access'

    _user_db = {_r for _r in SQLiteDB(db=_current_user).query(q=_query)}
    _system_db = {_r for _r in SQLiteDB(db=_system).query(q=_query)}

    for _app in _user_db.union(_system_db):
        if _app.service in services:
            try:
                result[_app.service].append(ServicesDict(**_app.__dict__).service)
            except KeyError:
                result[_app.service] = list()
                result[_app.service].append(ServicesDict(**_app.__dict__).service)

    return result


def list_services():
    """Read TCC SQLite Database."""
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

    print('Supported services found in TCC databases:')
    for _r in result:
        print('  {}'.format(_r))

    exit()
