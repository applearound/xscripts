from abc    import ABC
from struct import unpack
from typing import BinaryIO

def read_constant_utf8_info(class_file: BinaryIO):
    length = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    _bytes = class_file.read(length).decode('UTF-8')
    return {
        'length': length,
        'bytes': _bytes,
    }

def read_constant_integer_info(class_file: BinaryIO):
    _bytes = int.from_bytes(class_file.read(4), byteorder='big', signed=False)
    return {
        'bytes': _bytes,
    }

def read_constant_float_info(class_file: BinaryIO):
    _bytes = unpack('f', class_file.read(4))
    return {
        'bytes': _bytes,
    }

def read_constant_long_info(class_file: BinaryIO):
    high_bytes = int.from_bytes(class_file.read(4), byteorder='big', signed=False)
    low_bytes = int.from_bytes(class_file.read(4), byteorder='big', signed=False)
    return {
        'high_bytes': high_bytes,
        'low_bytes': low_bytes,
    }

def read_constant_double_info(class_file: BinaryIO):
    high_bytes = int.from_bytes(class_file.read(4), byteorder='big', signed=False)
    low_bytes = int.from_bytes(class_file.read(4), byteorder='big', signed=False)
    return {
        'high_bytes': high_bytes,
        'low_bytes': low_bytes,
    }

def read_constant_class_info(class_file: BinaryIO):
    name_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'name_index': name_index,
    }

def read_constant_string_info(class_file: BinaryIO):
    string_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'string_index': string_index,
    }

def read_constant_fieldref_info(class_file: BinaryIO):
    class_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    name_and_type_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'class_index': class_index,
        'name_and_type_index': name_and_type_index,
    }

def read_constant_methodref_info(class_file: BinaryIO):
    class_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    name_and_type_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'class_index': class_index,
        'name_and_type_index': name_and_type_index,
    }

def read_constant_interface_method_ref_info(class_file: BinaryIO):
    class_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    name_and_type_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'class_index': class_index,
        'name_and_type_index': name_and_type_index,
    }

def read_constant_name_and_type_info(class_file: BinaryIO):
    name_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    descriptor_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'name_index': name_index,
        'descriptor_index': descriptor_index,
    }

def read_constant_method_handle_info(class_file: BinaryIO):
    reference_kind = int.from_bytes(class_file.read(1), byteorder='big', signed=False)
    reference_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'reference_kind': reference_kind,
        'reference_index': reference_index,
    }

def read_constant_method_type_info(class_file: BinaryIO):
    descriptor_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'descriptor_index': descriptor_index,
    }

def read_constant_dynamic_info(class_file: BinaryIO):
    bootstrap_method_attr_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    name_and_type_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'bootstrap_method_attr_index': bootstrap_method_attr_index,
        'name_and_type_index': name_and_type_index,
    }

def read_constant_invoke_dynamic_info(class_file: BinaryIO):
    bootstrap_method_attr_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    name_and_type_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'bootstrap_method_attr_index': bootstrap_method_attr_index,
        'name_and_type_index': name_and_type_index,
    }

def read_constant_module_info(class_file: BinaryIO):
    name_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'name_index': name_index,
    }

def read_constant_packge_info(class_file: BinaryIO):
    name_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    return {
        'name_index': name_index,
    }

CONSTANT_POOL_TAGS = [None] * 21

CONSTANT_POOL_TAGS[1]  = 'CONSTANT_Utf8',
CONSTANT_POOL_TAGS[3]  = 'CONSTANT_Integer',
CONSTANT_POOL_TAGS[4]  = 'CONSTANT_Float',
CONSTANT_POOL_TAGS[5]  = 'CONSTANT_Long',
CONSTANT_POOL_TAGS[6]  = 'CONSTANT_Double',
CONSTANT_POOL_TAGS[7]  = 'CONSTANT_Class',
CONSTANT_POOL_TAGS[8]  = 'CONSTANT_String',
CONSTANT_POOL_TAGS[9]  = 'CONSTANT_Fieldref',
CONSTANT_POOL_TAGS[10] = 'CONSTANT_Methodref',
CONSTANT_POOL_TAGS[11] = 'CONSTANT_InterfaceMethodref',
CONSTANT_POOL_TAGS[12] = 'CONSTANT_NameAndType',
CONSTANT_POOL_TAGS[15] = 'CONSTANT_MethodHandle',
CONSTANT_POOL_TAGS[16] = 'CONSTANT_MethodType',
CONSTANT_POOL_TAGS[17] = 'CONSTANT_Dynamic',
CONSTANT_POOL_TAGS[18] = 'CONSTANT_InvokeDynamic',
CONSTANT_POOL_TAGS[19] = 'CONSTANT_Module',
CONSTANT_POOL_TAGS[20] = 'CONSTANT_Package',

class ConstantPool:
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw = raw_bytes

    def __len__(self) -> int:
        return self.get_constant_pool_count()

    def get_constant_pool_count(self) -> int:
        return int.from_bytes(self.raw[:2], "big")
    
class CpInfo(ABC):
    def __init__(self, raw_bytes: bytes) -> None:
        self.raw = raw_bytes

    def get_tag(self) -> str:
        return CONSTANT_POOL_TAGS[int.from_bytes(self.raw[:1], "big")]

class Utf8Info(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_length(self) -> int:
        return int.from_bytes(self.raw[1:3], "big")

    def get_string(self) -> str:
        return str(self.raw[3:], encoding="utf8")

class IntegerInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_integer(self) -> int:
        return int.from_bytes(self.raw[1:], "big")

class FloatInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_float(self) -> float:
        return unpack("f", self.raw[1:])

class LongInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_long(self) -> int:
        return int.from_bytes(self.raw[1:], "big")

class DoubleInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_double(self) -> float:
        return unpack("d", self.raw[1:])

class ClassInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_name_index(self) -> int:
        return int.from_bytes(self.raw[1:], "big")
    
class StringInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_string_index(self) -> int:
        return int.from_bytes(self.raw[1:], "big")

class FieldrefInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_class_index(self) -> int:
        return int.from_bytes(self.raw[1:3], "big")

    def get_name_and_type_index(self) -> int:
        return int.from_bytes(self.raw[3:5], "big")

class MethodrefInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_class_index(self) -> int:
        return int.from_bytes(self.raw[1:3], "big")

    def get_name_and_type_index(self) -> int:
        return int.from_bytes(self.raw[3:5], "big")

class InterfaceMethodrefInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_class_index(self) -> int:
        return int.from_bytes(self.raw[1:3], "big")

    def get_name_and_type_index(self) -> int:
        return int.from_bytes(self.raw[3:5], "big")

class NameAndTypeInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_name_index(self) -> int:
        return int.from_bytes(self.raw[1:3], "big")

    def get_descriptor_index(self) -> int:
        return int.from_bytes(self.raw[3:5], "big")

class MethodHandleInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)
    
    def get_reference_kind(self) -> int:
        return int.from_bytes(self.raw[1:2], "big")

    def get_reference_index(self) -> int:
        return int.from_bytes(self.raw[2:4], "big")

class MethodTypeInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_descriptor_index(self) -> int:
        return int.from_bytes(self.raw[1:2], "big") 

class DynamicInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_bootstrap_method_attr_index(self) -> int:
        return int.from_bytes(self.raw[1:3], "big")

    def get_name_and_type_index(self) -> int:
        return int.from_bytes(self.raw[3:5], "big") 

class InvokeDynamicInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_bootstrap_method_attr_index(self) -> int:
        return int.from_bytes(self.raw[1:3], "big")

    def get_name_and_type_index(self) -> int:
        return int.from_bytes(self.raw[3:5], "big")

class ModuleInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    def get_name_index(self) -> int:
        return int.from_bytes(self.raw[1:3], "big")

class PackageInfo(CpInfo):
    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)
    
    def get_name_index(self) -> int:
        return int.from_bytes(self.raw[1:3], "big")