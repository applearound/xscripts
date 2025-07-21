from dataclasses import dataclass
from typing import Iterable

from .enums import AccessFlags
from .constant_pool import dump_bytes, ConstantPool, ConstantPoolInfo
from .utils import parse_int


@dataclass
class JavaClass:
    """Java class representation.
    ClassFile {
        u4             magic;
        u2             minor_version;
        u2             major_version;
        u2             constant_pool_count;
        cp_info        constant_pool[constant_pool_count-1];
        u2             access_flags;
        u2             this_class;
        u2             super_class;
        u2             interfaces_count;
        u2             interfaces[interfaces_count];
        u2             fields_count;
        field_info     fields[fields_count];
        u2             methods_count;
        method_info    methods[methods_count];
        u2             attributes_count;
        attribute_info attributes[attributes_count];
    }
    """
    magic_segment: bytes
    minor_version_segment: bytes
    major_version_segment: bytes
    constant_pool_count_segment: bytes
    constant_pool_segment: bytes
    access_flags_segment: bytes
    this_class_segment: bytes
    super_class_segment: bytes
    interfaces_count_segment: bytes
    interfaces_segment: bytes
    fields_count_segment: bytes
    fields_info_segment: bytes
    methods_count_segment: bytes
    methods_info_segment: bytes
    attributes_count_segment: bytes
    attributes_info_segment: bytes

    @staticmethod
    def interfaces_dump_bytes(count: int, interfaces_segment: bytes, constant_pool: ConstantPool) -> tuple[str, ...]:
        interfaces = []
        for i in range(count):
            class_info_segment = interfaces_segment[i * 3:i * 3 + 3]
            name_index = parse_int(class_info_segment[1:3])
            utf8_info = constant_pool.get_utf8_constant_pool_info(name_index)
            interfaces.append(utf8_info.string)

        return tuple(interfaces)

    def __post_init__(self):
        self.magic: str = self.magic_segment.hex().upper()
        self.minor_version: int = parse_int(self.minor_version_segment)
        self.major_version: int = parse_int(self.major_version_segment)
        self.constant_pool_count: int = parse_int(self.constant_pool_count_segment)
        self.constant_pool: ConstantPool = dump_bytes(self.constant_pool_segment)
        self.access_flags: int = parse_int(self.access_flags_segment)
        self.this_class: int = parse_int(self.this_class_segment)
        self.super_class: int = parse_int(self.super_class_segment)
        self.interfaces_count: int = parse_int(self.interfaces_count_segment)
        self.interfaces: tuple[str, ...] = JavaClass.interfaces_dump_bytes(self.interfaces_count,
                                                                           self.interfaces_segment,
                                                                           self.constant_pool)
        self.fields_count = parse_int(self.fields_count_segment)

    def get_magic(self) -> str:
        """Get the magic number of the Java class."""
        return self.magic

    def get_minor_version(self) -> int:
        """Get the minor version of the Java class."""
        return self.minor_version

    def get_major_version(self) -> int:
        """Get the major version of the Java class."""
        return self.major_version

    def get_constant_pool_count(self) -> int:
        """Get the count of the constant pool entries."""
        return self.constant_pool_count

    def constant_pool_info(self) -> Iterable[ConstantPoolInfo]:
        return iter(self.constant_pool)

    def get_access_flags(self) -> tuple[AccessFlags, ...]:
        """Get the access flags of the Java class."""
        return AccessFlags.parse_flags(self.access_flags)

    def get_class_name(self) -> str:
        """Get the name of the class."""
        class_info = self.constant_pool.get_class_constant_pool_info(self.this_class)
        utf8_info = self.constant_pool.get_utf8_constant_pool_info(class_info.name_index)

        return utf8_info.string

    def get_super_class_name(self) -> str:
        """Get the name of the superclass."""
        super_class_info = self.constant_pool.get_class_constant_pool_info(self.super_class)
        utf8_info = self.constant_pool.get_utf8_constant_pool_info(super_class_info.name_index)

        return utf8_info.string

    def get_interfaces_count(self) -> int:
        """Get the count of interfaces implemented by the class."""
        return self.interfaces_count

    def get_interfaces(self) -> tuple[str, ...]:
        """Get the names of interfaces implemented by the class."""
