class Magic:
    def __init__(self, raw_bytes: bytes) -> None:
        if not isinstance(raw_bytes, bytes) or len(raw_bytes) != 4:
            raise Exception()
        
        self.raw = raw_bytes

    def get_magic(self) -> str:
        return self.raw.hex().upper()
