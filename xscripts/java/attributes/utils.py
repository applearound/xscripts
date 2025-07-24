import logging

from .attr import AttributeInfo
from ..constant_pool import ConstantPool

logger = logging.getLogger(__name__)


def dump_bytes(count: int, raw_bytes: bytes, constant_pool: ConstantPool) -> tuple[AttributeInfo, ...]:
    """ Dump bytes into a tuple of Attribute objects.
    """
    attributes = []
    cursor = 0
    for _ in range(count):
        attribute_name_index_segment = raw_bytes[cursor:cursor + 2]
        attribute_name_index = AttributeInfo.parse_int(attribute_name_index_segment)

        attribute_length_segment = raw_bytes[cursor + 2:cursor + 6]
        attribute_length = AttributeInfo.parse_int(attribute_length_segment)

        utf8_info = constant_pool.get_utf8_constant_pool_info(attribute_name_index)
        logger.info(
            f"Processing attribute: {utf8_info.string} (index: {attribute_name_index}, length: {attribute_length})")

        full_length = 6 + attribute_length

        cursor += full_length

    return tuple(attributes)
