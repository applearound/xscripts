from functools import cached_property

from .constant_pool_info import ConstantPoolInfo

from ..enums import ConstantPoolInfoTags


class MethodHandleConstantPoolInfo(ConstantPoolInfo):
    """ Represents a Method Handle constant pool entry in a Java class file.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.4.8
    """

    @staticmethod
    def get_tag() -> ConstantPoolInfoTags:
        return ConstantPoolInfoTags.METHOD_HANDLE

    @classmethod
    def size_check(cls, raw_bytes: bytes) -> bool:
        return len(raw_bytes) == 4

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def reference_kind(self) -> int:
        """ Get the reference kind of the method handle.

        Returns:
            int: The reference kind, which indicates the type of method handle.
        """
        return self.parse_int(self.raw[1:2])

    @cached_property
    def reference_index(self) -> int:
        """ Get the reference index of the method handle.

        Returns:
            int: The index in the constant pool that the method handle refers to.
        """
        return self.parse_int(self.raw[2:4])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(reference_kind={self.reference_kind}, reference_index={self.reference_index})"
