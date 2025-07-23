from functools import cached_property

from .constant_pool_info import ConstantPoolInfo

from ..enums import ConstantPoolInfoTags


class PackageConstantPoolInfo(ConstantPoolInfo):
    """ Represents a package constant pool info entry.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.4.12
    """

    @staticmethod
    def get_tag() -> ConstantPoolInfoTags:
        return ConstantPoolInfoTags.PACKAGE

    @classmethod
    def size_check(cls, raw_bytes: bytes) -> bool:
        return len(raw_bytes) == 3

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def name_index(self) -> int:
        """ Get the name index of the package.
        """
        return self.parse_int(self.raw[1:3])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.name_index})"
