class Magic:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw = raw_bytes

    def get_magic(self) -> str:
        return self.raw.hex().upper()
