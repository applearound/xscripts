from .attribute import Attribute


class ExceptionsAttribute(Attribute):
    """ Represents an exceptions attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.5
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.number_of_exceptions: int = self.parse_int(self.raw[6:8])
        self.exception_index_table: bytes = self.raw[8:]

    def get_number_of_exceptions(self) -> int:
        return self.number_of_exceptions

    def get_exception_index_table(self) -> bytes:
        return self.exception_index_table

    def __repr__(self) -> str:
        return f"ExceptionsAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_exceptions={self.number_of_exceptions})"
