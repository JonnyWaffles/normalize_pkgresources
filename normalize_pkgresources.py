"""
Normalizes pkg_resources and the newer, better importlib.resources.

importlib.resources.path and pkg_resources.resource_filename are normalized to
:func:`get_pkg_resource_path`. Both APIs safely return a Path object.

legacy pkg_resources are mapped to their importlib equivalents.

    ``resource_filename`` = ``resource_path``
    ``resource_stream`` = ``open_binary``
    ``resource_string`` = ``read_text``
"""
import atexit
from contextlib import ExitStack
from pathlib import Path


try:
    # Use the better API provided in 3.7
    from importlib.resources import path as resource_path
    from importlib.resources import read_text
    from importlib.resources import open_binary


    def get_pkg_resource_path(package: str, resource: str) -> Path:
        """The new package resource API returns a context manager.
        Use this function to safely get the path.
        """
        file_manager = ExitStack()
        atexit.register(file_manager.close)
        return file_manager.enter_context(resource_path(package, resource))

except ImportError:
    # Fall back on the older one.
    from pkg_resources import resource_filename as resource_path
    from pkg_resources import resource_stream as open_binary
    from pkg_resources import resource_string as _legacy_resource_string

    def read_text(package, resource, encoding='utf-8', errors='strict'):
        return _legacy_resource_string(package, resource).decode(encoding)

    def get_pkg_resource_path(package: str, resource: str) -> Path:
        """Old API returns a string, so normalize to a path.
        """
        # noinspection PyTypeChecker
        return Path(resource_path(package, resource))
