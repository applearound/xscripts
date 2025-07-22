from .attribute import Attribute


class CodeAttribute(Attribute):
    """ Represents a code attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.3
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.max_stack: int = self.parse_int(self.raw[6:8])
        self.max_locals: int = self.parse_int(self.raw[8:10])
        self.code_length: int = self.parse_int(self.raw[10:14])
        self.code: bytes = self.raw[14:14 + self.code_length]
        self.exception_table_length: int = self.parse_int(self.raw[14 + self.code_length:16 + self.code_length])
        self.exception_table: bytes = self.raw[16 + self.code_length:]
        self.attributes_count: int = self.parse_int(self.raw[16 + self.code_length + self.exception_table_length:
                                                             18 + self.code_length + self.exception_table_length])
        self.attributes: tuple[Attribute, ...]

    def get_max_stack(self) -> int:
        return self.max_stack

    def get_max_locals(self) -> int:
        return self.max_locals

    def get_code_length(self) -> int:
        return self.code_length

    def get_code(self) -> bytes:
        return self.code

    def __repr__(self) -> str:
        return f"CodeAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"max_stack={self.max_stack}, max_locals={self.max_locals}, code_length={self.code_length})"
