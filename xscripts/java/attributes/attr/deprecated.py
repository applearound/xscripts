from .attribute_info import AttributeInfo


class DeprecatedAttributeInfo(AttributeInfo):
    """ Represents a deprecated attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.15
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

    def __repr__(self) -> str:
        return f"DeprecatedAttribute(name_index={self.attribute_name_index}, length={self.attribute_length})"
