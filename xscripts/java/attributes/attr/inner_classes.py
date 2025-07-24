from dataclasses import dataclass
from functools import cached_property

from .attribute_info import AttributeInfo


class InnerClassesAttributeInfo(AttributeInfo):
    """ Represents an inner class attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.6

    InnerClasses_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 number_of_classes;
        {   u2 inner_class_info_index;
            u2 outer_class_info_index;
            u2 inner_name_index;
            u2 inner_class_access_flags;
        } classes[number_of_classes];
    }
    """

    @dataclass(frozen=True)
    class Class:
        inner_class_info_index: int
        outer_class_info_index: int
        inner_name_index: int
        inner_class_access_flags: int

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def number_of_classes(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def classes(self) -> tuple[Class, ...]:
        start = 8
        end = start + self.number_of_classes * 8
        return tuple(
            self.Class(
                inner_class_info_index=self.parse_int(self.raw[i:i + 2]),
                outer_class_info_index=self.parse_int(self.raw[i + 2:i + 4]),
                inner_name_index=self.parse_int(self.raw[i + 4:i + 6]),
                inner_class_access_flags=self.parse_int(self.raw[i + 6:i + 8])
            )
            for i in range(start, end, 8)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_classes={self.number_of_classes}, classes={self.classes})"
