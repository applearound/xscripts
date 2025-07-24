from .attribute_info import AttributeInfo


class RuntimeInvisibleTypeAnnotationsAttributeInfo(AttributeInfo):
    """ Represents a runtime invisible type annotations attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.21
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.annotations: bytes = self.__raw[6:]

    def get_annotations(self) -> bytes:
        return self.annotations

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length})"
