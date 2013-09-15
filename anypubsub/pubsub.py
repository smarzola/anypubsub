try:
    import pkg_resources
except ImportError:
    pkg_resources = None

import sys


class ConfigurationError(Exception):
    pass


def _load_backend(name):
    try:
        module_name = 'anypubsub.backends.%s' % name
        __import__(module_name)
        module = sys.modules[module_name]
        return module.backend
    except ImportError:
        module = _load_entry_point(name)
        if module is not None:
            return module
        raise ConfigurationError('Could not determine backend for "%s"' % name)


def _load_entry_point(name):
    if pkg_resources is None:
        return None

    for res in pkg_resources.iter_entry_points('anypubsub.backends'):
        if res.name == name:
            return res.load()


def create_pubsub(name, **kwargs):
    backend_cls = _load_backend(name)
    return backend_cls(**kwargs)


def create_pubsub_from_settings(settings, prefix='', **kwargs):
    plen = len(prefix)
    for k, v in settings.items():
        if k.startswith(prefix):
            kwargs[k[plen:]] = v
    name = kwargs.pop('backend')
    return create_pubsub(name, **kwargs)
