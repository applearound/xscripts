from .utils import parse_int


class Attribute:
    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int, info) -> None:
        self.raw: bytes = raw_bytes

        self.attribute_name_index: int = attribute_name_index
        self.attribute_length: int = attribute_length
        self.info = info

    def get_attribute_name_index(self) -> int:
        return self.attribute_name_index

    def get_attribute_length(self) -> int:
        return self.attribute_length


def dump_bytes(count: int, raw_bytes: bytes) -> tuple[Attribute, ...]:
    """ Dump bytes into a tuple of Attribute objects.
    """
    attributes = []
    cursor = 0
    for _ in range(count):
        attribute_name_index = parse_int(raw_bytes[cursor:cursor + 2])
        attribute_length = parse_int(raw_bytes[cursor + 2:cursor + 6])
        info = raw_bytes[cursor + 6:cursor + 6 + attribute_length]

        full_length = 6 + attribute_length

        attributes.append(
            Attribute(raw_bytes[cursor:cursor + full_length], attribute_name_index, attribute_length, info))

        cursor += full_length

    return tuple(attributes)
