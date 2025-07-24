from dataclasses import dataclass
from functools import cached_property

from .attribute_info import AttributeInfo


class ModuleAttributeInfo(AttributeInfo):
    """ Represents a module attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.25

    Module_attribute {
        u2 attribute_name_index;
        u4 attribute_length;

        u2 module_name_index;
        u2 module_flags;
        u2 module_version_index;

        u2 requires_count;
        {   u2 requires_index;
            u2 requires_flags;
            u2 requires_version_index;
        } requires[requires_count];

        u2 exports_count;
        {   u2 exports_index;
            u2 exports_flags;
            u2 exports_to_count;
            u2 exports_to_index[exports_to_count];
        } exports[exports_count];

        u2 opens_count;
        {   u2 opens_index;
            u2 opens_flags;
            u2 opens_to_count;
            u2 opens_to_index[opens_to_count];
        } opens[opens_count];

        u2 uses_count;
        u2 uses_index[uses_count];

        u2 provides_count;
        {   u2 provides_index;
            u2 provides_with_count;
            u2 provides_with_index[provides_with_count];
        } provides[provides_count];
    }
    """

    @dataclass(frozen=True)
    class Require:
        requires_index: int
        requires_flags: int
        requires_version_index: int

    @dataclass(frozen=True)
    class Export:
        exports_index: int
        exports_flags: int
        exports_to_count: int
        exports_to_index: tuple[int, ...]

    @dataclass(frozen=True)
    class Open:
        opens_index: int
        opens_flags: int
        opens_to_count: int
        opens_to_index: tuple[int, ...]

    @dataclass(frozen=True)
    class Provides:
        provides_index: int
        provides_with_count: int
        provides_with_index: tuple[int, ...]

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def module_name_index(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def module_flags(self) -> int:
        return self.parse_int(self.raw[8:10])

    @cached_property
    def module_version_index(self) -> int:
        return self.parse_int(self.raw[10:12])

    @cached_property
    def number_of_exports(self) -> int:
        return self.parse_int(self.raw[12:14])

    @cached_property
    def exports(self) -> tuple[Export, ...]:
        """ Parses the exports from the raw bytes. """
        start = 14
        exports = []
        for _ in range(self.number_of_exports):
            exports_index = self.parse_int(self.raw[start:start + 2])
            exports_flags = self.parse_int(self.raw[start + 2:start + 4])
            exports_to_count = self.parse_int(self.raw[start + 4:start + 6])
            exports_to_index = tuple(
                self.parse_int(self.raw[start + 6 + i:start + 8 + i]) for i in range(0, exports_to_count * 2, 2)
            )
            exports.append(self.Export(exports_index, exports_flags, exports_to_count, exports_to_index))
            start += 6 + exports_to_count * 2
        return tuple(exports)

    @cached_property
    def number_of_opens(self) -> int:
        start = 14 + sum(6 + export.exports_to_count * 2 for export in self.exports)
        return self.parse_int(self.raw[start:start + 2])

    @cached_property
    def opens(self) -> tuple[Open, ...]:
        """ Parses the opens from the raw bytes. """
        start = 14 + sum(6 + export.exports_to_count * 2 for export in self.exports) + 2
        opens = []
        for _ in range(self.number_of_opens):
            opens_index = self.parse_int(self.raw[start:start + 2])
            opens_flags = self.parse_int(self.raw[start + 2:start + 4])
            opens_to_count = self.parse_int(self.raw[start + 4:start + 6])
            opens_to_index = tuple(
                self.parse_int(self.raw[start + 6 + i:start + 8 + i]) for i in range(0, opens_to_count * 2, 2)
            )
            opens.append(self.Open(opens_index, opens_flags, opens_to_count, opens_to_index))
            start += 6 + opens_to_count * 2
        return tuple(opens)

    @cached_property
    def number_of_uses(self) -> int:
        start = 14 + sum(6 + export.exports_to_count * 2 for export in self.exports) + 2 + \
                sum(6 + open.opens_to_count * 2 for open in self.opens)
        return self.parse_int(self.raw[start:start + 2])

    @cached_property
    def uses(self) -> tuple[int, ...]:
        """ Parses the uses from the raw bytes. """
        start = 14 + sum(6 + export.exports_to_count * 2 for export in self.exports) + 2 + \
                sum(6 + open.opens_to_count * 2 for open in self.opens) + 2
        return tuple(self.parse_int(self.raw[start + i:start + i + 2]) for i in range(0, self.number_of_uses * 2, 2))

    @cached_property
    def number_of_provides(self) -> int:
        start = 14 + sum(6 + export.exports_to_count * 2 for export in self.exports) + 2 + \
                sum(6 + open.opens_to_count * 2 for open in self.opens) + 2 + \
                self.number_of_uses * 2
        return self.parse_int(self.raw[start:start + 2])

    @cached_property
    def provides(self) -> tuple[Provides, ...]:
        """ Parses the provides from the raw bytes. """
        start = 14 + sum(6 + export.exports_to_count * 2 for export in self.exports) + 2 + \
                sum(6 + _open.opens_to_count * 2 for _open in self.opens) + 2 + \
                self.number_of_uses * 2 + 2
        provides = []
        for _ in range(self.number_of_provides):
            provides_index = self.parse_int(self.raw[start:start + 2])
            provides_with_count = self.parse_int(self.raw[start + 2:start + 4])
            provides_with_index = tuple(
                self.parse_int(self.raw[start + 4 + i:start + 6 + i]) for i in range(0, provides_with_count * 2, 2)
            )
            provides.append(self.Provides(provides_index, provides_with_count, provides_with_index))
            start += 4 + provides_with_count * 2
        return tuple(provides)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"module_name_index={self.module_name_index}, module_flags={self.module_flags}, " \
               f"module_version_index={self.module_version_index}, number_of_exports={self.number_of_exports}, " \
               f"exports={self.exports}, number_of_opens={self.number_of_opens}, opens={self.opens}, " \
               f"number_of_uses={self.number_of_uses}, uses={self.uses}, " \
               f"number_of_provides={self.number_of_provides}, provides={self.provides})"
