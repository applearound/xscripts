from io import BufferedReader
from os import SEEK_CUR, SEEK_SET
from dataclasses import dataclass

from .constant_pool import ConstantPoolFactory, ConstantPoolInfoTags
from .utils import parse_int


@dataclass
class ChunkedJavaClass:
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


class JavaClassDumpPipeline:
    @staticmethod
    def __process_constant_pool_info(count: int, reader: BufferedReader) -> bytes:
        """Process the constant pool info based on the tag number."""
        savepoint = reader.tell()
        index = 0
        while index < count - 1:
            tag = ConstantPoolInfoTags(parse_int(reader.read(1)))

            size = ConstantPoolFactory.sizeof(tag)
            if size < 0:
                raise ValueError(f"Invalid constant pool tag size for tag {tag}")

            if size == 0:
                # handle UTF8 info
                utf8_length_segment = reader.read(2)
                utf8_length = parse_int(utf8_length_segment)

                reader.seek(utf8_length, SEEK_CUR)
            else:
                reader.seek(size - 1, SEEK_CUR)

            if tag is ConstantPoolInfoTags.LONG or tag is ConstantPoolInfoTags.DOUBLE:
                index += 2
            else:
                index += 1

        end_cursor = reader.tell()

        reader.seek(savepoint, SEEK_SET)

        return reader.read(end_cursor - savepoint)

    @staticmethod
    def __process_attributes_info(count: int, reader: BufferedReader) -> bytes:
        """Process the attributes info based on the count."""
        savepoint = reader.tell()
        for _ in range(count):
            reader.seek(2, SEEK_CUR)
            attribute_length = parse_int(reader.read(4))
            reader.seek(attribute_length, SEEK_CUR)

        end_cursor = reader.tell()

        reader.seek(savepoint, SEEK_SET)

        return reader.read(end_cursor - savepoint)

    @staticmethod
    def __process_fields_and_methods_info(count: int, reader: BufferedReader) -> bytes:
        savepoint = reader.tell()
        for _ in range(count):
            reader.seek(6, SEEK_CUR)

            attribute_count = parse_int(reader.read(2))

            for _ in range(attribute_count):
                # Skip attribute name index and length
                reader.seek(2, SEEK_CUR)
                attribute_length = parse_int(reader.read(4))
                # Skip the attribute info
                reader.seek(attribute_length, SEEK_CUR)

        end_cursor = reader.tell()

        reader.seek(savepoint, SEEK_SET)

        return reader.read(end_cursor - savepoint)

    def __init__(self, class_file_path: str) -> None:
        self.class_file_path = class_file_path

    def run(self) -> ChunkedJavaClass:
        with open(self.class_file_path, "rb") as class_file:
            magic_segment = class_file.read(4)
            minor_version_segment = class_file.read(2)
            major_version_segment = class_file.read(2)
            constant_pool_count_segment = class_file.read(2)
            # Read constant pool info
            constant_pool_info_segment = self.__process_constant_pool_info(parse_int(constant_pool_count_segment),
                                                                           class_file)
            access_flags_segment = class_file.read(2)
            this_class_segment = class_file.read(2)
            super_class_segment = class_file.read(2)
            interfaces_count_segment = class_file.read(2)
            interfaces_segment = class_file.read(2 * parse_int(interfaces_count_segment))
            fields_count_segment = class_file.read(2)
            # Read fields info
            fields_info_segment = self.__process_fields_and_methods_info(parse_int(fields_count_segment),
                                                                         class_file)
            methods_count_segment = class_file.read(2)
            # Read methods info
            methods_info_segment = self.__process_fields_and_methods_info(parse_int(methods_count_segment),
                                                                          class_file)
            attributes_count_segment = class_file.read(2)
            # Read attributes info
            attributes_info_segment = self.__process_attributes_info(parse_int(attributes_count_segment),
                                                                     class_file)

            return ChunkedJavaClass(
                magic_segment,
                minor_version_segment,
                major_version_segment,
                constant_pool_count_segment,
                constant_pool_info_segment,
                access_flags_segment,
                this_class_segment,
                super_class_segment,
                interfaces_count_segment,
                interfaces_segment,
                fields_count_segment,
                fields_info_segment,
                methods_count_segment,
                methods_info_segment,
                attributes_count_segment,
                attributes_info_segment
            )

    def __repr__(self) -> str:
        return f"JavaClassDumpPipeline(class_file_path={self.class_file_path})"
