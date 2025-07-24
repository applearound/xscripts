from functools import cached_property

from .attribute_info import AttributeInfo


class SourceDebugExtensionAttributeInfo(AttributeInfo):
    """ Represents a source debug extension attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.11

    SourceDebugExtension_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u1 debug_extension[attribute_length];
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def debug_extension(self) -> str:
        return self.raw[6:6 + self.attribute_length].decode("utf-8")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"debug_extension='{self.debug_extension}')"
