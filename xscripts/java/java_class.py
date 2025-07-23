from typing import Iterable

from .attributes import dump_bytes as dump_attributes_bytes, AttributeInfo
from .constant_pool import ConstantPoolFactory, ConstantPool, ConstantPoolInfo
from .enums import ClassAccessFlags
from .fields import dump_bytes as dump_fields_bytes, Field
from .methods import Method, dump_bytes as dump_methods_bytes
from .pipeline import ChunkedJavaClass
from .utils import parse_int


class JavaClass:
    """ Java class representation.

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

    @staticmethod
    def parse_int(segment: bytes) -> int:
        return int.from_bytes(segment, byteorder='big', signed=False)

    def __init__(self, java_class: ChunkedJavaClass) -> None:
        self.chunked_java_class: ChunkedJavaClass = java_class

        self.magic: str = self.chunked_java_class.magic_segment.hex().upper()
        self.minor_version: int = self.parse_int(self.chunked_java_class.minor_version_segment)
        self.major_version: int = self.parse_int(self.chunked_java_class.major_version_segment)
        self.constant_pool_count: int = self.parse_int(self.chunked_java_class.constant_pool_count_segment)
        self.constant_pool: ConstantPool = ConstantPoolFactory.make_constant_pool(
            self.chunked_java_class.constant_pool_segment)
        self.access_flags: int = self.parse_int(self.chunked_java_class.access_flags_segment)
        self.this_class: int = self.parse_int(self.chunked_java_class.this_class_segment)
        self.super_class: int = self.parse_int(self.chunked_java_class.super_class_segment)
        self.interfaces_count: int = self.parse_int(self.chunked_java_class.interfaces_count_segment)
        self.interfaces: tuple[str, ...] = JavaClass.interfaces_dump_bytes(self.interfaces_count,
                                                                           self.chunked_java_class.interfaces_segment,
                                                                           self.constant_pool)
        self.fields_count: int = self.parse_int(self.chunked_java_class.fields_count_segment)
        self.fields: tuple[Field, ...] = tuple(
            dump_fields_bytes(self.fields_count, self.chunked_java_class.fields_info_segment, self.constant_pool))
        self.methods_count: int = self.parse_int(self.chunked_java_class.methods_count_segment)
        self.methods: tuple[Method, ...] = tuple(
            dump_methods_bytes(self.methods_count, self.chunked_java_class.methods_info_segment, self.constant_pool))
        self.attributes_count: int = self.parse_int(self.chunked_java_class.attributes_count_segment)
        self.attributes: tuple[AttributeInfo, ...] = tuple(
            dump_attributes_bytes(self.attributes_count, self.chunked_java_class.attributes_info_segment,
                                  self.constant_pool))

    @staticmethod
    def interfaces_dump_bytes(count: int, interfaces_segment: bytes, constant_pool: ConstantPool) -> tuple[str, ...]:
        interfaces = []
        for i in range(count):
            index_segment = interfaces_segment[i * 2:i * 2 + 2]
            name_index = parse_int(index_segment)
            class_info = constant_pool.get_class_constant_pool_info(name_index)
            utf8_info = constant_pool.get_utf8_constant_pool_info(class_info.name_index)
            interfaces.append(utf8_info.string)

        return tuple(interfaces)

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

    def get_constant_pool(self) -> Iterable[ConstantPoolInfo]:
        return self.constant_pool

    def get_access_flags(self) -> Iterable[ClassAccessFlags]:
        """Get the access flags of the Java class."""
        return ClassAccessFlags.parse_flags(self.access_flags)

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

    def get_interfaces(self) -> Iterable[str]:
        """Get the names of interfaces implemented by the class."""
        return self.interfaces

    def get_fields_count(self) -> int:
        """Get the count of fields in the class."""
        return self.fields_count

    def get_fields(self) -> Iterable[Field]:
        """Get the fields of the class."""
        return self.fields

    def get_methods_count(self) -> int:
        """Get the count of methods in the class."""
        return self.methods_count

    def get_methods(self) -> Iterable[Method]:
        """Get the methods of the class."""
        return self.methods

    def get_attributes_count(self) -> int:
        """Get the count of attributes in the class."""
        return self.attributes_count

    def get_attributes(self) -> Iterable[AttributeInfo]:
        """Get the attributes of the class."""
        return self.attributes

    def get_constant_pool_info(self, index: int) -> ConstantPoolInfo:
        """Get a specific constant pool info by index."""
        return self.constant_pool.get(index)
