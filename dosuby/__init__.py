try:
    from .version import __version__
except ImportError:
    # When installing with pip install -e . or running tests
    try:
        from setuptools_scm import get_version
        __version__ = get_version(root='..', relative_to=__file__)
    except (ImportError, LookupError):
        __version__ = "unknown"