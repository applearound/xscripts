from functools import cached_property

from .constant_pool_info import ConstantPoolInfo

from ..enums import ConstantPoolInfoTags


class FieldrefConstantPoolInfo(ConstantPoolInfo):
    """ Represents a Fieldref constant pool info entry in a Java class file.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.4.2
    """

    @staticmethod
    def get_tag() -> ConstantPoolInfoTags:
        return ConstantPoolInfoTags.FIELDREF

    @classmethod
    def size_check(cls, raw_bytes: bytes) -> bool:
        return len(raw_bytes) == 5

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def class_index(self) -> int:
        """ Get the class index of the fieldref.
        """
        return self.parse_int(self.raw[1:3])

    @cached_property
    def name_and_type_index(self) -> int:
        """ Get the name and type index of the fieldref.
        """
        return self.parse_int(self.raw[3:5])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(class_index={self.class_index}, name_and_type_index={self.name_and_type_index})"
