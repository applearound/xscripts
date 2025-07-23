from typing import Iterable

from .attribute_info import AttributeInfo


class CodeAttributeInfo(AttributeInfo):
    """ Represents a code attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.3

    Code_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 max_stack;
        u2 max_locals;
        u4 code_length;
        u1 code[code_length];
        u2 exception_table_length;
        {   u2 start_pc;
            u2 end_pc;
            u2 handler_pc;
            u2 catch_type;
        } exception_table[exception_table_length];
        u2 attributes_count;
        attribute_info attributes[attributes_count];
    }
    """

    class Exception(Exception):
        def __init__(self, start_pc: int, end_pc: int, handler_pc: int, catch_type: int) -> None:
            self.start_pc: int = start_pc
            self.end_pc: int = end_pc
            self.handler_pc: int = handler_pc
            self.catch_type: int = catch_type

        def __repr__(self) -> str:
            return f"Exception(start_pc={self.start_pc}, end_pc={self.end_pc}, handler_pc={self.handler_pc}, catch_type={self.catch_type})"

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int,
                 max_stack: int, max_locals: int, code_length: int, code: bytes, exception_table_length: int,
                 exception_table: Iterable[Exception], attributes_count: int,
                 attribute_info: Iterable[AttributeInfo]) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.max_stack: int = max_stack
        self.max_locals: int = max_locals
        self.code_length: int = code_length
        self.code: bytes = code
        self.exception_table_length: int = exception_table_length
        self.exception_table: tuple[Exception, ...] = tuple(exception_table)
        self.attributes_count: int = attributes_count
        self.attributes: tuple[AttributeInfo, ...] = tuple(attribute_info)

    def get_max_stack(self) -> int:
        return self.max_stack

    def get_max_locals(self) -> int:
        return self.max_locals

    def get_code_length(self) -> int:
        return self.code_length

    def get_code(self) -> bytes:
        return self.code

    def get_exception_table_length(self) -> int:
        return self.exception_table_length

    def get_exception_table(self) -> Iterable[Exception]:
        return self.exception_table

    def get_attributes_count(self) -> int:
        return self.attributes_count

    def get_attributes(self) -> Iterable[AttributeInfo]:
        """Get the attributes of the code attribute."""
        return self.attributes

    def __repr__(self) -> str:
        return f"CodeAttributeInfo(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"max_stack={self.max_stack}, max_locals={self.max_locals}, code_length={self.code_length}, " \
               f"exception_table_length={self.exception_table_length}, attributes_count={self.attributes_count})"
