from abc import ABCMeta


class AttributeInfo(metaclass=ABCMeta):
    """ Represents a Java class attribute.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7
    """

    @staticmethod
    def parse_int(segment: bytes) -> int:
        return int.from_bytes(segment, byteorder='big', signed=False)

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        self.raw: bytes = raw_bytes

        self.attribute_name_index: int = attribute_name_index
        self.attribute_length: int = attribute_length

    def get_attribute_name_index(self) -> int:
        return self.attribute_name_index

    def get_attribute_length(self) -> int:
        return self.attribute_length

    def __repr__(self) -> str:
        return f"AttributeInfo(name_index={self.attribute_name_index}, length={self.attribute_length})"
