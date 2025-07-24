from .attribute_info import AttributeInfo


class SyntheticAttributeInfo(AttributeInfo):
    """ Represents a synthetic attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.8

    Synthetic_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length})"
