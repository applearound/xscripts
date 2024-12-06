class ThisAndSuperClass:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw = raw_bytes

    def get_this_class_index(self) -> int:
        return int.from_bytes(self.raw[:2], "big")

    def get_super_class_index(self) -> int:
        return int.from_bytes(self.raw[2:4], "big")