from .attribute import Attribute


class EnclosingMethodAttribute(Attribute):
    """ Represents an enclosing method attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.7
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.class_index: int = self.parse_int(self.raw[6:8])
        self.method_index: int = self.parse_int(self.raw[8:10])

    def get_class_index(self) -> int:
        return self.class_index

    def get_method_index(self) -> int:
        return self.method_index

    def __repr__(self) -> str:
        return f"EnclosingMethodAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"class_index={self.class_index}, method_index={self.method_index})"
