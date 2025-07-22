from .attr import Attribute


def dump_bytes(count: int, raw_bytes: bytes) -> tuple[Attribute, ...]:
    """Dump bytes into a tuple of Attribute objects."""
    attributes = []
    cursor = 0
    for _ in range(count):
        attribute_name_index = Attribute.parse_int(raw_bytes[cursor:cursor + 2])
        attribute_length = Attribute.parse_int(raw_bytes[cursor + 2:cursor + 6])

        full_length = 6 + attribute_length

        attributes.append(
            Attribute(raw_bytes[cursor:cursor + full_length], attribute_name_index, attribute_length))

        cursor += full_length

    return tuple(attributes)
