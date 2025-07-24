from functools import cached_property

from .attribute_info import AttributeInfo


class AnnotationDefaultAttributeInfo(AttributeInfo):
    """ Represents an annotation default attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.22

    AnnotationDefault_attribute {
        u2            attribute_name_index;
        u4            attribute_length;
        element_value default_value;
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def default_value(self) -> bytes:
        return self.raw[6:6 + self.attribute_length]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length})"
