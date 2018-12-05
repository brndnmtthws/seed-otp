import base64
import hashlib
import secrets
import struct

import click


def get_next_int():
    # BIP-0039 specifies 11 bits for representing words (i.e., 2048 possible
    # values per word)
    return secrets.randbelow(2048)


def generate_key(num_words):
    if num_words > 2**16:
        raise ValueError("Maximum number of possible words is 65536")
    ints = []
    for _ in range(0, num_words):
        ints.append(get_next_int())

    return encode_key(num_words, ints)


def encode_key(num_keys, keylist):
    # First 2 bytes are the number of words
    keystring = struct.pack('>H', num_keys)
    # Following groups of 2 bytes each are the word indexes
    for idx in keylist:
        keystring += struct.pack('>H', idx)

    # Last 4 bytes (checksum) is the first 4 bytes of the sha256 digest
    m = hashlib.sha256()
    m.update(keystring)
    keystring += m.digest()[0:4]

    return base64.urlsafe_b64encode(keystring).decode('ascii').rstrip('=')


class DecodingError(Exception):
    """Raised when there is a decoding error"""
    pass


def decode_key(keystring):
    # Add base64 padding if necessary
    missing_padding = len(keystring) % 4
    if missing_padding:
        keystring += '=' * (4 - missing_padding)

    buffer = base64.urlsafe_b64decode(keystring)

    # Extract checksum first, the last 4 bytes
    checksum = buffer[-4:]

    # Compute digest on the rest of the buffer
    m = hashlib.sha256()
    m.update(buffer[:-4])

    if checksum != m.digest()[0:4]:
        raise DecodingError("Checksums do not match")

    num_keys = struct.unpack('>H', buffer[0:2])[0]

    if num_keys != (len(buffer) - 6) / 2:
        raise DecodingError("Key length doesn't match expected value")

    keylist = []

    for i in range(0, num_keys):
        from_idx = 2 + i * 2
        to_idx = 2 + i * 2 + 2
        keylist.append(struct.unpack('>H', buffer[from_idx:to_idx])[0])

    return (num_keys, keylist)
