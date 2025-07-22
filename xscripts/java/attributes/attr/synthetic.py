from .attribute import Attribute


class SyntheticAttribute(Attribute):
    """ Represents a synthetic attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.8
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

    def __repr__(self) -> str:
        return f"SyntheticAttribute(name_index={self.attribute_name_index}, length={self.attribute_length})"
