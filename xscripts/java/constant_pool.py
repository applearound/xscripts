from io import BytesIO
from struct import unpack
from typing import Iterable, Iterator

from .enums import ConstantPoolInfoTags
from .utils import parse_int


class ConstantPoolInfo:
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        self.tag_segment: bytes = tag_segment
        self.info_segment: bytes = info_segment

        self.tag: int = parse_int(tag_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.tag})"


class ClassConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.name_index_segment = self.info_segment
        self.name_index: int = parse_int(self.info_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.name_index})"


class FieldRefConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.class_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.class_index: int = parse_int(self.class_index_segment)
        self.name_and_type_index: int = parse_int(self.name_and_type_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(class_index={self.class_index}, name_and_type_index={self.name_and_type_index})"


class MethodRefConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.class_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.class_index: int = parse_int(self.class_index_segment)
        self.name_and_type_index: int = parse_int(self.name_and_type_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(class_index={self.class_index}, name_and_type_index={self.name_and_type_index})"


class InterfaceRefConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.class_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.class_index: int = parse_int(self.class_index_segment)
        self.name_and_type_index: int = parse_int(self.name_and_type_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(class_index={self.class_index}, name_and_type_index={self.name_and_type_index})"


class StringConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.string_index_segment = self.info_segment

        self.string_index: int = parse_int(self.string_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(string_index={self.string_index})"


class IntegerConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.bytes_segment = self.info_segment

        self.value: int = parse_int(self.bytes_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"


class FloatConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.bytes_segment = self.info_segment

        self.value: float = unpack('>f', self.bytes_segment)[0]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"


class LongConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.high_bytes_segment = self.info_segment[:4]
        self.low_bytes_segment = self.info_segment[4:]

        self.value: int = (
                (parse_int(self.high_bytes_segment) << 32) | parse_int(self.low_bytes_segment)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"


class DoubleConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.high_bytes_segment = self.info_segment[:4]
        self.low_bytes_segment = self.info_segment[4:]

        self.value: float = unpack('>d', self.high_bytes_segment + self.low_bytes_segment)[0]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"


class NameAndTypeConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.name_index_segment = self.info_segment[:2]
        self.descriptor_index_segment = self.info_segment[2:]

        self.name_index: int = parse_int(self.name_index_segment)
        self.descriptor_index: int = parse_int(self.descriptor_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.name_index}, descriptor_index={self.descriptor_index})"


class Utf8ConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.length_segment = self.info_segment[:2]
        self.bytes_segment = self.info_segment[2:]

        self.length: int = parse_int(self.length_segment)
        self.string: str = self.bytes_segment.decode('UTF-8')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(length={self.length}, string='{self.string}')"


class MethodHandleConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.reference_kind_segment = self.info_segment[:1]
        self.reference_index_segment = self.info_segment[1:]

        self.reference_kind: int = parse_int(self.reference_kind_segment)
        self.reference_index: int = parse_int(self.reference_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(reference_kind={self.reference_kind}, reference_index={self.reference_index})"


class DynamicConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.bootstrap_method_attr_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.bootstrap_method_attr_index: int = parse_int(self.bootstrap_method_attr_index_segment)
        self.name_and_type_index: int = parse_int(self.name_and_type_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bootstrap_method_attr_index={self.bootstrap_method_attr_index}, name_and_type_index={self.name_and_type_index})"


class InvokeDynamicConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.bootstrap_method_attr_index_segment = self.info_segment[:2]
        self.name_and_type_index_segment = self.info_segment[2:]

        self.bootstrap_method_attr_index: int = parse_int(self.bootstrap_method_attr_index_segment)
        self.name_and_type_index: int = parse_int(self.name_and_type_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bootstrap_method_attr_index={self.bootstrap_method_attr_index}, name_and_type_index={self.name_and_type_index})"


class ModuleConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.name_index_segment = self.info_segment

        self.name_index: int = parse_int(self.name_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.name_index})"


class PackageConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.name_index_segment = self.info_segment
        self.name_index: int = parse_int(self.name_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.name_index})"


class MethodTypeConstantPoolInfo(ConstantPoolInfo):
    def __init__(self, tag_segment: bytes, info_segment: bytes) -> None:
        super().__init__(tag_segment, info_segment)

        self.descriptor_index_segment = self.info_segment

        self.descriptor_index: int = parse_int(self.descriptor_index_segment)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(descriptor_index={self.descriptor_index})"


class ConstantPool:
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

    def __iter__(self) -> Iterator[ConstantPoolInfo]:
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


easy_dict: dict[ConstantPoolInfoTags, type[ConstantPoolInfo]] = {
    ConstantPoolInfoTags.CLASS: ClassConstantPoolInfo,
    ConstantPoolInfoTags.FIELDREF: FieldRefConstantPoolInfo,
    ConstantPoolInfoTags.METHODREF: MethodRefConstantPoolInfo,
    ConstantPoolInfoTags.INTERFACE_METHODREF: InterfaceRefConstantPoolInfo,
    ConstantPoolInfoTags.STRING: StringConstantPoolInfo,
    ConstantPoolInfoTags.INTEGER: IntegerConstantPoolInfo,
    ConstantPoolInfoTags.FLOAT: FloatConstantPoolInfo,
    ConstantPoolInfoTags.LONG: LongConstantPoolInfo,
    ConstantPoolInfoTags.DOUBLE: DoubleConstantPoolInfo,
    ConstantPoolInfoTags.NAME_AND_TYPE: NameAndTypeConstantPoolInfo,
    ConstantPoolInfoTags.UTF8: Utf8ConstantPoolInfo,
    ConstantPoolInfoTags.METHOD_HANDLE: MethodHandleConstantPoolInfo,
    ConstantPoolInfoTags.METHOD_TYPE: MethodTypeConstantPoolInfo,
    ConstantPoolInfoTags.DYNAMIC: DynamicConstantPoolInfo,
    ConstantPoolInfoTags.INVOKE_DYNAMIC: InvokeDynamicConstantPoolInfo,
    ConstantPoolInfoTags.MODULE: ModuleConstantPoolInfo,
    ConstantPoolInfoTags.PACKAGE: PackageConstantPoolInfo,
}


def get_size(tag: ConstantPoolInfoTags) -> int:
    """ Returns the size of the constant pool entry based on its tag.

    The size is determined by the type of constant pool entry:
    - INTEGER and FLOAT: 5 bytes
    - LONG and DOUBLE: 9 bytes
    - CLASS, METHOD_TYPE, STRING, MODULE, PACKAGE: 3 bytes
    - FIELDREF, NAME_AND_TYPE, METHODREF, INTERFACE_METHODREF: 5 bytes
    - METHOD_HANDLE: 4 bytes
    - UTF8: 0 bytes (the size is variable and depends on the length of the UTF-8 string)
    - All other tags: -1 (indicating an unknown or unsupported tag)

    Returns:
        int: The size of the constant pool entry in bytes.
    """
    if tag in (ConstantPoolInfoTags.INTEGER, ConstantPoolInfoTags.FLOAT):
        return 5
    elif tag in (ConstantPoolInfoTags.LONG, ConstantPoolInfoTags.DOUBLE):
        return 9
    elif tag in (ConstantPoolInfoTags.CLASS, ConstantPoolInfoTags.METHOD_TYPE, ConstantPoolInfoTags.STRING,
                 ConstantPoolInfoTags.MODULE, ConstantPoolInfoTags.PACKAGE):
        return 3
    elif tag in (ConstantPoolInfoTags.FIELDREF, ConstantPoolInfoTags.NAME_AND_TYPE, ConstantPoolInfoTags.METHODREF,
                 ConstantPoolInfoTags.INVOKE_DYNAMIC, ConstantPoolInfoTags.INVOKE_DYNAMIC,
                 ConstantPoolInfoTags.INTERFACE_METHODREF):
        return 5
    elif tag is ConstantPoolInfoTags.METHOD_HANDLE:
        return 4
    elif tag is ConstantPoolInfoTags.UTF8:
        return 0
    else:
        return -1


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
                info_segment = segment_io.read(get_size(tag) - 1)

                constant_pool.append(easy_dict[tag](tag_segment, info_segment))

    return ConstantPool(constant_pool)
