from .attribute import Attribute


class LocalVariableTypeTableAttribute(Attribute):
    """ Represents a local variable type table attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.14
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.local_variable_type_table_length: int = self.parse_int(self.raw[6:8])
        self.local_variable_type_table: bytes = self.raw[8:]

    def get_local_variable_type_table_length(self) -> int:
        return self.local_variable_type_table_length

    def get_local_variable_type_table(self) -> bytes:
        return self.local_variable_type_table

    def __repr__(self) -> str:
        return f"LocalVariableTypeTableAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"local_variable_type_table_length={self.local_variable_type_table_length})"
