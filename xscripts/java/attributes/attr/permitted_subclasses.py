from functools import cached_property

from .attribute_info import AttributeInfo


class PermittedSubclassesAttributeInfo(AttributeInfo):
    """ Represents a permitted subclasses attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.31

    PermittedSubclasses_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 number_of_classes;
        u2 classes[number_of_classes];
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def number_of_classes(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def classes(self) -> tuple[int, ...]:
        start = 8
        end = start + self.number_of_classes * 2
        return tuple(self.parse_int(self.raw[i:i + 2]) for i in range(start, end, 2))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_classes={self.number_of_classes}, classes={self.classes})"
