class Interfaces:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw = raw_bytes

    def get_interfaces_count(self) -> int:
        return int.from_bytes(self.raw[:2], "big")