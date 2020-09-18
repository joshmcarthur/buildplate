"""Helpers for finding or creating the central project directory.

   The central project directory is the location in which all design files
   and artifacts should be stored.
"""

import os
import pathlib

WINDOWS = os.sys.platform.startswith("win")


def bootstrap():
    """ Create the project directory if it does not already exist"""
    return get_projects_dir().mkdir(exist_ok=True)


def expanduser(path):
    """
    Be compatible with Python 3.8, on Windows skip HOME and check for USERPROFILE
    """
    if not WINDOWS or not path.startswith("~") or "USERPROFILE" not in os.environ:
        return os.path.expanduser(path)
    return os.environ["USERPROFILE"] + path[1:]


def get_projects_dir():
    """
    Look up the default system 'Documents' folder, and append a 'Buildplate' directory onto the path
    """
    docs_dir = pathlib.Path(expanduser("~")).joinpath("Documents")
    try:
        assert WINDOWS
        import ctypes.wintypes  # pylint: disable=import-outside-toplevel

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
        docs_dir = buf.value
    except:  # pylint: disable=bare-except
        pass
    return pathlib.Path(docs_dir).joinpath("Buildplate")
