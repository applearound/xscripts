from .attribute_info import AttributeInfo


class RuntimeVisibleTypeAnnotationsAttributeInfo(AttributeInfo):
    """ Represents a runtime visible type annotations attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.20

    RuntimeVisibleTypeAnnotations_attribute {
        u2              attribute_name_index;
        u4              attribute_length;
        u2              num_annotations;
        type_annotation annotations[num_annotations];
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

        self.annotations_count: int = self.parse_int(self.__raw[6:8])
        self.annotations: bytes = self.__raw[8:]

    def get_annotations_count(self) -> int:
        return self.annotations_count

    def get_annotations(self) -> bytes:
        return self.annotations

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"annotations_count={self.annotations_count})"
