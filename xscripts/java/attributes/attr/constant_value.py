from .attribute import Attribute


class ConstantValueAttribute(Attribute):
    """ Represents a constant value attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.2
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.constant_value_index: int = self.parse_int(self.raw[6:8])

    def get_constant_value_index(self) -> int:
        return self.constant_value_index

    def __repr__(self) -> str:
        return f"ConstantValueAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"constant_value_index={self.constant_value_index})"
