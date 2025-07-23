from functools import cached_property

from .constant_pool_info import ConstantPoolInfo

from ..enums import ConstantPoolInfoTags


class FloatConstantPoolInfo(ConstantPoolInfo):
    """ Represents a float constant in the Java constant pool.

    Refer: https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html#jvms-4.4.4
    """

    @staticmethod
    def get_tag() -> ConstantPoolInfoTags:
        return ConstantPoolInfoTags.FLOAT

    @classmethod
    def size_check(cls, raw_bytes: bytes) -> bool:
        return len(raw_bytes) == 5

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def bytes(self) -> bytes:
        """ Get the raw bytes of the float constant.
        """
        return self.raw[1:5]

    @cached_property
    def value(self) -> float:
        """ Get the float value of the constant pool info.
        """
        return self.parse_float(self.bytes)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bytes={self.bytes.hex().upper()}, value={self.value})"
