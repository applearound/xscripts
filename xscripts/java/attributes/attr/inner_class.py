from .attribute import Attribute


class InnerClassAttribute(Attribute):
    """ Represents an inner class attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.6
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.number_of_classes: int = self.parse_int(self.raw[6:8])
        self.classes: bytes = self.raw[8:]

    def get_number_of_classes(self) -> int:
        return self.number_of_classes

    def get_classes(self) -> bytes:
        return self.classes

    def __repr__(self) -> str:
        return f"InnerClassAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_classes={self.number_of_classes})"
