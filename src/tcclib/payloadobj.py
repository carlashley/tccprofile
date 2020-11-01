"""Payload Object"""

from datetime import datetime
from uuid import uuid1

_NOW = datetime.now().strftime('%Y-%m-%d-%H%M%S')


class ServicesDict:
    _REQ_ATTRS = ['client',
                  'client_type',
                  'csreq',
                  'allowed']

    _TCC_SERVICE_PAYLOAD_MAP = {'client': 'Identifier',
                                'client_type': 'IdentifierType',
                                'csreq': 'CodeRequirement',
                                'allowed': 'Authorization',
                                'indirect_object_identifier': 'AEReceiverIdentifier',
                                'indirect_object_identifier_type': 'AEReceiverIdentifierType',
                                'indirect_object_code_identity': 'AEReceiverCodeRequirement'}

    def __init__(self, **kwargs):
        """Services Dict"""
        if not all([_a in kwargs for _a in self.__class__._REQ_ATTRS]):
            raise AttributeError('{} attributes required.'.format(self.__class__._REQ_ATTRS))

        self.service = dict()

        for _k, _v in kwargs.items():
            _attr = self.__class__._TCC_SERVICE_PAYLOAD_MAP.get(_k, None)

            # Only include the payload attributes that have a value.
            if _attr and _v:
                self.service[_attr] = _v

    def __hash__(self):
        if not isinstance(self, self.__class__):
            return NotImplemented
        else:
            _hash_str = ','.join(map(str, [self.__dict__.get(_k, 'None')
                                           for _k in self.__class__._REQ_ATTRS]))

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


class PayloadContentDict:
    """PayloadContent Dict"""
    _UUID = str(uuid1()).upper()
    _REQ_ATTRS = {'PayloadDescription': 'PPPCP profile',
                  'PayloadDisplayName': 'PPPCP profile',
                  'PayloadIdentifier': 'com.github.carlashley.tccprofile.{}'.format(_UUID),
                  'PayloadOrganization': 'com.github.carlashley.tccprofile',
                  'PayloadType': 'com.apple.TCC.configuration-profile-policy',
                  'PayloadUUID': _UUID,
                  'PayloadVersion': 1,
                  'Services': None}

    _MUTABLE_KEYS = ['PayloadIdentifier',
                     'PayloadOrganization']

    def __init__(self, services, **kwargs):
        """PPPCP Payload Content"""
        if not isinstance(services, dict):
            raise TypeError('\'services\' must be \'dict\'.')

        self.payload_content = self.__class__._REQ_ATTRS.copy()

        for _k, _v in kwargs.items():
            if _k in self.__class__._MUTABLE_KEYS:
                if _k == 'PayloadIdentifier':
                    _v = '{}.{}'.format(_v, self.__class__._UUID)

                self.payload_content[_k] = _v

        self.payload_content['Services'] = services


class ProfileDict:
    _UUID = str(uuid1()).upper()
    _REQ_ATTRS = {'PayloadDescription': 'PPPCP Profile generated from the System and Current user TCC databases.',
                  'PayloadDisplayName': 'PPPCP Profile Generated {}'.format(_NOW),
                  'PayloadIdentifier': 'com.github.carlashley.tccprofile',
                  'PayloadOrganization': 'com.github.carlashley.tccprofile',
                  'PayloadRemovalDisallowed': True,
                  'PayloadScope': 'system',
                  'PayloadType': 'Configuration',
                  'PayloadUUID': _UUID,
                  'PayloadVersion': 1}

    _MUTABLE_KEYS = ['PayloadDescription',
                     'PayloadDisplayName',
                     'PayloadIdentifier',
                     'PayloadOrganization',
                     'PayloadRemovalDisallowed']

    def __init__(self, payload_content, **kwargs):
        """Profile Dict"""
        self.payload = self.__class__._REQ_ATTRS.copy()

        for _k, _v in kwargs.items():
            if _k in self.__class__._MUTABLE_KEYS:
                self.payload[_k] = _v

        self.payload['PayloadContent'] = [payload_content]
