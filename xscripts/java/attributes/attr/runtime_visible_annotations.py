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
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def num_annotations(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def annotations(self) -> tuple[Annotation, ...]:
        start = 8
        annotations = []
        for _ in range(self.num_annotations):
            annotation = self.__parse_annotation(start)
            annotations.append(annotation)
            start += 4 + sum(
                len(pair[1]) if isinstance(pair[1], bytes) else 0 for pair in annotation.element_value_pairs)
        return tuple(annotations)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length})" \
               f", num_annotations={self.num_annotations})"
