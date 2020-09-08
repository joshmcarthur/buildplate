
import json
import os
from hashlib import sha1
from os import walk
from os.path import dirname, isdir, isfile, join

WINDOWS = os.sys.platform.startswith("win")

def bootstrap():
  if not isdir(get_library_dir()):
    os.mkdir(get_library_dir())

def expanduser(path):
    """
    Be compatible with Python 3.8, on Windows skip HOME and check for USERPROFILE
    """
    if not WINDOWS or not path.startswith("~") or "USERPROFILE" not in os.environ:
        return os.path.expanduser(path)
    return os.environ["USERPROFILE"] + path[1:]

def get_library_dir():
  docs_dir = join(expanduser("~"), "Documents")
  try:
      assert WINDOWS
      import ctypes.wintypes  # pylint: disable=import-outside-toplevel

      buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
      ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
      docs_dir = buf.value
  except:  # pylint: disable=bare-except
      pass
  return join(docs_dir, "Buildplate")