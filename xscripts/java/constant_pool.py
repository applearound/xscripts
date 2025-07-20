from struct import unpack
from dataclasses import dataclass, field


@dataclass
class ConstantPoolInfo:
    tag_segment: bytes
    info_segment: bytes

    def __post_init__(self) -> None:
        self.tag: int = int.from_bytes(self.tag_segment, byteorder='big', signed=False)


@dataclass
class ClassConstantPoolInfo(ConstantPoolInfo):
    name_index_segment: bytes = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        self.name_index_segment = self.info_segment
        self.name_index: int = int.from_bytes(self.name_index_segment, byteorder='big', signed=False)


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


@dataclass
class StringConstantPoolInfo(ConstantPoolInfo):
    string_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.string_index_segment = self.info_segment

        self.string_index: int = int.from_bytes(self.string_index_segment, byteorder='big', signed=False)


@dataclass
class IntegerConstantPoolInfo(ConstantPoolInfo):
    bytes_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.bytes_segment = self.info_segment

        self.value: int = int.from_bytes(self.bytes_segment, byteorder='big', signed=False)


@dataclass
class FloatConstantPoolInfo(ConstantPoolInfo):
    bytes_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.bytes_segment = self.info_segment

        self.value: float = unpack('>f', self.bytes_segment)[0]


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


@dataclass
class DoubleConstantPoolInfo(ConstantPoolInfo):
    high_bytes_segment: bytes = field(init=False)
    low_bytes_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.high_bytes_segment = self.info_segment[:4]
        self.low_bytes_segment = self.info_segment[4:]

        self.value: float = unpack('>d', self.high_bytes_segment + self.low_bytes_segment)[0]


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


@dataclass
class ModuleConstantPoolInfo(ConstantPoolInfo):
    name_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.name_index_segment = self.info_segment

        self.name_index: int = int.from_bytes(self.name_index_segment, byteorder='big', signed=False)


@dataclass
class PackageConstantPoolInfo(ConstantPoolInfo):
    name_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.name_index_segment = self.info_segment

        self.name_index: int = int.from_bytes(self.name_index_segment, byteorder='big', signed=False)


@dataclass
class MethodTypeConstantPoolInfo(ConstantPoolInfo):
    descriptor_index_segment: bytes = field(init=False)

    def __post_init__(self):
        super().__post_init__()

        self.descriptor_index_segment = self.info_segment

        self.descriptor_index: int = int.from_bytes(self.descriptor_index_segment, byteorder='big', signed=False)
