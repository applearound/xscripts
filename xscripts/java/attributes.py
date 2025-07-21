from .utils import parse_int


class Attribute:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw: bytes = raw_bytes

        self.attribute_name_index: int = parse_int(self.raw[0:2])
        self.attribute_length: int = parse_int(self.raw[2:6])
        self.info_raw: bytes = self.raw[6:]

    def get_attribute_name_index(self) -> int:
        return self.attribute_name_index

    def get_attribute_length(self) -> int:
        return self.attribute_length
