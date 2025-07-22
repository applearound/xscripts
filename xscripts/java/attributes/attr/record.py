from .attribute import Attribute


class RecordAttribute(Attribute):
    """ Represents a record attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.30
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.number_of_components: int = self.parse_int(self.raw[6:8])
        self.components: bytes = self.raw[8:]

    def get_number_of_components(self) -> int:
        return self.number_of_components

    def get_components(self) -> bytes:
        return self.components

    def __repr__(self) -> str:
        return f"RecordAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_components={self.number_of_components})"
