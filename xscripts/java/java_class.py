from dataclasses import dataclass
from io import BytesIO, BufferedReader

from .enums import ConstantPoolInfoTag
from .constant_pool import *


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
    def parse_int(segment: bytes) -> int:
        return int.from_bytes(segment, byteorder='big', signed=False)

    @staticmethod
    def __resolve_constant_pool(constant_pool_segment: bytes) -> list[ConstantPoolInfo]:
        """Resolve the constant pool segment into a list of constant pool entries."""
        constant_pool = []

        with BytesIO(constant_pool_segment) as segment_io:
            processing = True

            while processing:
                tag_segment = segment_io.read(1)

                if not tag_segment:
                    processing = False
                    continue

                tag = ConstantPoolInfoTag(JavaClass.parse_int(tag_segment))

                if tag is ConstantPoolInfoTag.UTF8:
                    # For UTF8, we need to read the length first
                    utf8_length_segment = segment_io.read(2)
                    utf8_length = JavaClass.parse_int(utf8_length_segment)
                    info_segment = utf8_length_segment + segment_io.read(utf8_length)

                    constant_pool.append(Utf8ConstantPoolInfo(tag_segment, info_segment))
                else:
                    info_segment = segment_io.read(tag.get_size() - 1)

                    if tag is ConstantPoolInfoTag.CLASS:
                        constant_pool.append(ClassConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.FIELDREF:
                        constant_pool.append(FieldRefConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.METHODREF:
                        constant_pool.append(MethodRefConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.INTERFACE_METHODREF:
                        constant_pool.append(InterfaceRefConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.STRING:
                        constant_pool.append(StringConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.INTEGER:
                        constant_pool.append(IntegerConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.FLOAT:
                        constant_pool.append(FloatConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.LONG:
                        constant_pool.append(LongConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.DOUBLE:
                        constant_pool.append(DoubleConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.NAME_AND_TYPE:
                        constant_pool.append(NameAndTypeConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.METHOD_HANDLE:
                        constant_pool.append(MethodHandleConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.METHOD_TYPE:
                        constant_pool.append(MethodTypeConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.DYNAMIC:
                        constant_pool.append(DynamicConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.INVOKE_DYNAMIC:
                        constant_pool.append(InvokeDynamicConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.MODULE:
                        constant_pool.append(ModuleConstantPoolInfo(tag_segment, info_segment))
                    elif tag is ConstantPoolInfoTag.PACKAGE:
                        constant_pool.append(PackageConstantPoolInfo(tag_segment, info_segment))
                    else:
                        raise ValueError(f"Unknown constant pool tag: {tag}")

        return constant_pool

    def __post_init__(self):
        self.magic: str = self.magic_segment.hex().upper()
        self.minor_version: int = self.parse_int(self.minor_version_segment)
        self.major_version: int = self.parse_int(self.major_version_segment)
        self.constant_pool_count: int = self.parse_int(self.constant_pool_count_segment)
        self.constant_pool: list[ConstantPoolInfo] = self.__resolve_constant_pool(self.constant_pool_segment)

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
