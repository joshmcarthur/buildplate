""" Utility functions that don't fit nicely into another context. """
import hashlib

def sha1(fname):
    """ Calculate the SHA1 hash of a file. """
    hash_sha1 = hashlib.sha1()
    with open(fname, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_sha1.update(chunk)
    return hash_sha1.hexdigest()
