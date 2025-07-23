from .attributeinfo import AttributeInfo


class LocalVariableTableAttributeInfo(AttributeInfo):
    """ Represents a local variable table attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.13
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.local_variable_table_length: int = self.parse_int(self.raw[6:8])
        self.local_variable_table: bytes = self.raw[8:]

    def get_local_variable_table_length(self) -> int:
        return self.local_variable_table_length

    def get_local_variable_table(self) -> bytes:
        return self.local_variable_table

    def __repr__(self) -> str:
        return f"LocalVariableTableAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"local_variable_table_length={self.local_variable_table_length})"
