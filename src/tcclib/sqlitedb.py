"""SQLite DB."""
import sqlite3

from .conf import KTCC_DENY_ONLY_PAYLOADS
from .tccobj import TCCDBEntry

# Note, in some circumstances, the 'csreq' value for items added to 'TCC.db'
# may contain a 'cdhash H"[hash]" or cdhash H"[hash]"' type value.
# This may be because the item is not actually codesigned in a manner
# that results in the "standard" codesign value of:
# 'identifier "org.example.foo" ... and certificate leaf[subject.OU] = [TeamID]'
# but it is still valid code requirement syntax.
# This means that you should still be able to add non codesigned items to
# a PPPCP profile (in testing this has only been observed for apps that trigger
# TCC requests to access storage/file/volume locations, but doesn't exclude other
# possibilities).


class SQLiteDB:
    """SQLite"""
    _HDR_MAP = {'client': 'identifier',
                'client_type': 'identifier_type',
                'indirect_object_identifier': 'apple_events_identifier',
                'indirect_object_identifier_type': 'apple_events_identifier_type',
                'indirect_object_code_identity': 'apple_events_csreq',
                'auth_value': 'allowed'}  # New in macOS Big Sur. Replaces 'allowed'.

    def __init__(self, db):
        self._db = db
        self._connection = None

        self.cursor = None

    def _connect(self):
        """Connect."""
        self._connection = sqlite3.connect(self._db)

        self.cursor = self._connection.cursor()

    def _disconnect(self):
        """Disconnect."""
        self._connection.close()

    def query(self, q):
        """Query - fetches all."""
        result = None

        self._connect()

        try:
            self.cursor.execute(q)

            # Tweak column headers to use for object attributes
            _columns = list()
            for _desc in self.cursor.description:
                try:
                    _hdr = self.__class__._HDR_MAP[_desc[0]]
                except KeyError:
                    _hdr = _desc[0]

                _columns.append(_hdr)

            # _columns = [_desc[0] for _desc in self.cursor.description]
            _rows = list()

            for _r in self.cursor.fetchall():
                _mapped_row = {_key: _value for _key, _value in zip(_columns, _r)}
                _row = TCCDBEntry(**_mapped_row)

                # Only append the row if the service type has a PPPCP Payload.
                if _row.service and _row.service not in KTCC_DENY_ONLY_PAYLOADS:
                    _rows.append(_row)

            result = _rows
        except Exception:
            self._disconnect()
            raise

        return result
