from dataclasses import dataclass
from functools import cached_property

from .attribute_info import AttributeInfo


class RecordAttributeInfo(AttributeInfo):
    """ Represents a record attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.30

    Record_attribute {
        u2                    attribute_name_index;
        u4                    attribute_length;
        u2                    components_count;
        record_component_info components[components_count];
    }

    record_component_info {
        u2             name_index;
        u2             descriptor_index;
        u2             attributes_count;
        attribute_info attributes[attributes_count];
    }
    """

    @dataclass
    class RecordComponentInfo:
        name_index: int
        descriptor_index: int
        attributes_count: int
        attributes: tuple[AttributeInfo, ...]

    def __init__(self, raw_bytes: bytes) -> None:
        super().__init__(raw_bytes)

    @cached_property
    def components_count(self) -> int:
        return self.parse_int(self.raw[6:8])

    @cached_property
    def components(self) -> tuple[AttributeInfo, ...]:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"components_count={self.components_count}, components={self.components})"
