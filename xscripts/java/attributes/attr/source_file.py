from functools import cached_property

from .attribute_info import AttributeInfo


class SourceFileAttributeInfo(AttributeInfo):
    """ Represents a source file attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.10

    SourceFile_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 sourcefile_index;
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def sourcefile_index(self) -> int:
        return self.sourcefile_index

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"sourcefile_index={self.sourcefile_index})"
