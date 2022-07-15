from dataclasses import Field
from pprint import pprint
from typing import BinaryIO, Dict

from java_class import Magic, Version, ConstantPool, AccessFlags, ThisAndSuperClass, Interfaces, Fields, Methods, Attributes

CONSTANT_POOL_TAGS = [None] * 21

CONSTANT_POOL_TAGS[3] = 5
CONSTANT_POOL_TAGS[4] = 5
CONSTANT_POOL_TAGS[5] = 9
CONSTANT_POOL_TAGS[6] = 9
CONSTANT_POOL_TAGS[7] = 3
CONSTANT_POOL_TAGS[8] = 3
CONSTANT_POOL_TAGS[9] = 5
CONSTANT_POOL_TAGS[10] = 5
CONSTANT_POOL_TAGS[11] = 5
CONSTANT_POOL_TAGS[12] = 5
CONSTANT_POOL_TAGS[15] = 4
CONSTANT_POOL_TAGS[16] = 3
CONSTANT_POOL_TAGS[17] = 5
CONSTANT_POOL_TAGS[18] = 5
CONSTANT_POOL_TAGS[19] = 3
CONSTANT_POOL_TAGS[20] = 3

def read_magic(class_file: BinaryIO) -> Magic:    
    return Magic(class_file.read(4))

def read_version(class_file: BinaryIO) -> Version:
    return Version(class_file.read(4))

def read_constant_pool(class_file: BinaryIO) -> ConstantPool:
    cur = class_file.tell()

    constant_pool_count = int.from_bytes(class_file.read(2), "big")
    length = 2

    for _ in range(constant_pool_count - 1):
        tag = int.from_bytes(class_file.read(1), "big")

        if tag == 1:
            utf8_length = int.from_bytes(class_file.read(2), "big")
            class_file.seek(utf8_length, 1)
            length += 3 + utf8_length
            continue

        class_file.seek(CONSTANT_POOL_TAGS[tag] - 1, 1)
        length += CONSTANT_POOL_TAGS[tag]

    class_file.seek(cur)
    return ConstantPool(class_file.read(length))

def read_access_flags(class_file: BinaryIO) -> AccessFlags:
    return AccessFlags(class_file.read(2))

def read_this_and_super_class(class_file: BinaryIO) -> ThisAndSuperClass:
    return ThisAndSuperClass(class_file.read(4))

def read_interfaces(class_file: BinaryIO) -> Interfaces:
    interfaces_count = int.from_bytes(class_file.read(2), byteorder='big', signed=False)

    class_file.seek(-2, 1)

    return Interfaces(class_file.read(2 + 2 * interfaces_count))

def read_fields(class_file: BinaryIO) -> Fields:
    cur = class_file.tell()

    fields_count = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    length = 2

    for _ in range(fields_count):
        class_file.seek(6, 1)

        attributes_count = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
        attributes_length = 2

        for _ in range(attributes_count):
            class_file.seek(2, 1)
            attribute_length = int.from_bytes(class_file.read(4), byteorder='big', signed=False)
            attributes_length += 6 + attribute_length

        length += 6 + attributes_length

    class_file.seek(cur)

    return Fields(class_file.read(length))

def read_methods(class_file: BinaryIO) -> Methods:
    cur = class_file.tell()

    methods_count = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
    length = 2

    for _ in range(methods_count):
        class_file.seek(6, 1)

        attributes_count = int.from_bytes(class_file.read(2), byteorder='big', signed=False)
        attributes_length = 2

        for _ in range(attributes_count):
            class_file.seek(2, 1)
            attribute_length = int.from_bytes(class_file.read(4), byteorder='big', signed=False)
            attributes_length += 6 + attribute_length

        length += 6 + attributes_length

    class_file.seek(cur)

    return Methods(class_file.read(length))

def read_attributes(class_file: BinaryIO) -> Attributes:
    cur = class_file.tell()
    
    attributes_count = int.from_bytes(class_file.read(2), byteorder="big", signed=False)
    length = 2

    for _ in range(attributes_count):
        class_file.seek(2, 1)
        attribute_length = int.from_bytes(class_file.read(4), byteorder='big', signed=False)
        length += 6 + attribute_length

    class_file.seek(cur)

    return Attributes(class_file.read(length))

def read_class_file(class_file: BinaryIO) -> Dict[str, Dict]:
    magic                = read_magic(class_file)
    version              = read_version(class_file)
    constant_pool        = read_constant_pool(class_file)
    access_flags         = read_access_flags(class_file)
    this_and_super_class = read_this_and_super_class(class_file)
    interfaces           = read_interfaces(class_file)
    fields               = read_fields(class_file)
    methods              = read_methods(class_file)
    attributes           = read_attributes(class_file)

    return {
        'magic'               : magic.raw,
        'minor_version'       : version.get_minor_version(),
        'major_version'       : version.get_major_version(),
        'constant_pool_count' : constant_pool.get_constant_pool_count(),
        'constant_pool'       : constant_pool.raw,
        'access_flags'        : access_flags.get_hex(),
        'this_class'          : this_and_super_class.get_this_class_index(),
        'super_class'         : this_and_super_class.get_super_class_index(),
        'interfaces_count'    : interfaces.get_interfaces_count(),
        'interfaces'          : interfaces.raw[2:],
        'field_count'         : fields.get_fields_count(),
        'fields'              : fields.raw[:2],
        'methods_count'       : methods.get_methods_count(),
        'methods'             : methods.raw[:2],
        'attributes_count'    : attributes.get_attributes_count(),
        'attributes'          : attributes.raw[2:],
    }

if __name__ == '__main__':
    file_path = '/Users/yezhou/Desktop/mygithub/mytest/HibernateTest/target/classes/me/yz/hibernate/test/entity/Payment.class'
    with open(file=file_path, mode='rb') as class_file:
        class_object = read_class_file(class_file)
    pprint(class_object)