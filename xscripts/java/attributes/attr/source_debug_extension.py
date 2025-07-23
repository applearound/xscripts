from .attributeinfo import AttributeInfo


class SourceDebugExtensionAttributeInfo(AttributeInfo):
    """ Represents a source debug extension attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.11
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.debug_extension: bytes = self.raw[6:]

    def get_debug_extension(self) -> bytes:
        return self.debug_extension

    def __repr__(self) -> str:
        return f"SourceDebugExtensionAttribute(name_index={self.attribute_name_index}, length={self.attribute_length})"
