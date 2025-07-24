from dataclasses import dataclass
from functools import cached_property

from .attribute_info import AttributeInfo


class LineNumberTableAttributeInfo(AttributeInfo):
    """ Represents a line number table attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.12

    LineNumberTable_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 line_number_table_length;
        {   u2 start_pc;
            u2 line_number;
        } line_number_table[line_number_table_length];
    }
    """

    @dataclass(frozen=True)
    class LineNumber:
        start_pc: int
        line_number: int

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def line_number_table_length(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def line_number_table(self) -> tuple[LineNumber, ...]:
        start = 8
        end = start + self.line_number_table_length * 4
        return tuple(
            self.LineNumber(
                start_pc=self.parse_int(self.raw[i:i + 2]),
                line_number=self.parse_int(self.raw[i + 2:i + 4])
            )
            for i in range(start, end, 4)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"line_number_table_length={self.line_number_table_length}, line_number_table={self.line_number_table})"
