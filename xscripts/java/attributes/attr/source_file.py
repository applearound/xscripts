from .attribute_info import AttributeInfo


class SourceFileAttributeInfo(AttributeInfo):
    """ Represents a source file attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.10
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.sourcefile_index: int = self.parse_int(self.__raw[6:8])

    def get_sourcefile_index(self) -> int:
        return self.sourcefile_index

    def __repr__(self) -> str:
        return f"SourceFileAttribute(name_index={self.attribute_name_index}, length={self.attribute_length}, " \
               f"sourcefile_index={self.sourcefile_index})"
