from .attribute import Attribute


class NestHostAttribute(Attribute):
    """ Represents a nest host attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.28
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.host_class_index: int = self.parse_int(self.raw[6:8])

    def get_host_class_index(self) -> int:
        return self.host_class_index

    def __repr__(self) -> str:
        return f"NestHostAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"host_class_index={self.host_class_index})"
