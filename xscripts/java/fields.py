from typing import Iterable

from .enums import FieldAccessFlags
from .utils import parse_int
from .attributes import Attribute, dump_bytes as dump_attributes_bytes


class Field:
    def __init__(self, raw_bytes: bytes, access_flags: int, name_index: int, descriptor_index: int,
                 attributes_count: int, attributes: Iterable[Attribute]) -> None:
        self.raw: bytes = raw_bytes

        self.access_flags: int = access_flags
        self.name_index: int = name_index
        self.descriptor_index: int = descriptor_index
        self.attributes_count: int = attributes_count
        self.attributes: tuple[Attribute, ...] = tuple(attributes)

    def get_access_flags(self) -> tuple[FieldAccessFlags, ...]:
        return FieldAccessFlags.parse_flags(self.access_flags)

    def is_public(self) -> bool:
        return FieldAccessFlags.is_public(self.access_flags)

    def is_private(self) -> bool:
        return FieldAccessFlags.is_private(self.access_flags)

    def get_name_index(self) -> int:
        return self.name_index

    def get_descriptor_index(self) -> int:
        return self.descriptor_index

    def get_attributes_count(self) -> int:
        return self.attributes_count

    def get_attributes(self) -> tuple[Attribute, ...]:
        """Get the attributes of the field."""
        return self.attributes

    def __repr__(self) -> str:
        return f"Field(access_flags={self.access_flags}, name_index={self.name_index}, " \
               f"descriptor_index={self.descriptor_index}, attributes_count={self.attributes_count})"


def dump_bytes(count: int, raw_bytes: bytes) -> tuple[Field, ...]:
    """Dump bytes into a tuple of Field objects."""
    fields = []
    cursor = 0
    for _ in range(count):
        access_flags = parse_int(raw_bytes[cursor: cursor + 2])
        name_index = parse_int(raw_bytes[cursor + 2: cursor + 4])
        descriptor_index = parse_int(raw_bytes[cursor + 4: cursor + 6])
        attributes_count = parse_int(raw_bytes[cursor + 6: cursor + 8])

        attributes = dump_attributes_bytes(attributes_count, raw_bytes[cursor + 8:])

        full_attributes_length = sum(len(attr.raw) for attr in attributes)

        fields.append(
            Field(raw_bytes[cursor: cursor + 8 + full_attributes_length], access_flags, name_index, descriptor_index,
                  attributes_count, attributes))

        cursor += 8 + full_attributes_length

    return tuple(fields)
