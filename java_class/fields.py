class Fields:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw = raw_bytes

    def get_fields_count(self) -> int:
        return int.from_bytes(self.raw[:2], byteorder="big", signed=False)