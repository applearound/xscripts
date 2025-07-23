from functools import cached_property

from .constant_pool_info import ConstantPoolInfo

from ..enums import ConstantPoolInfoTags


class Utf8ConstantPoolInfo(ConstantPoolInfo):
    """ Represents a UTF-8 constant pool entry in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.4.7
    """

    @staticmethod
    def get_tag() -> ConstantPoolInfoTags:
        return ConstantPoolInfoTags.UTF8

    @classmethod
    def size_check(cls, raw_bytes: bytes) -> bool:
        return len(raw_bytes) == 1 + 2 + cls.parse_int(raw_bytes[1:3])

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def length(self) -> int:
        return self.parse_int(self.raw[1:3])

    @cached_property
    def bytes(self) -> bytes:
        """ Get the raw bytes of the UTF-8 string, excluding the length prefix.
        """
        return self.raw[3:3 + self.length]

    @cached_property
    def string(self) -> str:
        return self.bytes.decode('utf-8')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(length={self.length}, bytes='{self.bytes.hex().upper()}', string='{self.string}')"
