"""Contains commonly used functions."""
import hashlib


def hash_product(raw: bytes) -> str:
    """Create a hash from a byte string."""
    hasher = hashlib.sha1()
    hasher.update(raw)

    return hasher.hexdigest()
