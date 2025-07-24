from dataclasses import dataclass
from functools import cached_property
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

    @dataclass(frozen=True)
    class Exception:
        start_pc: int
        end_pc: int
        handler_pc: int
        catch_type: int

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def max_stack(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def max_locals(self) -> int:
        return self.parse_int(self.raw[8:10])

    @cached_property
    def code_length(self) -> int:
        return self.parse_int(self.raw[10:14])

    @cached_property
    def code(self) -> bytes:
        return self.raw[14:14 + self.code_length]

    @cached_property
    def exception_table_length(self) -> int:
        return self.parse_int(self.raw[14 + self.code_length:16 + self.code_length])

    @cached_property
    def exception_table(self) -> tuple[Exception, ...]:
        """Get the exception table of the code attribute."""
        start = 16 + self.code_length
        end = start + self.exception_table_length * 8
        return tuple(
            self.Exception(
                start_pc=self.parse_int(self.raw[i:i + 2]),
                end_pc=self.parse_int(self.raw[i + 2:i + 4]),
                handler_pc=self.parse_int(self.raw[i + 4:i + 6]),
                catch_type=self.parse_int(self.raw[i + 6:i + 8])
            )
            for i in range(start, end, 8)
        )

    @cached_property
    def attributes_count(self) -> int:
        return self.parse_int(self.raw[
                              16 + self.code_length + self.exception_table_length * 8:18 + self.code_length + self.exception_table_length * 8])

    @cached_property
    def get_attributes(self) -> Iterable[AttributeInfo]:
        """Get the attributes of the code attribute."""
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"max_stack={self.max_stack}, max_locals={self.max_locals}, code_length={self.code_length}, " \
               f"exception_table_length={self.exception_table_length}, attributes_count={self.attributes_count})"
