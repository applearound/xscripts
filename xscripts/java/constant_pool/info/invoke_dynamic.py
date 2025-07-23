from functools import cached_property

from .constant_pool_info import ConstantPoolInfo

from ..enums import ConstantPoolInfoTags


class InvokeDynamicConstantPoolInfo(ConstantPoolInfo):
    """ Represents an InvokeDynamic constant pool entry in a Java class file.

    Refer: https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html#jvms-4.4.10
    """

    @staticmethod
    def get_tag() -> ConstantPoolInfoTags:
        return ConstantPoolInfoTags.INVOKE_DYNAMIC

    @classmethod
    def size_check(cls, raw_bytes: bytes) -> bool:
        return len(raw_bytes) == 5

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def bootstrap_method_attr_index(self) -> int:
        """ Get the bootstrap method attribute index.
        """
        return self.parse_int(self.raw[1:3])

    @cached_property
    def name_and_type_index(self) -> int:
        """ Get the name and type index.
        """
        return self.parse_int(self.raw[3:5])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bootstrap_method_attr_index={self.bootstrap_method_attr_index}, name_and_type_index={self.name_and_type_index})"
