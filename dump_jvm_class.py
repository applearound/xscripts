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
CONSTANT_POOL_TAGS[1] = { 'name': 'CONSTANT_Utf8', 'method': read_constant_utf8_info }
CONSTANT_POOL_TAGS[3] = { 'name': 'CONSTANT_Integer', 'method': read_constant_integer_info }
CONSTANT_POOL_TAGS[4] = { 'name': 'CONSTANT_Float', 'method': read_constant_float_info }
CONSTANT_POOL_TAGS[5] = { 'name': 'CONSTANT_Long', 'method': read_constant_long_info }
CONSTANT_POOL_TAGS[6] = { 'name': 'CONSTANT_Double', 'method': read_constant_double_info }
CONSTANT_POOL_TAGS[7] = { 'name': 'CONSTANT_Class', 'method': read_constant_class_info }
CONSTANT_POOL_TAGS[8] = { 'name': 'CONSTANT_String', 'method': read_constant_string_info }
CONSTANT_POOL_TAGS[9] = { 'name': 'CONSTANT_Fieldref', 'method': read_constant_fieldref_info }
CONSTANT_POOL_TAGS[10] = { 'name': 'CONSTANT_Methodref', 'method': read_constant_methodref_info }
CONSTANT_POOL_TAGS[11] = { 'name': 'CONSTANT_InterfaceMethodref', 'method': read_constant_interface_method_ref_info }
CONSTANT_POOL_TAGS[12] = { 'name': 'CONSTANT_NameAndType', 'method': read_constant_name_and_type_info }
CONSTANT_POOL_TAGS[15] = { 'name': 'CONSTANT_MethodHandle', 'method': read_constant_method_handle_info }
CONSTANT_POOL_TAGS[16] = { 'name': 'CONSTANT_MethodType', 'method': read_constant_method_type_info }
CONSTANT_POOL_TAGS[17] = { 'name': 'CONSTANT_Dynamic', 'method': read_constant_dynamic_info }
CONSTANT_POOL_TAGS[18] = { 'name': 'CONSTANT_InvokeDynamic', 'method': read_constant_invoke_dynamic_info }
CONSTANT_POOL_TAGS[19] = { 'name': 'CONSTANT_Module', 'method': read_constant_module_info }
CONSTANT_POOL_TAGS[20] = { 'name': 'CONSTANT_Package', 'method': read_constant_packge_info }

def read_attribute_info(class_file: BinaryIO):
    attribute_name_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    attribute_length = int.from_bytes(class_file.read(4), byteorder='big', signed=False)
    info = class_file.read(attribute_length)

    return {
        'attribute_name_index': attribute_name_index,
        'attribute_length': attribute_length,
        'info': info,
    }

def read_attributes(attributes_count: int, class_file: BinaryIO):
    return tuple(read_attribute_info(class_file) for _ in range(attributes_count))

def read_method_info(class_file: BinaryIO):
    access_flags = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    name_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    descriptor_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    attributes_count = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    attributes = read_attributes(attributes_count, class_file)

    return {
        'access_flags': access_flags,
        'name_index': name_index,
        'descriptor_index': descriptor_index,
        'attributes_count': attributes_count,
        'attributes': attributes,
    }

def read_field_info(class_file: BinaryIO):
    access_flags = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    name_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    descriptor_index = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    attributes_count = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    attributes = read_attributes(attributes_count, class_file)

    return {
        'access_flags': access_flags,
        'name_index': name_index,
        'descriptor_index': descriptor_index,
        'attributes_count': attributes_count,
        'attributes': attributes,
    }

def read_cp_info(class_file: BinaryIO):
    tag = int.from_bytes(class_file.read(1), byteorder='big', signed=False)
    info = CONSTANT_POOL_TAGS[tag]['method'](class_file)
    cp_info = {
        'tag': tag,
    }
    cp_info.update(info)
    return cp_info

def read_magic(class_file: BinaryIO):
    return class_file.read(4)

def read_minor_version(class_file: BinaryIO):
    miv = class_file.read(2)
    return int.from_bytes(miv, byteorder='big')

def read_major_version(class_file: BinaryIO):
    mav = class_file.read(2)
    return int.from_bytes(mav, byteorder='big')

def read_constant_pool_count(class_file: BinaryIO):
    mav = class_file.read(2)
    return int.from_bytes(mav, byteorder='big')

def read_constant_pool(constant_pool_count: int, class_file: BinaryIO):
    return tuple(read_cp_info(class_file) for _ in range(constant_pool_count - 1))

def read_access_flags(class_file: BinaryIO):
    return int.from_bytes(class_file.read(2), byteorder='big', signed=False)

def read_this_class(class_file: BinaryIO):
    return int.from_bytes(class_file.read(2), byteorder='big', signed=False)

def read_super_class(class_file: BinaryIO):
    return int.from_bytes(class_file.read(2), byteorder='big', signed=False)

def read_interfaces_count(class_file: BinaryIO):
    return int.from_bytes(class_file.read(2), byteorder='big', signed=False)

def read_interfaces(interfaces_count: int, class_file: BinaryIO):
    return tuple(int.from_bytes(class_file.read(2), byteorder='big', signed=False) for _ in range(interfaces_count))

def read_field_count(class_file: BinaryIO):
    return int.from_bytes(class_file.read(2), byteorder='big', signed=False)

def read_fields(fields_count:int, class_file: BinaryIO):
    return tuple(read_field_info(class_file) for _ in range(fields_count))

def read_methods_count(class_file: BinaryIO):
    return int.from_bytes(class_file.read(2), byteorder='big', signed=False)

def read_methods(methods_count:int, class_file: BinaryIO):
    return tuple(read_method_info(class_file) for _ in range(methods_count))

def read_attributes_count(class_file: BinaryIO):
    return int.from_bytes(class_file.read(2), byteorder='big', signed=False)

def read_class_file(class_file: BinaryIO):
    magic = read_magic(class_file)
    minor_version = read_minor_version(class_file)
    major_version = read_major_version(class_file)
    constant_pool_count = read_constant_pool_count(class_file)
    constant_pool = read_constant_pool(constant_pool_count, class_file)
    access_flags = read_access_flags(class_file)
    this_class = read_this_class(class_file)
    super_class = read_super_class(class_file)
    interfaces_count = read_interfaces_count(class_file)
    interfaces = read_interfaces(interfaces_count, class_file)
    field_count = read_field_count(class_file)
    fields = read_fields(field_count, class_file)
    methods_count = read_methods_count(class_file)
    methods = read_methods(methods_count, class_file)
    attributes_count = read_attributes_count(class_file)
    attributes = read_attributes(attributes_count, class_file)

    return {
        'magic': magic,
        'minor_version': minor_version,
        'major_version': major_version,
        'constant_pool_count': constant_pool_count,
        'constant_pool': constant_pool,
        'access_flags': access_flags,
        'this_class': this_class,
        'super_class': super_class,
        'interfaces_count': interfaces_count,
        'interfaces': interfaces,
        'field_count': field_count,
        'fields': fields,
        'methods_count': methods_count,
        'methods': methods,
        'attributes_count': attributes_count,
        'attributes': attributes,
    }

if __name__ == '__main__':
    file_path = '/Users/yezhou/Desktop/mygithub/DataStructureAndAlgorithm/target/classes/me/zyz/dsal/algorithm/sort/comparable/InsertionArraySort.class'
    with open(file=file_path, mode='rb') as class_file:
        class_object = read_class_file(class_file)
    print(class_object)
