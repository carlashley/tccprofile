"""Menu Maker"""

import argparse

from pathlib import PurePath
from sys import argv, exit

from .common import errmsg
from .conf import KTCC_MAP
from .templates import available as available_templates
from .vers import VERSION_STR


def arg_parser():
    """Argument Parser"""
    result = None

    _args = {'scan': {'args': ['--scan'],
                      'kwargs': {'action': 'store_true',
                                 'dest': 'scan',
                                 'required': False,
                                 'help': ('Scan the TCC configuration (system and current user) on this device.')}},
             'template': {'args': ['-t', '--template'],
                          'kwargs': {'nargs': '*',
                                     'type': str,
                                     'dest': 'template',
                                     'metavar': '[template]',
                                     'required': False,
                                     'choices': sorted([_k for _k, _v in available_templates().items()]),
                                     'help': ('Specify a template to generate a profile from.')}},
             'output': {'args': ['-o', '--output'],
                        'kwargs': {'nargs': 1,
                                   'type': str,
                                   'dest': 'output',
                                   'metavar': '[path]',
                                   'required': False,
                                   'help': ('Save mobileconfig profile to specified path.')}},
             'payload_desc': {'args': ['--description'],
                              'kwargs': {'nargs': 1,
                                         'type': str,
                                         'dest': 'payload_desc',
                                         'metavar': '[description]',
                                         'required': False,
                                         'help': ('Payload description.')}},
             'payload_disp_name': {'args': ['--display-name'],
                                   'kwargs': {'nargs': 1,
                                              'type': str,
                                              'dest': 'payload_disp_name',
                                              'metavar': '[display-name]',
                                              'required': False,
                                              'help': ('Payload display name.')}},
             'payload_identifier': {'args': ['--identifier'],
                                    'kwargs': {'nargs': 1,
                                               'type': str,
                                               'dest': 'payload_identifier',
                                               'metavar': '[identifier]',
                                               'required': False,
                                               'help': ('Payload identifier. Recommend bundle-id style, for example: \'org.example.foo\'.')}},
             'payload_org': {'args': ['--organization'],
                             'kwargs': {'nargs': 1,
                                        'type': str,
                                        'dest': 'payload_org',
                                        'metavar': '[organization]',
                                        'required': False,
                                        'help': ('Payload organization.')}},
             'profile_removable': {'args': ['--remove-profile'],
                                   'kwargs': {'action': 'store_true',
                                              'dest': 'profile_removable',
                                              'required': False,
                                              'help': ('Allow the profile to be removed. Default is disallow removal.')}},
             'services': {'args': ['--services'],
                          'kwargs': {'nargs': '+',
                                     'type': str,
                                     'dest': 'services',
                                     'metavar': '[services]',
                                     'required': False,
                                     'choices': [_v for _k, _v in KTCC_MAP.items()],
                                     'help': ('Services to include in profile if found in TCC databases. \
                                              Uses the service names as per Apple\'s PPPCP payloads.')}},
             'list_services': {'args': ['--list-services'],
                               'kwargs': {'action': 'store_true',
                                          'dest': 'list_services',
                                          'required': False,
                                          'help': ('Lists supported services found in the TCC database.')}},
             'version': {'args': ['-v', '--version'],
                         'kwargs': {'action': 'version',
                                    'help': 'Display version number and license and exit.',
                                    'version': VERSION_STR}}}

    _parser = argparse.ArgumentParser()

    for _k, _arg in _args.items():
        _parser.add_argument(*_arg['args'], **_arg['kwargs'])

    result = _parser.parse_args()

    if not len(argv) > 1:
        _parser.print_help()
        exit(1)

    if result.list_services and (result.services or result.profile_removable or
                                 result.payload_org or result.payload_identifier or
                                 result.payload_disp_name or result.payload_desc or
                                 result.output or result.scan):
        _name = PurePath(argv[0]).name

        _parser.print_usage()
        errmsg('{}: error: argument --list-services: can only be used on its own'.format(_name))

    if not (result.scan or result.template) and (result.services or result.profile_removable or
                                                 result.payload_org or result.payload_identifier or
                                                 result.payload_disp_name or result.payload_desc or
                                                 result.output):
        _name = PurePath(argv[0]).name

        _parser.print_usage()
        errmsg('{}: error: argument --scan or -t/--template: is required.'.format(_name))

    return result
