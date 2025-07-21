from struct import unpack
from dataclasses import dataclass, field
from io import BytesIO
from typing import Iterable

from .enums import ConstantPoolInfoTags
from .utils import parse_int


@dataclass
class ConstantPoolInfo:
    tag_segment: bytes
    info_segment: bytes

    def __post_init__(self) -> None:
        self.tag: int = int.from_bytes(self.tag_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(tag={self.tag})"


@dataclass
class ClassConstantPoolInfo(ConstantPoolInfo):
    name_index_segment: bytes = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        self.name_index_segment = self.info_segment
        self.name_index: int = int.from_bytes(self.name_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(name_index={self.name_index})"


@dataclass
class FieldRefConstantPoolInfo(ConstantPoolInfo):
    class_index_segment: bytes = field(init=False)
    name_and_type_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.class_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.class_index: int = int.from_bytes(self.class_index_segment, byteorder='big', signed=False)
        self.name_and_type_index: int = int.from_bytes(self.name_and_type_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(class_index={self.class_index}, name_and_type_index={self.name_and_type_index})"


@dataclass
class MethodRefConstantPoolInfo(ConstantPoolInfo):
    class_index_segment: bytes = field(init=False)
    name_and_type_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.class_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.class_index: int = int.from_bytes(self.class_index_segment, byteorder='big', signed=False)
        self.name_and_type_index: int = int.from_bytes(self.name_and_type_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(class_index={self.class_index}, name_and_type_index={self.name_and_type_index})"


@dataclass
class InterfaceRefConstantPoolInfo(ConstantPoolInfo):
    class_index_segment: bytes = field(init=False)
    name_and_type_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.class_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.class_index: int = int.from_bytes(self.class_index_segment, byteorder='big', signed=False)
        self.name_and_type_index: int = int.from_bytes(self.name_and_type_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(class_index={self.class_index}, name_and_type_index={self.name_and_type_index})"


@dataclass
class StringConstantPoolInfo(ConstantPoolInfo):
    string_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.string_index_segment = self.info_segment

        self.string_index: int = int.from_bytes(self.string_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(string_index={self.string_index})"


@dataclass
class IntegerConstantPoolInfo(ConstantPoolInfo):
    bytes_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.bytes_segment = self.info_segment

        self.value: int = int.from_bytes(self.bytes_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"


@dataclass
class FloatConstantPoolInfo(ConstantPoolInfo):
    bytes_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.bytes_segment = self.info_segment

        self.value: float = unpack('>f', self.bytes_segment)[0]

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"


@dataclass
class LongConstantPoolInfo(ConstantPoolInfo):
    high_bytes_segment: bytes = field(init=False)
    low_bytes_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.high_bytes_segment = self.info_segment[:4]
        self.low_bytes_segment = self.info_segment[4:]

        self.value: int = (
                (int.from_bytes(self.high_bytes_segment, byteorder='big', signed=False) << 32) |
                int.from_bytes(self.low_bytes_segment, byteorder='big', signed=False)
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"


@dataclass
class DoubleConstantPoolInfo(ConstantPoolInfo):
    high_bytes_segment: bytes = field(init=False)
    low_bytes_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.high_bytes_segment = self.info_segment[:4]
        self.low_bytes_segment = self.info_segment[4:]

        self.value: float = unpack('>d', self.high_bytes_segment + self.low_bytes_segment)[0]

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"


@dataclass
class NameAndTypeConstantPoolInfo(ConstantPoolInfo):
    name_index_segment: bytes = field(init=False)
    descriptor_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.name_index_segment = self.info_segment[:2]
        self.descriptor_index_segment = self.info_segment[2:]

        self.name_index: int = int.from_bytes(self.name_index_segment, byteorder='big', signed=False)
        self.descriptor_index: int = int.from_bytes(self.descriptor_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(name_index={self.name_index}, descriptor_index={self.descriptor_index})"


@dataclass
class Utf8ConstantPoolInfo(ConstantPoolInfo):
    length_segment: bytes = field(init=False)
    bytes_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.length_segment = self.info_segment[:2]
        self.bytes_segment = self.info_segment[2:]

        self.length: int = int.from_bytes(self.length_segment, byteorder='big', signed=False)
        self.string: str = self.bytes_segment.decode('UTF-8')

    def __repr__(self):
        return f"{self.__class__.__name__}(length={self.length}, string='{self.string}')"


@dataclass
class MethodHandleConstantPoolInfo(ConstantPoolInfo):
    reference_kind_segment: bytes = field(init=False)
    reference_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.reference_kind_segment = self.info_segment[:1]
        self.reference_index_segment = self.info_segment[1:]

        self.reference_kind: int = int.from_bytes(self.reference_kind_segment, byteorder='big', signed=False)
        self.reference_index: int = int.from_bytes(self.reference_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(reference_kind={self.reference_kind}, reference_index={self.reference_index})"


@dataclass
class DynamicConstantPoolInfo(ConstantPoolInfo):
    bootstrap_method_attr_index_segment: bytes = field(init=False)
    name_and_type_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.bootstrap_method_attr_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.bootstrap_method_attr_index: int = int.from_bytes(self.bootstrap_method_attr_index_segment,
                                                               byteorder='big', signed=False)
        self.name_and_type_index: int = int.from_bytes(self.name_and_type_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(bootstrap_method_attr_index={self.bootstrap_method_attr_index}, name_and_type_index={self.name_and_type_index})"


@dataclass
class InvokeDynamicConstantPoolInfo(ConstantPoolInfo):
    bootstrap_method_attr_index_segment: bytes = field(init=False)
    name_and_type_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.bootstrap_method_attr_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.bootstrap_method_attr_index: int = int.from_bytes(self.bootstrap_method_attr_index_segment,
                                                               byteorder='big', signed=False)
        self.name_and_type_index: int = int.from_bytes(self.name_and_type_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(bootstrap_method_attr_index={self.bootstrap_method_attr_index}, name_and_type_index={self.name_and_type_index})"


@dataclass
class ModuleConstantPoolInfo(ConstantPoolInfo):
    name_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.name_index_segment = self.info_segment

        self.name_index: int = int.from_bytes(self.name_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(name_index={self.name_index})"


@dataclass
class PackageConstantPoolInfo(ConstantPoolInfo):
    name_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.name_index_segment = self.info_segment

        self.name_index: int = int.from_bytes(self.name_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(name_index={self.name_index})"


@dataclass
class MethodTypeConstantPoolInfo(ConstantPoolInfo):
    descriptor_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.descriptor_index_segment = self.info_segment

        self.descriptor_index: int = int.from_bytes(self.descriptor_index_segment, byteorder='big', signed=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(descriptor_index={self.descriptor_index})"


class ConstantPool:
    """CONSTANT_Class 	7
        CONSTANT_Fieldref 	9
        CONSTANT_Methodref 	10
        CONSTANT_InterfaceMethodref 	11
        CONSTANT_String 	8
        CONSTANT_Integer 	3
        CONSTANT_Float 	4
        CONSTANT_Long 	5
        CONSTANT_Double 	6
        CONSTANT_NameAndType 	12
        CONSTANT_Utf8 	1
        CONSTANT_MethodHandle 	15
        CONSTANT_MethodType 	16
        CONSTANT_Dynamic 	17
        CONSTANT_InvokeDynamic 	18
        CONSTANT_Module 	19
        CONSTANT_Package 	20
    """

    def __init__(self, pool: Iterable[ConstantPoolInfo]) -> None:
        self.pool: dict[int, ConstantPoolInfo] = dict()

        index = 1
        for info in pool:
            self.pool[index] = info
            if isinstance(info, LongConstantPoolInfo) or isinstance(info, DoubleConstantPoolInfo):
                self.pool[index + 1] = info
                index += 2
            else:
                index += 1

    def __iter__(self):
        """Iterate over the constant pool entries."""
        return iter(self.pool.values())

    def get(self, index: int) -> ConstantPoolInfo:
        """Get a constant pool entry by its index.
        Attention: The constant_pool table is indexed from 1 to constant_pool_count - 1.
        """
        if index < 1 or index > len(self.pool):
            raise IndexError(
                f"Constant pool index {index} out of range. Valid range is 1 to {len(self.pool)}.")
        return self.pool[index]

    def get_class_constant_pool_info(self, index: int) -> ClassConstantPoolInfo:
        """Get a ClassConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, ClassConstantPoolInfo):
            raise TypeError(f"Expected ClassConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_field_ref_constant_pool_info(self, index: int) -> FieldRefConstantPoolInfo:
        """Get a FieldRefConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, FieldRefConstantPoolInfo):
            raise TypeError(f"Expected FieldRefConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_method_ref_constant_pool_info(self, index: int) -> MethodRefConstantPoolInfo:
        """Get a MethodRefConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, MethodRefConstantPoolInfo):
            raise TypeError(f"Expected MethodRefConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_interface_ref_constant_pool_info(self, index: int) -> InterfaceRefConstantPoolInfo:
        """Get a InterfaceRefConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, InterfaceRefConstantPoolInfo):
            raise TypeError(f"Expected InterfaceRefConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_string_constant_pool_info(self, index: int) -> StringConstantPoolInfo:
        """Get a StringConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, StringConstantPoolInfo):
            raise TypeError(f"Expected StringConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_integer_constant_pool_info(self, index: int) -> IntegerConstantPoolInfo:
        """Get a IntegerConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, IntegerConstantPoolInfo):
            raise TypeError(f"Expected IntegerConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_float_constant_pool_info(self, index: int) -> FloatConstantPoolInfo:
        """Get a FloatConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, FloatConstantPoolInfo):
            raise TypeError(f"Expected FloatConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_long_constant_pool_info(self, index: int) -> LongConstantPoolInfo:
        """Get a LongConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, LongConstantPoolInfo):
            raise TypeError(f"Expected LongConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_double_constant_pool_info(self, index: int) -> DoubleConstantPoolInfo:
        info = self.get(index)
        if not isinstance(info, DoubleConstantPoolInfo):
            raise TypeError(f"Expected DoubleConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_name_and_type_constant_pool_info(self, index: int) -> NameAndTypeConstantPoolInfo:
        """Get a NameAndTypeConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, NameAndTypeConstantPoolInfo):
            raise TypeError(f"Expected NameAndTypeConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_utf8_constant_pool_info(self, index: int) -> Utf8ConstantPoolInfo:
        """Get a Utf8ConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, Utf8ConstantPoolInfo):
            raise TypeError(f"Expected Utf8ConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_method_handle_constant_pool_info(self, index: int) -> MethodHandleConstantPoolInfo:
        """Get a MethodHandleConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, MethodHandleConstantPoolInfo):
            raise TypeError(f"Expected MethodHandleConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_method_type_constant_pool_info(self, index: int) -> MethodTypeConstantPoolInfo:
        """Get a MethodTypeConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, MethodTypeConstantPoolInfo):
            raise TypeError(f"Expected MethodTypeConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_dynamic_constant_pool_info(self, index: int) -> DynamicConstantPoolInfo:
        """Get a DynamicConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, DynamicConstantPoolInfo):
            raise TypeError(f"Expected DynamicConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_invoke_dynamic_constant_pool_info(self, index: int) -> InvokeDynamicConstantPoolInfo:
        """Get a InvokeDynamicConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, InvokeDynamicConstantPoolInfo):
            raise TypeError(f"Expected InvokeDynamicConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_package_constant_pool_info(self, index: int) -> PackageConstantPoolInfo:
        """Get a PackageConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, PackageConstantPoolInfo):
            raise TypeError(f"Expected PackageConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info

    def get_module_constant_pool_info(self, index: int) -> ModuleConstantPoolInfo:
        """Get a ModuleConstantPoolInfo by its index."""
        info = self.get(index)
        if not isinstance(info, ModuleConstantPoolInfo):
            raise TypeError(f"Expected ModuleConstantPoolInfo at index {index}, got {type(info).__name__}.")
        return info


def dump_bytes(constant_pool_segment: bytes) -> ConstantPool:
    """Resolve the constant pool segment into a list of constant pool entries."""
    constant_pool = []

    with BytesIO(constant_pool_segment) as segment_io:
        processing = True

        while processing:
            tag_segment = segment_io.read(1)

            if not tag_segment:
                processing = False
                continue

            tag = ConstantPoolInfoTags(parse_int(tag_segment))

            if tag is ConstantPoolInfoTags.UTF8:
                # For UTF8, we need to read the length first
                utf8_length_segment = segment_io.read(2)
                utf8_length = parse_int(utf8_length_segment)
                info_segment = utf8_length_segment + segment_io.read(utf8_length)

                constant_pool.append(Utf8ConstantPoolInfo(tag_segment, info_segment))
            else:
                info_segment = segment_io.read(tag.get_size() - 1)

                if tag is ConstantPoolInfoTags.CLASS:
                    constant_pool.append(ClassConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.FIELDREF:
                    constant_pool.append(FieldRefConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.METHODREF:
                    constant_pool.append(MethodRefConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.INTERFACE_METHODREF:
                    constant_pool.append(InterfaceRefConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.STRING:
                    constant_pool.append(StringConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.INTEGER:
                    constant_pool.append(IntegerConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.FLOAT:
                    constant_pool.append(FloatConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.LONG:
                    constant_pool.append(LongConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.DOUBLE:
                    constant_pool.append(DoubleConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.NAME_AND_TYPE:
                    constant_pool.append(NameAndTypeConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.METHOD_HANDLE:
                    constant_pool.append(MethodHandleConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.METHOD_TYPE:
                    constant_pool.append(MethodTypeConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.DYNAMIC:
                    constant_pool.append(DynamicConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.INVOKE_DYNAMIC:
                    constant_pool.append(InvokeDynamicConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.MODULE:
                    constant_pool.append(ModuleConstantPoolInfo(tag_segment, info_segment))
                elif tag is ConstantPoolInfoTags.PACKAGE:
                    constant_pool.append(PackageConstantPoolInfo(tag_segment, info_segment))
                else:
                    raise ValueError(f"Unknown constant pool tag: {tag}")

    return ConstantPool(constant_pool)
