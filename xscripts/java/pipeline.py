from .java_class import JavaClass
from .enums import ConstantPoolInfoTag


class JavaClassDumpPipeline:
    @staticmethod
    def parse_int(int_bytes: bytes) -> int:
        """Parse a byte array into an integer."""
        return int.from_bytes(int_bytes, byteorder="big", signed=False)

    def __init__(self, class_file_path: str) -> None:
        self.class_file_path = class_file_path

    def run(self) -> JavaClass:
        with open(self.class_file_path, "rb") as class_file:
            magic_segment = class_file.read(4)
            minor_version_segment = class_file.read(2)
            major_version_segment = class_file.read(2)
            constant_pool_count_segment = class_file.read(2)

            # Read constant pool info
            constant_pool_info_segment_appender = bytearray()
            for _ in range(self.parse_int(constant_pool_count_segment) - 1):
                tag_num_segment = class_file.read(1)

                constant_pool_info_segment_appender.extend(tag_num_segment)

                tag_num = self.parse_int(tag_num_segment)
                tag = ConstantPoolInfoTag(tag_num)

                size = tag.get_size()
                if size < 0:
                    raise ValueError(f"Invalid constant pool tag size for tag {tag_num}")

                if size == 0:
                    utf8_length_segment = class_file.read(2)
                    utf8_length = self.parse_int(utf8_length_segment)
                    tag_value_segment = utf8_length_segment + class_file.read(utf8_length)
                else:
                    tag_value_segment = class_file.read(size - 1)

                constant_pool_info_segment_appender.extend(tag_value_segment)

            constant_pool_info_segment = bytes(constant_pool_info_segment_appender)

            access_flags_segment = class_file.read(2)
            this_class_segment = class_file.read(2)
            super_class_segment = class_file.read(2)
            interfaces_count_segment = class_file.read(2)
            interfaces_segment = class_file.read(2 * self.parse_int(interfaces_count_segment))
            fields_count_segment = class_file.read(2)

            # Read fields info
            fields_info_segment_appender = bytearray()
            for _ in range(self.parse_int((fields_count_segment))):
                fields_info_segment_appender.extend(class_file.read(6))

                attributes_count_segment = class_file.read(2)
                fields_info_segment_appender.extend(attributes_count_segment)

                for _ in range(self.parse_int(attributes_count_segment)):
                    fields_info_segment_appender.extend(class_file.read(2))

                    attribute_length_segment = class_file.read(4)

                    fields_info_segment_appender.extend(attribute_length_segment)
                    fields_info_segment_appender.extend(class_file.read(
                        self.parse_int(attribute_length_segment)
                    ))

            fields_info_segment = bytes(fields_info_segment_appender)
            methods_count_segment = class_file.read(2)

            # Read methods info
            methods_info_segment_appender = bytearray()
            for _ in range(self.parse_int(methods_count_segment)):
                methods_info_segment_appender.extend(class_file.read(6))

                attributes_count_segment = class_file.read(2)
                methods_info_segment_appender.extend(attributes_count_segment)

                for _ in range(self.parse_int((attributes_count_segment))):
                    methods_info_segment_appender.extend(class_file.read(2))

                    attribute_length_segment = class_file.read(4)

                    methods_info_segment_appender.extend(attribute_length_segment)
                    methods_info_segment_appender.extend(class_file.read(
                        self.parse_int(attribute_length_segment)
                    ))

            methods_info_segment = bytes(methods_info_segment_appender)
            attributes_count_segment = class_file.read(2)

            # Read attributes info
            attributes_info_segment_appender = bytearray()
            for _ in range(self.parse_int(attributes_count_segment)):
                attributes_info_segment_appender.extend(class_file.read(2))

                attribute_length_segment = class_file.read(4)

                attributes_info_segment_appender.extend(attribute_length_segment)
                attributes_info_segment_appender.extend(class_file.read(
                    self.parse_int(attribute_length_segment)
                ))

            attributes_info_segment = bytes(attributes_info_segment_appender)

            return JavaClass(
                magic_segment=magic_segment,
                minor_version_segment=minor_version_segment,
                major_version_segment=major_version_segment,
                constant_pool_count_segment=constant_pool_count_segment,
                constant_pool_segment=constant_pool_info_segment,
                access_flags_segment=access_flags_segment,
                this_class_segment=this_class_segment,
                super_class_segment=super_class_segment,
                interfaces_count_segment=interfaces_count_segment,
                interfaces_segment=interfaces_segment,
                fields_count_segment=fields_count_segment,
                fields_info_segment=fields_info_segment,
                methods_count_segment=methods_count_segment,
                methods_info_segment=methods_info_segment,
                attributes_count_segment=attributes_count_segment,
                attributes_info_segment=attributes_info_segment
            )

    def __repr__(self) -> str:
        return f"JavaClassDumpPipeline(class_file_path={self.class_file_path})"
