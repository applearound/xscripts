from dataclasses import dataclass
from functools import cached_property

from .attribute_info import AttributeInfo


class LocalVariableTableAttributeInfo(AttributeInfo):
    """ Represents a local variable table attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.13

    LocalVariableTable_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u2 local_variable_table_length;
        {   u2 start_pc;
            u2 length;
            u2 name_index;
            u2 descriptor_index;
            u2 index;
        } local_variable_table[local_variable_table_length];
    }
    """

    @dataclass(frozen=True)
    class LocalVariable:
        start_pc: int
        length: int
        name_index: int
        descriptor_index: int
        index: int

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def local_variable_table_length(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def local_variable_table(self) -> tuple[LocalVariable, ...]:
        start = 8
        end = start + self.local_variable_table_length * 10
        return tuple(
            self.LocalVariable(
                start_pc=self.parse_int(self.raw[i:i + 2]),
                length=self.parse_int(self.raw[i + 2:i + 4]),
                name_index=self.parse_int(self.raw[i + 4:i + 6]),
                descriptor_index=self.parse_int(self.raw[i + 6:i + 8]),
                index=self.parse_int(self.raw[i + 8:i + 10])
            )
            for i in range(start, end, 10)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"local_variable_table_length={self.local_variable_table_length}, local_variable_table={self.local_variable_table})"
