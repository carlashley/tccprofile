"""TCC Objects"""

from datetime import datetime

from .codesign import csreq
from .conf import BIG_SUR_VER, KTCC_MAP, KTCC_ALLOW_STD_USER_PAYLOADS, MAC_OS_VER


class TCCApplication:
    """TCC Application (local file paths) object."""
    _ATTRS = ['csreq',
              'identifier',
              'identifier_type',
              'is_signed',
              'name',
              'path']

    def __init__(self, **kwargs):
        if not all([_a in kwargs for _a in self.__class__._ATTRS]):
            raise AttributeError('{} attributes required.'.format(self.__class__._ATTRS))

        for _k, _v in kwargs.items():
            if _k in self.__class__._ATTRS:  # Only include attributes that are necessary
                setattr(self, _k, _v)

    def __hash__(self):
        if not isinstance(self, self.__class__):
            return NotImplemented
        else:
            _hash_str = ','.join(map(str, [self.__dict__.get(_k, 'None')
                                           for _k in self.__class__._ATTRS]))

            return hash(_hash_str)

    def __eq__(self, other):
        """Equal."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Not Equal."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return not self.__eq__(other)


class TCCDBEntry:
    """TCC Database object."""
    # NOTE: Changes to the TCC.db in Big Sur drops the 'prompt_count' field,
    #       so this has been removed as a required attribute.
    #       The 'allowed' field also changed in Big Sur to 'auth_value' so
    #       this is remapped to 'allowed' in the 'sqlitedb' class.
    _ATTRS = ['allowed',
              'identifier',
              'identifier_type',
              'csreq',
              'flags',
              'apple_events_csreq',
              'apple_events_identifier',
              'apple_events_identifier_type',
              'last_modified',
              'policy_id',
              'service']

    def __init__(self, **kwargs):
        if not all([_a in kwargs for _a in self.__class__._ATTRS]):
            raise AttributeError('{} attributes required.'.format(self.__class__._ATTRS))

        # Determine kTCC service type and if this is an AppleEvent entry.
        _tcc_service_type = KTCC_MAP.get(kwargs['service'], None)
        _is_ae_event = not kwargs.get('apple_events_identifier', 'UNUSED') == 'UNUSED'

        for _k, _v in kwargs.items():
            # NOTE:In the SQL, the 'client_type' value of '1' represents
            # is a 'path' identifier type, while '0' indicates a 'bundleID'.
            if _k == 'identifier_type':
                _v = 'path' if _v == 1 else 'bundleID'

            # As above for 'client_type'.
            if _k == 'apple_events_identifier_type':
                if _is_ae_event:
                    _v = 'path' if _v == 1 else 'bundleID'
                else:
                    _v = None

            # NOTE:In the SQL, the 'allowed' value of '1' represents
            # the entry is enabled, while '0' indicates not allowed.
            if _k == 'allowed':
                if MAC_OS_VER < BIG_SUR_VER:
                    _allow_value = 1
                elif MAC_OS_VER >= BIG_SUR_VER:
                    _allow_value = 2

                if _tcc_service_type and _tcc_service_type in KTCC_ALLOW_STD_USER_PAYLOADS:
                    _v = 'AllowStandardUserToSetSystemService' if _v == _allow_value else 'Deny'
                elif _tcc_service_type and _tcc_service_type not in KTCC_ALLOW_STD_USER_PAYLOADS:
                    _v = 'Allow' if _v == _allow_value else 'Deny'

            # NOTE: In the SQL, the 'last_modified' value is an 'epoch'
            # time entry.
            if _k == 'last_modified':
                _v = datetime.fromtimestamp(_v).strftime('%Y-%m-%d %H:%M:%S')

            # Reverse the 'csreq' generated codesign requirements.
            if _k == 'csreq':
                if _v:
                    _v = csreq(str.encode(_v.hex()))

            if _k == 'apple_events_csreq':
                if _v and _is_ae_event:
                    _v = csreq(str.encode(_v.hex()))
                else:
                    _v = None

            # If this isn't an AppleEvent, value is None
            if _k == 'apple_events_identifier':
                if not _is_ae_event:
                    _v = None

            # Convert the 'KTCC[Service]' to the PPPCP payload type.
            # Gets set to 'None' if there is no PPPCP payload.
            if _k == 'service':
                _v = KTCC_MAP.get(_v, None)

            setattr(self, _k, _v)

    def __hash__(self):
        if not isinstance(self, self.__class__):
            return NotImplemented
        else:
            _hash_str = ','.join(map(str, [self.__dict__.get(_k, 'None')
                                           for _k in self.__class__._ATTRS]))

            return hash(_hash_str)

    def __eq__(self, other):
        """Equal."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Not Equal."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            return not self.__eq__(other)
