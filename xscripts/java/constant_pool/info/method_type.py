from functools import cached_property

from .constant_pool_info import ConstantPoolInfo

from ..enums import ConstantPoolInfoTags


class MethodTypeConstantPoolInfo(ConstantPoolInfo):
    """ Represents a MethodType constant pool entry in a Java class file.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.4.9
    """

    @staticmethod
    def get_tag() -> ConstantPoolInfoTags:
        return ConstantPoolInfoTags.METHOD_TYPE

    @classmethod
    def size_check(cls, raw_bytes: bytes) -> bool:
        return len(raw_bytes) == 3

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def descriptor_index(self) -> int:
        """ Get the descriptor index of the method type.

        Returns:
            int: The descriptor index.
        """
        return self.parse_int(self.raw[1:3])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(descriptor_index={self.descriptor_index})"
