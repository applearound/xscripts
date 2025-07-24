from functools import cached_property

from .attribute_info import AttributeInfo


class RuntimeInvisibleAnnotationsAttributeInfo(AttributeInfo):
    """ Represents a runtime invisible annotations attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.17

    RuntimeInvisibleAnnotations_attribute {
        u2         attribute_name_index;
        u4         attribute_length;
        u2         num_annotations;
        annotation annotations[num_annotations];
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def annotations_count(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def annotations(self) -> bytes:
        return self.annotations

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"annotations_count={self.annotations_count}, annotations={self.annotations})"
