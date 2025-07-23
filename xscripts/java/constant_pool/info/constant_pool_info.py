import struct

from abc import ABCMeta, abstractmethod

from ..enums import ConstantPoolInfoTags


class ConstantPoolInfo(metaclass=ABCMeta):
    @staticmethod
    def parse_int(segment: bytes) -> int:
        """ Parse an integer from a byte segment.
        """
        return int.from_bytes(segment, byteorder='big', signed=False)

    @staticmethod
    def parse_float(segment: bytes) -> float:
        """ Parse a float from a byte segment.
        """
        return struct.unpack('>f', segment)[0]

    @classmethod
    def get_tag_value(cls) -> int:
        """ Get the tag of the constant pool info.
        """
        return cls.get_tag().value

    @staticmethod
    @abstractmethod
    def get_tag() -> ConstantPoolInfoTags:
        """ Get the info segment of the constant pool info.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def size_check(cls, raw_bytes: bytes) -> bool:
        """ Check if the raw bytes match the expected size for this constant pool info.
        """
        raise NotImplementedError()

    def __init__(self, raw_bytes: bytes) -> None:
        tag = self.parse_int(raw_bytes[0:1])

        if tag != self.get_tag_value():
            raise ValueError(
                f"Invalid tag value: {tag}, for {self.__class__.__name__}, expected: {self.get_tag_value()}")

        if not self.size_check(raw_bytes):
            raise ValueError(f"Invalid size {len(raw_bytes)} bytes, for {self.__class__.__name__}")

        self.__raw: bytes = raw_bytes

    @property
    def raw(self) -> bytes:
        """ Get the raw bytes of the constant pool info.
        """
        return self.__raw

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.get_tag()})"
