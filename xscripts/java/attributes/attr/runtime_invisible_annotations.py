from .attribute_info import AttributeInfo


class RuntimeInvisibleAnnotationsAttributeInfo(AttributeInfo):
    """ Represents a runtime invisible annotations attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.17
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.annotations_count: int = self.parse_int(self.__raw[6:8])
        self.annotations: bytes = self.__raw[8:]

    def get_annotations_count(self) -> int:
        return self.annotations_count

    def get_annotations(self) -> bytes:
        return self.annotations

    def __repr__(self) -> str:
        return f"RuntimeInvisibleAnnotationsAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"annotations_count={self.annotations_count})"
