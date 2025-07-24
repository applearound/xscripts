from functools import cached_property

from .attribute_info import AttributeInfo


class EnclosingMethodAttributeInfo(AttributeInfo):
    """ Represents an enclosing method attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.7

    EnclosingMethod_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 class_index;
        u2 method_index;
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def class_index(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def method_index(self) -> int:
        return self.parse_int(self.raw[8:10])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"class_index={self.class_index}, method_index={self.method_index})"
