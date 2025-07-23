from abc import ABCMeta
from functools import cached_property


class AttributeInfo(metaclass=ABCMeta):
    """ Represents a Java class attribute.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7
    """

    @staticmethod
    def parse_int(segment: bytes) -> int:
        return int.from_bytes(segment, byteorder='big', signed=False)

    def __init__(self, raw_bytes: bytes) -> None:
        if len(raw_bytes) <= 6:
            raise ValueError("Raw bytes must be longer than 6 bytes for attribute info.")

        length = self.parse_int(raw_bytes[2:6])

        if len(raw_bytes) != length + 6:
            raise ValueError(f"Raw bytes length {len(raw_bytes)} does not match expected length {length + 6}.")

        self.__raw: bytes = raw_bytes

    @property
    def raw(self) -> bytes:
        return self.__raw

    @cached_property
    def attribute_name_index(self) -> int:
        return self.parse_int(self.raw[:2])

    @cached_property
    def attribute_length(self) -> int:
        return self.parse_int(self.raw[2:6])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length})"
