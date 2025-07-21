def parse_int(segment: bytes) -> int:
    """Parse a byte segment into an integer."""
    return int.from_bytes(segment, byteorder='big', signed=False)
