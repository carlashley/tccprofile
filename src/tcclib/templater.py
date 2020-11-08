from pathlib import Path, PurePath
from .common import errmsg

try:
    import yaml
except ImportError:
    errmsg('PyYaml required. Please use \'pip3 install pyyaml\' to install.')


def included(path=None):
    """Returns a set of included templates."""
    result = dict()

    if not path:
        path = Path.cwd() / 'templates/included'

    for _file in path.glob('*.yaml'):
        _bn = str(PurePath(_file).name).replace('com.github.carlashley.tccprofile.', '')  # Removes prefix.
        _bn = str(PurePath(_bn).stem)
        result[_bn] = _file

    return result


def read(path):
    """Read a template."""
    result = None
    _path = Path(path)

    if _path.exists():
        with open(path, 'r') as _f:
            result = yaml.safe_load(_f)

    return result


def write(data, path):
    """Write a template."""
    with open(path, 'w') as _f:
        yaml.dump(data, _f)
