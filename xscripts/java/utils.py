def parse_int(segment: bytes) -> int:
    """Parse a byte segment into an integer."""
    return int.from_bytes(segment, byteorder='big', signed=False)


def decode_utf8(segment: bytes) -> str:
    """ Decode a java byte segment into a UTF-8 string.

    There are two differences between this format and the "standard" UTF-8 format.
    First, the null character (char)0 is encoded using the 2-byte format rather than the 1-byte format, so that modified UTF-8 strings never have embedded nulls.
    Second, only the 1-byte, 2-byte, and 3-byte formats of standard UTF-8 are used.
    The Java Virtual Machine does not recognize the four-byte format of standard UTF-8; it uses its own two-times-three-byte format instead.
    Characters with code points above U+FFFF (so-called supplementary characters) are represented by separately encoding the two surrogate code units of their UTF-16 representation.
    """
    return segment.decode('utf-8', errors='replace').replace('\x00', '\u0000')
