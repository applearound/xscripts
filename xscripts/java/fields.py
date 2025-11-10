import logging
from functools import cached_property
from io import BytesIO

from .attributes import (
    AttributeInfo,
    AttributesTypes,
    ConstantValueAttributeInfo,
    DeprecatedAttributeInfo,
    RuntimeInvisibleAnnotationsAttributeInfo,
    RuntimeInvisibleTypeAnnotationsAttributeInfo,
    RuntimeVisibleAnnotationsAttributeInfo,
    RuntimeVisibleTypeAnnotationsAttributeInfo,
    SignatureAttributeInfo,
    SyntheticAttributeInfo,
)
from .constant_pool import ConstantPool
from .enums import FieldAccessFlags
from .utils import parse_int

logger = logging.getLogger(__name__)


class Field:
    """Represents a Java class field.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.5

    field_info {
        u2             access_flags;
        u2             name_index;
        u2             descriptor_index;
        u2             attributes_count;
        attribute_info attributes[attributes_count];
    }
    """

    def __init__(self, raw_bytes: bytes, constant_pool: ConstantPool) -> None:
        self.__raw: bytes = raw_bytes
        self.__constant_pool: ConstantPool = constant_pool

    @cached_property
    def access_flags(self) -> int:
        return parse_int(self.raw[0:2])

    @cached_property
    def name_index(self) -> int:
        return parse_int(self.raw[2:4])

    @cached_property
    def descriptor_index(self) -> int:
        return parse_int(self.raw[4:6])

    @cached_property
    def attributes_count(self) -> int:
        return parse_int(self.raw[6:8])

    @cached_property
    def attributes(self) -> tuple[AttributeInfo, ...]:
        attributes: list[AttributeInfo] = []

        with BytesIO(self.raw[8:]) as reader:
            for _ in range(self.attributes_count):
                attribute_name_index_segment = reader.read(2)
                attribute_name_index = AttributeInfo.parse_int(
                    attribute_name_index_segment
                )

                attribute_name = self.__constant_pool.get_utf8_constant_pool_info(
                    attribute_name_index
                ).string

                attribute_length_segment = reader.read(4)
                attribute_length = AttributeInfo.parse_int(attribute_length_segment)

                logger.debug(
                    f"Processing attribute: {attribute_name}(index: {attribute_name_index}, length: {attribute_length})"
                )

                raw_attribute_bytes = (
                    attribute_name_index_segment
                    + attribute_length_segment
                    + reader.read(attribute_length)
                )

                if attribute_name == AttributesTypes.CONSTANT_VALUE:
                    attribute = ConstantValueAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.SYNTHETIC:
                    attribute = SyntheticAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.DEPRECATED:
                    attribute = DeprecatedAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.SIGNATURE:
                    attribute = SignatureAttributeInfo(raw_attribute_bytes)
                elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_ANNOTATIONS:
                    attribute = RuntimeVisibleAnnotationsAttributeInfo(
                        raw_attribute_bytes
                    )
                elif attribute_name == AttributesTypes.RUNTIME_INVISIBLE_ANNOTATIONS:
                    attribute = RuntimeInvisibleAnnotationsAttributeInfo(
                        raw_attribute_bytes
                    )
                elif attribute_name == AttributesTypes.RUNTIME_VISIBLE_TYPE_ANNOTATIONS:
                    attribute = RuntimeVisibleTypeAnnotationsAttributeInfo(
                        raw_attribute_bytes
                    )
                elif (
                    attribute_name == AttributesTypes.RUNTIME_INVISIBLE_TYPE_ANNOTATIONS
                ):
                    attribute = RuntimeInvisibleTypeAnnotationsAttributeInfo(
                        raw_attribute_bytes
                    )
                else:
                    raise ValueError(f"Unsupported attribute type: {attribute_name}")

                attributes.append(attribute)

        return tuple(attributes)

    @property
    def raw(self) -> bytes:
        return self.__raw

    def field_access_flags(self) -> tuple[FieldAccessFlags, ...]:
        return FieldAccessFlags.parse_flags(self.access_flags)

    def is_public(self) -> bool:
        return FieldAccessFlags.is_public(self.access_flags)

    def is_private(self) -> bool:
        return FieldAccessFlags.is_private(self.access_flags)

    def is_protected(self) -> bool:
        return FieldAccessFlags.is_protected(self.access_flags)

    def is_static(self) -> bool:
        return FieldAccessFlags.is_static(self.access_flags)

    def is_final(self) -> bool:
        return FieldAccessFlags.is_final(self.access_flags)

    def is_volatile(self) -> bool:
        return FieldAccessFlags.is_volatile(self.access_flags)

    def is_transient(self) -> bool:
        return FieldAccessFlags.is_transient(self.access_flags)

    def is_synthetic(self) -> bool:
        return FieldAccessFlags.is_synthetic(self.access_flags)

    def is_enum(self) -> bool:
        return FieldAccessFlags.is_enum(self.access_flags)

    def __repr__(self) -> str:
        return (
            f"Field(access_flags={self.access_flags}, name_index={self.name_index}, "
            f"descriptor_index={self.descriptor_index}, attributes_count={self.attributes_count}), "
            f"attributes={self.attributes}"
        )


def load_fields(count: int, raw_bytes: bytes, constant_pool) -> tuple[Field, ...]:
    """Load fields from raw bytes."""
    ...
