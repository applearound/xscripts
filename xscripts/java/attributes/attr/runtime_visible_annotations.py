from dataclasses import dataclass
from functools import cached_property

from .attribute_info import AttributeInfo


class RuntimeVisibleAnnotationsAttributeInfo(AttributeInfo):
    """ Represents a runtime visible annotations attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.16

    RuntimeVisibleAnnotations_attribute {
        u2         attribute_name_index;
        u4         attribute_length;
        u2         num_annotations;
        annotation annotations[num_annotations];
    }

    annotation {
        u2 type_index;
        u2 num_element_value_pairs;
        {   u2            element_name_index;
            element_value value;
        } element_value_pairs[num_element_value_pairs];
    }

    element_value {
        u1 tag;
        union {
            u2 const_value_index;

            {   u2 type_name_index;
                u2 const_name_index;
            } enum_const_value;

            u2 class_info_index;

            annotation annotation_value;

            {   u2            num_values;
                element_value values[num_values];
            } array_value;
        } value;
    }
    """

    @dataclass(frozen=True)
    class Annotation:
        type_index: int
        num_element_value_pairs: int
        element_value_pairs: tuple[tuple[int, bytes], ...]

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def num_annotations(self) -> int:
        return self.parse_int(self.raw[6:8])

    def annotations(self) -> bytes:
        return self.annotations

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length})" \
               f", num_annotations={self.num_annotations})"
