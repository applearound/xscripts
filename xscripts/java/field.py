from .enums import FieldAccessFlags
from .utils import parse_int


class Field:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw: bytes = raw_bytes

        self.access_flags: int = parse_int(self.raw[0:2])
        self.name_index: int = parse_int(self.raw[2:4])
        self.descriptor_index: int = parse_int(self.raw[4:6])
        self.attributes_count: int = parse_int(self.raw[6:8])

    def get_access_flags(self) -> tuple[FieldAccessFlags, ...]:
        return FieldAccessFlags.parse_flags(self.access_flags)

    def get_name_index(self) -> int:
        return self.name_index

    def get_descriptor_index(self) -> int:
        return self.descriptor_index

    def get_attributes_count(self) -> int:
        return self.attributes_count
