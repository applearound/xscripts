from .attributeinfo import AttributeInfo


class LineNumberTableAttributeInfo(AttributeInfo):
    """ Represents a line number table attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.12
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.line_number_table_length: int = self.parse_int(self.raw[6:8])
        self.line_number_table: bytes = self.raw[8:]

    def get_line_number_table_length(self) -> int:
        return self.line_number_table_length

    def get_line_number_table(self) -> bytes:
        return self.line_number_table

    def __repr__(self) -> str:
        return f"LineNumberTableAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"line_number_table_length={self.line_number_table_length})"
