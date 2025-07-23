from functools import cached_property

from .constant_pool_info import ConstantPoolInfo

from ..enums import ConstantPoolInfoTags


class DoubleConstantPoolInfo(ConstantPoolInfo):
    """ Represents a double constant pool info in the Java class file.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.4.5
    """

    @staticmethod
    def get_tag() -> ConstantPoolInfoTags:
        return ConstantPoolInfoTags.DOUBLE

    @classmethod
    def size_check(cls, raw_bytes: bytes) -> bool:
        """ Check if the raw bytes match the expected size for this constant pool info.
        """
        return len(raw_bytes) == 9

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def high_bytes(self) -> bytes:
        """ Get the high bytes of the double constant pool info.
        """
        return self.raw[1:5]

    @cached_property
    def low_bytes(self) -> bytes:
        """ Get the low bytes of the double constant pool info.
        """
        return self.raw[5:9]

    @cached_property
    def value(self) -> float:
        """ Get the double value of the constant pool info.
        """
        return self.parse_float(self.raw[1:9])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(high_bytes={self.high_bytes.hex().upper()}, low_bytes={self.low_bytes.hex().upper()}, value={self.value})"
