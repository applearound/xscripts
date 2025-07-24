from functools import cached_property

from .attribute_info import AttributeInfo


class StackMapTableAttributeInfo(AttributeInfo):
    """ Represents a stack map table attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.4

    StackMapTable_attribute {
        u2              attribute_name_index;
        u4              attribute_length;
        u2              number_of_entries;
        stack_map_frame entries[number_of_entries];
    }
    """

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def number_of_entries(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def entries(self) -> bytes:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"number_of_entries={self.number_of_entries})"
