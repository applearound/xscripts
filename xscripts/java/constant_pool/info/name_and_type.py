from functools import cached_property

from .constant_pool_info import ConstantPoolInfo

from ..enums import ConstantPoolInfoTags


class NameAndTypeConstantPoolInfo(ConstantPoolInfo):
    """ Represents a Name and Type constant pool info entry in a Java class file.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.4.6
    """

    @staticmethod
    def get_tag() -> ConstantPoolInfoTags:
        return ConstantPoolInfoTags.NAME_AND_TYPE

    @classmethod
    def size_check(cls, raw_bytes: bytes) -> bool:
        return len(raw_bytes) == 5

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def name_index(self) -> int:
        """ Get the name index of the name and type entry.
        """
        return self.parse_int(self.raw[1:3])

    @cached_property
    def descriptor_index(self) -> int:
        """ Get the descriptor index of the name and type entry.
        """
        return self.parse_int(self.raw[3:5])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.name_index}, descriptor_index={self.descriptor_index})"
