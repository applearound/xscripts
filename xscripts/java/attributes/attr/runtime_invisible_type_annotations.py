from .attribute_info import AttributeInfo


class RuntimeInvisibleTypeAnnotationsAttributeInfo(AttributeInfo):
    """ Represents a runtime invisible type annotations attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.21

    RuntimeInvisibleTypeAnnotations_attribute {
        u2              attribute_name_index;
        u4              attribute_length;
        u2              num_annotations;
        type_annotation annotations[num_annotations];
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

        self.annotations: bytes = self.__raw[6:]

    def get_annotations(self) -> bytes:
        return self.annotations

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length})"
