from .attribute import Attribute


class MethodParametersAttribute(Attribute):
    """ Represents a method parameters attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.24
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.parameters_count: int = self.parse_int(self.raw[6:8])
        self.parameters: bytes = self.raw[8:]

    def get_parameters_count(self) -> int:
        return self.parameters_count

    def get_parameters(self) -> bytes:
        return self.parameters

    def __repr__(self) -> str:
        return f"MethodParametersAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"parameters_count={self.parameters_count})"
