from .attributeinfo import AttributeInfo


class AnnotationDefaultAttributeInfo(AttributeInfo):
    """ Represents an annotation default attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.22
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.default_value: bytes = self.raw[6:]

    def get_default_value(self) -> bytes:
        return self.default_value

    def __repr__(self) -> str:
        return f"AnnotationDefaultAttributeInfo(name_index={self.attribute_name_index}, length={self.attribute_length})"
