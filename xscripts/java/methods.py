from typing import Iterable

from .attributes import Attribute
from .enums import FieldAccessFlags


class Method:
    def __init__(self, raw_bytes: bytes, access_flags: int, name_index: int, descriptor_index: int,
                 attributes_count: int, attributes: Iterable[Attribute]) -> None:
        self.raw = raw_bytes

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
