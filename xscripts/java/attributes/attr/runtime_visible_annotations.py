from .attribute import Attribute


class RuntimeVisibleAnnotationsAttribute(Attribute):
    """ Represents a runtime visible annotations attribute in a Java class.

    Refer: https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.7.16
    """

    def __init__(self, raw_bytes: bytes, attribute_name_index: int, attribute_length: int) -> None:
        super().__init__(raw_bytes, attribute_name_index, attribute_length)

        self.annotations: bytes = self.raw[6:]

    def get_annotations(self) -> bytes:
        return self.annotations

    def __repr__(self) -> str:
        return f"RuntimeVisibleAnnotationsAttribute(name_index={self.attribute_name_index}, length={self.attribute_length})"
