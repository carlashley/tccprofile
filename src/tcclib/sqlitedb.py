"""SQLite DB."""
import sqlite3

from .conf import KTCC_DENY_ONLY_PAYLOADS
from .tccobj import TCCDBEntry


class SQLiteDB:
    """SQLite"""
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
            _columns = [_desc[0] for _desc in self.cursor.description]
            _rows = list()

            for _r in self.cursor.fetchall():
                _mapped_row = {_key: _value for _key, _value in zip(_columns, _r)}
                _row = TCCDBEntry(**_mapped_row)

                # Only append the row if the service type has a PPPCP Payload.
                if _row.service and _row.service not in KTCC_DENY_ONLY_PAYLOADS and _row.csreq:
                    _rows.append(_row)

            result = _rows
        except Exception:
            self._disconnect()
            raise

        return result
