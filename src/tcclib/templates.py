from pathlib import Path, PurePath

from .common import errmsg
from .conf import KTCC_ALLOW_STD_USER_PAYLOADS, KTCC_ALLOW_ONLY_PAYLOADS
from .codesign import requirements
from .payloadobj import ServicesDict

try:
    from .tpm import yaml
except ImportError:
    errmsg('PyYaml required. Please use \'pip3 install pyyaml\' to install.')


def _fetch(path):
    """Fetches templates from a path."""
    result = dict()

    _path = Path(path)

    for _file in _path.glob('*.yaml'):
        _bn = str(PurePath(_file).name).replace('com.github.carlashley.tccprofile.', '')  # Removes prefix.
        _bn = str(PurePath(_bn).stem)
        result[_bn] = _file

    return result


def _included(path=str(Path.cwd() / 'templates/included')):
    """Returns a dictionary of included templates."""
    result = None

    result = _fetch(path)

    return result


def _overrides(path=str(Path.cwd() / 'templates/overrides')):
    """Returns a dictionary of override templates."""
    result = None

    result = _fetch(path)

    return result


def _read(path):
    """Read a template."""
    result = None
    _path = Path(path)

    if _path.exists():
        with open(path, 'r') as _f:
            result = yaml.safe_load(_f)

    return result


def available():
    """All available templates. Override versions take precedence."""
    result = dict()

    result.update(_included())
    result.update(_overrides())

    return result


def services(template):
    """Returns a service."""
    result = dict()

    _tmplate = _read(template)

    for _svc, _apps in _tmplate.items():
        if not result.get(_svc):
            result[_svc] = list()

        for _a in _apps:
            _ae_codesig = None
            _path = _a.get('path', None)
            _receiver_path = _a.get('receiver_path', None)

            if _svc == 'AppleEvents':
                if _receiver_path and Path(_receiver_path).exists():
                    _ae_codesig = requirements(_receiver_path, apple_event=True)
                else:
                    _ae_keys = ['apple_events_identifier',
                                'apple_events_identifier_type',
                                'apple_events_csreq']

                    _ae_codesig = dict()

                    for _k in _ae_keys:
                        _ae_codesig[_k] = _a.get(_k, None)

            if _path and Path(_path).exists():
                _app = dict()
                _codesig = requirements(_path)

                try:
                    _app['allowed'] = _a['authorization']
                except KeyError:
                    if _svc in KTCC_ALLOW_STD_USER_PAYLOADS:
                        _app['allowed'] = 'AllowStandardUserToSetSystemService'
                    elif _svc in KTCC_ALLOW_ONLY_PAYLOADS:
                        _app['allowed'] = 'Allow'

                _app.update(_codesig)

                if _ae_codesig:
                    _app.update(_ae_codesig)
            else:
                _app = dict()
                _app.update(_a)

            _sd = ServicesDict(**_a)
            result[_svc].append(_sd.service)

    return result


def write(data, path):
    """Write a template."""
    with open(path, 'w') as _f:
        yaml.dump(data, _f)
