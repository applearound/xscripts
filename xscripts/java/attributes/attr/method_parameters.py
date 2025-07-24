from dataclasses import dataclass
from functools import cached_property

from .attribute_info import AttributeInfo


class MethodParametersAttributeInfo(AttributeInfo):
    """ Represents a method parameters attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.24

    MethodParameters_attribute {
        u2 attribute_name_index;
        u4 attribute_length;
        u1 parameters_count;
        {   u2 name_index;
            u2 access_flags;
        } parameters[parameters_count];
    }
    """

    @dataclass(frozen=True)
    class Parameter:
        name_index: int
        access_flags: int

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def parameters_count(self) -> int:
        return self.parse_int(self.raw[6:7])

    @cached_property
    def parameters(self) -> tuple[Parameter, ...]:
        start = 7
        end = start + self.parameters_count * 4
        return tuple(
            self.Parameter(
                name_index=self.parse_int(self.raw[i:i + 2]),
                access_flags=self.parse_int(self.raw[i + 2:i + 4])
            )
            for i in range(start, end, 4)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"parameters_count={self.parameters_count}, parameters={self.parameters})"
