class Version:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw = raw_bytes

    def get_minor_version(self) -> int:
        return int.from_bytes(self.raw[:2], byteorder="big")

    def get_major_version(self) -> int:
        return int.from_bytes(self.raw[2:], byteorder="big")