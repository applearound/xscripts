from functools import cached_property

from .attribute_info import AttributeInfo


class ModulePackagesAttributeInfo(AttributeInfo):
    """ Represents a module packages attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.26

    ModulePackages_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 package_count;
        u2 package_index[package_count];
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def number_of_packages(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def packages(self) -> bytes:
        return self.raw[8:8 + self.number_of_packages * 2]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_packages={self.number_of_packages}, packages={self.packages})"
