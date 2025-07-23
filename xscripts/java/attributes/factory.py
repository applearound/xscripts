import logging
from io import BytesIO

from .attr import *
from ..constant_pool import ConstantPool

logger = logging.getLogger(__name__)


class AttributeFactory:
    """ Factory class for creating attribute instances.
    """

    def __init__(self, constant_pool: ConstantPool):
        self.constant_pool = constant_pool

    def make_attributes(self, count: int, raw_bytes: bytes) -> tuple[AttributeInfo, ...]:
        """ Dump bytes into a tuple of Attribute objects.
        """
        attributes = []

        with BytesIO(raw_bytes) as reader:
            for _ in range(count):
                attribute_name_index_segment = reader.read(2)
                attribute_name_index = AttributeInfo.parse_int(attribute_name_index_segment)

                utf8_info = self.constant_pool.get_utf8_constant_pool_info(attribute_name_index)
                attribute_name = utf8_info.string

                attribute_length_segment = reader.read(4)
                attribute_length = AttributeInfo.parse_int(attribute_length_segment)

                logger.info(
                    f"Processing attribute: {attribute_name} (index: {attribute_name_index}, length: {attribute_length})")

        return tuple(attributes)

    def make_constant_value_attribute(self, attribute_name_index: int, attribute_length: int,
                                      attribute_segment: bytes) -> ConstantValueAttributeInfo:
        """ Create a ConstantValueAttribute from raw bytes.

        Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.2
        """
        with BytesIO(attribute_segment[6:]) as reader:
            constantvalue_index_segment = reader.read(2)
            constantvalue_index = AttributeInfo.parse_int(constantvalue_index_segment)

            attribute = ConstantValueAttributeInfo(attribute_segment, attribute_name_index, attribute_length,
                                                   constantvalue_index)

            logger.debug(f"ConstantValueAttribute: {attribute}")

            return attribute

    def make_code_attribute(self, attribute_name_index: int, attribute_length: int,
                            attribute_segment: bytes) -> CodeAttributeInfo:
        """ Create a CodeAttribute from raw bytes.

        Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.3
        """
        with BytesIO(attribute_segment[6:]) as reader:
            max_stack_segment = reader.read(2)
            max_stack = AttributeInfo.parse_int(max_stack_segment)

            max_locals_segment = reader.read(2)
            max_locals = AttributeInfo.parse_int(max_locals_segment)

            code_length_segment = reader.read(4)
            code_length = AttributeInfo.parse_int(code_length_segment)

            code_segment = reader.read(code_length)

            exception_table_length_segment = reader.read(2)
            exception_table_length = AttributeInfo.parse_int(exception_table_length_segment)

            exception_table = []
            for _ in range(exception_table_length):
                start_pc_segment = reader.read(2)
                start_pc = AttributeInfo.parse_int(start_pc_segment)

                end_pc_segment = reader.read(2)
                end_pc = AttributeInfo.parse_int(end_pc_segment)

                handler_pc_segment = reader.read(2)
                handler_pc = AttributeInfo.parse_int(handler_pc_segment)

                catch_type_segment = reader.read(2)
                catch_type = AttributeInfo.parse_int(catch_type_segment)

                exception_table.append(CodeAttributeInfo.Exception(start_pc, end_pc, handler_pc, catch_type))

            attributes_count_segment = reader.read(2)
            attributes_count = AttributeInfo.parse_int(attributes_count_segment)

            attributes = self.make_attributes(attributes_count, reader.read())

            return CodeAttributeInfo(
                attribute_segment, attribute_name_index, attribute_length,
                max_stack, max_locals, code_length, code_segment,
                exception_table_length, exception_table, attributes_count, attributes
            )

    def make_stack_map_table_attribute(self, attribute_name_index: int, attribute_length: int,
                                       attribute_segment: bytes) -> StackMapTableAttributeInfo:
        """ Create a StackMapTableAttribute from raw bytes.

        Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.4
        """
        with BytesIO(attribute_segment[6:]) as reader:
            number_of_entries_segment = reader.read(2)
            number_of_entries = AttributeInfo.parse_int(number_of_entries_segment)

            entries = []
            for _ in range(number_of_entries):
                entry = StackMapTableAttributeInfo.Entry.from_bytes(reader, self.constant_pool)
                entries.append(entry)

            return StackMapTableAttributeInfo(
                attribute_segment, attribute_name_index, attribute_length, number_of_entries, entries
            )

    def make_exceptions_attribute(self, attribute_name_index: int, attribute_length: int,
                                  attribute_segment: bytes) -> ExceptionsAttributeInfo:
        """ Create an ExceptionsAttribute from raw bytes.

        Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.5
        """
        with BytesIO(attribute_segment[6:]) as reader:
            number_of_exceptions_segment = reader.read(2)
            number_of_exceptions = AttributeInfo.parse_int(number_of_exceptions_segment)

            exception_index_table = []
            for _ in range(number_of_exceptions):
                exception_index_segment = reader.read(2)
                exception_index = AttributeInfo.parse_int(exception_index_segment)
                exception_index_table.append(exception_index)

            return ExceptionsAttributeInfo(
                attribute_segment, attribute_name_index, attribute_length, number_of_exceptions, exception_index_table
            )
